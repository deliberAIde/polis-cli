"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='sendemailexportready endpoints (1)', no_args_is_help=True)


@app.command("create-sendemailexportready", help='[internal] Server-to-server hook (called by the export worker) that emails a user a download link when their data export finishes.')
def create_sendemailexportready_create_sendemailexportready(
    webserver_username: str = typer.Option(..., "--webserver-username", help="internal service username; must equal Config.webserverUsername or 403"),
    webserver_pass: str = typer.Option(..., "--webserver-pass", help="internal service password; must equal Config.webserverPass or 403"),
    email: str = typer.Option(..., "--email", help="recipient of the export-ready email"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation id used to build the download URL (string only; no zid lookup)"),
    filename: str = typer.Option(..., "--filename", help="export filename used in the /api/v3/dataExport/results download URL"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/sendEmailExportReady", query={}, body={"webserver_username": webserver_username, "webserver_pass": webserver_pass, "email": email, "conversation_id": conversation_id, "filename": filename})
    emit(result)

