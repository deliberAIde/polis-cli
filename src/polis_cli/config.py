"""Profile-based configuration for polis-cli.

Profiles live in ~/.polis-cli/config.toml, one table per instance:

    [profiles.local]
    base_url = "http://localhost"
    auth = "password"            # "password" | "oidc"
    email = "admin@polis.local"
    # password prompted or via POLIS_PASSWORD env var

    [profiles.voxit-demo]
    base_url = "https://demo.voxit.example"
    auth = "oidc"
    oidc_token_url = "https://idp.example/realms/polis/protocol/openid-connect/token"
    oidc_client_id = "polis-cli"

Tokens/cookies are cached per profile in ~/.polis-cli/credentials.toml (0600).
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import tomli_w

CONFIG_DIR = Path(os.environ.get("POLIS_CLI_HOME", Path.home() / ".polis-cli"))
CONFIG_FILE = CONFIG_DIR / "config.toml"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.toml"


@dataclass
class Profile:
    name: str
    base_url: str
    auth: str = "password"  # "password" | "oidc"
    email: str | None = None
    oidc_token_url: str | None = None
    oidc_client_id: str | None = None
    api_version_tag: str | None = None  # pinned instance version, informational
    extra: dict = field(default_factory=dict)


def _load_toml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def load_profile(name: str) -> Profile:
    data = _load_toml(CONFIG_FILE)
    profiles = data.get("profiles", {})
    if name not in profiles:
        raise KeyError(
            f"Profile '{name}' not found in {CONFIG_FILE}. "
            f"Known profiles: {', '.join(profiles) or '(none)'}"
        )
    raw = dict(profiles[name])
    known = {k: raw.pop(k) for k in list(raw) if k in Profile.__dataclass_fields__}
    return Profile(name=name, **known, extra=raw)


def save_profile(profile: Profile) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_toml(CONFIG_FILE)
    profiles = data.setdefault("profiles", {})
    entry = {"base_url": profile.base_url, "auth": profile.auth}
    for key in ("email", "oidc_token_url", "oidc_client_id", "api_version_tag"):
        value = getattr(profile, key)
        if value is not None:
            entry[key] = value
    entry.update(profile.extra)
    profiles[profile.name] = entry
    with CONFIG_FILE.open("wb") as f:
        tomli_w.dump(data, f)


def load_cached_credential(profile_name: str) -> dict:
    return _load_toml(CREDENTIALS_FILE).get(profile_name, {})


def save_cached_credential(profile_name: str, credential: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_toml(CREDENTIALS_FILE)
    data[profile_name] = credential
    with CREDENTIALS_FILE.open("wb") as f:
        tomli_w.dump(data, f)
    try:
        CREDENTIALS_FILE.chmod(0o600)
    except OSError:
        pass  # best-effort on Windows
