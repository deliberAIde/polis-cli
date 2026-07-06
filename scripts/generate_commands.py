"""Codegen: api/endpoints.json -> full Typer command tree + OpenAPI spec.

One source of truth (the extracted endpoint catalog) generates:
  * src/polis_cli/generated/<group>.py  — one Typer sub-app per API group
  * api/openapi.yaml                    — the OpenAPI spec Pol.is never had

Scope rule: only true API routes (path starts with /api/) become commands;
SPA/HTML/static routes stay catalog-only. Dead/disabled endpoints are skipped
(list below). Everything else is generated — full-coverage by construction.

Run:  python scripts/generate_commands.py
"""

from __future__ import annotations

import json
import keyword
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "api" / "endpoints.json"
GEN_DIR = ROOT / "src" / "polis_cli" / "generated"
OPENAPI = ROOT / "api" / "openapi.yaml"

# endpoints the sweep proved dead/disabled at source level
SKIP = {
    ("GET", "/api/v3/snapshot"),      # handler throws TODO unconditionally
    ("POST", "/api/v3/metrics"),      # hard-disabled (enabled = false)
}

VERB = {"GET": "get", "POST": "create", "PUT": "update", "DELETE": "delete", "PATCH": "patch", "HEAD": "head"}

TYPE_MAP = [
    (re.compile(r"getBool", re.I), "bool"),
    (re.compile(r"getInt|getNumber", re.I), "int"),
]


def py_type(validator: str | None) -> str:
    for pattern, t in TYPE_MAP:
        if validator and pattern.search(validator):
            return t
    return "str"


def safe_ident(name: str) -> str:
    ident = re.sub(r"[^0-9a-zA-Z_]", "_", name)
    if keyword.iskeyword(ident) or ident in ("json", "id"):
        ident += "_"
    if ident and ident[0].isdigit():
        ident = "p_" + ident
    return ident


def path_params(path: str) -> list[str]:
    return re.findall(r"[:{]([a-zA-Z_]+)}?", path)


def command_name(method: str, path: str, group: str) -> str:
    segs = [s for s in path.split("/") if s and s not in ("api", "v3") and not s.startswith(":") and not s.startswith("{")]
    rest = [s for s in segs[1:]] if segs and segs[0] == group else segs
    name = "-".join([VERB[method]] + rest) if rest else (
        "list" if method == "GET" else VERB[method]
    )
    return re.sub(r"[^0-9a-zA-Z-]", "-", name).strip("-").lower()


def api_group(path: str) -> str:
    segs = [s for s in path.split("/") if s and s not in ("api", "v3")]
    g = segs[0] if segs else "misc"
    return re.sub(r"[^0-9a-zA-Z]", "_", g).lower()


HEADER = '''"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: {source}
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help={group_help!r}, no_args_is_help=True)

'''

CMD_TEMPLATE = '''
@app.command("{cmd}", help={help!r})
def {fn}(
{args}    profile: str = typer.Option("local", "--profile", "-p"),
):
{body}
'''


def build() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    endpoints = [
        e for e in catalog["endpoints"]
        if e["path"].startswith("/api/") and (e["method"], e["path"]) not in SKIP
    ]
    groups: dict[str, list[dict]] = defaultdict(list)
    for e in endpoints:
        groups[api_group(e["path"])].append(e)

    GEN_DIR.mkdir(parents=True, exist_ok=True)
    for old in GEN_DIR.glob("*.py"):
        old.unlink()

    registered: list[tuple[str, str]] = []
    used_names: dict[str, set] = defaultdict(set)

    for group, eps in sorted(groups.items()):
        lines = [HEADER.format(source=catalog["source"], group_help=f"{group} endpoints ({len(eps)})")]
        for e in sorted(eps, key=lambda x: (x["path"], x["method"])):
            method, path = e["method"], e["path"]
            cmd = command_name(method, path, group)
            # disambiguate collisions deterministically
            base_cmd = cmd
            n = 2
            while cmd in used_names[group]:
                cmd = f"{base_cmd}-{n}"
                n += 1
            used_names[group].add(cmd)

            fn = safe_ident(f"{VERB[method]}_{group}_{cmd}".replace("-", "_"))
            p_params = path_params(path)
            arg_lines, q_items, b_items, p_items = [], [], [], []

            for name in p_params:
                ident = safe_ident(name)
                arg_lines.append(f'    {ident}: str = typer.Argument(..., help="path param {name}"),\n')
                p_items.append((name, ident))

            for p in e.get("params", []):
                if p["location"] == "path":
                    continue
                ident = safe_ident(p["name"])
                if ident in {i for _, i in p_items}:
                    continue
                t = py_type(p.get("type"))
                helptext = (p.get("description") or p.get("type") or "")[:90].replace('"', "'")
                flag = "--" + p["name"].replace("_", "-")
                if p.get("required"):
                    arg_lines.append(
                        f'    {ident}: {t} = typer.Option(..., "{flag}", help="{helptext}"),\n'
                    )
                else:
                    default = "None"
                    t = f"Optional[{t}]"
                    arg_lines.append(
                        f'    {ident}: {t} = typer.Option({default}, "{flag}", help="{helptext}"),\n'
                    )
                target = q_items if (method == "GET" or p["location"] == "query") else b_items
                target.append((p["name"], ident))

            fmt_path = re.sub(r":([a-zA-Z_]+)", r"{\1}", path)
            path_expr = f'f"{fmt_path}"' if p_items else f'"{path}"'
            q_dict = "{" + ", ".join(f'"{n}": {i}' for n, i in q_items) + "}"
            b_dict = "{" + ", ".join(f'"{n}": {i}' for n, i in b_items) + "}"
            body = (
                f'    client = get_client(profile)\n'
                f'    result = client.call("{method}", {path_expr}, query={q_dict}, body={b_dict})\n'
                f'    emit(result)\n'
            )
            helptext = f"[{e['stability']}] {e.get('description', '')}"[:200].replace('"', "'")
            lines.append(CMD_TEMPLATE.format(cmd=cmd, help=helptext, fn=fn, args="".join(arg_lines), body=body))

        (GEN_DIR / f"{group}.py").write_text("".join(lines), encoding="utf-8")
        registered.append((group, len(eps)))

    init = ['"""AUTO-GENERATED package — do not edit."""\n', "GROUPS = [\n"]
    init += [f'    "{g}",\n' for g, _ in registered]
    init.append("]\n")
    (GEN_DIR / "__init__.py").write_text("".join(init), encoding="utf-8")

    write_openapi(catalog, endpoints)
    total = sum(n for _, n in registered)
    print(f"generated {total} commands across {len(registered)} groups -> {GEN_DIR}")
    print(f"openapi spec -> {OPENAPI}")


def write_openapi(catalog: dict, endpoints: list[dict]) -> None:
    """Emit a minimal-but-valid OpenAPI 3.1 spec from the catalog."""
    import yaml  # lazy: only needed for codegen

    paths: dict = defaultdict(dict)
    for e in endpoints:
        path = re.sub(r":([a-zA-Z_]+)", r"{\1}", e["path"])
        op = {
            "operationId": safe_ident(f'{VERB[e["method"]]}_{api_group(e["path"])}_{command_name(e["method"], e["path"], api_group(e["path"]))}'),
            "summary": (e.get("description") or "")[:120],
            "description": f"Handler: {e['handler']}. Auth: {e['auth']}. Stability: {e['stability']}.",
            "tags": [api_group(e["path"]), e["stability"]],
            "responses": {"200": {"description": e.get("response_hint") or "OK"}},
        }
        params, body_props, body_required = [], {}, []
        for name in path_params(e["path"]):
            params.append({"name": name, "in": "path", "required": True, "schema": {"type": "string"}})
        for p in e.get("params", []):
            if p["location"] == "path":
                continue
            schema_type = {"bool": "boolean", "int": "integer"}.get(py_type(p.get("type")), "string")
            if e["method"] == "GET" or p["location"] == "query":
                params.append({
                    "name": p["name"], "in": "query", "required": bool(p.get("required")),
                    "schema": {"type": schema_type},
                    "description": (p.get("description") or "")[:200],
                })
            else:
                body_props[p["name"]] = {"type": schema_type, "description": (p.get("description") or "")[:200]}
                if p.get("required"):
                    body_required.append(p["name"])
        if params:
            op["parameters"] = params
        if body_props:
            schema = {"type": "object", "properties": body_props}
            if body_required:
                schema["required"] = body_required
            op["requestBody"] = {"content": {"application/json": {"schema": schema}}}
        paths[path][e["method"].lower()] = op

    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": "Pol.is HTTP API (community-documented)",
            "version": catalog["source"],
            "description": (
                "Unofficial OpenAPI description of the Pol.is server API, extracted from source "
                f"({catalog['source']}). Pol.is publishes no API contract; endpoints may change without notice. "
                "Auth: OIDC bearer JWT (email claim required) on current builds; legacy builds use "
                "cookie-session via POST /api/v3/auth/login."
            ),
        },
        "servers": [{"url": "https://localhost", "description": "self-hosted instance"}],
        "paths": dict(sorted(paths.items())),
    }
    OPENAPI.write_text(yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


if __name__ == "__main__":
    build()
