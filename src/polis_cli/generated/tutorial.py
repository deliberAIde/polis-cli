"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='tutorial endpoints (1)', no_args_is_help=True)


@app.command("create", help="[internal] Persist the caller's UI tutorial progress step on their user record.")
def create_tutorial_create(
    step: int = typer.Option(..., "--step", help="tutorial step number to persist (stored in users.tut)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/tutorial", query={}, body={"step": step})
    emit(result)

