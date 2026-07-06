"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='comments endpoints (4)', no_args_is_help=True)


@app.command("list", help="[core] List a conversation's comments; legacy bare-array response, or {comments, pagination} wrapper when limit is passed (zid stripped, conversation_id added).")
def get_comments_list(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to list comments for (resolved to internal zid)"),
    report_id: Optional[str] = typer.Option(None, "--report-id", help="if given, each comment gets an includeInReport flag from report_comment_selections"),
    tids: Optional[str] = typer.Option(None, "--tids", help="restrict to specific comment ids"),
    moderation: Optional[bool] = typer.Option(None, "--moderation", help="include moderation fields/view (owner/moderator listing)"),
    mod: Optional[int] = typer.Option(None, "--mod", help="filter by exact moderation status (-1 rejected, 0 unmoderated, 1 accepted)"),
    modIn: Optional[bool] = typer.Option(None, "--modIn", help="true = comments participant-visible under current strict-mod setting, false = invisible on"),
    mod_gt: Optional[int] = typer.Option(None, "--mod-gt", help="filter comments with mod greater than this value"),
    include_voting_patterns: Optional[bool] = typer.Option(None, "--include-voting-patterns", help="include agree/disagree/pass counts per comment"),
    limit: Optional[int] = typer.Option(None, "--limit", help="enables paginated response format; default 50, max 500"),
    offset: Optional[int] = typer.Option(None, "--offset", help="pagination offset (only with limit)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/comments", query={"conversation_id": conversation_id, "report_id": report_id, "tids": tids, "moderation": moderation, "mod": mod, "modIn": modIn, "mod_gt": mod_gt, "include_voting_patterns": include_voting_patterns, "limit": limit, "offset": offset}, body={})
    emit(result)


@app.command("create", help='[core] Submit a new comment/statement; creates the participant if missing, runs profanity/toxicity moderation (pro conversations), detects language, optionally records an initial vote, notifies modera')
def create_comments_create(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to post into"),
    txt: str = typer.Option(..., "--txt", help="the statement text (max 997 chars); duplicates within a conversation are rejected 409"),
    xid: Optional[str] = typer.Option(None, "--xid", help="external identity id for SSO participants (processed before ensureParticipant)"),
    vote: Optional[int] = typer.Option(None, "--vote", help="auto-vote on own comment (-1 agree, 0 pass, 1 disagree); seed comments default to 0 if omi"),
    is_seed: Optional[bool] = typer.Option(None, "--is-seed", help="mark as seed statement; auto-approved regardless of moderation settings"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/comments", query={}, body={"conversation_id": conversation_id, "txt": txt, "xid": xid, "vote": vote, "is_seed": is_seed})
    emit(result)


@app.command("update", help='[admin] Moderate a comment: set active, mod status, and is_meta. Moderator/owner only.')
def update_comments_update(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the comment belongs to"),
    tid: int = typer.Option(..., "--tid", help="comment id to moderate"),
    active: bool = typer.Option(..., "--active", help="whether the comment is active (shown to participants)"),
    mod: int = typer.Option(..., "--mod", help="moderation status (-1 rejected, 0 unmoderated, 1 accepted)"),
    is_meta: bool = typer.Option(..., "--is-meta", help="flag comment as meta (excluded from opinion math)"),
    velocity: int = typer.Option(..., "--velocity", help="required by the validator chain but IGNORED by the handler (update touches only active/mod"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/comments", query={}, body={"conversation_id": conversation_id, "tid": tid, "active": active, "mod": mod, "is_meta": is_meta, "velocity": velocity})
    emit(result)


@app.command("get-translations", help='[core] Fetch stored translations of a comment for a language; if none exist, translates on demand (external translate service), stores, and returns the result.')
def get_comments_get_translations(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the comment belongs to"),
    tid: Optional[int] = typer.Option(None, "--tid", help="comment id — declared optional (want) but the handler dereferences it; effectively require"),
    lang: Optional[str] = typer.Option(None, "--lang", help="target language code; matched on first 2 chars against stored translations; also effective"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/comments/translations", query={"conversation_id": conversation_id, "tid": tid, "lang": lang}, body={})
    emit(result)

