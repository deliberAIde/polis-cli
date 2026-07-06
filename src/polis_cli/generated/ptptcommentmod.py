"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='ptptcommentmod endpoints (1)', no_args_is_help=True)


@app.command("create-ptptcommentmod", help='[legacy] Participant crowdsourced moderation: records per-comment flags (spam/offtopic/important/etc.) into crowd_mod table')
def create_ptptcommentmod_create_ptptcommentmod(
    tid: int = typer.Option(..., "--tid", help="getInt"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    as_abusive: Optional[bool] = typer.Option(None, "--as-abusive", help="getBool (default null)"),
    as_factual: Optional[bool] = typer.Option(None, "--as-factual", help="getBool (default null)"),
    as_feeling: Optional[bool] = typer.Option(None, "--as-feeling", help="getBool (default null)"),
    as_important: Optional[bool] = typer.Option(None, "--as-important", help="getBool (default null)"),
    as_notfact: Optional[bool] = typer.Option(None, "--as-notfact", help="getBool (default null)"),
    as_notgoodidea: Optional[bool] = typer.Option(None, "--as-notgoodidea", help="getBool (default null)"),
    as_notmyfeeling: Optional[bool] = typer.Option(None, "--as-notmyfeeling", help="getBool (default null)"),
    as_offtopic: Optional[bool] = typer.Option(None, "--as-offtopic", help="getBool (default null)"),
    as_spam: Optional[bool] = typer.Option(None, "--as-spam", help="getBool (default null)"),
    as_unsure: Optional[bool] = typer.Option(None, "--as-unsure", help="getBool (default null)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/ptptCommentMod", query={}, body={"tid": tid, "conversation_id": conversation_id, "as_abusive": as_abusive, "as_factual": as_factual, "as_feeling": as_feeling, "as_important": as_important, "as_notfact": as_notfact, "as_notgoodidea": as_notgoodidea, "as_notmyfeeling": as_notmyfeeling, "as_offtopic": as_offtopic, "as_spam": as_spam, "as_unsure": as_unsure})
    emit(result)

