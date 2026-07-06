"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='participants endpoints (2)', no_args_is_help=True)


@app.command("list", help="[core] Returns the calling user's own participant row for the conversation (SELECT * FROM participants WHERE uid AND zid), or null if the caller has not joined.")
def get_participants_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose participant record to fetch"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/participants", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("create", help='[core] Joins the authenticated user to a conversation as a participant (idempotent: returns the existing participant row if already joined); rejects with 400 if required metadata questions are unanswe')
def create_participants_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to join; resolved to internal zid"),
    answers: Optional[str] = typer.Option(None, "--answers", help="Array of pmaid choices answering required participant-metadata questions"),
    parent_url: Optional[str] = typer.Option(None, "--parent-url", help="Embedding page URL, stored as extended participant info"),
    referrer: Optional[str] = typer.Option(None, "--referrer", help="Referrer URL, stored as extended participant info"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/participants", query={}, body={"conversation_id": conversation_id, "answers": answers, "parent_url": parent_url, "referrer": referrer})
    emit(result)

