# Handover: idea-sweep (AI Workspace / PM OS) blocked — Linear MCP unauthenticated

**For:** Any agent/session with an authenticated Linear MCP connector
**From:** Claude, scheduled `idea-sweep` run, AI Workspace (PM OS), 2026-07-26
**Blocked by:** Linear MCP requires an interactive OAuth flow; this session was started by a schedule (no live user), so no `mcp__Linear__*` tools were ever exposed — confirmed via `ToolSearch`, not just a slow-connect timeout.
**Action:** Re-authorize the Linear connector (claude.ai connector settings, or `/mcp` in an interactive session), then re-run `idea-sweep` for AI Workspace (PM OS) from step 1.
**Issue:** No Linear issue could be created or referenced — Linear itself is the blocked dependency.

---

## What this run could and couldn't do

Followed `routines/idea-sweep.md` exactly. Target project: **AI Workspace (PM OS)**
(repo `rohrasharad-ship-it/AI-Workspace`, Linear project ID
`3703a715-c49d-4b9e-b6f1-5975d3ebe39a`, Slack `#pm-ops`).

| Step | Result |
|---|---|
| Pre-flight Issue Cap check | **Blocked** — needs `list_issues` (Linear). Not performed; count unknown this run. |
| spec-drift steps 1–9 (gap-filing) | **Blocked** — needs Linear search + create. Not attempted. |
| bug-error (all steps) | **Blocked** — needs Linear search + create (would otherwise have read Vercel logs fine — Vercel MCP tools are available). Not attempted. |
| market-feature (all steps) | **Blocked** — needs Linear search + create. Not attempted. |
| spec-drift step 10 (stale-issue sweep) | **Blocked** — needs Linear read + comment. Not attempted. |
| spec-drift step 11 (preview-branch cleanup) | **Blocked** — `scripts/cleanup-preview-branches.sh` hard-requires `LINEAR_API_KEY`, which is not set in this session's environment. Not run. |
| spec-drift step 12 (OpenSpec archive sweep) | **Ran successfully** (no Linear dependency): `bash scripts/archive-merged-openspec-changes.sh --sweep --dry-run` → `sweep: no completed active changes` (0 archived; `openspec/changes/` has only the `archive/` folder, no active change dirs). |

Nothing was filed, commented, or deleted. No guessing at the cap or dedupe search — per
`agents/shared/conventions.md` Blocked-agent handover guidance, this session did only
what it could verify with the tools actually available, then wrote this handover
instead of going silent or acting blind.

## New evidence worth surfacing (for SHA-61, the existing tracked issue for this recurring blocker)

- `git ls-remote --heads origin | grep -c preview` → **111** `preview/*` branches
  currently on the remote. Consistent with `cleanup-preview-branches.sh` having been
  unable to run (no `LINEAR_API_KEY`) across many prior sweep cycles, not just this
  one — this session did not delete any of them (correctly, since Linear is required
  to determine which are safe to remove).
- This exact blocker (Linear MCP unauthenticated in scheduled/non-interactive
  sessions) was already reported to `#pm-ops` twice earlier today
  (2026-07-26 ~05:06 and ~05:14 IST) for this same project and for Resume Website.
  This run hit the identical wall again — nothing has changed since those reports.
  Posting a brief thread reply rather than a third duplicate top-level message.

## Instructions for receiving agent

1. Confirm Linear MCP tools are present this session (`ToolSearch` for
   `mcp__Linear__*`, or just attempt `list_issues`).
2. Re-run `routines/idea-sweep.md` for **AI Workspace (PM OS)** from step 1 of the
   pre-flight (Issue Cap check) — do not assume this handover's "unknown" cap count,
   recheck live.
3. If under cap, run spec-drift → bug-error → market-feature normally.
4. Run `LINEAR_API_KEY=<key> bash scripts/cleanup-preview-branches.sh --dry-run`
   first given the 111-branch backlog above, review the output, then run for real
   if it looks sane.
5. Delete this handover file once a Linear-connected run of `idea-sweep` for AI
   Workspace (PM OS) has completed successfully.
