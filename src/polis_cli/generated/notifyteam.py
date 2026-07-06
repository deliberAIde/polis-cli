"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='notifyteam endpoints (1)', no_args_is_help=True)


@app.command("create-notifyteam", help='[internal] Server-internal hook (used by sibling services) to email the admin team')
def create_notifyteam_create_notifyteam(
    webserver_username: str = typer.Option(..., "--webserver-username", help="getStringLimitLength(1,999)"),
    webserver_pass: str = typer.Option(..., "--webserver-pass", help="getStringLimitLength(1,999)"),
    subject: str = typer.Option(..., "--subject", help="getStringLimitLength(9999)"),
    body: str = typer.Option(..., "--body", help="getStringLimitLength(99999)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/notifyTeam", query={}, body={"webserver_username": webserver_username, "webserver_pass": webserver_pass, "subject": subject, "body": body})
    emit(result)

