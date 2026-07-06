"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='ptptois endpoints (2)', no_args_is_help=True)


@app.command("list", help="[core] Lists social 'participants of interest' (participants with xid profile data: xid, x_name, x_profile_image_url, pid, mod) for display under the visualization.")
def get_ptptois_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation whose participants-of-interest to list"),
    mod: Optional[int] = typer.Option(None, "--mod", help="Filter by participant mod status"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/ptptois", query={"conversation_id": conversation_id, "mod": mod}, body={})
    emit(result)


@app.command("update", help="[admin] Moderator sets a participant's mod status (UPDATE participants SET mod), hiding or showing them as a participant-of-interest.")
def update_ptptois_update(
    mod: int = typer.Option(..., "--mod", help="New mod status for the participant (controls visibility as participant-of-interest)"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation containing the participant"),
    pid: Optional[str] = typer.Option(None, "--pid", help="Target participant; moderators pass the explicit pid to moderate"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/ptptois", query={}, body={"mod": mod, "conversation_id": conversation_id, "pid": pid})
    emit(result)

