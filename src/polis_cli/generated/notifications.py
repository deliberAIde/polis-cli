"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='notifications endpoints (2)', no_args_is_help=True)


@app.command("get-subscribe", help='[core] Email-link target that sets participants.subscribed=1 for the user with that email in the conversation; verifies HMAC signature, responds with an HTML confirmation page.')
def get_notifications_get_subscribe(
    signature: str = typer.Option(..., "--signature", help="HMAC-SHA1 of path+sorted params; secret is hardcoded in notify.ts"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="declared twice: one validator resolves zid, the other preserves the string for URL buildin"),
    email: str = typer.Option(..., "--email", help="email address of the participant to subscribe"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/notifications/subscribe", query={"signature": signature, "conversation_id": conversation_id, "email": email}, body={})
    emit(result)


@app.command("get-unsubscribe", help='[core] Email-link target that sets participants.subscribed=0 for the user with that email; verifies HMAC signature, responds with an HTML confirmation page.')
def get_notifications_get_unsubscribe(
    signature: str = typer.Option(..., "--signature", help="HMAC-SHA1 of path+sorted params; secret hardcoded in notify.ts"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="declared twice (zid resolution + string preserved); client passes once"),
    email: str = typer.Option(..., "--email", help="email address of the participant to unsubscribe"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/notifications/unsubscribe", query={"signature": signature, "conversation_id": conversation_id, "email": email}, body={})
    emit(result)

