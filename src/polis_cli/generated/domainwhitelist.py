"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='domainwhitelist endpoints (2)', no_args_is_help=True)


@app.command("get-domainwhitelist", help="[admin] Fetch the embed domain whitelist (comma-separated string) for the authenticated user's site_id.")
def get_domainwhitelist_get_domainwhitelist(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/domainWhitelist", query={}, body={})
    emit(result)


@app.command("create-domainwhitelist", help="[admin] Insert or update the embed domain whitelist for the authenticated user's site_id (controls which third-party domains may embed conversations).")
def create_domainwhitelist_create_domainwhitelist(
    domain_whitelist: str = typer.Option(..., "--domain-whitelist", help="comma-separated allowed embed domains; declared with need() but has default '' so effectiv"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/domainWhitelist", query={}, body={"domain_whitelist": domain_whitelist})
    emit(result)

