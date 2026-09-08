# Handover: idea-sweep routine for AI Landscape 2026 could not run — no Linear MCP tool access this session

**For:** Any agent/session with working Linear MCP access
**From:** idea-sweep routine (orchestrator), triggered for "AI Landscape" 2026-09-08
**Blocked by:** This session's tool list has no Linear MCP tools at all. The
Linear connector is present but reports "requires authentication before its
tools can be used," and this is a non-interactive scheduled session, so the
OAuth flow cannot be completed here. This is a different blocker from the
long-standing, separately-tracked `LINEAR_API_KEY` repo-secret issue in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one blocks the
*script-based* housekeeping steps even when Linear MCP works; this one blocks
*every* Linear MCP call — search, cap-count, create, comment — because the
tool isn't callable in this session at all).
**Action:** Re-run the `idea-sweep` routine for AI Landscape from a session
that has authenticated Linear MCP access (re-authorize the Linear connector
for this account: claude.ai Settings → Connectors, or `claude mcp`/`/mcp` in
an interactive session). No analysis from this run needs to be preserved —
none was done (see below).

## Payload

Per `routines/idea-sweep.md`, before running any of spec-drift / bug-error /
market-feature for a project, the orchestrator must first do the Issue Cap
pre-flight (`agents/shared/issue-cap.md`), which requires `list_issues`
against the AI Landscape Linear Project ID
(`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`, from `projects.md`). With zero Linear
MCP tools available, that check cannot be performed at all — not "returned
zero," genuinely uncallable.

Because the cap check gates everything downstream, and every one of the three
role files also requires Linear for its own dedupe search ("Search Linear
first — skip anything already tracked") and for filing, I deliberately did
**not** run the read-only halves of spec-drift/bug-error/market-feature
(reading `openspec/specs/` vs. the AI Landscape codebase, reading prod for
errors, drafting candidate features) this session. Doing that analysis
without the ability to cross-check it against existing Linear issues risks
handing the next session stale or duplicate-looking findings that read as
authoritative when they're not verified against the backlog. Better to leave
a clean blocker than a half-finished, unverified analysis.

No issues were created, no comments were posted, no stale-issue sweep ran,
and no preview-branch/OpenSpec-archive housekeeping ran (those also need
Linear: spec-drift step 10 needs `list_issues` + comments; step 11's script
needs `LINEAR_API_KEY`, separately tracked as unresolved in
`handovers/preview-branch-cleanup-linear-api-key.md` as of its last update).

A ledger line has been appended to `data/sweep-runs.jsonl` for this run with
`"blocked": true` (extra field, ignored by `scripts/generate-routine-log.mjs`)
so the raw ledger reflects that this was a skipped/blocked run, not a clean
sweep that found nothing — though note the dashboard generator itself treats
any `filed: 0` entry as `clean: true` regardless, so the generated
`data/routine-log.json` will still render this as a clean day if it's
regenerated. That's a pre-existing quirk of `buildSweeps()` in
`scripts/generate-routine-log.mjs`, not something this handover fixes.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually callable in your session (e.g. a
   `list_issues` or equivalent call succeeds) before starting.
2. Re-run `routines/idea-sweep.md` for "AI Landscape" from the top — Issue Cap
   pre-flight, then spec-drift → bug-error → market-feature per the routine.
   Nothing from this session needs to be re-read or reconciled; treat it as a
   fresh run.
3. Once the run completes (filed or clean), append its own ledger line to
   `data/sweep-runs.jsonl` as normal and delete this handover file — it will
   no longer describe current state.
4. Do not use this handover as evidence that AI Landscape's backlog is empty
   or that no gaps exist — it only documents that no check was possible this
   run.
