"""Offline verification of the full demo loop + generated surface.

No Docker, no live instance: pytest-httpx mocks Pol.is responses using the
request/response shapes recorded in api/endpoints.json. This proves the client
and generated commands build correct requests and parse responses — everything
except the live TLS/auth handshake against a real instance.

    pip install -e ".[dev]" && pytest -q
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from polis_cli.client import PolisClient
from polis_cli.config import Profile

ROOT = Path(__file__).resolve().parents[1]
runner = CliRunner()


@pytest.fixture
def profile():
    return Profile(name="test", base_url="https://polis.test", auth="oidc", email="a@b.c")


@pytest.fixture
def client(profile):
    c = PolisClient(profile)
    c._bearer = "test.jwt.token"  # skip the auth handshake; exercise the API calls
    return c


# --------------------------------------------------------------- demo loop


def test_full_loop(client, httpx_mock):
    """create -> seed -> vote -> math -> close -> report -> export."""
    base = "https://polis.test/api/v3"

    httpx_mock.add_response(
        method="POST", url=f"{base}/conversations",
        json={"conversation_id": "3jwxyz", "url": "https://polis.test/3jwxyz"},
    )
    for tid in range(3):
        httpx_mock.add_response(
            method="POST", url=f"{base}/comments",
            json={"tid": tid, "currentPid": 0},
        )
    httpx_mock.add_response(
        method="GET", url=f"{base}/comments?conversation_id=3jwxyz",
        json=[{"tid": i, "txt": f"s{i}"} for i in range(3)],
    )
    httpx_mock.add_response(method="POST", url=f"{base}/votes", json={"nextComment": {}}, is_reusable=True)
    httpx_mock.add_response(
        method="GET", url=f"{base}/math/pca2?conversation_id=3jwxyz",
        json={"group-clusters": [{"id": 0}, {"id": 1}], "n": 3},
    )
    httpx_mock.add_response(method="POST", url=f"{base}/conversation/close", json={})
    # close/reopen are fire-and-verify (upstream never answers the POST), so the
    # client always follows up with a GET to confirm the state actually changed.
    httpx_mock.add_response(
        method="GET", url=f"{base}/conversations?conversation_id=3jwxyz",
        json={"conversation_id": "3jwxyz", "is_active": False},
    )
    httpx_mock.add_response(method="POST", url=f"{base}/reports", json={"report_id": "r9abc"})
    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        httpx_mock.add_response(
            method="GET", url=f"{base}/reportExport/r9abc/{kind}.csv",
            text=f"col_a,col_b\n1,2\n# {kind}\n",
        )

    convo = client.create_conversation("Test topic", "desc")
    assert convo["conversation_id"] == "3jwxyz"

    for i in range(3):
        client.seed_comment("3jwxyz", f"statement {i}")

    comments = client.list_comments("3jwxyz")
    assert [c["tid"] for c in comments] == [0, 1, 2]

    for tid in [c["tid"] for c in comments]:
        client.vote("3jwxyz", tid, -1)

    math = client.math("3jwxyz")
    assert len(math["group-clusters"]) == 2

    client.close_conversation("3jwxyz")

    report = client.create_report("3jwxyz")
    assert report["report_id"] == "r9abc"

    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        csv_text = client.export_csv("r9abc", kind)
        assert kind in csv_text and "col_a" in csv_text


def test_auth_header_sent(client, httpx_mock):
    httpx_mock.add_response(method="POST", url="https://polis.test/api/v3/conversations", json={"conversation_id": "x"})
    client.create_conversation("t")
    req = httpx_mock.get_requests()[0]
    assert req.headers["Authorization"] == "Bearer test.jwt.token"


def test_legacy_login_404_gives_clear_error(profile, httpx_mock):
    """The removed-in-Jul-2025 password endpoint must yield the actionable message."""
    httpx_mock.add_response(method="POST", url="https://polis.test/api/v3/auth/login", status_code=404, text="")
    c = PolisClient(profile)
    with pytest.raises(Exception, match="OIDC-only"):
        c.login_password("a@b.c", "pw")


# --------------------------------------------------- generated surface sanity


def test_generated_layer_imports_and_registers():
    """All generated groups import cleanly and register commands on the api app."""
    from polis_cli import generated
    import importlib

    assert generated.GROUPS, "no generated groups"
    total = 0
    for group in generated.GROUPS:
        mod = importlib.import_module(f"polis_cli.generated.{group}")
        cmds = mod.app.registered_commands
        total += len(cmds)
    assert total >= 100, f"expected 100+ generated commands, got {total}"


def test_catalog_integrity():
    catalog = json.loads((ROOT / "api" / "endpoints.json").read_text(encoding="utf-8"))
    eps = catalog["endpoints"]
    assert catalog["endpoint_count"] == len(eps)
    # no duplicate (method, path)
    keys = [(e["method"], e["path"]) for e in eps]
    assert len(keys) == len(set(keys)), "duplicate endpoints in catalog"
    # every endpoint has the fields codegen depends on
    for e in eps:
        assert e["method"] and e["path"] and "stability" in e and "agent_relevance" in e


def test_cli_help_renders():
    """The top-level app and the generated api sub-app render without error."""
    from polis_cli.main import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "api" in result.output

    result = runner.invoke(app, ["api", "conversations", "--help"])
    assert result.exit_code == 0
    assert "create" in result.output
