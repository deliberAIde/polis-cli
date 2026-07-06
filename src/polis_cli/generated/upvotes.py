"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='upvotes endpoints (1)', no_args_is_help=True)


@app.command("create", help='[legacy] Upvote a conversation (once per user); updates conversations.upvotes counter')
def create_upvotes_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/upvotes", query={}, body={"conversation_id": conversation_id})
    emit(result)

