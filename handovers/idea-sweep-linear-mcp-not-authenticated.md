# Handover: idea-sweep routine blocked — Linear MCP not authenticated this session

**For:** Any agent/human who can authorize the Linear MCP connector, or a future session that has it already connected
**From:** idea-sweep routine run for Application Agent, 2026-08-26 (scheduled trigger, Claude Code non-interactive session)
**Blocked by:** The Linear MCP server was listed as requiring authentication ("Linear" under servers that need auth before their tools can be used), and this is a non-interactive scheduled session that cannot run an OAuth flow. Confirmed by searching the live tool list for Linear tools (query "linear issue create list search") — zero Linear tools returned, only GitHub/Slack/TaskCreate/WebSearch matches. No `LINEAR_API_KEY` env var is set either (checked via `env | grep -i linear`, empty).
**Action:** Authorize the Linear MCP connector for this account/session type (via `claude mcp` or `/mcp` in an interactive session, or the relevant connector settings), so future scheduled/automated idea-sweep runs actually have Linear access. This is a different, more severe blocker than the long-running `LINEAR_API_KEY` repo-secret issue tracked in `handovers/preview-branch-cleanup-linear-api-key.md` — that file covers only the shell-script housekeeping path (step 11) and assumes Linear MCP itself works, which it usually has in prior runs (see the `list_issues`/search usage documented in that file's update history). This run had **no Linear access of any kind**, MCP or raw API key.
**Issue:** N/A — this is a routine-trigger-level blocker, not a single Linear issue. No Linear issue could be created to track it (that's the whole problem), so it's filed here instead.

## Payload

Trigger: `Run the "idea-sweep" routine for Application Agent. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`

Project resolved from `projects.md`: **Application Agent**, repo
`rohrasharad-ship-it/Application-Agent`, Linear Project ID
`7dc5202c-a586-4bed-b2d3-fba10f2dd913`, Slack `#application-agent`, Vercel Prod
`TBD` (no production deployment registered yet, which would have also blocked
`agents/bug-error.md` step 1 — no runtime logs to read — even if Linear had
worked).

Every step of `routines/idea-sweep.md` that touches Linear was blocked before
it could run:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — needs
  `list_issues` filtered by Linear Project ID. Could not run at all, so it's
  unknown whether Application Agent is at/over the 5-issue active-pipeline cap.
- **`agents/spec-drift.md` steps 1–9** (gap-filing) — needs Linear search +
  create. Blocked.
- **`agents/spec-drift.md` step 10** (stale-issue sweep) — needs `list_issues`
  + comment. Blocked.
- **`agents/spec-drift.md` step 11** (preview-branch housekeeping) — needs
  Linear label/status lookups per branch. Blocked (also independently blocked
  by the missing `LINEAR_API_KEY` repo secret and the proxy's git-push-delete
  403, both already fully documented in
  `handovers/preview-branch-cleanup-linear-api-key.md` — no new information to
  add there this run since this session couldn't even reach the Linear lookup
  step to build a branch list).
- **`agents/spec-drift.md` step 12** (openspec archive sweep) — does **not**
  need Linear. Checked `rohrasharad-ship-it/AI-Workspace` `openspec/changes/`
  directly via GitHub MCP: only an `archive/` subfolder exists, no active
  change folders. Confirms the same "clean, nothing to archive" state noted in
  the 2026-08-08/08-12 updates to the preview-branch handover — not a new
  blocker, just still empty.
- **`agents/bug-error.md`** — needs Linear (cap check, search, create) and
  Vercel runtime logs. Blocked on both counts; Application Agent's
  `projects.md` row lists Vercel Prod as `TBD`, so there is no deployment to
  read logs from regardless of Linear access.
- **`agents/market-feature.md`** — needs Linear (cap check, search, create).
  Blocked.

Nothing was filed, searched, commented on, or archived this run. No Linear
issue existed for this trigger to comment on, so no in-Linear breadcrumb was
left — this file and the sweep ledger line below are the only record.

Logged `{"at":"2026-08-26T...","project":"Application Agent","filed":{"bugs":0,"features":0},"clean":false,"blocked":"linear-mcp-not-authenticated"}`
to `data/sweep-runs.jsonl` (extra `blocked` field kept alongside the normal
schema — distinguishes "checked and found nothing" from "could not check").
Did not run `node scripts/generate-routine-log.mjs` — it also requires
`LINEAR_API_KEY`, already a known-blocked path.

## Instructions for receiving agent

1. Get the Linear MCP connector authenticated for whatever session type runs
   scheduled `idea-sweep` triggers (this was a Claude Code non-interactive
   scheduled session).
2. Once confirmed working (e.g. a trivial `list_issues` call succeeds), re-run
   this trigger: `Run the "idea-sweep" routine for Application Agent. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`
3. Delete this handover file once a session with working Linear access
   confirms the connector is fine and completes a normal run for Application
   Agent (whether it files 0 or several issues — either outcome proves access
   works).
4. Do not treat this file as evidence the project is at/under the issue cap —
   that check never ran.
