# Handover: idea-sweep routine can't run — this session has no Linear access at all

**For:** Sharad (connector setup — this one needs a human), or any future agent
session confirmed to have working Linear MCP access
**From:** Claude Code (scheduled `idea-sweep` trigger), Application Agent run,
2026-09-20
**Blocked by:** This session has **zero Linear access** — not the narrower
`LINEAR_API_KEY`-for-shell-scripts gap already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`, but no Linear MCP tool
at all (the platform lists Linear under "MCP servers that require
authentication before their tools can be used" for this session), no
`LINEAR_API_KEY` env var, and outbound HTTPS to `api.linear.app` itself
returns `403` through this session's network proxy.
**Action:** Connect/reauthorize the Linear connector for this account in
claude.ai connector settings so scheduled Claude Code sessions actually have
Linear MCP tools available. This is a one-time account-level fix, not
something any agent session can do for itself.
**Issue:** N/A — this run is routine-triggered (`routines/idea-sweep.md`), not
driven by a Linear issue.

## Payload

Triggered task: "Run the idea-sweep routine for Application Agent" per
`routines/idea-sweep.md`. Followed the routine exactly: read
`routines/README.md`, `projects.md` (Application Agent → repo
`rohrasharad-ship-it/Application-Agent`, Linear Project ID
`7dc5202c-a586-4bed-b2d3-fba10f2dd913`, Vercel Prod still `TBD`),
`agents/shared/issue-cap.md`, and all three role files
(`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`).

Could not get past the routine's own pre-flight (`agents/shared/issue-cap.md`
— count active pipeline issues via Linear `list_issues`) because:

1. No Linear MCP tool is loaded or loadable this session (checked via
   `ToolSearch` for `list_issues`/create/search — nothing Linear-shaped came
   back; the platform's own notice lists Linear as requiring authorization
   first).
2. No `LINEAR_API_KEY` in the environment (`env | grep -i linear` — empty).
3. Direct network fallback also closed: `curl https://api.linear.app/graphql`
   → `CONNECT tunnel failed, response 403` through this session's proxy — so
   even a hand-rolled GraphQL call from Bash isn't an option here.
4. No Playwright/browser tool is available this session either (checked via
   `ToolSearch`), which would also have blocked the mandatory Visual Self-QA
   screenshot step on any issue this run could otherwise have filed.

Net effect: none of spec-drift/bug-error/market-feature could search Linear
for dedupe, run the issue-cap count, file issues, or comment on existing
issues. **No issues were filed, no comments were posted, no branches were
deleted, and no `data/sweep-runs.jsonl` line was appended** — appending a
`"clean": true` ledger line would misrepresent this run as having actually
checked the project, which it could not do.

Two things I *could* still read (GitHub MCP has no such gap) and are worth
handing to whoever runs this next with real Linear access:

- Application Agent (`rohrasharad-ship-it/Application-Agent`) is a Python
  CLI/agent project (`pyproject.toml`, `src/application_agent/`), not a
  deployed web app — `projects.md` correctly has Vercel Prod as `TBD`. There
  is currently nothing for the **bug-error** role to read (no prod
  deployment, no runtime logs) regardless of Linear access — that role will
  keep finding nothing to check until a deployment exists.
- `openspec/specs/` has six capability specs (`browser`, `generation`,
  `integrations`, `orchestrator`, `profile`, `tracker`) mirrored 1:1 by
  `src/application_agent/{browser,generation,integrations,orchestrator,profile,tracker}/`
  — the module skeleton exists per-capability. I did not go further into a
  file-by-file spec-vs-code diff (spec-drift steps 1–3), since without Linear
  search access any gaps found couldn't be dedupe-checked or filed anyway,
  and I didn't want to hand the next agent unverified/possibly-duplicate
  candidates dressed up as findings.

Separately, and likely the same root cause: `data/sweep-runs.jsonl` shows
three prior "Application Agent" entries (2026-07-11, 2026-08-06, 2026-08-19)
all logged `"clean": true, "filed": {"bugs":0,"features":0}`. I can't confirm
from this session whether those runs genuinely had working Linear access and
found nothing, or hit a version of this same wall and defaulted to a "clean"
entry rather than skipping it. Worth a spot-check once Linear access is
confirmed working end-to-end again.

## Instructions for receiving agent / human

1. **Human step (can't be done from any agent session):** in claude.ai
   connector settings for this account, confirm/reconnect the Linear
   connector so scheduled Claude Code sessions get Linear MCP tools. This is
   distinct from — and likely upstream of — the `LINEAR_API_KEY` repo-secret
   gap tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that
   one blocks the GitHub Action's shell script specifically; this one blocks
   agent sessions from using Linear at all).
2. Once a session has confirmed working Linear MCP (e.g. a successful
   `list_issues` call), re-run `idea-sweep` for Application Agent from
   `routines/idea-sweep.md` step 1 — nothing from this attempt can be reused
   as-is since no gap-finding or dedupe work was completed.
3. If re-running turns up real work, also spot-check whether the three
   `"clean": true` Application Agent ledger entries above were genuine.
4. Delete this handover file once a session confirms Linear MCP access works
   for this account again — no need to keep it once the connector is fixed.
