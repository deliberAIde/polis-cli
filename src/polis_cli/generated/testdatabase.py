"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='testdatabase endpoints (1)', no_args_is_help=True)


@app.command("get-testdatabase", help="[internal] DB health check; runs 'select uid from users limit 1' and returns {status:'ok'} or 500")
def get_testdatabase_get_testdatabase(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/testDatabase", query={}, body={})
    emit(result)

