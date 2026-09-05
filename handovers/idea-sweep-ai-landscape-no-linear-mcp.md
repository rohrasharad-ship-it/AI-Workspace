# Handover: idea-sweep for AI Landscape 2026 could not run — no Linear MCP tool in this session at all

**For:** Sharad (connector authorization) — then any agent session that has a working Linear MCP connection
**From:** idea-sweep routine (orchestrating session, Claude Code on the web), triggered for AI Landscape 2026, 2026-09-05
**Blocked by:** This session has **no Linear MCP tool whatsoever** — not "list_issues returns empty for this project" (the known display-name bug in `agents/shared/issue-cap.md`), not "the shell script has no `LINEAR_API_KEY`" (the already-documented, still-open issue in `handovers/preview-branch-cleanup-linear-api-key.md`). A tool search for any Linear-related tool returned zero results, and the session was told directly: the `Linear` MCP server "requires authentication before its tools can be used" and, being non-interactive, this session cannot run the OAuth flow to authorize it. There is also no `LINEAR_API_KEY` (or similar) in this session's environment as a fallback for direct GraphQL calls.
**Action:** Authorize the Linear connector for Claude Code web/cloud sessions (claude.ai → Settings → Connectors → Linear — see the connector-auth note in this session's own instructions). This is a **different fix** from adding a `LINEAR_API_KEY` repo secret (that unblocks the GitHub Action script; this unblocks agent sessions that need to call Linear directly). Once authorized, re-run the `idea-sweep` routine for AI Landscape 2026 (and probably every other project — this session's account-level connector gap isn't project-specific).
**Issue:** N/A — this blocks the routine before any Linear issue could be read or created, including the Issue Cap pre-flight itself.

## What this blocked, concretely

Per `routines/idea-sweep.md`, before any of the three idea-generation roles can run for a project, the orchestrating session must do the Issue Cap pre-flight (`agents/shared/issue-cap.md`) — which requires `list_issues` against the Linear Project ID. With zero Linear tools available, this session could not:

- Run the Issue Cap check for AI Landscape 2026 (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`)
- Run spec-drift steps 1–9 (gap-filing) or step 10 (stale-issue sweep — needs to read/comment on existing issues)
- Run bug-error or market-feature at all (both search Linear before filing, and file directly)

So **none of the three roles ran this cycle** — not "ran and found nothing." This is not a `"clean": true` sweep, and I have deliberately **not** appended a `data/sweep-runs.jsonl` line claiming one — a fabricated clean entry would misrepresent an unchecked project as a verified-empty one on the `/routine-log.html` dashboard.

Steps 11–12 (preview-branch cleanup, OpenSpec archive sweep) are shell scripts run from a real clone of AI-Workspace; this session type (GitHub MCP only, per its own operating instructions) can't run them regardless of Linear access — this matches what prior sessions already found and documented in `handovers/preview-branch-cleanup-linear-api-key.md` (2026-08-08 update onward), so it isn't new information and I haven't re-verified it.

## Separate, smaller note: AI Landscape 2026 isn't a Vercel project

Independent of the Linear blocker: `projects.md` lists AI Landscape 2026's prod URL as `https://rohrasharad-ship-it.github.io/ai-landscape/` (GitHub Pages), not a `*.vercel.app` domain. `agents/bug-error.md` step 1 says "Read the Vercel production runtime logs/errors from the last 24 hours" — that has no target for this project as currently configured (no Vercel deployment to read logs from). Whoever picks bug-error back up for this project should either confirm there's a Vercel project behind it that isn't reflected in `projects.md`, or treat this project as log-source-less and adapt (e.g. skip step 1's log read, rely only on Playwright-observed console/network errors against the live GitHub Pages URL). Not blocking this handover's main fix — just flagging so the next bug-error run doesn't stall rediscovering it.

## Instructions for receiving agent / for Sharad

1. Authorize the Linear connector for this account's Claude Code sessions (claude.ai connector settings).
2. Re-trigger `idea-sweep` for AI Landscape 2026 (and spot-check one other project) to confirm Linear MCP tools are now present in the session's tool list before assuming the fix worked.
3. Once a run completes normally, delete this handover file.
4. Separately (not required to close this handover): decide how `agents/bug-error.md` should treat AI Landscape 2026 given it has no Vercel deployment — see note above.
