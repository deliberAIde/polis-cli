"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='conversationuuid endpoints (1)', no_args_is_help=True)


@app.command("get-conversationuuid", help='[experimental] Get-or-create a persistent UUID for the conversation (stored on the zinvites row); used to give the conversation a stable external identifier.')
def get_conversationuuid_get_conversationuuid(
    conversation_id: str = typer.Option(..., "--conversation-id", help="resolved to zid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversationUuid", query={"conversation_id": conversation_id}, body={})
    emit(result)

