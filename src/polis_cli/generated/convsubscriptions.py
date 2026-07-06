"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='convsubscriptions endpoints (1)', no_args_is_help=True)


@app.command("create-convsubscriptions", help='[core] Subscribe/unsubscribe the authenticated participant to new-statement email notifications for a conversation (updates participants.subscribed and participants_extended.subscribe_email).')
def create_convsubscriptions_create_convsubscriptions(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to (un)subscribe from"),
    type: int = typer.Option(..., "--type", help="1 = subscribe to email notifications, 0 = unsubscribe; anything else -> 400 polis_err_bad_"),
    email: str = typer.Option(..., "--email", help="email to store in participants_extended.subscribe_email (used even for type=0, though igno"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/convSubscriptions", query={}, body={"conversation_id": conversation_id, "type": type, "email": email})
    emit(result)

