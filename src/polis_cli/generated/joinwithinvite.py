"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='joinwithinvite endpoints (1)', no_args_is_help=True)


@app.command("create-joinwithinvite", help='[core] Joins a conversation via zid or single-use suzinvite, creating an anonymous user if there is no existing auth; enforces xid allow-list / xid_required conversation settings; returns pid/uid plus')
def create_joinwithinvite_create_joinwithinvite(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to join; resolved to zid"),
    suzinvite: Optional[str] = typer.Option(None, "--suzinvite", help="Single-use invite token; consumed (deleted) on successful join"),
    answers: Optional[str] = typer.Option(None, "--answers", help="pmaid choices for required metadata questions"),
    referrer: Optional[str] = typer.Option(None, "--referrer", help="Referrer URL stored with the participant"),
    parent_url: Optional[str] = typer.Option(None, "--parent-url", help="Embedding page URL stored with the participant"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/joinWithInvite", query={}, body={"conversation_id": conversation_id, "suzinvite": suzinvite, "answers": answers, "referrer": referrer, "parent_url": parent_url})
    emit(result)

