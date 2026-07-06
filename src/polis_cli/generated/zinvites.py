"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='zinvites endpoints (2)', no_args_is_help=True)


@app.command("list", help='[admin] List all zinvite (conversation share/invite) codes for a conversation; owner-only (SQL checks conversations.owner = uid).')
def get_zinvites_list(
    zid: str = typer.Argument(..., help="path param zid"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="public conversation id; resolved to internal zid. Note: the :zid path segment is vestigial"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", f"/api/v3/zinvites/{zid}", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("create", help='[admin] Generate and register a new zinvite (share/invite) code for a conversation; owner-only.')
def create_zinvites_create(
    zid: str = typer.Argument(..., help="path param zid"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="public conversation id; resolved to internal zid. :zid path segment vestigial (see GET)"),
    short_url: Optional[bool] = typer.Option(None, "--short-url", help="generate a short-form zinvite code"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", f"/api/v3/zinvites/{zid}", query={}, body={"conversation_id": conversation_id, "short_url": short_url})
    emit(result)

