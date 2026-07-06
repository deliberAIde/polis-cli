"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='collectivestatement endpoints (2)', no_args_is_help=True)


@app.command("get-collectivestatement", help='[experimental] Fetches stored collective statement(s) from DynamoDB')
def get_collectivestatement_get_collectivestatement(
    report_id: Optional[str] = typer.Option(None, "--report-id", help="returns all statements for the conversation, deduplicated to latest per topic"),
    statement_id: Optional[str] = typer.Option(None, "--statement-id", help="fetch a single stored statement; one of report_id/statement_id required"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/collectiveStatement", query={"report_id": report_id, "statement_id": statement_id}, body={})
    emit(result)


@app.command("create-collectivestatement", help='[experimental] Generates an LLM (Claude via Anthropic SDK) first-person-plural collective statement from high-consensus comments of a topic and stores it in DynamoDB Delphi_CollectiveStatement')
def create_collectivestatement_create_collectivestatement(
    report_id: str = typer.Option(..., "--report-id", help="handler-validated string"),
    topic_key: str = typer.Option(..., "--topic-key", help="handler-validated string"),
    topic_name: str = typer.Option(..., "--topic-name", help="handler-validated string"),
    qualifying_tids: Optional[str] = typer.Option(None, "--qualifying-tids", help="handler-read array of comment ids"),
    group_consensus: Optional[str] = typer.Option(None, "--group-consensus", help="handler-read object"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/collectiveStatement", query={}, body={"report_id": report_id, "topic_key": topic_key, "topic_name": topic_name, "qualifying_tids": qualifying_tids, "group_consensus": group_consensus})
    emit(result)

