"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='topicagenda endpoints (4)', no_args_is_help=True)


@app.command("delete-topicagenda-selections", help="[experimental] Deletes the calling participant's topic-agenda selections for a conversation.")
def delete_topicagenda_delete_topicagenda_selections(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("DELETE", "/api/v3/topicAgenda/selections", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-topicagenda-selections", help="[experimental] Returns the calling participant's own topic-agenda selections for a conversation.")
def get_topicagenda_get_topicagenda_selections(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicAgenda/selections", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("create-topicagenda-selections", help="[experimental] Participant-facing: records the calling participant's topic-agenda selections for a conversation, creating the participant and issuing a participant JWT if needed.")
def create_topicagenda_create_topicagenda_selections(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    selections: str = typer.Option(..., "--selections", help="The participant's chosen topics for the agenda"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/topicAgenda/selections", query={}, body={"conversation_id": conversation_id, "selections": selections})
    emit(result)


@app.command("update-topicagenda-selections", help="[experimental] Replaces/updates the calling participant's existing topic-agenda selections.")
def update_topicagenda_update_topicagenda_selections(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    selections: str = typer.Option(..., "--selections", help="array (raw req.body)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/topicAgenda/selections", query={}, body={"conversation_id": conversation_id, "selections": selections})
    emit(result)

