"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='all_conversations endpoints (1)', no_args_is_help=True)


@app.command("list", help='[internal] Server-operator-only paginated listing of ALL conversations on the instance with participant/comment counts and owner_email, filterable and sortable.')
def get_all_conversations_list(
    limit: Optional[int] = typer.Option(None, "--limit", help="default 50, capped at 500 by pagination helper"),
    offset: Optional[int] = typer.Option(None, "--offset", help="getIntInRange(0, 99999999)"),
    sort_by: Optional[str] = typer.Option(None, "--sort-by", help="created (default) | updated/modified | participant_count | comment_count"),
    sort_dir: Optional[str] = typer.Option(None, "--sort-dir", help="asc | desc (default)"),
    owner_email: Optional[str] = typer.Option(None, "--owner-email", help="ILIKE substring match on owner email"),
    is_active: Optional[bool] = typer.Option(None, "--is-active", help="getBool"),
    recently_updated_days: Optional[int] = typer.Option(None, "--recently-updated-days", help="getIntInRange(0, 36500)"),
    recently_created_days: Optional[int] = typer.Option(None, "--recently-created-days", help="getIntInRange(0, 36500)"),
    min_comment_count: Optional[int] = typer.Option(None, "--min-comment-count", help="getIntInRange(0, 100000000)"),
    min_participant_count: Optional[int] = typer.Option(None, "--min-participant-count", help="getIntInRange(0, 100000000)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/all_conversations", query={"limit": limit, "offset": offset, "sort_by": sort_by, "sort_dir": sort_dir, "owner_email": owner_email, "is_active": is_active, "recently_updated_days": recently_updated_days, "recently_created_days": recently_created_days, "min_comment_count": min_comment_count, "min_participant_count": min_participant_count}, body={})
    emit(result)

