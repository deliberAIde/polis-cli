"""Post-export analysis — the layer Pol.is doesn't have.

Reads exports/<cid>-{comments,participant-votes,comment-groups}.csv (+ math.json)
and computes, per statement and per opinion group:

  * consensus ranking      — statements ALL groups agree on (common ground)
  * divisiveness ranking   — statements that split the groups hardest
  * group profiles         — the statements that DEFINE each group vs the rest
  * minority signals       — coherent group positions that simple majority
                             voting would erase (deliberAIde's core concern)
  * bridge candidates      — non-consensus statements with the best chance
                             of uniting groups (high min-group agreement)

Usage: python scripts/analyze_export.py <conversation_id> [--json]
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

EXPORTS = Path(__file__).resolve().parents[1] / "exports"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    cid = sys.argv[1]
    as_json = "--json" in sys.argv

    comments = {int(r["comment-id"]): r for r in read_csv(EXPORTS / f"{cid}-comments.csv")}
    groups_rows = read_csv(EXPORTS / f"{cid}-comment-groups.csv")
    participants = read_csv(EXPORTS / f"{cid}-participant-votes.csv")

    # comment-groups.csv is WIDE: group-a-votes, group-a-agrees, ... per row
    import re

    sample = groups_rows[0] if groups_rows else {}
    group_ids = sorted({m.group(1) for k in sample for m in [re.match(r"group-([a-z])-votes$", k)] if m})
    per_stmt: dict[int, dict] = {}
    for r in groups_rows:
        tid = int(r["comment-id"])
        s = per_stmt.setdefault(
            tid,
            {"tid": tid,
             "text": r.get("comment") or comments.get(tid, {}).get("comment-body", "?"),
             "groups": {}},
        )
        for gid in group_ids:
            agrees = int(r.get(f"group-{gid}-agrees") or 0)
            disagrees = int(r.get(f"group-{gid}-disagrees") or 0)
            passes = int(r.get(f"group-{gid}-passes") or 0)
            votes = int(r.get(f"group-{gid}-votes") or 0) or (agrees + disagrees + passes)
            rate = agrees / votes if votes else 0.0
            s["groups"][gid] = {"agree_rate": round(rate, 3), "agrees": agrees,
                                "disagrees": disagrees, "passes": passes, "votes": votes}

    stmts = []
    for tid, s in per_stmt.items():
        rates = [g["agree_rate"] for g in s["groups"].values() if g["votes"] >= 3]
        if not rates:
            continue
        total_agree = sum(g["agrees"] for g in s["groups"].values())
        total_votes = sum(g["votes"] for g in s["groups"].values())
        s["overall_agree_rate"] = round(total_agree / total_votes, 3) if total_votes else 0
        s["min_group_agree"] = round(min(rates), 3)
        s["max_group_agree"] = round(max(rates), 3)
        s["spread"] = round(max(rates) - min(rates), 3)
        stmts.append(s)

    consensus = sorted([s for s in stmts if s["min_group_agree"] >= 0.6],
                       key=lambda s: -s["min_group_agree"])
    divisive = sorted(stmts, key=lambda s: -s["spread"])[:6]
    minority = [s for s in stmts
                if s["overall_agree_rate"] < 0.5 and s["max_group_agree"] >= 0.7]
    bridges = sorted([s for s in stmts if s not in consensus and s["spread"] <= 0.35
                      and s["min_group_agree"] >= 0.4],
                     key=lambda s: -s["min_group_agree"])[:5]

    # group profiles: statements with the largest agree-rate lead for that group
    profiles = {}
    for gid in group_ids:
        diffs = []
        for s in stmts:
            mine = s["groups"].get(gid, {}).get("agree_rate")
            others = [g["agree_rate"] for k, g in s["groups"].items() if k != gid and g["votes"] >= 3]
            if mine is None or not others:
                continue
            diffs.append((mine - sum(others) / len(others), s))
        diffs.sort(key=lambda d: -d[0])
        numeric_gid = str(ord(gid) - ord("a"))  # participant-votes.csv uses 0/1/...
        size = sum(1 for p in participants if p.get("group-id") == numeric_gid)
        profiles[gid] = {"size": size,
                         "defining": [{"text": s["text"], "own_agree": s["groups"][gid]["agree_rate"],
                                       "lead": round(d, 3)} for d, s in diffs[:4]]}

    result = {
        "conversation_id": cid,
        "n_statements": len(stmts),
        "n_participants": len(participants),
        "n_groups": len(group_ids),
        "group_profiles": profiles,
        "consensus": [{"tid": s["tid"], "text": s["text"], "min_group_agree": s["min_group_agree"],
                       "overall": s["overall_agree_rate"]} for s in consensus],
        "divisive": [{"tid": s["tid"], "text": s["text"], "spread": s["spread"],
                      "by_group": {k: v["agree_rate"] for k, v in s["groups"].items()}} for s in divisive],
        "minority_signals": [{"tid": s["tid"], "text": s["text"], "overall": s["overall_agree_rate"],
                              "champion_group_agree": s["max_group_agree"]} for s in minority],
        "bridge_candidates": [{"tid": s["tid"], "text": s["text"],
                               "min_group_agree": s["min_group_agree"]} for s in bridges],
    }
    print(json.dumps(result, indent=None if as_json else 2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
