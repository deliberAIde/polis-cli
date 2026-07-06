"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='conversations endpoints (6)', no_args_is_help=True)


@app.command("list", help='[core] List conversations the user owns/co-admins (optionally participates in), list by context, or fetch one conversation by conversation_id; adds conversation_id, url, is_owner, is_mod and strips zi')
def get_conversations_list(
    include_all_conversations_i_am_in: Optional[bool] = typer.Option(None, "--include-all-conversations-i-am-in", help="also include conversations the user participates in (not just site-admin/owned)"),
    is_active: Optional[bool] = typer.Option(None, "--is-active", help="filter"),
    is_draft: Optional[bool] = typer.Option(None, "--is-draft", help="filter"),
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="if given, returns that single conversation (works without login)"),
    limit: Optional[int] = typer.Option(None, "--limit", help="default 999 when listing"),
    context: Optional[str] = typer.Option(None, "--context", help="list conversations in a context; '/' lists all public root conversations"),
    xid: Optional[str] = typer.Option(None, "--xid", help="if set, each conversation's url becomes a single-use /ot/ suzinvite URL for this external "),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversations", query={"include_all_conversations_i_am_in": include_all_conversations_i_am_in, "is_active": is_active, "is_draft": is_draft, "conversation_id": conversation_id, "limit": limit, "context": context, "xid": xid}, body={})
    emit(result)


@app.command("create", help='[core] Create a conversation owned by the authenticated user (org_id defaults to uid, is_public forced true, auth_needed_to_vote/write come from server DEFAULTS); registers or claims a zinvite and ret')
def create_conversations_create(
    is_active: Optional[bool] = typer.Option(None, "--is-active", help="default true"),
    is_draft: Optional[bool] = typer.Option(None, "--is-draft", help="default false"),
    is_anon: Optional[bool] = typer.Option(None, "--is-anon", help="default false"),
    owner_sees_participation_stats: Optional[bool] = typer.Option(None, "--owner-sees-participation-stats", help="default false"),
    profanity_filter: Optional[bool] = typer.Option(None, "--profanity-filter", help="default true"),
    short_url: Optional[bool] = typer.Option(None, "--short-url", help="default false; generate a 6-char zinvite instead of 12"),
    spam_filter: Optional[bool] = typer.Option(None, "--spam-filter", help="default true"),
    strict_moderation: Optional[bool] = typer.Option(None, "--strict-moderation", help="default false"),
    context: Optional[str] = typer.Option(None, "--context", help="default ''; context (group) name to attach the conversation to"),
    topic: Optional[str] = typer.Option(None, "--topic", help="default ''"),
    description: Optional[str] = typer.Option(None, "--description", help="default ''"),
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="default ''; claim a previously reserved conversation_id (from POST /reserve_conversation_i"),
    is_data_open: Optional[bool] = typer.Option(None, "--is-data-open", help="default false"),
    ownerXid: Optional[str] = typer.Option(None, "--ownerXid", help="validated but unused by the handler in this build"),
    treevite_enabled: Optional[bool] = typer.Option(None, "--treevite-enabled", help="default false"),
    topics_enabled: Optional[bool] = typer.Option(None, "--topics-enabled", help="default false"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/conversations", query={}, body={"is_active": is_active, "is_draft": is_draft, "is_anon": is_anon, "owner_sees_participation_stats": owner_sees_participation_stats, "profanity_filter": profanity_filter, "short_url": short_url, "spam_filter": spam_filter, "strict_moderation": strict_moderation, "context": context, "topic": topic, "description": description, "conversation_id": conversation_id, "is_data_open": is_data_open, "ownerXid": ownerXid, "treevite_enabled": treevite_enabled, "topics_enabled": topics_enabled})
    emit(result)


@app.command("update", help='[core] Update conversation settings (moderator-only); optionally regenerates a short zinvite and/or sends the creation email; returns the full updated conversation row with is_mod=true.')
def update_conversations_update(
    conversation_id: str = typer.Option(..., "--conversation-id", help="declared twice: resolves zid and keeps the string for URL building"),
    is_active: Optional[bool] = typer.Option(None, "--is-active", help="getBool"),
    is_anon: Optional[bool] = typer.Option(None, "--is-anon", help="getBool"),
    is_draft: Optional[bool] = typer.Option(None, "--is-draft", help="DEFAULT false — omitted means it is actively reset to false"),
    is_data_open: Optional[bool] = typer.Option(None, "--is-data-open", help="DEFAULT false — reset to false when omitted"),
    owner_sees_participation_stats: Optional[bool] = typer.Option(None, "--owner-sees-participation-stats", help="DEFAULT false — reset to false when omitted"),
    profanity_filter: Optional[bool] = typer.Option(None, "--profanity-filter", help="getBool"),
    short_url: Optional[bool] = typer.Option(None, "--short-url", help="DEFAULT false; true regenerates the zinvite as a 6-char short id and returns 201"),
    spam_filter: Optional[bool] = typer.Option(None, "--spam-filter", help="getBool"),
    strict_moderation: Optional[bool] = typer.Option(None, "--strict-moderation", help="getBool"),
    topic: Optional[str] = typer.Option(None, "--topic", help="getOptionalStringLimitLength(1000)"),
    description: Optional[str] = typer.Option(None, "--description", help="getOptionalStringLimitLength(50000)"),
    importance_enabled: Optional[bool] = typer.Option(None, "--importance-enabled", help="getBool"),
    vis_type: Optional[int] = typer.Option(None, "--vis-type", help="getInt"),
    help_type: Optional[int] = typer.Option(None, "--help-type", help="getInt"),
    write_type: Optional[int] = typer.Option(None, "--write-type", help="getInt"),
    bgcolor: Optional[str] = typer.Option(None, "--bgcolor", help="'default' clears to null"),
    help_color: Optional[str] = typer.Option(None, "--help-color", help="'default' clears to null"),
    help_bgcolor: Optional[str] = typer.Option(None, "--help-bgcolor", help="'default' clears to null"),
    style_btn: Optional[str] = typer.Option(None, "--style-btn", help="getOptionalStringLimitLength(500)"),
    auth_needed_to_vote: Optional[bool] = typer.Option(None, "--auth-needed-to-vote", help="validated but IGNORED by the handler (never written)"),
    auth_needed_to_write: Optional[bool] = typer.Option(None, "--auth-needed-to-write", help="validated but IGNORED by the handler (never written)"),
    auth_opt_allow_3rdparty: Optional[bool] = typer.Option(None, "--auth-opt-allow-3rdparty", help="getBool"),
    verifyMeta: Optional[bool] = typer.Option(None, "--verifyMeta", help="true = reject update unless every metadata question has at least one live answer"),
    send_created_email: Optional[bool] = typer.Option(None, "--send-created-email", help="sends the 'Conversation created' email with the share link (creation email deliberately ha"),
    context: Optional[str] = typer.Option(None, "--context", help="validated but not written by the handler in this build"),
    link_url: Optional[str] = typer.Option(None, "--link-url", help="getStringLimitLength(1, 9999)"),
    subscribe_type: Optional[int] = typer.Option(None, "--subscribe-type", help="getInt"),
    treevite_enabled: Optional[bool] = typer.Option(None, "--treevite-enabled", help="DEFAULT false — reset to false when omitted"),
    topics_enabled: Optional[bool] = typer.Option(None, "--topics-enabled", help="DEFAULT false — reset to false when omitted"),
    use_xid_whitelist: Optional[bool] = typer.Option(None, "--use-xid-whitelist", help="getBool"),
    xid_required: Optional[bool] = typer.Option(None, "--xid-required", help="getBool"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/conversations", query={}, body={"conversation_id": conversation_id, "is_active": is_active, "is_anon": is_anon, "is_draft": is_draft, "is_data_open": is_data_open, "owner_sees_participation_stats": owner_sees_participation_stats, "profanity_filter": profanity_filter, "short_url": short_url, "spam_filter": spam_filter, "strict_moderation": strict_moderation, "topic": topic, "description": description, "importance_enabled": importance_enabled, "vis_type": vis_type, "help_type": help_type, "write_type": write_type, "bgcolor": bgcolor, "help_color": help_color, "help_bgcolor": help_bgcolor, "style_btn": style_btn, "auth_needed_to_vote": auth_needed_to_vote, "auth_needed_to_write": auth_needed_to_write, "auth_opt_allow_3rdparty": auth_opt_allow_3rdparty, "verifyMeta": verifyMeta, "send_created_email": send_created_email, "context": context, "link_url": link_url, "subscribe_type": subscribe_type, "treevite_enabled": treevite_enabled, "topics_enabled": topics_enabled, "use_xid_whitelist": use_xid_whitelist, "xid_required": xid_required})
    emit(result)


@app.command("get-preload", help='[core] Public, cacheable conversation metadata used to preload the participation client: topic, description, created, link_url, parent_url, vis/write/help types, colors, style_btn, auth_opt_allow_3rdp')
def get_conversations_get_preload(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getStringLimitLength(1, 1000)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversations/preload", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-recent-activity", help='[internal] Server-operator-only: raw conversations rows modified since the given time.')
def get_conversations_get_recent_activity(
    sinceUnixTimestamp: Optional[str] = typer.Option(None, "--sinceUnixTimestamp", help="seconds; default = last 7 days"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversations/recent_activity", query={"sinceUnixTimestamp": sinceUnixTimestamp}, body={})
    emit(result)


@app.command("get-recently-started", help='[internal] Server-operator-only: raw conversations rows created since the given time (unprocessed DB rows, zid included).')
def get_conversations_get_recently_started(
    sinceUnixTimestamp: Optional[str] = typer.Option(None, "--sinceUnixTimestamp", help="seconds; default = last 7 days"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/conversations/recently_started", query={"sinceUnixTimestamp": sinceUnixTimestamp}, body={})
    emit(result)

