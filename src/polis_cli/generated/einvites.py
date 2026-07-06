"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='einvites endpoints (2)', no_args_is_help=True)


@app.command("list", help='[legacy] Look up an einvite token and return its row (used by the registration page to prefill the email); 500 polis_err_missing_einvite if not found.')
def get_einvites_list(
    einvite: str = typer.Option(..., "--einvite", help="einvite token from the emailed link"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/einvites", query={"einvite": einvite}, body={})
    emit(result)


@app.command("create", help='[legacy] Generate a 30-char einvite token, store it in the einvites table, and email an account-signup invite link to the address (legacy invite-gated registration flow, not conversation invites).')
def create_einvites_create(
    email: str = typer.Option(..., "--email", help="address to send the account-creation invite to"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/einvites", query={}, body={"email": email})
    emit(result)

