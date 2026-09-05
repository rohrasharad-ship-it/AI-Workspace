# Handover: idea-sweep (Application Agent) fully blocked — no Linear MCP tool in this session at all

**For:** Any agent/session with working Linear MCP access
**From:** Claude Code (scheduled `idea-sweep` routine run for Application Agent), 2026-09-05
**Blocked by:** This session's toolset has no Linear MCP tools whatsoever — not "list_issues fails," not "missing API key for a shell script," but no `mcp__Linear__*` tool exists to call in the first place. The harness's own system notice states: "The following MCP servers require authentication before their tools can be used: Linear" and "This session is non-interactive, so Claude cannot run the OAuth flow here." A `ToolSearch` for Linear-related tools (issue list/create/comment) returned zero Linear tools — only GitHub, Slack, Vercel, and generic harness tools.
**Action:** Re-authorize the Linear MCP connector for this account/session type (via `claude mcp` or `/mcp` in an interactive session, or the account's connector settings), then re-run this routine for Application Agent.
**Issue:** N/A — this run never got far enough to create or touch a Linear issue.

## Why this is a new/distinct blocker

Prior idea-sweep sessions (see `handovers/preview-branch-cleanup-linear-api-key.md`, updates from 2026-08-06 through 2026-08-12) all had **working Linear MCP read access** — they ran `list_issues`, checked issue status/labels, and cross-referenced preview branches successfully. Their blocker was narrower: no `LINEAR_API_KEY` secret for the *shell script* path (`scripts/cleanup-preview-branches.sh`), and a proxy that blocks mutating git/GitHub-API calls (branch deletion) needed for that same housekeeping step. Those are documented and, per that file's own most recent update, don't need re-verifying.

This session is different in kind: **Linear MCP tools are absent entirely**, so even the read-only parts of the routine (Issue Cap pre-flight, searching for duplicates, the stale-issue sweep) cannot run — not just the write/delete side.

## What this blocked, per `routines/idea-sweep.md` and its constituent role files, for Application Agent

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — requires `list_issues` filtered by the Application Agent Linear Project ID (`7dc5202c-a586-4bed-b2d3-fba10f2dd913` per `projects.md`). Could not run.
- **spec-drift steps 1–9** (gap-finding + filing) — blocked transitively (cap check is a prerequisite), and step 4/5 themselves need Linear search + `create_issue`.
- **spec-drift step 10** (stale-issue sweep, runs independent of the cap) — needs to list/read/comment on open Backlog issues. Blocked, no Linear access.
- **spec-drift step 11** (preview-branch cleanup housekeeping) — separately blocked regardless of Linear: this session's own operating rules require all GitHub interaction to go through GitHub MCP tools, not local `git`/`gh` via shell, so the cleanup script (which needs a real `git clone` + `git push --delete`) can't run here either. This matches the already-documented, unrelated blocker in `handovers/preview-branch-cleanup-linear-api-key.md` (missing `LINEAR_API_KEY` repo secret + proxy blocking mutating git/API calls) — see that file for the full history; no need to re-derive it. Not re-verified this run.
- **spec-drift step 12** (OpenSpec archive sweep) — checked `openspec/changes/` in AI-Workspace directly via GitHub MCP: only an `archive/` subfolder exists, no active change folders. Clean 0, not a new blocker, tooling-independent.
- **bug-error, all steps** — blocked at the same Issue Cap pre-flight. Also, independently: `projects.md` lists Application Agent's Vercel Prod URL as `TBD` — there is no production URL to pull runtime logs/errors from yet, so bug-error has nothing to read even once Linear access is restored. Worth fixing `projects.md` (or deploying the app) before the next bug-error run is useful.
- **market-feature, all steps** — blocked at the same Issue Cap pre-flight.

No Linear issues were searched, created, or commented on. No preview branches or OpenSpec changes were touched. Nothing in the Application-Agent repo was modified — this routine never reached the point of proposing anything.

## Instructions for receiving agent/human

1. Restore Linear MCP access for scheduled/non-interactive sessions (or confirm it's already fixed by trying `list_issues` on the Application Agent project ID above).
2. Re-run `idea-sweep` for Application Agent per `routines/idea-sweep.md`.
3. Separately, consider filling in a real Vercel Prod URL for Application Agent in `projects.md` (currently `TBD`) so `bug-error` has something to check.
4. Delete this handover file once a subsequent run confirms Linear MCP access works from this session type.
