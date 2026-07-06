"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='dummybutton endpoints (1)', no_args_is_help=True)


@app.command("get-dummybutton", help='[internal] Feature-interest tracker: emails the admin team that a dummy button was clicked, returns empty 200')
def get_dummybutton_get_dummybutton(
    button: str = typer.Option(..., "--button", help="label of the placeholder feature button that was clicked"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/dummyButton", query={"button": button}, body={})
    emit(result)

