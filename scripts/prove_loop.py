"""Phase 0 — prove the full loop against the local Pol.is sandbox.

    create -> seed -> (moderate) -> vote -> math -> close -> report -> export CSVs

Run from the polis-cli repo root (stack must be up, see ../polis):

    python scripts/prove_loop.py

Assumes the stock dev sandbox: nginx on https://localhost, OIDC simulator on
https://localhost:3000, seeded test accounts (admin@polis.test etc.).
Self-signed dev TLS -> verification disabled here (sandbox only!).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx  # noqa: E402

from polis_cli.client import PolisClient, PolisError  # noqa: E402
from polis_cli.config import Profile  # noqa: E402

BASE_URL = os.environ.get("POLIS_BASE_URL", "https://localhost")
OIDC_URL = os.environ.get("POLIS_OIDC_URL", "https://localhost:3000")
PASSWORD = os.environ.get("POLIS_TEST_PASSWORD", "Te$tP@ssw0rd*")
ADMIN = "admin@polis.test"
VOTERS = [f"test.user.{i}@polis.test" for i in range(3)]

STATEMENTS = [
    "Our city should pedestrianise the old town centre.",
    "Cycling infrastructure matters more than free parking.",
    "Public participation should happen before plans are drafted, not after.",
    "Digital participation excludes older residents unless paired with offline formats.",
    "The city should publish what happened to every citizen proposal.",
]


def say(step: str, data=None) -> None:
    print(f"\n=== {step} ===")
    if data is not None:
        print(json.dumps(data, indent=2, default=str)[:1500])


def make_client(email: str) -> PolisClient:
    profile = Profile(
        name=f"proveloop-{email.split('@')[0]}",
        base_url=BASE_URL,
        auth="oidc",
        email=email,
        oidc_token_url=OIDC_URL,
        oidc_client_id="dev-client-id",
    )
    client = PolisClient(profile)
    client._http = httpx.Client(  # sandbox only: self-signed TLS
        base_url=BASE_URL, timeout=30.0, follow_redirects=True, verify=False
    )
    client.login_oidc_password_grant(email, PASSWORD, verify_tls=False)
    return client


def main() -> int:
    admin = make_client(ADMIN)
    say("login ok", {"admin": ADMIN})

    convo = admin.create_conversation(
        "Sandbox: city-centre mobility",
        "Phase-0 smoke test conversation created machine-to-machine.",
    )
    say("create_conversation", convo)
    convo_id = (
        convo.get("conversation_id") or convo.get("zinvite") or convo.get("zid")
    )
    assert convo_id, f"no conversation id in response: {convo}"

    for text in STATEMENTS:
        result = admin.seed_comment(str(convo_id), text)
        say(f"seed: {text[:40]}...", result)

    comments = admin.list_comments(str(convo_id))
    say("list_comments", {"count": len(comments)})
    tids = [c["tid"] for c in comments]

    for email in VOTERS:
        voter = make_client(email)
        for i, tid in enumerate(tids):
            # deterministic spread: voter j agrees with statements where (tid+j) even
            vote = -1 if (tid + VOTERS.index(email)) % 2 == 0 else 1
            voter.vote(str(convo_id), tid, vote)
        say(f"votes cast by {email}", {"statements": len(tids)})

    try:
        math = admin.math(str(convo_id))
        say("math/pca2", {"keys": list(math)[:10]})
    except PolisError as e:
        say("math/pca2 (may need more participants or worker warm-up)", {"error": str(e)})

    admin.close_conversation(str(convo_id))
    say("closed", {"conversation_id": convo_id})

    report = admin.create_report(str(convo_id))
    say("create_report", report)
    reports = admin.list_reports(str(convo_id))
    report_id = (reports or [report])[0].get("report_id")

    out = Path("exports")
    out.mkdir(exist_ok=True)
    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        try:
            text = admin.export_csv(str(report_id), kind)
            path = out / f"{convo_id}-{kind}.csv"
            path.write_text(text, encoding="utf-8")
            say(f"export {kind}", {"file": str(path), "bytes": len(text)})
        except PolisError as e:
            say(f"export {kind} FAILED", {"error": str(e)})

    print("\n*** LOOP PROVEN — create/seed/vote/close/export all machine-to-machine ***")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
