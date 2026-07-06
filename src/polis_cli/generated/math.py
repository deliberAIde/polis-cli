"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='math endpoints (3)', no_args_is_help=True)


@app.command("get-correlationmatrix", help="[core] Fetches the comment correlation matrix for a report from math_report_correlationmatrix; if absent, enqueues a 'generate_report_data' worker task and returns 202 pending; returns 202 'polis_repo")
def get_math_get_correlationmatrix(
    report_id: str = typer.Option(..., "--report-id", help="Report whose correlation matrix to fetch"),
    math_tick: Optional[int] = typer.Option(None, "--math-tick", help="Minimum math_tick of acceptable cached result"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/math/correlationMatrix", query={"report_id": report_id, "math_tick": math_tick}, body={})
    emit(result)


@app.command("get-pca", help='[legacy] Dead endpoint: clients were migrated off this path; unconditionally returns HTTP 304 with empty body.')
def get_math_get_pca(
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/math/pca", query={}, body={})
    emit(result)


@app.command("get-pca2", help='[core] Primary math-results endpoint: returns the full PCA/clustering payload for a conversation (pca, base-clusters, group-clusters, consensus, repness, votes-base, math_tick), served as pre-gzipped ')
def get_math_get_pca2(
    conversation_id: str = typer.Option(..., "--conversation-id", help="Conversation to fetch math results for"),
    math_tick: Optional[int] = typer.Option(None, "--math-tick", help="Return results only if newer than this tick; mutually exclusive with If-None-Match header;"),
    keys: Optional[str] = typer.Option(None, "--keys", help="Filter response to only these top-level keys of the math object (e.g. group-clusters, cons"),
    If_None_Match: Optional[str] = typer.Option(None, "--If-None-Match", help="ETag conditional fetch; parsed to a math_tick; 400 if combined with math_tick param"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/math/pca2", query={"conversation_id": conversation_id, "math_tick": math_tick, "keys": keys, "If-None-Match": If_None_Match}, body={})
    emit(result)

