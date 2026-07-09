"""Simulate a crowd voting on an EXISTING Voxit conversation, through the SOCKS5
gateway. Voxit's Polis requires registered voters, so each simulated voter signs
up (POST /api/v3/auth/new -> authenticated session) and then votes per archetype
stance. Voters run concurrently (the emulated amd64 engine is slow per-request).

    N_VOTERS=3  python scripts/simulate_votes_voxit.py     # smoke test
    N_VOTERS=40 python scripts/simulate_votes_voxit.py     # real run
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import httpx  # noqa: E402
from simulate_project import SEEDS, ARCHETYPES, STANCE_VOTE  # noqa: E402

BASE = os.environ.get("VOXIT_BASE", "https://polis.voxit.internal")
PROXY = os.environ.get("VOXIT_PROXY", "socks5h://127.0.0.1:1080")
CID = os.environ.get("VOXIT_CID") or Path(r"C:\Users\lukas\dev\civic-agent-demo\voxit_cid.txt").read_text().strip()
N = int(os.environ.get("N_VOTERS", "40"))
RUN = os.environ.get("VOXIT_RUN_TAG", "r1")
WORKERS = int(os.environ.get("VOXIT_WORKERS", "8"))
random.seed(2030)
FLIP_NOISE, PASS_PROB, SKIP_PROB = 0.10, 0.05, 0.02


def new_client() -> httpx.Client:
    return httpx.Client(proxy=PROXY, verify=False, base_url=BASE, timeout=45, follow_redirects=True)


def pick_archetype(i: int) -> int:
    r, acc = (i + 0.5) / N, 0.0
    for idx, (_, share) in enumerate(ARCHETYPES):
        acc += share
        if r <= acc:
            return idx
    return len(ARCHETYPES) - 1


def sim_vote(stance: str, rng: random.Random):
    if rng.random() < SKIP_PROB:
        return None
    if rng.random() < PASS_PROB:
        return 0
    v = STANCE_VOTE[stance]
    if rng.random() < FLIP_NOISE:
        v = -v if v != 0 else rng.choice([-1, 1])
    return v


def load_tid_stance() -> dict:
    c = new_client()
    comments = c.get("/api/v3/comments", params={"conversation_id": CID, "moderation": "true"}).json()
    seed_by_txt = {t: s for t, s in SEEDS}
    out = {}
    for cm in comments:
        st = seed_by_txt.get(cm["txt"]) or "".join(random.choice("AAP") for _ in range(len(ARCHETYPES)))
        out[cm["tid"]] = st
    return out


def one_voter(i: int, tid_stance: dict) -> int:
    """Sign up voter i and cast their votes. Returns number of votes cast."""
    rng = random.Random(1000 + i)
    arch = pick_archetype(i)
    c = new_client()
    email = f"v{RUN}-{i:03d}@voxit.local"
    su = c.post("/api/v3/auth/new", json={"hname": f"Voter {i}", "email": email,
                                          "password": "Vox!tCrowd1", "gatekeeperTosPrivacy": True})
    if su.status_code >= 400:
        # already exists -> log in instead
        c.post("/api/v3/auth/login", json={"email": email, "password": "Vox!tCrowd1"})
    cast = 0
    for tid, stances in tid_stance.items():
        v = sim_vote(stances[arch], rng)
        if v is None:
            continue
        try:
            r = c.post("/api/v3/votes", json={"conversation_id": CID, "tid": tid, "vote": v, "pid": "mypid"})
            if r.status_code < 300:
                cast += 1
        except Exception:
            pass
    c.close()
    return cast


def main() -> int:
    t0 = time.time()
    tid_stance = load_tid_stance()
    print(f"conversation {CID}: {len(tid_stance)} statements; {N} voters x{WORKERS} concurrent...", flush=True)
    total = 0
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(one_voter, i, tid_stance): i for i in range(N)}
        for f in as_completed(futs):
            total += f.result() or 0
            done += 1
            if done % 10 == 0 or done == N:
                print(f"  {done}/{N} voters done ({total} votes, {time.time()-t0:.0f}s)", flush=True)

    print(f"votes cast: {total} (~{total//max(len(tid_stance),1)}/statement) in {time.time()-t0:.0f}s", flush=True)

    groups = None
    admin = new_client()
    for _ in range(48):
        for path in ("/api/v3/math/pca2", "/api/v3/math/pca"):
            try:
                m = admin.get(path, params={"conversation_id": CID}).json()
                gc = (m or {}).get("group-clusters") or []
                if gc:
                    groups = len(gc)
                    break
            except Exception:
                pass
        if groups:
            break
        time.sleep(5)
    print(json.dumps({"conversation_id": CID, "voters": N, "votes": total,
                      "statements": len(tid_stance), "groups": groups, "seconds": round(time.time() - t0)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
