"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='mathupdate endpoints (1)', no_args_is_help=True)


@app.command("create-mathupdate", help="[admin] Moderator-only trigger: enqueues an 'update_math' worker task so the math (Clojure) service recomputes or updates clustering for the conversation.")
def create_mathupdate_create_mathupdate(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (assigned as zid)"),
    math_update_type: str = typer.Option(..., "--math-update-type", help="Expected values: 'recompute' or 'update'"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/mathUpdate", query={}, body={"conversation_id": conversation_id, "math_update_type": math_update_type})
    emit(result)

