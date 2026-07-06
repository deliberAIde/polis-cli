"""polis-cli — drive Pol.is/Voxit instances from the command line (or from an agent)."""

from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .client import PolisClient, PolisError
from .config import Profile, load_profile, save_profile

app = typer.Typer(help=__doc__, no_args_is_help=True)
convo_app = typer.Typer(help="Conversation lifecycle: create, open/close, status.")
app.add_typer(convo_app, name="convo")

# full-coverage generated surface: polis api <group> <command>
api_app = typer.Typer(
    help="Full generated API surface (one command per endpoint, from api/endpoints.json).",
    no_args_is_help=True,
)
app.add_typer(api_app, name="api")
try:
    import importlib

    from . import generated as _generated

    for _group in _generated.GROUPS:
        _mod = importlib.import_module(f".generated.{_group}", package=__package__)
        api_app.add_typer(_mod.app, name=_group.replace("_", "-"))
except ImportError:
    pass  # generated modules absent until scripts/generate_commands.py has run

console = Console()
err_console = Console(stderr=True)

_JSON = False  # set by --json


def _client(profile_name: str) -> PolisClient:
    try:
        return PolisClient(load_profile(profile_name))
    except KeyError as e:
        err_console.print(f"[red]{e}[/red]")
        raise typer.Exit(2) from e


def _emit(data, human_render=None) -> None:
    if _JSON:
        print(json.dumps(data, indent=2, default=str))
    elif human_render:
        human_render(data)
    else:
        console.print(data)


@app.callback()
def _global(json_output: bool = typer.Option(False, "--json", help="Machine-readable output.")):
    global _JSON
    _JSON = json_output


# --------------------------------------------------------------------- setup


@app.command()
def profile_add(
    name: str,
    base_url: str,
    auth: str = typer.Option("password", help="password | oidc"),
    email: Optional[str] = None,
    oidc_token_url: Optional[str] = typer.Option(None, help="OIDC issuer for token grants"),
    oidc_client_id: Optional[str] = typer.Option(None),
    no_verify_tls: bool = typer.Option(False, help="Disable TLS verification (dev sandboxes only)"),
):
    """Register an instance profile."""
    extra = {"verify": False} if no_verify_tls else {}
    save_profile(
        Profile(
            name=name, base_url=base_url, auth=auth, email=email,
            oidc_token_url=oidc_token_url, oidc_client_id=oidc_client_id, extra=extra,
        )
    )
    _emit({"profile": name, "base_url": base_url, "auth": auth, "status": "saved"})


@app.command()
def login(
    profile: str = typer.Option("local", "--profile", "-p"),
    password: Optional[str] = typer.Option(None, envvar="POLIS_PASSWORD"),
    bearer: Optional[str] = typer.Option(None, envvar="POLIS_BEARER", help="OIDC JWT"),
):
    """Authenticate against the instance and cache the credential."""
    client = _client(profile)
    if bearer:
        client.login_bearer(bearer)
        _emit({"profile": profile, "auth": "oidc", "status": "token cached"})
        return
    email = client.profile.email or typer.prompt("email")
    password = password or typer.prompt("password", hide_input=True)
    try:
        if client.profile.auth == "oidc":
            client.login_oidc_password_grant(
                email, password, verify_tls=client.profile.extra.get("verify", True)
            )
            _emit({"profile": profile, "auth": "oidc", "status": "token cached"})
        else:
            client.login_password(email, password)
            _emit({"profile": profile, "auth": "password", "status": "session cached"})
    except PolisError as e:
        err_console.print(f"[red]{e}[/red]")
        raise typer.Exit(1) from e


# -------------------------------------------------------------- conversation


@convo_app.command("create")
def convo_create(
    topic: str,
    description: str = typer.Option("", "--description", "-d"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    """Create a conversation; prints its id."""
    client = _client(profile)
    result = client.create_conversation(topic, description)
    _emit(result)


@convo_app.command("status")
def convo_status(
    conversation_id: str,
    profile: str = typer.Option("local", "--profile", "-p"),
):
    """Participation counts + opinion-cluster snapshot."""
    client = _client(profile)
    convo = client.get_conversation(conversation_id)
    try:
        math = client.math(conversation_id)
        groups = len(math.get("group-clusters", math.get("group_clusters", [])) or [])
    except PolisError:
        groups = None
    payload = {"conversation": convo, "opinion_groups": groups}
    _emit(payload)


@convo_app.command("close")
def convo_close(conversation_id: str, profile: str = typer.Option("local", "--profile", "-p")):
    _client(profile).close_conversation(conversation_id)
    _emit({"conversation_id": conversation_id, "status": "closed"})


@convo_app.command("reopen")
def convo_reopen(conversation_id: str, profile: str = typer.Option("local", "--profile", "-p")):
    _client(profile).reopen_conversation(conversation_id)
    _emit({"conversation_id": conversation_id, "status": "reopened"})


# ---------------------------------------------------------------- statements


@app.command()
def seed(
    conversation_id: str,
    statements_file: Path = typer.Argument(..., help="CSV/TXT: one statement per line."),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    """Bulk-seed statements into a conversation."""
    client = _client(profile)
    lines = [
        row[0].strip()
        for row in csv.reader(statements_file.read_text(encoding="utf-8").splitlines())
        if row and row[0].strip()
    ]
    results = []
    for text in lines:
        results.append(client.seed_comment(conversation_id, text))
    _emit({"conversation_id": conversation_id, "seeded": len(results)})


@app.command()
def moderate(
    conversation_id: str,
    profile: str = typer.Option("local", "--profile", "-p"),
    accept_all: bool = typer.Option(False, help="Accept every queued statement."),
):
    """List (and optionally accept) statements awaiting moderation."""
    client = _client(profile)
    queued = client.list_comments(conversation_id, moderation=True)
    if accept_all:
        for c in queued:
            client.moderate_comment(conversation_id, c["tid"], accept=True)
        _emit({"conversation_id": conversation_id, "accepted": len(queued)})
    else:
        _emit(queued)


# -------------------------------------------------------------------- export


@app.command()
def export(
    conversation_id: str,
    out_dir: Path = typer.Option(Path("."), "--out", "-o"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    """Export raw votes, comments, and cluster CSVs for synthesis."""
    client = _client(profile)
    reports = client.list_reports(conversation_id)
    if not reports:
        client.create_report(conversation_id)  # create returns no body; re-list for the id
        reports = client.list_reports(conversation_id)
    if not reports:
        err_console.print("[red]no report available for this conversation[/red]")
        raise typer.Exit(1)
    report_id = reports[0].get("report_id") or reports[0].get("rid")
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        try:
            csv_text = client.export_csv(str(report_id), kind)
        except PolisError as e:
            err_console.print(f"[yellow]skipped {kind}: {e}[/yellow]")
            continue
        path = out_dir / f"{conversation_id}-{kind}.csv"
        path.write_text(csv_text, encoding="utf-8")
        written.append(str(path))
    _emit({"conversation_id": conversation_id, "report_id": report_id, "files": written})


if __name__ == "__main__":
    app()
