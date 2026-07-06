"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='reports endpoints (3)', no_args_is_help=True)


@app.command("list", help='[core] Lists report objects. Internal rid/zid are stripped and replaced with the public conversation_id; returns report_id, report_name, label_* fields, created/modified etc.')
def get_reports_list(
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="List all reports for this conversation (moderator only). Mutually exclusive with report_id"),
    report_id: Optional[str] = typer.Option(None, "--report-id", help="Fetch a single report by public id; acts as an access capability"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/reports", query={"conversation_id": conversation_id, "report_id": report_id}, body={})
    emit(result)


@app.command("create", help="[core] Creates a new report for a conversation: generates a public report_id ('r' + 20-char token) and inserts into the reports table.")
def create_reports_create(
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="Declared with want() but effectively required — without it the moderator check fails with "),
    mod_level: Optional[int] = typer.Option(None, "--mod-level", help="Moderation level stored on the report"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/reports", query={}, body={"conversation_id": conversation_id, "mod_level": mod_level})
    emit(result)


@app.command("update", help="[core] Updates a report's name and axis/group labels (only report_name and label_* columns are writable; everything else is filtered out).")
def update_reports_update(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    report_id: str = typer.Option(..., "--report-id", help="getReportIdFetchRid (rid)"),
    report_name: Optional[str] = typer.Option(None, "--report-name", help="getStringLimitLength(999)"),
    label_x_neg: Optional[str] = typer.Option(None, "--label-x-neg", help="getStringLimitLength(999)"),
    label_x_pos: Optional[str] = typer.Option(None, "--label-x-pos", help="getStringLimitLength(999)"),
    label_y_neg: Optional[str] = typer.Option(None, "--label-y-neg", help="getStringLimitLength(999)"),
    label_y_pos: Optional[str] = typer.Option(None, "--label-y-pos", help="getStringLimitLength(999)"),
    label_group_0: Optional[str] = typer.Option(None, "--label-group-0", help="getStringLimitLength(999)"),
    label_group_1: Optional[str] = typer.Option(None, "--label-group-1", help="getStringLimitLength(999)"),
    label_group_2: Optional[str] = typer.Option(None, "--label-group-2", help="getStringLimitLength(999)"),
    label_group_3: Optional[str] = typer.Option(None, "--label-group-3", help="getStringLimitLength(999)"),
    label_group_4: Optional[str] = typer.Option(None, "--label-group-4", help="getStringLimitLength(999)"),
    label_group_5: Optional[str] = typer.Option(None, "--label-group-5", help="getStringLimitLength(999)"),
    label_group_6: Optional[str] = typer.Option(None, "--label-group-6", help="getStringLimitLength(999)"),
    label_group_7: Optional[str] = typer.Option(None, "--label-group-7", help="getStringLimitLength(999)"),
    label_group_8: Optional[str] = typer.Option(None, "--label-group-8", help="getStringLimitLength(999)"),
    label_group_9: Optional[str] = typer.Option(None, "--label-group-9", help="getStringLimitLength(999)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("PUT", "/api/v3/reports", query={}, body={"conversation_id": conversation_id, "report_id": report_id, "report_name": report_name, "label_x_neg": label_x_neg, "label_x_pos": label_x_pos, "label_y_neg": label_y_neg, "label_y_pos": label_y_pos, "label_group_0": label_group_0, "label_group_1": label_group_1, "label_group_2": label_group_2, "label_group_3": label_group_3, "label_group_4": label_group_4, "label_group_5": label_group_5, "label_group_6": label_group_6, "label_group_7": label_group_7, "label_group_8": label_group_8, "label_group_9": label_group_9})
    emit(result)

