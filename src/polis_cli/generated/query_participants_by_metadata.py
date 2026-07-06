"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='query_participants_by_metadata endpoints (1)', no_args_is_help=True)


@app.command("create", help='[legacy] Returns pids of participants whose metadata answers are not excluded by the given pmaid selection (used to filter visualizations by demographic metadata).')
def create_query_participants_by_metadata_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to query"),
    pmaids: str = typer.Option(..., "--pmaids", help="Checked metadata-answer ids; empty array returns []"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/query_participants_by_metadata", query={}, body={"conversation_id": conversation_id, "pmaids": pmaids})
    emit(result)

