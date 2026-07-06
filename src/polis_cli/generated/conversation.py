"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='conversation endpoints (2)', no_args_is_help=True)


@app.command("create-close", help='[admin] Close a conversation (sets is_active=false). BUG in this build: the handler never sends a success response — only error paths respond, so a successful close leaves the HTTP request hanging.')
def create_conversation_create_close(
    conversation_id: str = typer.Option(..., "--conversation-id", help="resolved to zid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/conversation/close", query={}, body={"conversation_id": conversation_id})
    emit(result)


@app.command("create-reopen", help='[admin] Reopen a closed conversation (sets is_active=true).')
def create_conversation_create_reopen(
    conversation_id: str = typer.Option(..., "--conversation-id", help="resolved to zid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/conversation/reopen", query={}, body={"conversation_id": conversation_id})
    emit(result)

