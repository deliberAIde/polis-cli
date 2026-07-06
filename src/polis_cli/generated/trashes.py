"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='trashes endpoints (1)', no_args_is_help=True)


@app.command("create", help="[legacy] Record a participant-side 'trash' flag on a comment (participant marks a comment as junk); insert-only, duplicates return 406.")
def create_trashes_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the comment belongs to"),
    tid: int = typer.Option(..., "--tid", help="comment id to flag"),
    trashed: int = typer.Option(..., "--trashed", help="1 to trash, 0 to untrash"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/trashes", query={}, body={"conversation_id": conversation_id, "tid": tid, "trashed": trashed})
    emit(result)

