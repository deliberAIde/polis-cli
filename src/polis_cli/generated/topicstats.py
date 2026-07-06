"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='topicstats endpoints (1)', no_args_is_help=True)


@app.command("get-topicstats", help='[experimental] Returns per-topic comment counts and comment tids from Delphi DynamoDB topic-cluster tables for a report')
def get_topicstats_get_topicstats(
    report_id: str = typer.Option(..., "--report-id", help="report id; resolved to zid via getZidFromReport"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicStats", query={"report_id": report_id}, body={})
    emit(result)

