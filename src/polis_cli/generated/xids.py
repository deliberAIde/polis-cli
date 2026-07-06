"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='xids endpoints (2)', no_args_is_help=True)


@app.command("list", help='[admin] Moderator-only paginated list of external-identity (xid) records in use by participants of a conversation, with pid and vote_count per record.')
def get_xids_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose xid mappings to list"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Page size (default 50, max 500)"),
    offset: Optional[int] = typer.Option(None, "--offset", help="Records to skip"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/xids", query={"conversation_id": conversation_id, "limit": limit, "offset": offset}, body={})
    emit(result)


@app.command("get-csv", help='[admin] Moderator-only CSV export (attachment download) of all in-use xid records for a conversation: columns pid, xid, vote_count.')
def get_xids_get_csv(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose xid mappings to export"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/xids/csv", query={"conversation_id": conversation_id}, body={})
    emit(result)

