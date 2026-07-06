"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='conversationstats endpoints (1)', no_args_is_help=True)


@app.command("get-conversationstats", help='[admin] Participation time-series and histograms for a conversation: every vote/comment timestamp, first-vote/first-comment per participant, votes-per-participant histogram, and vote-burst histogram (')
def get_conversationstats_get_conversationstats(
    conversation_id: str = typer.Option(..., "--conversation-id", help="resolved to zid"),
    report_id: Optional[str] = typer.Option(None, "--report-id", help="grants read access without moderator rights"),
    until: Optional[int] = typer.Option(None, "--until", help="only include comments/votes created before this ms timestamp"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversationStats", query={"conversation_id": conversation_id, "report_id": report_id, "until": until}, body={})
    emit(result)

