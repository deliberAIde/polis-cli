"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='treevite endpoints (9)', no_args_is_help=True)


@app.command("create-acceptinvite", help='[experimental] Redeem a treevite invite code: creates an anonymous user+participant if not already authenticated, marks the invite used atomically, issues a persistent login_code, lazily creates the p')
def create_treevite_create_acceptinvite(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation the invite belongs to"),
    invite_code: str = typer.Option(..., "--invite-code", help="unused (status=0) treevite invite code to redeem"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/treevite/acceptInvite", query={}, body={"conversation_id": conversation_id, "invite_code": invite_code})
    emit(result)


@app.command("get-invites", help='[experimental] Paginated list of owner-generated (invite_owner_pid IS NULL) treevite invite codes for a conversation, joined with wave number, newest first.')
def get_treevite_get_invites(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose owner-generated treevite invites to list"),
    wave_id: Optional[int] = typer.Option(None, "--wave-id", help="filter to one treevite wave"),
    status: Optional[int] = typer.Option(None, "--status", help="filter by invite status (0=unused, 1=used)"),
    limit: Optional[int] = typer.Option(None, "--limit", help="page size; default 50, max 500"),
    offset: Optional[int] = typer.Option(None, "--offset", help="pagination offset"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/invites", query={"conversation_id": conversation_id, "wave_id": wave_id, "status": status, "limit": limit, "offset": offset}, body={})
    emit(result)


@app.command("get-invites-csv", help='[experimental] Download all owner-generated treevite invite codes for a conversation as a CSV attachment (columns: wave, invite_code, status, invite_used_at, created_at).')
def get_treevite_get_invites_csv(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose owner invites to export"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/invites/csv", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("create-login", help='[experimental] Verifies a treevite login code (SHA-256 lookup + bcrypt compare) and issues a participant JWT for re-entry')
def create_treevite_create_login(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    login_code: str = typer.Option(..., "--login-code", help="returning-participant login code issued at acceptInvite time"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/treevite/login", query={}, body={"conversation_id": conversation_id, "login_code": login_code})
    emit(result)


@app.command("get-me", help="[experimental] Returns the calling participant's treevite status: the wave they entered through and their own invite codes (nulls/empty if not a participant)")
def get_treevite_get_me(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/me", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-myinvites", help="[experimental] List the calling participant's own unused (status=0) treevite invite codes for a conversation; returns [] if the caller has no pid yet.")
def get_treevite_get_myinvites(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to list the calling participant's invites for"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/myInvites", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-myinvites-csv", help="[experimental] Download the calling participant's own unused treevite invite codes as a CSV attachment (columns: invite_code, status, created_at); header-only CSV if the caller has no pid.")
def get_treevite_get_myinvites_csv(
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation to export the calling participant's invites for"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/myInvites/csv", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-waves", help='[experimental] Lists treevite waves for a conversation (wave, parent_wave, invites_per_user, owner_invites, size, timestamps)')
def get_treevite_get_waves(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    wave: Optional[int] = typer.Option(None, "--wave", help="filter to a single wave number"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/treevite/waves", query={"conversation_id": conversation_id, "wave": wave}, body={})
    emit(result)


@app.command("create-waves", help='[experimental] Creates the next tree-invite wave for a conversation and generates invite codes sized by the parent wave')
def create_treevite_create_waves(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid"),
    invites_per_user: Optional[int] = typer.Option(None, "--invites-per-user", help="invite codes generated per participant of the parent wave"),
    owner_invites: Optional[int] = typer.Option(None, "--owner-invites", help="extra owner-held invite codes; at least one of invites_per_user/owner_invites must be > 0"),
    parent_wave: Optional[int] = typer.Option(None, "--parent-wave", help="defaults to latest existing wave"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/treevite/waves", query={}, body={"conversation_id": conversation_id, "invites_per_user": invites_per_user, "owner_invites": owner_invites, "parent_wave": parent_wave})
    emit(result)

