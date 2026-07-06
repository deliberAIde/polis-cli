"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='participants_extended endpoints (1)', no_args_is_help=True)


@app.command("update", help="[core] Updates the caller's participants_extended row for a conversation (currently only the show_translation_activated flag).")
def update_participants_extended_update(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose extended participant row to update"),
    show_translation_activated: Optional[bool] = typer.Option(None, "--show-translation-activated", help="Currently the only updatable field: whether the participant enabled comment translation"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/participants_extended", query={}, body={"conversation_id": conversation_id, "show_translation_activated": show_translation_activated})
    emit(result)

