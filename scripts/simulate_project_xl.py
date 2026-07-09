"""Larger demo simulation via ANONYMOUS XID participants (no login cap).

Pol.is's consensus prompt requires >=100 votes/statement to report a finding.
The 50 seeded OIDC accounts can't reach that, so this uses anonymous XID
participants (POST /votes with a unique xid + fresh session each) — Pol.is's
native mass-participation path — to run ~130 voters at low sparsity.

    python scripts/simulate_project_xl.py            # 130 voters
    POLIS_SIM_USERS=100 python scripts/...           # custom

Creates a fresh conversation, seeds 22 statements (as admin), then the crowd
votes by archetype. Leaves it OPEN, runs report+export.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx  # noqa: E402

from polis_cli.client import PolisClient  # noqa: E402
from polis_cli.config import Profile  # noqa: E402

BASE_URL = os.environ.get("POLIS_BASE_URL", "https://localhost")
OIDC_URL = os.environ.get("POLIS_OIDC_URL", "https://localhost:3000")
PASSWORD = os.environ.get("POLIS_TEST_PASSWORD", "Te$tP@ssw0rd*")
N_USERS = int(os.environ.get("POLIS_SIM_USERS", "130"))
random.seed(2030)

TOPIC = "Munich City Centre 2030"
DESCRIPTION = (
    "How should Munich's city centre change by 2030? A large citizen "
    "consultation, orchestrated end-to-end by an AI agent via polis-cli."
)

# reuse the exact statement set + archetype stances from the base sim
from simulate_project import SEEDS, ARCHETYPES, USER_STATEMENTS, STANCE_VOTE  # noqa: E402

# LOW sparsity so every statement clears the 100-vote threshold
FLIP_NOISE = 0.10
PASS_PROB = 0.05
SKIP_PROB = 0.02


def admin_client() -> PolisClient:
    prof = Profile(name="admin-xl", base_url=BASE_URL, auth="oidc", email="admin@polis.test",
                   oidc_token_url=OIDC_URL, oidc_client_id="dev-client-id")
    c = PolisClient(prof)
    c._http = httpx.Client(base_url=BASE_URL, timeout=30, follow_redirects=True, verify=False)
    c.login_oidc_password_grant("admin@polis.test", PASSWORD, verify_tls=False)
    return c


def pick_archetype(i: int) -> int:
    r, acc = (i + 0.5) / N_USERS, 0.0
    for idx, (_, share) in enumerate(ARCHETYPES):
        acc += share
        if r <= acc:
            return idx
    return len(ARCHETYPES) - 1


def sim_vote(stance: str) -> int | None:
    if random.random() < SKIP_PROB:
        return None
    if random.random() < PASS_PROB:
        return 0
    v = STANCE_VOTE[stance]
    if random.random() < FLIP_NOISE:
        v = -v if v != 0 else random.choice([-1, 1])
    return v


def main() -> int:
    t0 = time.time()
    admin = admin_client()
    convo = admin.create_conversation(TOPIC, DESCRIPTION)
    cid = convo["conversation_id"]
    print(f"conversation: {cid}  url: {convo.get('url')}", flush=True)

    for text, _ in SEEDS:
        admin.seed_comment(cid, text)
    # a few citizen-submitted statements via xid participants
    for arch_idx, text in USER_STATEMENTS:
        xc = httpx.Client(base_url=BASE_URL, timeout=30, follow_redirects=True, verify=False)
        xc.post("/api/v3/comments", json={"conversation_id": cid, "txt": text, "xid": f"author-{arch_idx}"})
    print(f"seeded {len(SEEDS)} statements + {len(USER_STATEMENTS)} citizen statements", flush=True)

    comments = admin.list_comments(cid)
    tid_stance = {}
    seed_by_txt = {t: s for t, s in SEEDS}
    for c in comments:
        stances = seed_by_txt.get(c["txt"])
        if stances is None:
            stances = "".join(random.choice("AAP") if random.random() < 0.5 else random.choice("ADP") for _ in range(4))
        tid_stance[c["tid"]] = stances
    tids = list(tid_stance)
    print(f"statements to vote on: {len(tids)}; simulating {N_USERS} anonymous voters...", flush=True)

    total = 0
    for i in range(N_USERS):
        arch = pick_archetype(i)
        sess = httpx.Client(base_url=BASE_URL, timeout=30, follow_redirects=True, verify=False)
        xid = f"sim-voter-{i:04d}"
        for tid in tids:
            v = sim_vote(tid_stance[tid][arch])
            if v is None:
                continue
            try:
                sess.post("/api/v3/votes", json={"conversation_id": cid, "tid": tid, "vote": v, "xid": xid})
                total += 1
            except Exception:
                pass
        sess.close()
        if (i + 1) % 20 == 0:
            print(f"  {i+1}/{N_USERS} voters done ({total} votes, {time.time()-t0:.0f}s)", flush=True)

    print(f"votes cast: {total} (~{total//len(tids)}/statement) in {time.time()-t0:.0f}s", flush=True)

    # wait for clustering
    groups = None
    for _ in range(40):
        try:
            m = admin.math(cid)
            cl = m.get("group-clusters") or []
            if cl:
                groups = len(cl)
                break
        except Exception:
            pass
        time.sleep(5)

    admin.create_report(cid)
    rid = (admin.list_reports(cid) or [{}])[0].get("report_id")
    out = Path("exports"); out.mkdir(exist_ok=True)
    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        try:
            (out / f"{cid}-{kind}.csv").write_text(admin.export_csv(str(rid), kind), encoding="utf-8")
        except Exception:
            pass
    print(json.dumps({"conversation_id": cid, "url": convo.get("url"), "voters": N_USERS,
                      "votes": total, "votes_per_statement": total // len(tids),
                      "statements": len(tids), "groups": groups, "report_id": rid,
                      "seconds": round(time.time() - t0)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
