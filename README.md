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

## Install

```bash
pip install polis-cli          # command: polis
```

## Part of the civic tech agent-bridges toolkit

`polis-cli` is one bridge in the [civic tech agent-bridges toolkit](https://github.com/deliberAIde/civic-tech-agent-bridges): open-source
command-line clients that let any AI agent drive a civic-tech platform through its own API, so
platforms interoperate without waiting for a standards process. Sibling bridges: [consul-cli](https://github.com/deliberAIde/consul-cli) (CONSUL DEMOCRACY), [decidim-cli](https://github.com/deliberAIde/decidim-cli) (Decidim), [deliberaide-cli](https://pypi.org/project/deliberaide-cli/) (deliberAIde).

## Relationship to upstream

This is an independent client. It contains no Pol.is or Voxit source code and speaks only to the
documented HTTP API of a running instance. deliberAIde offers it to the Pol.is and Voxit community for
adoption; the Apache-2.0 licence is chosen so the code can be vendored into AGPL-3.0 (Pol.is) or EUPL-1.2 (Voxit)
repositories without friction, since permissive code can be combined into copyleft ones but not
the other way round.

## Licence

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE). Copyright 2026 deliberAIde.
