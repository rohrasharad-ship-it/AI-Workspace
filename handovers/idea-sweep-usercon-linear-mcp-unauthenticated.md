# Handover: idea-sweep routine for Usercon could not run — no Linear MCP access this session

**For:** Any agent/session with an authenticated Linear MCP connector
**From:** Scheduled `idea-sweep` routine trigger, Usercon, 2026-09-14 (Claude Code, non-interactive scheduled session)
**Blocked by:** No Linear MCP tools available at all this session. The runtime's own tool listing flagged Linear explicitly: *"The following MCP servers require authentication before their tools can be used: Linear"* and *"This session is non-interactive, so Claude cannot run the OAuth flow here."* No `mcp__Linear__*` tool appeared anywhere in this session's tool set (deferred or otherwise), so there was no `list_issues`, `search`, `create_issue`, or `comment` call available — not a rate limit, not a wrong-project-ID pitfall (`agents/shared/issue-cap.md`), a genuine absent connector authorization for this session.
**Action:** Once Linear MCP is authorized for a session (via claude.ai connector settings, per the runtime's own guidance), run `routines/idea-sweep.md` for Usercon from step 0 — nothing from this run can be reused since no reads happened.
**Issue:** N/A — this block happened before any Linear read, so there is no specific issue to link.

## Payload

This is a routine-level blocker, not a single-issue one, so the usual `<ISSUE-ID>-<slug>` handover naming (`agents/shared/conventions.md`) doesn't quite fit — using a routine+project slug instead since nothing in this run reached a specific Linear issue.

Nothing in `routines/idea-sweep.md` could execute:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) needs `list_issues` — unavailable.
- **spec-drift** steps 1–9 need Linear search + `save_issue`; step 10 (stale-issue sweep) needs to read/comment on existing issues; step 11 (preview-branch housekeeping) needs `LINEAR_API_KEY` for the cleanup script, which is a separate, already-documented, still-unresolved blocker — see `handovers/preview-branch-cleanup-linear-api-key.md` (7 consecutive prior runs hit that one; this session couldn't even get that far since step 0 already failed).
- **bug-error** needs Linear search + `save_issue`, plus a Vercel prod URL for Usercon — `projects.md` currently lists Usercon's Vercel Prod as `TBD`, so this role is doubly blocked for this project regardless of Linear.
- **market-feature** needs Linear search + `save_issue`.

No openspec-vs-codebase reading, no Vercel log reading, and no Playwright screenshotting was attempted, since none of it could lead anywhere without Linear to file into or dedupe against — doing that work now and discarding it seemed worse than flagging the real blocker plainly, per `agents/shared/conventions.md`'s "hard tool-access wall" definition (uncertainty isn't the trigger; definitive unavailability is, and this was definitive from the very first line of the session).

## Instructions for receiving agent

1. Confirm Linear MCP tools are present in your session's tool set before starting (a quick `list_projects` or equivalent works as a smoke test).
2. Run `routines/idea-sweep.md` for **Usercon** from the top, including the Issue Cap pre-flight.
3. Also check whether `projects.md`'s Usercon Vercel Prod row is still `TBD` — if a prod URL now exists, update that row so bug-error can run; if it's still TBD, bug-error stays skipped for Usercon (not a new blocker, just missing infra) and only spec-drift + market-feature apply.
4. Delete this handover file once a session with working Linear access has completed a real idea-sweep run for Usercon (the ledger entry in `data/sweep-runs.jsonl` for that run is the confirmation).
