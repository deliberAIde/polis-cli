"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='reportnarrative endpoints (1)', no_args_is_help=True)


@app.command("get-reportnarrative", help="[experimental] Streams an LLM-generated narrative report (group-informed consensus, uncertainty, topic sections) for a report as a chunked text/plain stream interleaved with 'POLIS-PING:' keepalive ma")
def get_reportnarrative_get_reportnarrative(
    report_id: str = typer.Option(..., "--report-id", help="getReportIdFetchRid (rid)"),
    model: Optional[str] = typer.Option(None, "--model", help="LLM vendor for narrative generation (openai / anthropic / gemini paths exist in the file)"),
    modelVersion: Optional[str] = typer.Option(None, "--modelVersion", help="Specific model version override"),
    noCache: Optional[str] = typer.Option(None, "--noCache", help="Skip the DynamoDB report_narrative_store cache"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/reportNarrative", query={"report_id": report_id, "model": model, "modelVersion": modelVersion, "noCache": noCache}, body={})
    emit(result)

