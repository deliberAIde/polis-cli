"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='xidallowlist endpoints (3)', no_args_is_help=True)


@app.command("get-xidallowlist", help='[admin] Moderator-only paginated view of the xid_whitelist for a conversation (including legacy owner-scoped entries); each entry shows the xid and the pid if that xid is already in use, else null.')
def get_xidallowlist_get_xidallowlist(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose allow-list to read"),
    limit: Optional[int] = typer.Option(None, "--limit", help="Page size (default 50, max 500)"),
    offset: Optional[int] = typer.Option(None, "--offset", help="Records to skip"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/xidAllowList", query={"conversation_id": conversation_id, "limit": limit, "offset": offset}, body={})
    emit(result)


@app.command("create-xidallowlist", help="[admin] Adds xids to a conversation's allow list (INSERT ... ON CONFLICT DO NOTHING); with replace_all=true it synchronizes the list to exactly the incoming set.")
def create_xidallowlist_create_xidallowlist(
    xid_allow_list: str = typer.Option(..., "--xid-allow-list", help="External identities to allow into the conversation"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose allow-list to modify"),
    replace_all: Optional[bool] = typer.Option(None, "--replace-all", help="If true, deletes existing allow-list entries not present in the incoming list (preserves k"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/xidAllowList", query={}, body={"xid_allow_list": xid_allow_list, "conversation_id": conversation_id, "replace_all": replace_all})
    emit(result)


@app.command("get-xidallowlist-csv", help='[admin] Moderator-only CSV export of the full xid allow list for a conversation: columns pid, xid.')
def get_xidallowlist_get_xidallowlist_csv(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose allow-list to export"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/xidAllowList/csv", query={"conversation_id": conversation_id}, body={})
    emit(result)

