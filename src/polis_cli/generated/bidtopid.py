"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='bidtopid endpoints (1)', no_args_is_help=True)


@app.command("get-bidtopid", help="[core] Returns the full mapping of base-cluster index to participant ids for a conversation (marked in source: 'TODO doesn't scale, stop sending entire mapping'); 304 if no mapping available.")
def get_bidtopid_get_bidtopid(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    math_tick: Optional[int] = typer.Option(None, "--math-tick", help="getInt (default 0)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/bidToPid", query={"conversation_id": conversation_id, "math_tick": math_tick}, body={})
    emit(result)

