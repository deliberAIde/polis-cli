"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='stars endpoints (1)', no_args_is_help=True)


@app.command("create", help='[legacy] Record a star (favorite) on a comment for the calling participant; duplicate star for same comment returns 406.')
def create_stars_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the comment belongs to"),
    tid: int = typer.Option(..., "--tid", help="comment id to star/unstar"),
    starred: int = typer.Option(..., "--starred", help="1 to star, 0 to unstar"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/stars", query={}, body={"conversation_id": conversation_id, "tid": tid, "starred": starred})
    emit(result)

