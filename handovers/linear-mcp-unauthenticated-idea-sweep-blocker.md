# Handover: idea-sweep routine blocked — Linear MCP not authenticated in this session

**For:** Sharad (or any human with access to this account's connector settings)
**From:** idea-sweep routine, triggered for "AI Workspace" (PM OS), 2026-08-29
**Blocked by:** the Linear MCP server requires authentication before its tools can be
used. `ToolSearch` for `list_issues` / `create_issue` / project queries returned only
GitHub tools — no `mcp__Linear__*` tool exists in this session's tool set at all. This
is the same root cause documented in commit `219db5e` ("idea-sweep: AI Workspace (PM OS)
run blocked — Linear MCP not authenticated", 2026-08-25), which added this exact file —
but that commit's branch was never merged to `main`, so the file wasn't here for this
run to find. Recreating it now rather than assuming it's still open elsewhere.

It's distinct from the older, already-documented `LINEAR_API_KEY` GitHub Actions secret
issue in `handovers/preview-branch-cleanup-linear-api-key.md` (that one blocks a
workflow's shell script; that file is marked "no further action needed" as of
2026-08-12 and doesn't need re-confirming here). Here, no Linear operation of any kind
is available in an interactive/agent session at all — not the Issue Cap check
(`agents/shared/issue-cap.md`), not `list_issues` for the stale-issue sweep
(`agents/spec-drift.md` step 10), not issue filing for any of the three roles.

**Action needed:** Authorize the Linear connector for this account via claude.ai
connector settings — this session is non-interactive and cannot run an OAuth flow
itself. Once authorized, the next scheduled or manual `idea-sweep` firing picks it up
with no other change needed.

## What did and didn't run this session

- Read `routines/idea-sweep.md`, `routines/README.md`, and `projects.md` and resolved
  the target: **AI Workspace (PM OS)** — repo `rohrasharad-ship-it/AI-Workspace`,
  Linear Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`.
- Could not perform the mandatory pre-flight Issue Cap check (`agents/shared/issue-cap.md`)
  because it requires `list_issues` filtered by Linear Project ID — no Linear tool
  available to call.
- Because pre-flight itself couldn't run, none of spec-drift, bug-error, or
  market-feature executed — including spec-drift steps 10–11 (stale-issue sweep,
  preview-branch housekeeping), which the routine says to run even when a project is at
  cap. Those steps also depend on Linear reads.
- Did **not** write a `data/sweep-runs.jsonl` entry for this run, matching the
  2026-08-25 precedent — every existing entry in that ledger represents a run that
  actually queried Linear, and writing one here would misrepresent a blocked run as a
  completed sweep.

## Recurring-blocker note

Git history on this repo (`git log --oneline --all | grep -i "linear mcp"`) shows
dozens of near-identical blocked-run handovers across many unmerged session branches
going back to July 2026, none consolidated into `main`. This suggests Linear MCP
authorization for scheduled/automated sessions on this account is intermittent or not
durably configured, rather than a one-off gap. Worth fixing at the connector-config
level rather than continuing to re-document per run.

## Instructions for the next agent/human

1. Authorize the Linear MCP connector for this account (claude.ai connector settings).
2. Re-run: "Run the idea-sweep routine for AI Workspace. Follow
   `rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md` exactly."
3. Once Linear reads succeed, this file can be deleted.
