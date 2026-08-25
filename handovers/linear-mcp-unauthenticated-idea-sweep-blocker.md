# Handover: idea-sweep routine blocked — Linear MCP not authenticated in this session

**For:** Sharad (or any human with access to this account's connector settings)
**From:** idea-sweep routine, triggered for "AI Workspace" (PM OS), 2026-08-25
**Blocked by:** the Linear MCP server is listed as requiring authentication before its
tools can be used — no `mcp__Linear__*` tools appeared in this session's tool set at
all (confirmed via `ToolSearch` for `list_issues`/`create_issue`/project queries; only
GitHub, Vercel, and Slack MCP tools resolved). This is a harder blocker than the
previously-documented `LINEAR_API_KEY` / proxy-write issue in
`handovers/preview-branch-cleanup-linear-api-key.md` and
`handovers/linear-issue-vercel-preview-blocker.md` — those assumed working Linear MCP
*read* access (used to list issues, check status, cross-reference branches) and only
blocked the *write* path (deleting refs) or a specific workflow's secret. Here, no
Linear operation of any kind is available: not the Issue Cap check
(`agents/shared/issue-cap.md`), not `list_issues` for the stale-issue sweep
(`agents/spec-drift.md` step 10), not issue filing for any of the three roles.

**Action needed:** Authorize the Linear connector for this account — per this session's
own instructions, that happens via claude.ai connector settings (this session is
non-interactive and cannot run an OAuth flow itself). Once authorized, the next
scheduled or manual `idea-sweep` firing should pick it up with no other change needed.

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
  cap. Those steps also depend on Linear reads, so they could not run either.
- Did **not** write a `data/sweep-runs.jsonl` entry for this run — every existing entry
  in that ledger represents a run that actually queried Linear (even the `"clean":true`
  ones reflect a real 0-count check). Writing one here would misrepresent a blocked run
  as a completed clean sweep. Leaving the ledger untouched until a real run happens.
- Did not delete this file's blocker even though it overlaps in spirit with the two
  existing Linear-related handovers above — this is a distinct root cause (no MCP
  session auth at all, vs. a missing repo secret / proxy write block), so keeping it
  separate until resolved.

## Instructions for the next agent/human

1. Authorize the Linear MCP connector for this account (claude.ai connector settings).
2. Re-run: "Run the idea-sweep routine for AI Workspace. Follow
   `rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md` exactly."
3. Once Linear reads succeed, this file can be deleted — it documents a one-time
   session-auth gap, not an ongoing structural issue like the other two Linear
   handovers (which still need the `LINEAR_API_KEY` repo secret separately).
