# Handover: idea-sweep routine for Usercon could not run — no Linear MCP tool access at all this session

**For:** Any agent/session with Linear MCP access
**From:** Claude Code idea-sweep run for Usercon (scheduled trigger), 2026-09-20
**Blocked by:** This session's tool list has no Linear MCP tools whatsoever — Linear is
listed as an MCP server that "requires authentication before its tools can be used," and
`ToolSearch` for "Linear" returns no matching deferred tools either. There is also no
`LINEAR_API_KEY` in the shell environment (`env | grep -i linear` empty). This is a
different, more severe blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (7 prior runs): those sessions had
working Linear MCP **read/search** access and only lacked a git-push/API-write path for
branch deletion. This session has **zero** Linear access of any kind — no `list_issues`,
no `search_issues`, no `create_issue`, no `create_comment`.
**Action:** Once Linear MCP (or a `LINEAR_API_KEY`) is available in an idea-sweep session,
re-run `idea-sweep` for Usercon from `routines/idea-sweep.md` step 0 onward. Nothing below
was completed — this is a clean restart, not a resume.
**Issue:** No specific Linear issue was driving this session — it was `idea-sweep`'s own
scheduled trigger for Usercon, not an issue assignment.

## What could not be done (entire routine, for Usercon)

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues` filtered by
  Usercon's Linear Project ID (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` per `projects.md`).
  Not checked. **Do not assume Usercon is under cap** — see the circumstantial evidence
  below suggesting it may already be at or over cap.
- **spec-drift steps 1–9** (gap-filing) — not run; also blocked downstream even if run,
  since dedupe search and `create_issue` both need Linear.
- **spec-drift step 10** (stale-issue sweep / comments on Backlog issues) — not run, needs
  Linear read + comment.
- **spec-drift step 11** (preview-branch housekeeping) — not attempted this run; already
  covered by the separate, extensively-documented `LINEAR_API_KEY` repo-secret blocker in
  `handovers/preview-branch-cleanup-linear-api-key.md` (7 consecutive failures as of
  2026-08-12). No new information to add there — don't re-verify it again.
- **spec-drift step 12** (OpenSpec archive sweep in AI-Workspace) — checked, does not need
  Linear. `openspec/changes/` in AI-Workspace currently has only the `archive/` subfolder,
  no active change folders — same clean-0 state as the 2026-08-12 update. Nothing to
  archive.
- **bug-error** (all steps) — not run. Also note: `projects.md` lists Usercon's Vercel Prod
  as `TBD`, so even with Linear access, this role has no known production URL/Vercel
  project to read runtime logs from yet — that's a separate gap worth flagging to Sharad
  when Linear access is restored.
- **market-feature** (all steps) — not run (needs Linear dedupe search + `create_issue`).

## Payload — groundwork for the receiving agent (read-only research, no Linear needed)

I read `openspec/project.md` and `openspec/specs/` in the Usercon repo
(`rohrasharad-ship-it/Usercon`) to save the next session a re-read:

- **Vision** (from `openspec/project.md`): Usercon is a user-owned context layer for AI
  agents — stores structured personal context, lets trusted agents (Claude, Codex) read
  and write it via MCP/OAuth so the user doesn't re-explain themselves. Explicitly **not**
  an acting agent (no shopping/food/health/travel).
- **8 specced capabilities**: context-graph, context-review, agent-api, context-usage-insights,
  context-receipt, drive-storage, mcp-oauth, settings-screen (plus mobile-shell, specced
  under an open change rather than `openspec/specs/`).
- **Out of scope** (never propose these for market-feature): built-in chatbot/LLM, native
  iOS/Android app, full permission dashboard, conflict/duplicate resolution workflow,
  payment/billing, browser clipboard flow, full manual questionnaire/onboarding, hard
  delete, custom life areas in v1.
- **Signal the Issue Cap check should weight heavily:** `openspec/changes/` in the Usercon
  repo currently has **~23 active (non-archived) change folders** (e.g. `sha-139-...`
  through `sha-243-...`, plus `portable-context-packet-export`), each named after what
  looks like a Linear issue ID. That volume of in-flight change folders is a strong signal
  this project may already be well over the 5-issue active-pipeline cap — the receiving
  agent should run the Issue Cap check **first** and expect it to likely skip straight to
  steps 10–11 (which are themselves separately blocked/already clean, per above).
- No codebase-vs-spec gap analysis was attempted beyond this — with cap likely already
  exceeded, spending session budget on step 1–9 candidate-finding before confirming cap
  status would likely be wasted work.

## Instructions for receiving agent

1. Confirm Linear MCP access works (`list_issues` for a known project).
2. Run the Issue Cap pre-flight for Usercon using Linear Project ID
   `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` (paginate, count Backlog/Todo/In Progress/In
   Review per `agents/shared/issue-cap.md`).
3. If at/over cap: skip spec-drift steps 1–9, bug-error, and market-feature. Still attempt
   spec-drift step 10 (stale-issue sweep) — that only needs Linear, which this session
   lacked but the receiving one should have.
4. If under cap: run the full routine per `routines/idea-sweep.md`, using the groundwork
   above to skip re-reading Usercon's `openspec/project.md`/`specs/` from scratch.
5. Flag to Sharad separately (not as a filed issue — this is infra, not product) that
   Usercon's Vercel Prod URL is still `TBD` in `projects.md`, so `bug-error` cannot run for
   this project until that's filled in.
6. Append the real sweep-ledger entry for this run once it completes (see
   `data/sweep-runs.jsonl` — I've appended a placeholder entry below marking this run
   blocked; replace it with real filed counts once the routine actually executes).
7. Delete this handover file once a Linear-capable session has completed the routine for
   Usercon (or confirmed it wasn't blocked).
