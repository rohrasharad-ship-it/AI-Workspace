# Handover: idea-sweep routine for Application Agent could not run — no Linear access at all this session

**For:** Any agent session with working Linear MCP access (or a human who can
authorize the Linear connector for this account)
**From:** idea-sweep routine trigger for Application Agent, scheduled run, 2026-09-13
**Blocked by:** Linear MCP server requires OAuth authorization that this
session cannot perform (non-interactive scheduled session — no browser flow
available), and there is no `LINEAR_API_KEY` env var as a fallback. Unlike
prior housekeeping-only blockers documented in
`handovers/preview-branch-cleanup-linear-api-key.md` (where sessions had
working Linear MCP *read/write* access but lacked a raw API key for the shell
script and lacked git push permission for branch deletion), this session had
**zero** Linear tool access of any kind — `ToolSearch` confirms no Linear
tool schema is reachable, and the harness explicitly flagged Linear as
"requires authentication before its tools can be used."
**Action:** Authorize the Linear connector for this account (via
claude.ai Settings → Connectors, or `claude mcp`/`/mcp` in an interactive
session), or add `LINEAR_API_KEY` as an available secret/env var for
scheduled sessions, then re-run the idea-sweep routine for Application Agent.

## Payload

Per `routines/idea-sweep.md`, running idea-sweep for Application Agent
requires, in order:

1. Issue Cap pre-flight (`agents/shared/issue-cap.md`) — needs `list_issues`
   filtered by Application Agent's Linear Project ID
   (`7dc5202c-a586-4bed-b2d3-fba10f2dd913` per `projects.md`).
2. `agents/spec-drift.md` steps 1–9 (gap-filing) — needs Linear search +
   create.
3. `agents/spec-drift.md` step 10 (stale-issue sweep) — needs Linear list +
   comment.
4. `agents/spec-drift.md` step 11 (preview-branch housekeeping) — needs
   `LINEAR_API_KEY` for `scripts/cleanup-preview-branches.sh` (already a
   known, separately-tracked blocker — see
   `handovers/preview-branch-cleanup-linear-api-key.md`, 7+ consecutive runs).
5. `agents/bug-error.md` (all steps) — needs Linear search + create. Note
   Application Agent's Vercel Prod URL is still listed as `TBD` in
   `projects.md`, so this role may have had nothing to check regardless.
6. `agents/market-feature.md` (all steps) — needs Linear search + create.

**Every one of 1–3, 5, 6 requires at least Linear read access, which this
session did not have.** I did not attempt to guess at cap status or file
issues blind — that would risk violating the 5-issue cap and the "search
Linear first, skip anything already tracked" dedupe rule.

**Step 12** (`agents/spec-drift.md`, OpenSpec archive housekeeping) does not
require Linear, but I did not run it standalone this session: it needs a
local clone with `npx openspec` + `gh` (this session has no `gh` CLI per its
own operating instructions), and running it without the `gh`-based open-PR
check would silently skip that safety check rather than fail loudly — not a
good tradeoff to take unilaterally for a minor housekeeping step when the
main routine already couldn't run. Leaving this for a session with proper
`gh` access, consistent with how `spec-drift.md` step 12 is meant to run.

**No Linear issue exists to comment on for this blocker** — this is a
routine-level failure at trigger time, not tied to a specific issue, so the
usual "comment on the Linear issue" handover step doesn't apply here.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable (`ToolSearch` for
   `list_issues`/`create_issue`/`save_issue`, or just try a `list_projects`
   call).
2. Re-run the idea-sweep routine for Application Agent per
   `routines/idea-sweep.md` from the top — no prior state from this session
   to reconcile, since nothing was filed, commented, or changed in Linear.
3. While there, the Application Agent row in `projects.md` still lists
   Vercel Prod as `TBD` — if a prod URL now exists, update that row so
   `agents/bug-error.md` has something to check.
4. Delete this handover file once a session completes a real idea-sweep run
   for Application Agent with working Linear access.
