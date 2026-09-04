# Handover: idea-sweep for AI Workspace (PM OS) could not run — Linear MCP server unauthenticated

**For:** Any human with claude.ai connector settings access, or the next agent/human touching Linear connector auth.
**From:** idea-sweep routine run for AI Workspace (PM OS), triggered 2026-09-04 (scheduled/automated firing, no live user present).
**Blocked by:** the Linear MCP server is listed as requiring authentication before any of its tools can be used in this session ("The following MCP servers require authentication before their tools can be used: Linear"). This session is non-interactive (scheduled trigger), so the OAuth flow cannot be run here, and there is no `LINEAR_API_KEY` env var available as a fallback either (checked — not set).

## Why this blocks the entire routine, not just part of it

Unlike the prior `preview-branch-cleanup.yml` blocker (documented in
`handovers/preview-branch-cleanup-linear-api-key.md`), where Linear MCP tools
worked fine and only the *shell-script* path (which needs a raw
`LINEAR_API_KEY` secret) was blocked, this session has **zero** Linear access
of any kind — no MCP tools, no API key. Every actionable step of
`routines/idea-sweep.md` for AI Workspace (PM OS) depends on Linear MCP:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — needs
  `list_issues` filtered by Linear Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`.
  Could not run, so it's unknown whether this project is even under cap.
- **spec-drift steps 1–9** (search Linear, file issues) — needs Linear search
  and issue creation.
- **spec-drift step 10** (stale-issue sweep) — needs to list open Backlog
  issues and read their comments via Linear MCP.
- **spec-drift step 11** (preview-branch housekeeping) — needs to look up each
  `preview/<issue-id>-v<n>` branch's issue status in Linear before deciding to
  delete it.
- **bug-error and market-feature roles** — both file directly to Linear.

So nothing in this routine could execute this run — not even the
cap-check-skip path (steps 10–11 only), since those also require Linear reads.

## Action needed

Someone with access to claude.ai connector settings needs to authorize the
Linear connector for this account (per the standard instruction: "for
claude.ai connectors, via their claude.ai connector settings"). Once
authorized, the next scheduled or manual idea-sweep run for AI Workspace
(PM OS) should proceed normally — no code or routine-file changes are needed,
this is purely a connector-auth gap.

## What was checked this run (no repo mutations made)

- Resolved project via `projects.md`: **AI Workspace (PM OS)** — repo
  `rohrasharad-ship-it/AI-Workspace`, Linear Project "PM OS", ID
  `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`, prod
  `ai-workspace-blond.vercel.app`.
- Confirmed no `LINEAR_API_KEY` (or similar) present in this session's shell
  environment.
- Read `routines/idea-sweep.md`, `routines/README.md`, and the start of
  `agents/spec-drift.md` to confirm every step needs Linear MCP before
  attempting anything — did not proceed to file issues, comment, or delete
  branches without that access, to avoid acting on stale/incomplete
  information (e.g. filing a duplicate issue without being able to search
  first, or deleting a preview branch without confirming its issue's status).
- No `data/sweep-runs.jsonl` entry was appended for this run since no role
  actually ran (filing a `"clean": true` line would misrepresent this as a
  verified-clean sweep rather than a blocked one).

## Next steps for the receiving session

1. Confirm Linear MCP tools are authenticated and callable.
2. Re-run: "Run the idea-sweep routine for AI Workspace (PM OS)."
3. Once it completes (or confirms at-cap / clean), append the sweep ledger
   line and delete this handover file — no need to hand-verify anything else
   here since no Linear-side state was inspected or changed this run.
