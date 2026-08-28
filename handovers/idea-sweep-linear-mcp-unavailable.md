# Handover: idea-sweep routine could not run for Usercon — Linear MCP not connected in this session

**For:** Sharad Rohra (connector authorization), or any future agent session that does have Linear MCP access
**From:** idea-sweep routine run, Claude Code (claude.ai scheduled trigger), 2026-08-28, targeting Usercon
**Blocked by:** The Linear MCP server is not authorized/connected for this session at all — every Linear tool (`list_issues`, `create_issue`, `search_issues`, comment/attachment tools) is unavailable, not just missing. This session's own tool inventory explicitly lists Linear under "MCP servers require authentication before their tools can be used" and states OAuth cannot be completed in a non-interactive session.
**Action:** Authorize/connect the Linear connector for this environment (claude.ai → connector settings), or run idea-sweep for Usercon again from a session that already has Linear MCP connected.
**Issue:** none — no Linear issue could be created or referenced, since Linear was unreachable for the entire run.

---

## Payload

`routines/idea-sweep.md` was triggered for **Usercon** only (single-project run). Per
`routines/README.md`, the mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`)
must run before any of the three idea-generation roles can file. That pre-flight itself
calls `list_issues` — which requires Linear MCP. With Linear entirely unavailable, none of
the following could run for Usercon this cycle:

- **Issue Cap pre-flight** — could not count active pipeline issues.
- **spec-drift steps 1–9** (gap-filing) — blocked; also step 4 dedupe search needs Linear.
- **spec-drift step 10** (stale-issue sweep) — blocked; needs to list/read/comment on
  open Backlog issues.
- **bug-error** — blocked; needs Linear search + issue creation (separately, Usercon's
  Vercel Prod URL is still listed as `TBD` in `projects.md`, so this role has no runtime
  logs to read for Usercon regardless of Linear — a second, unrelated gap worth closing
  when someone sets up Usercon's Vercel deployment).
- **market-feature** — blocked; needs Linear search + issue creation.

**This is a different, more fundamental blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`.** That file documents prior sessions
that *did* have working Linear MCP (used to search/create/comment/paginate issues) but
lacked the raw `LINEAR_API_KEY` env var needed by `scripts/cleanup-preview-branches.sh`
(step 11) and hit a proxy 403 on `git push --delete`. This session has neither — Linear
MCP itself is not connected, so nothing in steps 0–10 could execute for any role. Given
that pre-existing handover is already extensively verified (7 consecutive independent
confirmations through 2026-08-12, explicitly noting no further re-verification is needed),
this session did not re-run or re-verify step 11/12 housekeeping — same root fix
(`LINEAR_API_KEY` repo secret) applies there; see that file for the full branch list.

No research toward candidate spec-drift/bug-error/market-feature issues was attempted
this run: every role's guardrails require searching Linear first to skip anything already
tracked (`routines/README.md` shared guardrails, "Search Linear first — skip anything
already tracked"). Generating candidate issues without the ability to dedupe against
Usercon's existing Backlog risks re-proposing something already filed, so none were
drafted — nothing to hand off there beyond this blocker itself.

## Instructions for receiving agent / human

1. **Root fix:** authorize the Linear connector for whichever environment runs scheduled
   `idea-sweep` triggers (claude.ai → connector settings, per this session's own guidance —
   not something an agent session can do for itself).
2. Once Linear MCP is connected, re-run: `Run the "idea-sweep" routine for Usercon. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.` — nothing about the
   routine itself needs to change, only connector access.
3. Separately (not blocking, lower priority): Usercon's `Vercel Prod` cell in
   `projects.md` is `TBD`. If/when Usercon has a production deployment, fill it in so the
   bug-error role has runtime logs to read.
4. Delete this handover file once a Linear-connected session confirms idea-sweep runs
   end-to-end for Usercon again.
