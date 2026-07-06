"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='reserve_conversation_id endpoints (1)', no_args_is_help=True)


@app.command("create", help='[core] Reserve a conversation_id (zinvite registered against zid=0) so the id/URL is known before the conversation is created; pass it later as conversation_id to POST /api/v3/conversations. Code comm')
def create_reserve_conversation_id_create(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/reserve_conversation_id", query={}, body={})
    emit(result)

