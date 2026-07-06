"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='reportexport endpoints (1)', no_args_is_help=True)


@app.command("get-reportexport", help="[core] Streams a CSV data export for the report's conversation; the report_type selects which dataset (conversation summary, comments, raw votes, participant vote matrix, participant importance, comme")
def get_reportexport_get_reportexport(
    report_id: str = typer.Argument(..., help="path param report_id"),
    report_type: str = typer.Argument(..., help="path param report_type"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", f"/api/v3/reportExport/{report_id}/{report_type}", query={}, body={})
    emit(result)

