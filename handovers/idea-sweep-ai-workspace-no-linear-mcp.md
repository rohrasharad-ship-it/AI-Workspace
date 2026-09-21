# Handover: idea-sweep for AI Workspace (PM OS) blocked — no Linear MCP in this session at all

**For:** Any agent with Linear MCP access
**From:** idea-sweep routine (scheduled trigger), AI Workspace (PM OS), 2026-09-21
**Blocked by:** This session (Claude Code on the web, fired by a scheduled/automated trigger) has **no Linear MCP tool loaded at all** — `ToolSearch` for any Linear tool (`list_issues`, etc.) returns nothing, and the system context states the Linear MCP server "requires authentication before its tools can be used" and that this non-interactive session cannot run the OAuth flow. This is a step beyond the already-documented `LINEAR_API_KEY` gap in `handovers/preview-branch-cleanup-linear-api-key.md` (that one blocks only the shell script in step 11) — here the **MCP tool itself is unavailable**, so nothing in `routines/idea-sweep.md` that touches Linear could run this cycle.
**Action:** Connect/authorize the Linear MCP connector for this session type (via claude.ai connector settings, per the standard guidance for unauthenticated MCP servers), or re-run this routine from a session that already has Linear MCP connected (e.g. an interactive Claude Code session, or whichever session type produced the prior successful idea-sweep runs logged in `data/sweep-runs.jsonl`).
**Issue:** N/A — no Linear issue exists for this yet; the receiving agent should create one in **PM OS** if it doesn't already have Linear access to check, or fold this into whatever secret/connector work resolves the LINEAR_API_KEY handover above.

## Payload

What I could **not** do this cycle for **AI Workspace (PM OS)** (Linear Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`), per `routines/idea-sweep.md`:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — requires `list_issues` via Linear MCP. Not run. Issue count for this project is **unknown** this cycle.
- **spec-drift steps 1–9** (gap-filing) — requires searching Linear for dedupe before filing. Not run.
- **spec-drift step 10** (stale-issue sweep / comments on Backlog issues) — requires listing + reading comments on Linear issues. Not run.
- **bug-error** and **market-feature** roles — both require the same pre-flight cap check and Linear search-before-file step. Not run.

What I **did** do this cycle, since it needs no Linear access:

- **spec-drift step 12** (OpenSpec archive housekeeping): ran `npm install` (node_modules was missing, `npx openspec` failed with "could not determine executable to run" until installed), then `bash scripts/archive-merged-openspec-changes.sh --sweep --dry-run` → `sweep: no completed active changes`. Clean, nothing to archive.
- **spec-drift step 11** (preview-branch cleanup script): still fails immediately with `error: LINEAR_API_KEY is required` — unchanged from the existing handover in `handovers/preview-branch-cleanup-linear-api-key.md`. `preview/*` branch count on `origin` is now **125** (up from the 121 classified as of the 2026-08-12 update in that file) — did not re-derive the full safe/keep classification since that file already says re-verifying the proxy-level block wastes tokens with no new information; the fix (add the `LINEAR_API_KEY` repo secret) is unchanged and still not applied a month later.

No Linear issues were filed, no Linear comments were posted, and no issue-cap count was recorded for AI Workspace (PM OS) this cycle — all deferred until Linear MCP access exists.

## Instructions for receiving agent

1. Once Linear MCP access is confirmed working, run the full `idea-sweep` routine for **AI Workspace (PM OS)** from scratch per `routines/idea-sweep.md` (pre-flight cap check, then spec-drift/bug-error/market-feature in order) — treat this as if it had never run this cycle, since nothing Linear-dependent executed.
2. While there, also pick up the still-open `handovers/preview-branch-cleanup-linear-api-key.md` blocker if you have repo-secret access — it's a separate, longer-standing issue but affects the same step 11.
3. Append the real sweep-ledger line to `data/sweep-runs.jsonl` for this project once the actual run completes (do not backfill one now — a fabricated `filed`/`clean` value would misrepresent a cycle where the cap was never even checked).
4. Delete this handover file once a session with working Linear MCP has completed a full idea-sweep pass for this project.
