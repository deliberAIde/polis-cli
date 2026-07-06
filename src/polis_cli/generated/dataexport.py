"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='dataexport endpoints (2)', no_args_is_help=True)


@app.command("get-dataexport", help='[admin] Queue an asynchronous data-export job (votes/comments dump) for the conversation via the math worker; the result is uploaded to S3 and the requesting user is notified by email.')
def get_dataexport_get_dataexport(
    conversation_id: str = typer.Option(..., "--conversation-id", help="declared twice: resolves zid and keeps the string"),
    format: Optional[str] = typer.Option(None, "--format", help="export format passed to the math worker (e.g. csv)"),
    unixTimestamp: Optional[str] = typer.Option(None, "--unixTimestamp", help="SECONDS; multiplied by 1000 server-side; NaN if omitted"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/dataExport", query={"conversation_id": conversation_id, "format": format, "unixTimestamp": unixTimestamp}, body={})
    emit(result)


@app.command("get-dataexport-results", help='[admin] Redirect to a pre-signed S3 URL (7-day expiry) for a previously generated export file in the polis-datadump bucket.')
def get_dataexport_get_dataexport_results(
    conversation_id: str = typer.Option(..., "--conversation-id", help="required by validators but UNUSED by the handler"),
    filename: Optional[str] = typer.Option(None, "--filename", help="S3 object name under {mathEnv}/ in bucket polis-datadump; effectively required"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/dataExport/results", query={"conversation_id": conversation_id, "filename": filename}, body={})
    emit(result)

