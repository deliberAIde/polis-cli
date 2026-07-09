"""Beat 3: the WIDER PUBLIC votes on the assembly-derived Voxit poll (6s8brhaamj).

Unlike simulate_votes_voxit.py (which matched the generic seed set), this uses an
explicit per-statement stance map for the 20 assembly-recommendation statements,
so the crowd's opinion is realistic — and deliberately lets the raw public land
MORE skeptical of the City-Maut than the deliberating assembly did (a well-known
mini-public vs maxi-public divergence).

Archetype order in each stance string: green-urbanist, car-commuter,
small-business, accessibility. A=agree, D=disagree, P=pass.

Reuses the signup+vote machinery from simulate_votes_voxit.
"""
from __future__ import annotations
import json, os, time, random, sys, warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import httpx  # noqa
from simulate_project import ARCHETYPES, STANCE_VOTE  # noqa

BASE = "https://polis.voxit.internal"
PROXY = "socks5h://127.0.0.1:1080"
CID = os.environ.get("VOXIT_CID") or Path(r"C:\Users\lukas\dev\civic-agent-demo\voxit_poll_cid.txt").read_text().strip()
N = int(os.environ.get("N_VOTERS", "40"))
RUN = os.environ.get("VOXIT_RUN_TAG", "poll1")
WORKERS = int(os.environ.get("VOXIT_WORKERS", "3"))
random.seed(2030)
FLIP_NOISE, PASS_PROB, SKIP_PROB = 0.12, 0.06, 0.03

# tid -> [green, car, business, accessibility]
STANCES = {
    0: "ADPA", 1: "AAAA", 2: "AAAA", 3: "AAAA", 4: "APPA", 5: "AAAA",
    6: "APAP", 7: "DAAP", 8: "APAA", 9: "APAA", 10: "AAAA", 11: "PAAA",
    12: "PAAA", 13: "ADDP", 14: "PAPA", 15: "PAAA", 16: "APPA", 17: "DAAP",
    18: "APPA", 19: "AAAA",
}


def new_client():
    return httpx.Client(proxy=PROXY, verify=False, base_url=BASE, timeout=45, follow_redirects=True)


def pick_archetype(i):
    r, acc = (i + 0.5) / N, 0.0
    for idx, (_, share) in enumerate(ARCHETYPES):
        acc += share
        if r <= acc:
            return idx
    return len(ARCHETYPES) - 1


def sim_vote(stance, rng):
    if rng.random() < SKIP_PROB:
        return None
    if rng.random() < PASS_PROB:
        return 0
    v = STANCE_VOTE[stance]
    if rng.random() < FLIP_NOISE:
        v = -v if v != 0 else rng.choice([-1, 1])
    return v


def tids_present():
    c = new_client()
    cs = c.get("/api/v3/comments", params={"conversation_id": CID, "moderation": "true"}).json()
    return sorted(cm["tid"] for cm in cs)


def one_voter(i, tids):
    rng = random.Random(2000 + i)
    arch = pick_archetype(i)
    c = new_client()
    email = f"v{RUN}-{i:03d}@voxit.local"
    su = c.post("/api/v3/auth/new", json={"hname": f"Voter {i}", "email": email,
                                          "password": "Vox!tCrowd1", "gatekeeperTosPrivacy": True})
    if su.status_code >= 400:
        c.post("/api/v3/auth/login", json={"email": email, "password": "Vox!tCrowd1"})
    cast = 0
    for tid in tids:
        st = STANCES.get(tid)
        if not st:
            continue
        v = sim_vote(st[arch], rng)
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


def main():
    t0 = time.time()
    tids = tids_present()
    print(f"poll {CID}: {len(tids)} statements; {N} voters x{WORKERS}...", flush=True)
    total = done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(one_voter, i, tids): i for i in range(N)}
        for f in as_completed(futs):
            total += f.result() or 0
            done += 1
            if done % 10 == 0 or done == N:
                print(f"  {done}/{N} voters ({total} votes, {time.time()-t0:.0f}s)", flush=True)
    print(f"votes cast: {total} in {time.time()-t0:.0f}s", flush=True)
    groups = None
    admin = new_client()
    for _ in range(48):
        try:
            m = admin.get("/api/v3/math/pca2", params={"conversation_id": CID}).json()
            gc = (m or {}).get("group-clusters") or []
            if gc:
                groups = len(gc); break
        except Exception:
            pass
        time.sleep(5)
    print(json.dumps({"conversation_id": CID, "voters": N, "votes": total, "groups": groups,
                      "seconds": round(time.time() - t0)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
