"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='participation endpoints (2)', no_args_is_help=True)


@app.command("list", help='[admin] Owner-only participation stats: per-participant vote and comment counts, keyed by pid, or re-keyed by xid when xid records exist.')
def get_participation_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to summarize"),
    strict: Optional[bool] = typer.Option(None, "--strict", help="If true, 409s when participants are missing xid mappings"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/participation", query={"conversation_id": conversation_id, "strict": strict}, body={})
    emit(result)


@app.command("get-topicprioritize", help='[experimental] Lightweight public check used by client-participation-alpha: reports whether the conversation has a report (latest report_id) and, optimistically, Delphi data for the topic-prioritizati')
def get_participation_get_topicprioritize(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to check for report/Delphi availability"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/participation/topicPrioritize", query={"conversation_id": conversation_id}, body={})
    emit(result)

