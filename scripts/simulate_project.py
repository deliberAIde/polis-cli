"""Demo simulation: 'Munich City Centre 2030' — a realistic mid-size participation project.

Creates a conversation, seeds 22 statements, then simulates 50 citizens
(the sandbox's test.user.0-49 accounts) voting along 4 opinion archetypes
with noise; a few submit their own statements. Leaves the conversation OPEN
(so a live audience can still join), creates a report, exports CSVs + math.

    python scripts/simulate_project.py            # full run
    POLIS_SIM_USERS=20 python scripts/...         # smaller/faster
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

from polis_cli.client import PolisClient, PolisError  # noqa: E402
from polis_cli.config import Profile  # noqa: E402

BASE_URL = os.environ.get("POLIS_BASE_URL", "https://localhost")
OIDC_URL = os.environ.get("POLIS_OIDC_URL", "https://localhost:3000")
PASSWORD = os.environ.get("POLIS_TEST_PASSWORD", "Te$tP@ssw0rd*")
N_USERS = int(os.environ.get("POLIS_SIM_USERS", "50"))
random.seed(2030)  # reproducible demo

TOPIC = "Munich City Centre 2030"
DESCRIPTION = (
    "How should Munich's city centre change by 2030? Vote on statements "
    "(agree / disagree / pass) and add your own. Demo project orchestrated "
    "end-to-end by an AI agent via polis-cli."
)

# (statement, stance per archetype: green, car, business, access)  A=agree D=disagree P=pass
SEEDS = [
    ("Turn the old town inside Sendlinger/Frauenstrasse into a car-free zone by 2030.", "ADDP"),
    ("Build a continuous, protected bike-lane ring around the city centre.", "ADPD"),
    ("Halve the price of the monthly public-transport pass.", "APPA"),
    ("Add 2,000 secure bike-parking spots at U-Bahn and S-Bahn stations.", "APPP"),
    ("Keep at least the current number of car-parking spaces in the centre.", "DAAP"),
    ("Allow delivery vehicles in pedestrian zones only before 10:00.", "APAP"),
    ("Plant 1,000 additional street trees in the city centre by 2028.", "APAA"),
    ("Convert 20% of on-street parking into parklets and green space.", "ADDP"),
    ("Install more drinking fountains and free public toilets.", "AAAA"),
    ("Regulate ground-floor commercial rents to protect small shops.", "APAP"),
    ("Simplify permits to create housing above shops.", "APAP"),
    ("Extend Sunday shopping hours in the city centre.", "DAAD"),
    ("Every tram and U-Bahn station must be fully barrier-free by 2030.", "AAAA"),
    ("Add more benches and resting spots along shopping streets.", "APAA"),
    ("Ban e-scooters from sidewalks and pedestrian zones.", "DAPA"),
    ("Increase visible police presence in the city centre at night.", "DAAA"),
    ("Host more free cultural events on public squares in summer.", "AAAA"),
    ("Run public transport all night on weekends.", "APAP"),
    ("Introduce a congestion charge for cars entering the Mittlerer Ring.", "ADDP"),
    ("Give citizens a binding vote on major city-centre projects.", "AAAA"),
    ("Use AI to summarise citizen input - always with human oversight.", "APAA"),
    ("Create more playgrounds and shaded areas for families in the centre.", "AAAA"),
]

# archetype: (name, share of participants)
ARCHETYPES = [
    ("green-urbanist", 0.34),
    ("car-commuter", 0.26),
    ("small-business", 0.20),
    ("accessibility", 0.20),
]

# statements submitted BY simulated citizens (archetype index, text)
USER_STATEMENTS = [
    (0, "Try one car-free Sunday per month in the whole city centre."),
    (1, "Expand Park+Ride capacity BEFORE restricting cars in the centre."),
    (3, "Install tactile guidance systems for blind people on all main squares."),
    (2, "Lower business taxes for shops that survive the construction phase."),
]

FLIP_NOISE = 0.12   # chance an individual flips their archetype stance
PASS_PROB = 0.10    # chance to pass regardless
SKIP_PROB = 0.08    # chance to skip a statement entirely (sparsity)

STANCE_VOTE = {"A": -1, "D": 1, "P": 0}  # polis wire: -1 agree, 1 disagree, 0 pass


def make_client(email: str) -> PolisClient:
    profile = Profile(
        name=f"sim-{email.split('@')[0]}", base_url=BASE_URL, auth="oidc",
        email=email, oidc_token_url=OIDC_URL, oidc_client_id="dev-client-id",
    )
    c = PolisClient(profile)
    c._http = httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True, verify=False)
    c.login_oidc_password_grant(email, PASSWORD, verify_tls=False)
    return c


def pick_archetype(i: int) -> int:
    r, acc = (i + 0.5) / N_USERS, 0.0
    for idx, (_, share) in enumerate(ARCHETYPES):
        acc += share
        if r <= acc:
            return idx
    return len(ARCHETYPES) - 1


def simulate_vote(stance: str) -> int | None:
    if random.random() < SKIP_PROB:
        return None
    if random.random() < PASS_PROB:
        return 0
    vote = STANCE_VOTE[stance]
    if random.random() < FLIP_NOISE:
        vote = -vote if vote != 0 else random.choice([-1, 1])
    return vote


def main() -> int:
    t0 = time.time()
    admin = make_client("admin@polis.test")
    convo = admin.create_conversation(TOPIC, DESCRIPTION)
    cid = convo["conversation_id"]
    print(f"conversation: {cid}  url: {convo.get('url')}", flush=True)

    for text, _ in SEEDS:
        admin.seed_comment(cid, text)
    print(f"seeded {len(SEEDS)} statements", flush=True)

    # participants: assign archetypes, log in, some submit their own statements first
    emails = [f"test.user.{i}@polis.test" for i in range(N_USERS)]
    assigned = [pick_archetype(i) for i in range(N_USERS)]
    submitters = {}
    for arch_idx, text in USER_STATEMENTS:
        candidates = [i for i, a in enumerate(assigned) if a == arch_idx]
        if candidates:
            submitters[random.choice(candidates)] = text

    # collect tids once seeds + user statements are all in
    clients: dict[int, PolisClient] = {}
    for i, text in submitters.items():
        clients[i] = make_client(emails[i])
        clients[i]._post("/comments", {"conversation_id": cid, "txt": text})
    comments = admin.list_comments(cid)
    tid_stance: dict[int, str] = {}
    seed_by_txt = {t: s for t, s in SEEDS}
    for c in comments:
        stances = seed_by_txt.get(c["txt"])
        if stances is None:
            # user-submitted: sympathisers agree, others mixed
            stances = "".join(random.choice("AAP") if random.random() < 0.5 else random.choice("ADP") for _ in range(4))
        tid_stance[c["tid"]] = stances
    print(f"total statements: {len(tid_stance)}", flush=True)

    total_votes = 0
    for i, email in enumerate(emails):
        arch = assigned[i]
        client = clients.get(i) or make_client(email)
        for tid, stances in tid_stance.items():
            v = simulate_vote(stances[arch])
            if v is None:
                continue
            try:
                client.vote(cid, tid, v)
                total_votes += 1
            except PolisError:
                pass  # e.g. own-statement auto-vote conflicts
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{N_USERS} participants voted ({total_votes} votes)", flush=True)

    print(f"votes cast: {total_votes} in {time.time()-t0:.0f}s", flush=True)

    # wait for the math worker to cluster
    groups = None
    for _ in range(30):
        try:
            math = admin.math(cid)
            clusters = math.get("group-clusters") or []
            if clusters:
                groups = len(clusters)
                Path("exports").mkdir(exist_ok=True)
                (Path("exports") / f"{cid}-math.json").write_text(json.dumps(math, indent=2), encoding="utf-8")
                break
        except PolisError:
            pass
        time.sleep(5)
    print(f"opinion groups: {groups}", flush=True)

    # report + export (conversation stays OPEN for live audience)
    admin.create_report(cid)
    report_id = (admin.list_reports(cid) or [{}])[0].get("report_id")
    out = Path("exports")
    for kind in ("comments", "votes", "participant-votes", "comment-groups", "summary"):
        try:
            (out / f"{cid}-{kind}.csv").write_text(admin.export_csv(str(report_id), kind), encoding="utf-8")
        except PolisError as e:
            print(f"export {kind} failed: {e}", flush=True)
    print(f"exports written to exports/{cid}-*.csv (+ math.json)", flush=True)
    print(json.dumps({"conversation_id": cid, "url": convo.get("url"),
                      "participants": N_USERS, "votes": total_votes,
                      "statements": len(tid_stance), "groups": groups,
                      "report_id": report_id, "seconds": round(time.time()-t0)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
