"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='comments_bulk endpoints (1)', no_args_is_help=True)


@app.command("create-comments-bulk", help='[admin] Bulk-upload seed statements from CSV; moderator-only (403 polis_err_post_comment_auth otherwise); per-row success/skip/error results; original_id stored for external vote mapping.')
def create_comments_bulk_create_comments_bulk(
    conversation_id: str = typer.Option(..., "--conversation-id", help="target conversation"),
    csv: str = typer.Option(..., "--csv", help="CSV string with header row; columns comment_text and optional original_id; 400 polis_err_p"),
    is_seed: Optional[bool] = typer.Option(None, "--is-seed", help="treat all rows as seed statements (each gets a default pass vote)"),
    xid: Optional[str] = typer.Option(None, "--xid", help="external identity id"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/comments-bulk", query={}, body={"conversation_id": conversation_id, "csv": csv, "is_seed": is_seed, "xid": xid})
    emit(result)

