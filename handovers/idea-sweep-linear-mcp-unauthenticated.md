# Handover: idea-sweep can't run — Linear MCP not authenticated in scheduled sessions

**For:** Any agent/human who can complete the Linear MCP OAuth connection for this
account (via `claude mcp` / `/mcp` in an interactive session, or claude.ai connector
settings)
**From:** idea-sweep routine run for AI Workspace (PM OS), scheduled/automated session,
2026-08-27
**Blocked by:** The Linear MCP server requires an OAuth authorization that has not been
completed. A scheduled, non-interactive session cannot run that flow — there is no human
present to approve it. Every `mcp__Linear__*` tool is absent from this session's toolset
(confirmed via `ToolSearch`; the system explicitly lists Linear under "MCP servers that
require authentication before their tools can be used," separate from servers that were
merely still connecting).
**Action:** Authorize the Linear MCP connector once, interactively, so future scheduled
`idea-sweep` runs inherit a working connection.

---

## Why this blocks almost the entire routine

`routines/idea-sweep.md` runs spec-drift, bug-error, and market-feature for the named
project. Every one of those roles — and the routine's own mandatory Issue Cap pre-flight
(`agents/shared/issue-cap.md`) — requires Linear MCP to count active issues, search for
dedupes, create issues, or comment. With no Linear tools available at all:

- **Step 0 (Issue Cap pre-flight)** — cannot count active pipeline issues for the PM OS
  project (`3703a715-c49d-4b9e-b6f1-5975d3ebe39a`). Cannot safely determine whether the
  project is under or at the 5-issue cap.
- **spec-drift steps 1–9** (gap-filing) — cannot search or create issues. Skipped.
- **spec-drift step 10** (stale-issue sweep) — cannot list open issues or post comments.
  Skipped.
- **bug-error** (all steps) — cannot search or create issues. Skipped entirely.
- **market-feature** (all steps) — cannot search or create issues. Skipped entirely.

## What *did* run this session (no Linear dependency)

- **spec-drift step 11 (preview-branch housekeeping)** — also blocked, but for a
  **different, already-documented** reason: `scripts/cleanup-preview-branches.sh` needs
  `LINEAR_API_KEY` as a raw env var (calls the Linear GraphQL API directly, not via MCP),
  and it isn't set in this environment either. This is the same long-standing blocker
  tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (7 prior runs as of
  2026-08-12) — see that file for the fix (add the repo secret) and the fully verified
  branch classification list. Not re-verified again here per that file's own note that
  doing so a 4th/5th time wastes tokens with no new information.
- **spec-drift step 12 (openspec archive housekeeping)** — ran successfully (needs only
  git + the `openspec` CLI, no Linear). `openspec/changes/` has no active, non-archived
  change folders right now, so the sweep correctly did nothing:
  `sweep: no completed active changes`.

## Instructions for receiving agent/human

1. Complete the Linear MCP OAuth authorization for this account (interactive session
   required — `/mcp` in Claude Code, or the claude.ai connector settings page).
2. Once authorized, re-run `idea-sweep` for AI Workspace (PM OS) — this run filed nothing
   and checked nothing, so it should not be treated as a "clean" cycle; it simply didn't
   happen.
3. Separately (unrelated fix, already fully specified): add the `LINEAR_API_KEY` repo
   secret per `handovers/preview-branch-cleanup-linear-api-key.md` so step 11 and
   `scripts/generate-routine-log.mjs` stop failing too. Fixing Linear MCP auth does not
   fix this second one — they're different credentials for different call paths (MCP
   OAuth vs. raw API key in a shell script).
4. Delete this handover once a scheduled idea-sweep session confirms Linear MCP tools are
   present and a full run (cap check + all three roles) completes normally.
