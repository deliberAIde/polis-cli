"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='contexts endpoints (2)', no_args_is_help=True)


@app.command("list", help='[legacy] List all public context names (contexts group conversations; usable as the context filter on GET /conversations).')
def get_contexts_list(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/contexts", query={}, body={})
    emit(result)


@app.command("create", help='[legacy] Create a new public context owned by the authenticated user; fails if the name already exists.')
def create_contexts_create(
    name: str = typer.Option(..., "--name", help="unique context name"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/contexts", query={}, body={"name": name})
    emit(result)

