"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='votes endpoints (4)', no_args_is_help=True)


@app.command("list", help='[core] Get the latest unique votes of a single participant (per-comment dedup via votes_latest_unique), optionally filtered to one comment.')
def get_votes_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to read votes from"),
    tid: Optional[int] = typer.Option(None, "--tid", help="restrict to a single comment"),
    pid: Optional[str] = typer.Option(None, "--pid", help="participant whose votes to fetch; normally resolved from auth ('mypid'); returns [] if unr"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/votes", query={"conversation_id": conversation_id, "tid": tid, "pid": pid}, body={})
    emit(result)


@app.command("create", help='[core] Cast a vote on a comment; creates the participant if missing, and returns the next comment to vote on in the same response.')
def create_votes_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation being voted in (403 if closed)"),
    tid: int = typer.Option(..., "--tid", help="comment id being voted on"),
    vote: int = typer.Option(..., "--vote", help="-1 agree (pull), 0 pass, 1 disagree (push)"),
    xid: Optional[str] = typer.Option(None, "--xid", help="external identity id (processed before ensureParticipant)"),
    starred: Optional[bool] = typer.Option(None, "--starred", help="also star the comment in the same call"),
    high_priority: Optional[bool] = typer.Option(None, "--high-priority", help="mark vote as high priority"),
    lang: Optional[str] = typer.Option(None, "--lang", help="preferred language for the returned nextComment"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/votes", query={}, body={"conversation_id": conversation_id, "tid": tid, "vote": vote, "xid": xid, "starred": starred, "high_priority": high_priority, "lang": lang})
    emit(result)


@app.command("get-famous", help="[core] Get 'famous'/featured participants (participants-of-interest, authors of consensus comments) with their vote vectors and projected positions, for the visualization overlay.")
def get_votes_get_famous(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to fetch featured participants for"),
    math_tick: Optional[int] = typer.Option(None, "--math-tick", help="math result version to align with"),
    ptptoiLimit: Optional[int] = typer.Option(None, "--ptptoiLimit", help="max participants-of-interest to return (default 30)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/votes/famous", query={"conversation_id": conversation_id, "math_tick": math_tick, "ptptoiLimit": ptptoiLimit}, body={})
    emit(result)


@app.command("get-me", help='[core] Get the full vote history of the authenticated caller in a conversation (all rows from votes, weight normalized from int to [-1,1]).')
def get_votes_get_me(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to read own votes from"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/votes/me", query={"conversation_id": conversation_id}, body={})
    emit(result)

