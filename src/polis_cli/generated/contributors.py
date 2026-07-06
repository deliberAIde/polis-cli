"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='contributors endpoints (1)', no_args_is_help=True)


@app.command("create", help='[internal] Records an open-source contributor-license-agreement signature and emails the team')
def create_contributors_create(
    agreement_version: int = typer.Option(..., "--agreement-version", help="getIntInRange(1,999999)"),
    name: str = typer.Option(..., "--name", help="getStringLimitLength(746)"),
    email: str = typer.Option(..., "--email", help="getStringLimitLength(256)"),
    github_id: str = typer.Option(..., "--github-id", help="getStringLimitLength(256)"),
    company_name: str = typer.Option(..., "--company-name", help="getStringLimitLength(746)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/contributors", query={}, body={"agreement_version": agreement_version, "name": name, "email": email, "github_id": github_id, "company_name": company_name})
    emit(result)

