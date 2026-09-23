# Handover: idea-sweep routine (Application Agent) could not run — Linear MCP not authenticated in this session

**For:** Sharad, or any agent session with an authenticated Linear MCP connector
**From:** idea-sweep routine run (Claude Code cloud session), triggered for Application Agent, 2026-09-23
**Blocked by:** The Linear MCP server is listed by this session's runtime as requiring
authentication before any of its tools can be used — no `list_issues`, `create_issue`,
`search`, `comment`, or `attachment` tools were exposed at all (confirmed via tool search;
zero Linear-prefixed tools present, only GitHub and Vercel MCP tools loaded). This is a
session-auth problem, distinct from the long-running `LINEAR_API_KEY` repo-secret blocker
already tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that one affects
the *scripted* preview-branch-cleanup/routine-log paths specifically; this one affects the
*MCP tool* path that every idea-generation role and the Issue Cap pre-flight depend on).
**Action:** Authorize the Linear connector for this account (via claude.ai connector
settings — this is a claude.ai/Claude Code cloud session, not a local `claude mcp` CLI
session), then re-run the `idea-sweep` routine for Application Agent from
`routines/idea-sweep.md`.

## Payload

### Why this stopped the whole routine
Per `routines/README.md` and `agents/shared/issue-cap.md`, the Issue Cap pre-flight (count
active pipeline issues via `list_issues` filtered by the Linear Project ID) is **mandatory
before any idea-generation role creates issues**, and per `agents/spec-drift.md` even the
stale-issue sweep (step 10) needs to read/post Linear comments. With zero Linear MCP tools
available, none of the following could be attempted at all this run, for Application Agent
(Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`, repo
`rohrasharad-ship-it/Application-Agent`):
- Issue Cap pre-flight count
- spec-drift steps 4–10 (dedupe search, issue creation, first comments, stale-issue sweep)
- bug-error steps 3–7 (dedupe search, issue creation, comments)
- market-feature steps 4–8 (dedupe search, issue creation, comments)

No issues were created, no comments posted, no screenshots taken, no preview branches
pushed — there was nothing safe to do downstream of a blocked Issue Cap check.

### What I *could* still check (read-only, GitHub MCP only)
I read `openspec/project.md` and all six capability specs
(`profile`, `generation`, `tracker`, `integrations`, `browser`, `orchestrator`) in
`rohrasharad-ship-it/Application-Agent`. Two things worth flagging to whoever re-runs this
with Linear access, so the eventual spec-drift/market-feature pass isn't wasted effort:

1. **This repo's specs are unusually self-maintaining.** Every capability's `spec.md`
   already carries an explicit `Status` line with shipped `SHA-NNN` references and its own
   `Open / Next` section listing known gaps — e.g. `tracker`: SQLite vs Notion decision;
   `browser`: cloud headless Mode 2, Slack-triggered laptop fill; `orchestrator`: Slack
   command to trigger laptop fill, resume PDF upload automation; `integrations`: Slack
   bot/app event-subscription setup, Indeed/Notion MCP wiring; `generation`: ghost-job
   scoring, PDF export. A spec-drift pass here should treat these `Open / Next` lists as
   the starting candidate set (then dedupe against Linear, which I couldn't do), rather
   than re-deriving gaps from scratch against the codebase.
2. **Vercel prod is `TBD`** for Application Agent in `projects.md` — this repo is a Python
   CLI + Slack service (`pyproject.toml`, `src/application_agent/`), not a deployed web
   app, so bug-error's "read Vercel production runtime logs" step has no target to check
   regardless of Linear access. Don't re-flag this as a separate blocker on the next run —
   bug-error should just report "nothing to check, no prod deployment" and move on, unless
   a Vercel project gets configured for this repo later.

### Not re-investigating (already tracked elsewhere)
- `agents/spec-drift.md` step 11 (preview-branch cleanup) has a separate, well-documented,
  structural blocker (missing `LINEAR_API_KEY` repo secret + proxy blocks `git push
  --delete` and the equivalent REST call) — see
  `handovers/preview-branch-cleanup-linear-api-key.md` (7 prior updates, root cause fully
  isolated). Nothing new to add there.
- `agents/spec-drift.md` step 12 (openspec archive sweep) operates on **AI-Workspace's own**
  `openspec/changes/`, not the target project's — out of scope for this handover and
  already reported clean in recent updates to the file above.

### Sweep ledger
Appending a run line to `data/sweep-runs.jsonl` for this run marked blocked (not `clean`,
since cleanliness was never actually checked) — see that file for the exact line.

## Instructions for receiving agent

1. Confirm the Linear MCP connector is authenticated for this account (claude.ai connector
   settings, not a CLI `claude mcp` flow — this session type can't run its own OAuth).
2. Once Linear tools are present, re-run `routines/idea-sweep.md` for **Application Agent**
   from the top: Issue Cap pre-flight first, then spec-drift → bug-error → market-feature.
3. Use the two `Open / Next` and Vercel-prod notes above as context, but still do the full
   Linear dedupe search yourself — don't file from this list without checking.
4. Delete this handover file once a full idea-sweep run for Application Agent completes
   successfully with Linear access.
