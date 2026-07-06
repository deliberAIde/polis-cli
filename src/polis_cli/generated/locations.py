"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='locations endpoints (1)', no_args_is_help=True)


@app.command("list", help='[legacy] Returns lat/lng markers for participants in a given opinion group (participant_locations table; Facebook-era geolocation feature)')
def get_locations_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    gid: int = typer.Option(..., "--gid", help="opinion-group id"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/locations", query={"conversation_id": conversation_id, "gid": gid}, body={})
    emit(result)

