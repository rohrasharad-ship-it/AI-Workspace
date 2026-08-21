# Handover: idea-sweep routine for Resume Website could not run — Linear MCP not authenticated this session

**For:** Any agent/human who can authorize the Linear MCP connector for this account
**From:** idea-sweep routine run for Resume Website, 2026-08-21 (scheduled trigger)
**Blocked by:** No Linear MCP tools were exposed to this session at all. The session's own
tool-availability notice states: "The following MCP servers require authentication before
their tools can be used: Linear" and "This session is non-interactive, so Claude cannot run
the OAuth flow here." Unlike the prior `preview-branch-cleanup-linear-api-key.md` handover
(where Linear MCP *worked* but the `LINEAR_API_KEY` shell secret didn't), this session had
**zero** Linear tool calls available — no `list_issues`, no `create_issue`, no
`search_issues`, no comment tools, nothing.
**Action:** Authorize the Linear connector for this account (claude.ai → Settings →
Connectors, or reconnect via whatever surface manages this session's MCP auth), then re-run
this routine for Resume Website.

## Payload

Every step of `routines/idea-sweep.md` for a single project needs Linear MCP at some point:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues` filtered by
  Resume Website's Linear Project ID (`b01a99ac-46a3-4b00-9139-31e00fae781d`). Could not run,
  so I don't know whether Resume Website is at/over the 5-issue cap.
- **spec-drift steps 1–9** (gap-filing) — needs Linear search before filing. Blocked.
- **spec-drift step 10** (stale-issue sweep) — needs `list_issues` + reading comments. Blocked.
- **spec-drift step 11** (preview-branch housekeeping) — needs Linear label/status lookup
  (also independently blocked by the still-open `LINEAR_API_KEY` repo-secret issue in
  `handovers/preview-branch-cleanup-linear-api-key.md` — two separate blockers stacked here).
- **spec-drift step 12** (openspec archive housekeeping) — this one does **not** need
  Linear, so I checked it anyway: `openspec/changes/` in AI-Workspace has no active
  (non-archived) folders right now, so this is a genuine clean 0, not a blocked step.
- **bug-error** (all steps) — needs Linear search + cap check before filing. Blocked.
- **market-feature** (all steps) — needs Linear search + cap check before filing. Blocked.

I did **not** write a `data/sweep-runs.jsonl` ledger line for this run. Every existing line
in that file records `"clean": true` for runs that actually checked Linear and found
nothing — writing a `"clean": true` line here would misrepresent a run that couldn't check
anything as one that checked and found it clean. Leaving the ledger silent on this run seemed
more honest than inventing a schema field; happy to be overruled if a `"blocked": true` field
gets added to the schema later.

I also did not attempt any Vercel log reads, GitHub reads, or Playwright screenshots for
bug-error/market-feature, since even a perfectly-scoped issue draft would have nowhere to go
(no cap check possible, no dedupe search possible, no `create_issue` call possible) — spending
budget building an issue that can't be filed or checked against the cap seemed like the wrong
tradeoff versus just reporting the blocker plainly.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually callable in a fresh session (e.g. a trivial
   `list_issues` against Resume Website's project ID above).
2. Re-run `routines/idea-sweep.md` for Resume Website from scratch — nothing from this
   session can be resumed or cached, since no Linear reads happened at all.
3. Once a run completes normally (with or without filed issues), append the correct
   `data/sweep-runs.jsonl` line for that run per the routine's own instructions, and delete
   this handover file.
4. If Linear MCP is confirmed working but the *cap check* itself finds Resume Website at or
   over 5 active issues, that's expected routine behavior (see `agents/shared/issue-cap.md`)
   — not a reason to reopen this handover.
