# Handover: idea-sweep (Resume Website) blocked — no Linear MCP access this session

**For:** Any agent/session with an authorized Linear MCP connection
**From:** idea-sweep routine run, Resume Website, 2026-09-09 (scheduled trigger)
**Blocked by:** Linear MCP server is unauthenticated in this session — no `mcp__Linear__*` tools were offered at all (confirmed via tool search), so every Linear-dependent step in `agents/spec-drift.md`, `agents/bug-error.md`, and `agents/market-feature.md` is unreachable, not just degraded.
**Action:** Once Linear MCP is authorized (via `claude mcp` or `/mcp` in an interactive session — this is account/session config, not something fixable from inside a non-interactive run), re-run the full `idea-sweep` routine for Resume Website per `routines/idea-sweep.md`.
**Issue:** N/A — this is a routine-level block, not tied to one Linear issue. Nothing was filed, so there is no issue to comment on.

## Payload

This was a scheduled firing of `idea-sweep` for **Resume Website** only
(`rohrasharad-ship-it/resume-website`, Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`). Per `routines/idea-sweep.md`, all
three idea-generation roles should have run in order: spec-drift, bug-error,
market-feature.

**What actually happened:** the session had GitHub MCP and Vercel MCP tools
available, but zero Linear tools of any kind — the system confirmed Linear
"requires authentication before its tools can be used." Every one of the
following depends on Linear MCP and could not be attempted:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues`
  filtered by Linear Project ID. Not run. Cap status for Resume Website is
  **unknown** this cycle.
- **spec-drift steps 1–9** (gap-finding + filing) — blocked (needs Linear
  search + create + attach).
- **spec-drift step 10** (stale-issue sweep / comments) — blocked (needs
  Linear list + comment).
- **spec-drift step 11** (preview-branch cleanup) — blocked harder than the
  rest: `scripts/cleanup-preview-branches.sh` hard-fails without
  `LINEAR_API_KEY` (`error: LINEAR_API_KEY is required`), which also was not
  set in this session's environment. **125 `preview/*` branches** currently
  exist on `origin` (checked via `git ls-remote --heads origin 'preview/*'`)
  — this count is a pre-existing backlog, not something this run created, but
  it confirms the scheduled GitHub Action backup
  (`.github/workflows/preview-branch-cleanup.yml`) is also not clearing them,
  or has been accumulating between successful runs. Worth checking that the
  Action's `LINEAR_API_KEY` repo secret is actually set.
- **spec-drift step 12** (OpenSpec archive sweep) — not blocked by Linear, but
  checked directly instead of via the script: `openspec/changes/` in
  AI-Workspace currently has **no active change folders** (only `archive/`),
  so there is nothing to archive regardless. No action needed this cycle.
- **bug-error** (all steps) — blocked (needs Linear search + create + attach;
  Vercel MCP itself was reachable and could have supplied the runtime-log
  side, but there's no point reading logs if nothing can be filed).
- **market-feature** (all steps) — blocked (needs Linear search + create +
  attach).

**Nothing was filed, nothing was skipped-at-cap** — this is a hard tool
outage, not a normal "at cap" or "nothing found" cycle. Do not read the
sweep ledger entry for this run as a clean/empty result.

## Instructions for receiving agent

1. Confirm Linear MCP is authorized in the new session (try any
   `mcp__Linear__*` tool, e.g. a project or issue lookup).
2. Re-run `idea-sweep` for Resume Website from the top, per
   `routines/idea-sweep.md` — including the Issue Cap pre-flight, since cap
   status is unknown from this run.
3. Optionally investigate the 125-branch `preview/*` backlog on
   `rohrasharad-ship-it/AI-Workspace` once `LINEAR_API_KEY` is available —
   run `scripts/cleanup-preview-branches.sh --dry-run` first to see how many
   it would actually delete before running for real.
4. Delete this handover file once a Linear-authorized run of `idea-sweep` for
   Resume Website has completed successfully.

**Do not** treat this file as evidence that Resume Website has no real
issues to file — it only means this session couldn't check.
