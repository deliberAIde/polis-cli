"""Shared runtime helpers used by generated command modules."""

from __future__ import annotations

import json
import sys

from .client import PolisClient, PolisError
from .config import load_profile


def get_client(profile_name: str) -> PolisClient:
    try:
        return PolisClient(load_profile(profile_name))
    except KeyError as e:
        print(str(e), file=sys.stderr)
        raise SystemExit(2) from e


def emit(result) -> None:
    """Generated commands always emit JSON — agents are the primary consumer."""
    print(json.dumps(result, indent=2, default=str, ensure_ascii=False))
