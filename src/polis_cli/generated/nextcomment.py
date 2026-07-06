"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='nextcomment endpoints (1)', no_args_is_help=True)


@app.command("get-nextcomment", help="[core] Get the next comment for the participant to vote on (priority-weighted, excludes already-voted and 'without' ids); 15s timeout guard.")
def get_nextcomment_get_nextcomment(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to draw the next unvoted comment from"),
    not_voted_by_pid: Optional[str] = typer.Option(None, "--not-voted-by-pid", help="participant id to exclude already-voted comments for; normally resolved from auth (callers"),
    without: Optional[str] = typer.Option(None, "--without", help="comment ids to exclude (e.g. currently displayed)"),
    lang: Optional[str] = typer.Option(None, "--lang", help="preferred language; translation attached if available"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/nextComment", query={"conversation_id": conversation_id, "not_voted_by_pid": not_voted_by_pid, "without": without, "lang": lang}, body={})
    emit(result)

