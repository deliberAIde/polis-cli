"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='reportcommentselections endpoints (1)', no_args_is_help=True)


@app.command("create-reportcommentselections", help="[admin] Include/exclude a specific comment in a report's correlation-matrix analysis (upserts report_comment_selections) and invalidates the cached correlation matrix so it is regenerated on next fetc")
def create_reportcommentselections_create_reportcommentselections(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    report_id: str = typer.Option(..., "--report-id", help="getReportIdFetchRid (rid)"),
    tid: int = typer.Option(..., "--tid", help="Comment (statement) id"),
    include: bool = typer.Option(..., "--include", help="true = selection 1 (include in report), false = -1 (exclude)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/reportCommentSelections", query={}, body={"conversation_id": conversation_id, "report_id": report_id, "tid": tid, "include": include})
    emit(result)

