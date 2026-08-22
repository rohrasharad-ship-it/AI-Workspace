# Handover: idea-sweep routine for AI Workspace (PM OS) could not run — no Linear access this session

**For:** Any agent/human who can authorize the Linear connector for this account, or the next idea-sweep session that has working Linear MCP access
**From:** Scheduled idea-sweep run for AI Workspace (PM OS), 2026-08-22
**Blocked by:** No Linear MCP tools available in this session at all (not a specific tool failure — `ToolSearch` for Linear tools returns nothing, and the session's own startup notice states the Linear MCP server "requires authentication before its tools can be used"). Also no `LINEAR_API_KEY` as a Bash env var, so there's no fallback direct-API path either.
**Action:** Authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear), then re-run this routine: "Run the idea-sweep routine for AI Workspace. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly."
**Issue:** N/A — no Linear issue could be created or referenced this session (that's the blocker itself)

## What happened

Triggered as a scheduled task: `routines/idea-sweep.md` for **AI Workspace (PM OS)** (repo `rohrasharad-ship-it/AI-Workspace`, Linear Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`, per `projects.md`).

Read `routines/README.md`, `routines/idea-sweep.md`, `projects.md`, and the shared modules (`agents/shared/issue-cap.md`, `agents/shared/conventions.md`, `agents/shared/issue-brief.md`) to prepare for the run. Before starting the mandatory pre-flight Issue Cap check (`agents/shared/issue-cap.md`, requires `list_issues` via Linear MCP), confirmed via `ToolSearch` that **no Linear MCP tools are loaded or reachable this session** — a search for `list_issues`/"linear issue create project" surfaced only GitHub's `list_issues`/`issue_write`, nothing Linear-namespaced. The session's own tool-availability notice separately confirms Linear requires authentication that can't be completed in a non-interactive session.

This is a different, more fundamental blocker than the one already tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that one is about the `LINEAR_API_KEY` **repo secret** missing for the GitHub Action / shell-script path specifically — prior idea-sweep sessions running the AI Workspace project as recently as 2026-08-19 clearly *did* have working Linear MCP access, per the clean entry in `data/sweep-runs.jsonl`). Here, this session has **no Linear access via any path** — MCP or API key — so nothing downstream of the pre-flight could run:

- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — blocked, can't count active issues
- `agents/spec-drift.md` (all steps, including 10–11 stale-issue sweep / preview-branch housekeeping — both read/comment on Linear issues)
- `agents/bug-error.md` — blocked, can't dedupe-search or file
- `agents/market-feature.md` — blocked, can't dedupe-search or file

No Linear issues were created, no comments posted, no stale-issue sweep performed, no preview branches touched. Nothing was fabricated or skipped silently — the run stopped at the pre-flight step rather than guessing at cap status or filing without a dedupe check.

**Did not** write a `data/sweep-runs.jsonl` entry for this run — the ledger records completed sweeps (`"clean": true` means all three roles ran and found nothing), and that would misrepresent a run that never executed its roles.

## Instructions for receiving agent/human

1. If you're Sharad: authorize the Linear connector (claude.ai → Settings → Connectors → Linear) so future scheduled sessions have MCP access. This is a one-time per-account/session-type setup step, not something an agent can do from inside a non-interactive session.
2. If you're an agent with working Linear MCP access picking this up: just re-run `idea-sweep` for AI Workspace (PM OS) normally per `routines/idea-sweep.md` — there's no partial state to reconcile, since nothing was started or half-filed.
3. Delete this handover file once a subsequent idea-sweep run for AI Workspace (PM OS) completes successfully (with working Linear access) — at that point this note has served its purpose.
