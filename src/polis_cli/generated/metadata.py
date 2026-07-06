"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='metadata endpoints (8)', no_args_is_help=True)


@app.command("list", help='[admin] Fetch the combined metadata structure for a conversation: questions, answer options, and which participants chose each answer, as nested maps.')
def get_metadata_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose full metadata structure to fetch"),
    zinvite: Optional[str] = typer.Option(None, "--zinvite", help="conversation invite code; validated if provided"),
    suzinvite: Optional[str] = typer.Option(None, "--suzinvite", help="single-use invite code; validated if provided"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/metadata", query={"conversation_id": conversation_id, "zinvite": zinvite, "suzinvite": suzinvite}, body={})
    emit(result)


@app.command("get-answers", help='[core] List alive participant-metadata answer options for a conversation (each row returned with is_exclusive=true), optionally filtered by question.')
def get_metadata_get_answers(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose answers to list"),
    pmqid: Optional[int] = typer.Option(None, "--pmqid", help="restrict to a single metadata question"),
    suzinvite: Optional[str] = typer.Option(None, "--suzinvite", help="single-use invite code; validated before returning data if provided"),
    zinvite: Optional[str] = typer.Option(None, "--zinvite", help="conversation invite code; validated before returning data if provided"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/metadata/answers", query={"conversation_id": conversation_id, "pmqid": pmqid, "suzinvite": suzinvite, "zinvite": zinvite}, body={})
    emit(result)


@app.command("create-answers", help='[admin] Add an answer option to a metadata question (or revive a previously soft-deleted identical one); conversation-owner-only (checked in handler).')
def create_metadata_create_answers(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the question belongs to"),
    pmqid: int = typer.Option(..., "--pmqid", help="metadata question id to attach this answer option to"),
    value: str = typer.Option(..., "--value", help="answer option text"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/metadata/answers", query={}, body={"conversation_id": conversation_id, "pmqid": pmqid, "value": value})
    emit(result)


@app.command("delete-answers", help='[admin] Soft-delete (alive=FALSE) a single participant-metadata answer; conversation-owner-only (checked in handler).')
def delete_metadata_delete_answers(
    pmaid: str = typer.Argument(..., help="path param pmaid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("DELETE", f"/api/v3/metadata/answers/{pmaid}", query={}, body={})
    emit(result)


@app.command("get-choices", help='[admin] List alive participant_metadata_choices rows (which participant picked which answer) for a conversation.')
def get_metadata_get_choices(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose participant choices to list"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/metadata/choices", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-questions", help='[core] List alive participant-metadata questions for a conversation (each row returned with required=true); access gated by zinvite/suzinvite validity when supplied.')
def get_metadata_get_questions(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose metadata questions to list"),
    suzinvite: Optional[str] = typer.Option(None, "--suzinvite", help="single-use invite code; if provided, validated before returning data"),
    zinvite: Optional[str] = typer.Option(None, "--zinvite", help="conversation invite code; if provided, validated before returning data"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/metadata/questions", query={"conversation_id": conversation_id, "suzinvite": suzinvite, "zinvite": zinvite}, body={})
    emit(result)


@app.command("create-questions", help='[admin] Create a participant-metadata question on a conversation; conversation-owner-only (checked in handler).')
def create_metadata_create_questions(
    key: str = typer.Option(..., "--key", help="question text/key (e.g. a demographic question)"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to attach the question to"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/metadata/questions", query={}, body={"key": key, "conversation_id": conversation_id})
    emit(result)


@app.command("delete-questions", help='[admin] Soft-delete (alive=FALSE) a participant-metadata question and all its answers; conversation-owner-only (checked in handler).')
def delete_metadata_delete_questions(
    pmqid: str = typer.Argument(..., help="path param pmqid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("DELETE", f"/api/v3/metadata/questions/{pmqid}", query={}, body={})
    emit(result)

