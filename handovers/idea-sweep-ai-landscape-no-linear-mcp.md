# Handover: idea-sweep for AI Landscape 2026 could not run — no Linear MCP tool access this session

**For:** Any agent/human who can restore Linear MCP access for scheduled Claude Code sessions
**From:** idea-sweep routine run for AI Landscape 2026, 2026-09-18 (scheduled trigger, Claude Code)
**Blocked by:** This session's tool list contained no Linear MCP tools at all (not deferred, not
listed) — the harness reported the `Linear` MCP server as requiring OAuth authorization, which is
not something a non-interactive scheduled session can complete. This is a step above the
long-standing `LINEAR_API_KEY` repo-secret gap tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`: that gap blocks the *shell scripts*
(`cleanup-preview-branches.sh`, `generate-routine-log.mjs`), but this session had no way to call
`list_issues`, `create_issue`, `create_comment`, or any other Linear MCP tool at all. Every step of
`routines/idea-sweep.md` that depends on Linear was unreachable this run:

- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — needs `list_issues`.
- spec-drift steps 1–9 (gap-filing) — needs Linear search + `save_issue`.
- spec-drift step 10 (stale-issue sweep) — needs `list_issues` + comments.
- spec-drift step 11 (preview-branch cleanup) — separately blocked by missing `LINEAR_API_KEY`
  (unchanged, see the other handover).
- bug-error and market-feature — both need the cap check and Linear search/filing before doing
  anything.

**Action:** Authorize the Linear connector for this account (via claude.ai connector settings, or
`claude mcp` / `/mcp` in an interactive session) so scheduled/cloud Claude Code sessions running
`idea-sweep` can reach Linear MCP tools. This is an account-level connector auth step, separate
from the `LINEAR_API_KEY` repository secret needed for the shell-script paths.

## What this session actually did

- Ran spec-drift step 12 (OpenSpec archive housekeeping) for AI-Workspace, since it has no Linear
  dependency: `npx openspec list --json` shows zero active changes, so
  `scripts/archive-merged-openspec-changes.sh --sweep --dry-run` correctly reported "no completed
  active changes" — a clean 0, not a new blocker.
- Did **not** attempt spec-drift steps 1–9, bug-error, or market-feature for AI Landscape 2026 —
  doing the codebase/spec/log reading without being able to dedupe against Linear or file the
  result would just have to be redone once Linear MCP is back, so no partial analysis is included
  here.
- Logged this run in `data/sweep-runs.jsonl` with `"blocked": true` (not `"clean": true` — nothing
  was actually checked, so it should not read as a verified-empty run in the dashboard).

## Instructions for receiving agent

1. Once Linear MCP access is confirmed working (a `list_issues` call succeeds), re-run
   `idea-sweep` for **AI Landscape 2026** (Linear Project ID
   `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) from the top — the Issue Cap pre-flight first, then all
   three roles per `routines/idea-sweep.md`.
2. This handover file can be deleted once that re-run completes successfully.
3. No branch/issue state needs to be reconciled — this session created nothing in Linear and
   changed nothing in the AI Landscape repo.
