"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='xid endpoints (1)', no_args_is_help=True)


@app.command("list", help='[admin] Download a CSV summary of participant xids for a conversation identified by its UUID-based report filename')
def get_xid_list(
    xid_report: str = typer.Argument(..., help="path param xid_report"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", f"/api/v3/xid/{xid_report}", query={}, body={})
    emit(result)

