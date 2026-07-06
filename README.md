# polis-cli

Thin command-line client for driving **Pol.is-family instances** — [Pol.is](https://github.com/compdemocracy/polis) (Computational Democracy Project) and **Voxit** (Sitra / COSS Finland fork) — over their HTTP API.

Lets an operator **or an AI agent** run the full conversation lifecycle machine-to-machine, no browser required:

```
polis login                      # authenticate against an instance (profile-based)
polis convo create               # create a conversation (topic, description, settings)
polis seed statements.csv        # bulk-seed statements
polis convo open | close         # lifecycle
polis moderate                   # accept/reject queued statements
polis convo status               # live participation + opinion-cluster snapshot
polis export                     # raw votes, comments, cluster CSVs
polis simulate                   # synthetic participants (testing only)
```

## Design rules

1. **Arm's length, always.** This CLI is an independent HTTP client. It contains **no Pol.is code** — it never vendors, links, or modifies the (AGPL-3.0) Pol.is/Voxit codebase; it only talks to *unmodified* instances over their API. Keep it that way.
2. **Pin per instance.** Pol.is has no stable public API contract. Each profile records the instance's version/tag; the client's endpoint map is written against pinned versions (currently: `stable` branch, mid-2026).
3. **Two auth flavors.** Newer instances: OIDC bearer tokens (any issuer; token must carry an `email` claim). Older instances (and likely Voxit): legacy email/password session login. `polis login` autodetects.
4. **`--json` everywhere.** Every command supports machine-readable output so an agent can drive the CLI.

## Dev sandbox

The upstream Pol.is repo (cloned separately, e.g. `../polis` — **not** part of this repo) ships a docker-compose dev stack. See `scripts/prove_loop.py` for the end-to-end smoke test this CLI is built against.

## Status

- [ ] Phase 0 — runtime-prove the create → seed → vote → close → export loop against the local sandbox
- [ ] Phase 1 — CLI commands (login, convo, seed, moderate, status, export, simulate)
- [ ] Phase 2 — export → deliberAIde synthesis ingestion
- [ ] Phase 3 — Azure Container Apps disposable-instance template (public demo)
- [ ] Phase 4 — MCP twin (same commands as MCP tools)

*License: TBD. All rights reserved for now.*
