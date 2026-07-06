"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='votes_bulk endpoints (1)', no_args_is_help=True)


@app.command("create-votes-bulk", help='[experimental] Async bulk vote import (bring-your-own-data): uploads CSV to S3, records a byod_import_jobs row, and enqueues an SQS mapping job; comments must have been created via comments-bulk with ')
def create_votes_bulk_create_votes_bulk(
    conversation_id: str = typer.Option(..., "--conversation-id", help="target conversation; must contain at least one comment with non-null original_id (else 400"),
    csv: str = typer.Option(..., "--csv", help="CSV of external votes to import; 400 polis_err_param_missing_csv_votes if absent"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/votes-bulk", query={}, body={"conversation_id": conversation_id, "csv": csv})
    emit(result)

