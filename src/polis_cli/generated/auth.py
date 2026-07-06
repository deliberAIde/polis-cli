"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='auth endpoints (1)', no_args_is_help=True)


@app.command("create-deregister", help='[core] JWT-era logout stub: server does nothing and always returns 200; the client is responsible for discarding its JWT (and optionally hitting the OIDC logout endpoint).')
def create_auth_create_deregister(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/auth/deregister", query={}, body={})
    emit(result)

