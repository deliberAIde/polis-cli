"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='sendcreatedlinktoemail endpoints (1)', no_args_is_help=True)


@app.command("create-sendcreatedlinktoemail", help='[admin] Email the authenticated user (looked up by uid) a link to the conversation they just created.')
def create_sendcreatedlinktoemail_create_sendcreatedlinktoemail(
    conversation_id: str = typer.Option(..., "--conversation-id", help="declared twice: zid resolution plus the original string preserved for the emailed link; cl"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/sendCreatedLinkToEmail", query={}, body={"conversation_id": conversation_id})
    emit(result)

