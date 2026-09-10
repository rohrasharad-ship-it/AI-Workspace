# Handover: idea-sweep routine could not run for Usercon — Linear MCP entirely unavailable

**For:** Any agent/session with an authorized Linear MCP connector, or Sharad
(to authorize the Linear connector for scheduled/background sessions)
**From:** idea-sweep routine run for Usercon, triggered as a scheduled task, 2026-09-10
**Blocked by:** The Linear MCP server was not authenticated/connected in this
session at all — no `mcp__Linear__*` tools were exposed (not even as deferred
tools), and the session's own tooling explicitly reported: "The following MCP
servers require authentication before their tools can be used: Linear" with
guidance that a non-interactive session cannot run the OAuth flow itself.
This is a stricter blocker than the one logged in
`handovers/preview-branch-cleanup-linear-api-key.md` — prior idea-sweep
sessions had working Linear MCP tool access (just no `LINEAR_API_KEY` shell
env var for the housekeeping script); this session had **no Linear access of
any kind**.
**Action:** Authorize the Linear connector for this account so scheduled/
background Claude Code on the web sessions carry it too (claude.ai →
Settings → Connectors), then re-run `idea-sweep` for Usercon. Everything
below is scoped research to make that re-run faster — no issues were created,
searched, or commented on this cycle.

## What this blocked

Per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`, every step
that touches Linear requires MCP access — all of it was unavailable:

- **Issue Cap pre-flight** (count active pipeline issues for UserCon,
  project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) — could not run.
- **spec-drift** steps 1–9 (gap-filing) and step 10 (stale-issue sweep) —
  could not search/dedupe, create, or comment.
- **bug-error** steps 3–8 — could not search/create/comment. (Separately,
  moot this cycle anyway: `projects.md` still lists Usercon's Vercel Prod as
  `TBD` — no production deployment exists yet, so there are no runtime
  logs/errors to read regardless of Linear access.)
- **market-feature** steps 4–8 — could not search/create/comment.
- **spec-drift step 11** (preview-branch cleanup) — also needs
  `LINEAR_API_KEY` as a shell env var, which this session likewise did not
  have; same root cause, see the other handover for full branch
  classification history (last verified 2026-08-12, 101 safe-to-delete / 20
  keep, all still blocked on the missing repo secret + proxy write-block —
  no need to re-derive that list here).

## What did run (no Linear needed)

- **spec-drift step 12** (OpenSpec archive housekeeping): checked
  `openspec/changes/` in AI-Workspace directly — it contains only `archive/`,
  no active change folders. Same clean-0 result every prior session has
  logged since at least 2026-08-08. Nothing to archive.
- Confirmed git/GitHub MCP access to both `Usercon` and `AI-Workspace` repos
  works fine in this session — the blocker is Linear specifically, not
  general tool access.

## Research for the next Usercon run (not filed anywhere, just notes)

Read `openspec/project.md` in the Usercon repo (repo root has both a legacy
flat `SPEC.md`/`PRD.md`/`STRATEGY.md` set and the real `openspec/` tree — use
`openspec/`, the flat docs look like pre-OpenSpec artifacts). Capabilities
currently specced: `context-graph`, `context-review`, `agent-api`,
`context-usage-insights`, `context-receipt`, `drive-storage`, `mcp-oauth`,
`settings-screen`, `mobile-shell`. A full spec-drift/market-feature pass
(comparing each spec file against `src/`, plus a vision-based feature
proposal) was **not** done this cycle — with zero ability to dedupe against
existing Linear issues, generating candidate issues now risked producing
duplicates of things already tracked or already rejected in triage, which is
worse than doing that analysis fresh once Linear access exists.

## Instructions for receiving agent/session

1. Once Linear MCP is authorized for this account's scheduled sessions,
   re-run: `Run the "idea-sweep" routine for Usercon. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`
2. That run should do the full spec-drift + market-feature analysis from
   scratch (openspec vs. codebase, vision vs. spec) — this handover
   deliberately did not pre-generate candidate issues, for the dedupe reason
   above.
3. bug-error will still have nothing to check until Usercon has a real
   Vercel Prod URL — consider updating `projects.md`'s Vercel Prod column
   for Usercon once/if it's deployed, otherwise bug-error stays a correct
   no-op indefinitely.
4. Delete this handover file once a session with working Linear MCP has
   confirmed idea-sweep runs cleanly for Usercon again.
