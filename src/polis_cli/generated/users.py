"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='users endpoints (3)', no_args_is_help=True)


@app.command("list", help="[core] Returns the current user object for the JWT-authenticated caller (the API's 'whoami'); with xid+owner_uid it resolves and returns the xid-mapped user instead.")
def get_users_list(
    xid: Optional[str] = typer.Option(None, "--xid", help="External identity to look up (used together with owner_uid)"),
    owner_uid: Optional[int] = typer.Option(None, "--owner-uid", help="Owner uid scoping the xid lookup"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/users", query={"xid": xid, "owner_uid": owner_uid}, body={})
    emit(result)


@app.command("update", help="[core] Updates the caller's user record (email and/or display name); polis-dev users may update another account via uid_of_user.")
def update_users_update(
    email: Optional[str] = typer.Option(None, "--email", help="New email for the account"),
    hname: Optional[str] = typer.Option(None, "--hname", help="New display name"),
    uid_of_user: Optional[int] = typer.Option(None, "--uid-of-user", help="Target uid to update (polis-dev only; otherwise ignored)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/users", query={}, body={"email": email, "hname": hname, "uid_of_user": uid_of_user})
    emit(result)


@app.command("create-invite", help='[admin] Generates single-use suzinvite tokens, saves them, emails each address an invite link to the conversation, and records the inviter relationship.')
def create_users_create_invite(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation participants are invited to"),
    emails: str = typer.Option(..., "--emails", help="Email addresses to invite (one single-use token each)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/users/invite", query={}, body={"conversation_id": conversation_id, "emails": emails})
    emit(result)

