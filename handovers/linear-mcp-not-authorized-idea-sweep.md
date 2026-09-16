# Handover: Linear MCP not authorized in this session — idea-sweep routine for Resume Website completely blocked

**For:** Sharad (to authorize the Linear MCP connector), or any future agent session confirmed to have working Linear MCP access
**From:** idea-sweep routine run for Resume Website, scheduled/automated session, 2026-09-16
**Blocked by:** The Linear MCP server is configured for this account but **not authorized** in this session — the harness reported it explicitly ("requires authentication before its tools can be used") and zero `mcp__Linear__*` tools were exposed to `ToolSearch`. There is also no `LINEAR_API_KEY` env var available to this session (confirmed via `echo $LINEAR_API_KEY`).
**Action:** Authorize the Linear MCP connector for this account (interactively, via `/mcp` in a live Claude Code session or the claude.ai connector settings — this session is non-interactive/scheduled and cannot run that OAuth flow itself), so future scheduled `idea-sweep` runs actually have Linear access.
**Issue:** N/A — this is a routine-level blocker (`routines/idea-sweep.md`), not tied to a single Linear issue.

## Payload

This is a **broader** blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (7 independent hits, still
open) — that file documents sessions that *had* working Linear MCP access but
lacked a raw `LINEAR_API_KEY` for the `preview-branch-cleanup.yml` shell
script specifically. This session had **no Linear access of any kind**, which
blocks the entire idea-sweep routine, not just housekeeping step 11:

- **Step 0 (Issue Cap pre-flight, `agents/shared/issue-cap.md`)** — could not
  run at all. Cannot call `list_issues` filtered by the Resume Website Linear
  Project ID (`b01a99ac-46a3-4b00-9139-31e00fae781d` per `projects.md`), so
  the active-pipeline count (Backlog/Todo/In Progress/In Review) is unknown.
- **spec-drift steps 1–9, bug-error, market-feature** — none ran. Filing
  without first searching Linear for dupes would violate the "search Linear
  first" guardrail in `routines/README.md`, so nothing was created.
- **spec-drift step 10 (stale-issue sweep)** — could not list or comment on
  open Backlog issues. Skipped.
- **spec-drift step 11 (preview-branch housekeeping)** — separately, already
  blocked by the missing `LINEAR_API_KEY` repo secret, extensively documented
  across 7 runs in `handovers/preview-branch-cleanup-linear-api-key.md`. Did
  not re-attempt or re-verify the branch list — that file says a further
  re-check "wastes tokens with no new information," and this session has the
  same proxy-level git-push-mutation block those runs already confirmed
  (`git push` to a throwaway branch on AI-Workspace returned the same
  `RPC failed; HTTP 403`). Fix remains what that file says: add the
  `LINEAR_API_KEY` repo secret so the scheduled GitHub Action (real runner,
  not this proxy) can do the deletes.
- **spec-drift step 12 (openspec archive sweep)** — checked independently of
  the Linear blocker (this step doesn't need Linear): `openspec/changes/` in
  AI-Workspace currently contains only an `archive/` subdirectory, no active
  change folders, so there was nothing to archive this run regardless of
  tooling. Not a new blocker, a genuine clean 0 (matches the same finding
  noted in the other handover's 2026-08-08/08-12 updates).
- No Linear issues were searched, created, or commented on for Resume Website
  this run. No `data/sweep-runs.jsonl` "filed" counts are real progress —
  logged as blocked, not clean, see below.

## Instructions for receiving agent / Sharad

1. Authorize Linear MCP for this account — `/mcp` in an interactive Claude
   Code session, or via claude.ai connector settings (whichever this
   environment's scheduled sessions actually run under). This session could
   not do this itself; it's non-interactive.
2. Once authorized, re-run `idea-sweep` for Resume Website from Step 0
   (`routines/idea-sweep.md` → issue-cap pre-flight) — nothing needs undoing,
   since nothing was filed or changed in Linear this run.
3. This does **not** fix the separate `LINEAR_API_KEY` repo-secret blocker
   for the preview-branch-cleanup Action — that's tracked independently in
   `handovers/preview-branch-cleanup-linear-api-key.md` and needs the repo
   secret added regardless of MCP auth state.
4. Delete this handover once a scheduled idea-sweep session confirms Linear
   MCP tools are actually reachable (e.g. a successful `list_issues` call).
