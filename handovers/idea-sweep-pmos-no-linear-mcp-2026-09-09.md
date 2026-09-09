# Handover: idea-sweep routine for AI Workspace (PM OS) could not run — no Linear MCP tools in this session at all

**For:** Sharad, or any future agent session with working Linear MCP access
**From:** idea-sweep routine run for AI Workspace (PM OS), 2026-09-09 (scheduled trigger)
**Blocked by:** The Linear MCP connector is installed for this account (`enabledInChat: true`, `installState: unknown`) but its tools are not loaded in this session at all — this is a session-auth issue, not the previously-documented `LINEAR_API_KEY` shell-script gap (see `handovers/preview-branch-cleanup-linear-api-key.md`, which is about a repo secret for a `bash` script only). Confirmed via `ToolSearch` for any `mcp__Linear__*` tool name — zero results — and the harness's own system reminder stating Linear "needs authorization" and that this non-interactive session cannot run the OAuth flow.
**Action:** Re-authorize the Linear connector for this account at claude.ai → Settings → Connectors (or wherever `claude mcp`/`/mcp` surfaces it for a live session), then re-run this routine. No Linear-side data recovery is needed — nothing was created or modified, so a plain re-run is sufficient once auth is restored.
**Issue:** N/A — this is a routine-level session blocker, not driven by a specific Linear issue.

## Payload

Per `routines/idea-sweep.md`, running this routine for AI Workspace (PM OS)
(`rohrasharad-ship-it/AI-Workspace`, Linear project ID
`3703a715-c49d-4b9e-b6f1-5975d3ebe39a`) requires Linear MCP for essentially
every step:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — needs
  `list_issues` filtered by project ID. Not possible this run, so it's
  unknown whether the project is at/over the 5-issue cap.
- **spec-drift** (steps 1–9: dedupe search + filing; step 10: stale-issue
  sweep needs to list/read/comment on open issues) — none of this ran.
- **bug-error** and **market-feature** (dedupe search + filing) — neither ran.
- **spec-drift step 11** (preview-branch cleanup) — also independently
  blocked by the separate, already-tracked `LINEAR_API_KEY` gap (see the
  dedicated handover); moot this run since step 11 needs Linear either way.
- **spec-drift step 12** (OpenSpec archive sweep) — this one does **not**
  need Linear. I checked `openspec/changes/` directly: it currently contains
  only the `archive/` subfolder, i.e. zero active (non-archived) changes to
  sweep. So this step is a clean 0 regardless of the Linear outage, not a new
  blocker.

No Linear reads, writes, comments, or searches were attempted or performed
this run. No issues were filed, no comments were posted, and no assumption
about cap status was made — the run stopped cleanly at the pre-flight step
rather than guessing.

I deliberately did **not** append a line to `data/sweep-runs.jsonl` for this
run: every existing line in that ledger represents a run where the cap check
and/or the three roles actually executed (even a "0 filed" line means Linear
was queried and came back empty). Writing `{"filed":{"bugs":0,"features":0},
"clean":true}` here would misrepresent "we never checked" as "we checked and
it was clean." Once Linear access is restored, just resume normal ledger
behavior on the next run — no backfill needed for this skipped entry.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually loaded (e.g. `ToolSearch` for
   `mcp__Linear__*`, or just try `list_issues`/equivalent).
2. Re-run `routines/idea-sweep.md` for **AI Workspace (PM OS)** from the top
   — pre-flight cap check first, then all three roles per the normal
   under-cap/over-cap branching.
3. Append the ledger line and run `node scripts/generate-routine-log.mjs`
   as the routine normally requires, once the run actually completes.
4. Delete this handover file once that clean re-run has happened — there is
   no state here that needs manual reconciliation, so this file's only job
   is to explain why 2026-09-09 shows a gap in the sweep cadence.
