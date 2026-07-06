"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='participationinit endpoints (1)', no_args_is_help=True)


@app.command("get-participationinit", help='[core] One-shot bootstrap for the participation UI: returns user, participant record, conversation, own votes, next comment to vote on, PCA math, and famous/ptptoi voters; middleware may mint and retu')
def get_participationinit_get_participationinit(
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="Conversation to bootstrap; without it only the user object is returned"),
    ptptoiLimit: Optional[int] = typer.Option(None, "--ptptoiLimit", help="Max participants-of-interest in the famous block (default 30)"),
    includePCA: Optional[bool] = typer.Option(None, "--includePCA", help="Set false to omit PCA math payload"),
    lang: Optional[str] = typer.Option(None, "--lang", help="Preferred language for nextComment; 'acceptLang' uses the Accept-Language header"),
    domain_whitelist_override_key: Optional[str] = typer.Option(None, "--domain-whitelist-override-key", help="Bypass key for the embedding-domain whitelist check"),
    xid: Optional[str] = typer.Option(None, "--xid", help="External identity for xid-based participants"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/participationInit", query={"conversation_id": conversation_id, "ptptoiLimit": ptptoiLimit, "includePCA": includePCA, "lang": lang, "domain_whitelist_override_key": domain_whitelist_override_key, "xid": xid}, body={})
    emit(result)

