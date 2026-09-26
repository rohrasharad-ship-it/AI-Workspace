# Handover: idea-sweep for Application Agent could not run — Linear MCP not connected in this session

**For:** Any agent session with working Linear MCP access (or Sharad, to authorize the
Linear connector for scheduled/cloud sessions)
**From:** Claude Code cloud session, `idea-sweep` routine run for Application Agent, 2026-09-26
**Blocked by:** No Linear MCP tools exist in this session at all. A tool search for
Linear-related tools (`list_issues`, `create_issue`, `search_issues`, etc.) returned zero
Linear tools, and the session's own tool listing explicitly states: "The following MCP
servers require authentication before their tools can be used: Linear" and "This session is
non-interactive, so Claude cannot run the OAuth flow here." This is a different failure mode
than the `LINEAR_API_KEY` shell-script gap already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one only blocks step 11's cleanup
script and still assumes Linear MCP itself works for steps 1–10; this session has neither).
**Action:** Authorize/connect the Linear MCP connector for this account so scheduled cloud
sessions carry it (via claude.ai connector settings), or re-run this routine from a session
that already has Linear MCP connected (prior sessions referenced in
`handovers/preview-branch-cleanup-linear-api-key.md`, e.g. the 2026-08-08 and 2026-08-12
updates, explicitly used working Linear MCP — so this is intermittent/session-dependent, not
a permanent platform limitation).
**Issue:** N/A — this run was triggered by the `idea-sweep` routine
(`routines/idea-sweep.md`), not by an assigned Linear issue.

## Payload

Per `routines/README.md` step 2, the target project resolved cleanly from `projects.md`:

| Field | Value |
|---|---|
| Project | Application Agent |
| Repo | `rohrasharad-ship-it/Application-Agent` |
| Linear Project | Application Agent |
| Linear Project ID | `7dc5202c-a586-4bed-b2d3-fba10f2dd913` |
| Slack Channel | #application-agent (not used — idea-sweep is Linear-only, no Slack output) |
| Vercel Prod | **TBD** in `projects.md` — even with Linear restored, bug-error (step 1: "read
Vercel production runtime logs") cannot run for this project until a prod URL/deployment is
filled in. This is a second, independent gap worth fixing at the same time. |

**Everything that could not run this cycle, entirely because of the missing Linear MCP:**

1. **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — requires `list_issues`
   filtered by the Linear Project ID above. Could not determine whether Application Agent is
   at/over the 5-issue active-pipeline cap.
2. **spec-drift steps 1–9** (gap-filing) — requires Linear search (dedupe) and issue
   creation/comment. Not attempted since project's cap status is unknown and Linear write
   access doesn't exist anyway. (Read-only prep — `openspec/project.md` and
   `openspec/specs/` in `rohrasharad-ship-it/Application-Agent` — was not fetched either,
   since there is no way to act on any findings this cycle.)
3. **spec-drift step 10** (stale-issue sweep) — requires listing/reading Backlog issues and
   posting comments. Not run.
4. **spec-drift steps 11–12** (preview-branch + OpenSpec archive housekeeping in
   AI-Workspace) — these are independent of the Application Agent project specifically and
   already have a long-running, well-documented blocker in
   `handovers/preview-branch-cleanup-linear-api-key.md` (missing `LINEAR_API_KEY` repo
   secret + a proxy that blocks `git push --delete`/ref-delete REST calls). This session
   additionally has no shell git/gh access for GitHub operations (session instructions
   require GitHub MCP tools only), so it could not attempt the scripts directly even if the
   secret existed. No new information to add to that file — see it for full history and the
   still-unresolved fix (add the `LINEAR_API_KEY` repo secret).
5. **bug-error steps 1–8** — blocked by both the missing Linear MCP (cap check, search,
   create, comment) and the missing Vercel prod URL for this project (step 1 has nothing to
   read).
6. **market-feature steps 1–9** — blocked by the missing Linear MCP (cap check, search,
   create, comment).

**Sweep ledger:** deliberately **not** appended to `data/sweep-runs.jsonl` for this run. A
`"clean": true` entry would misrepresent this as "all three roles ran and found nothing,"
when in fact none of them ran at all. Logging a false clean sweep would also suppress a
real signal (this project hasn't had a working idea-sweep pass) the next time someone reviews
`/routine-log.html`.

## Instructions for receiving agent

1. Confirm Linear MCP tools are present in your session (a quick `list_issues` call against
   the Application Agent Linear Project ID above is enough).
2. If confirmed working, run the full `idea-sweep` routine for Application Agent from
   scratch per `routines/idea-sweep.md` — this handover did no filing, so there is nothing to
   reconcile, just start clean at the Issue Cap pre-flight.
3. Separately, flag to Sharad that Application Agent's `Vercel Prod` cell in `projects.md`
   is still `TBD` — bug-error can't do anything for this project until that's filled in with
   a real deployment URL.
4. Delete this handover file once a session with working Linear MCP has successfully run
   (or attempted) the routine for Application Agent — this file's only job is to make sure
   this cycle's skip isn't silent.
