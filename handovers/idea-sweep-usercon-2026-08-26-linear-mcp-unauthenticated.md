# Handover: idea-sweep for Usercon could not run — Linear connector unauthenticated in this session

**For:** Any agent/session with a working, authenticated Linear MCP connection
**From:** idea-sweep routine (orchestrator), triggered for Usercon, 2026-08-26
**Blocked by:** The Linear MCP server is listed as requiring authentication in this
non-interactive session ("This session is non-interactive, so Claude cannot run the
OAuth flow here"). No Linear tool of any kind was available — not `list_issues`,
not `list_projects`, not comment/create/search. This is a session-level connector
auth gap, not the already-known-and-documented `LINEAR_API_KEY` repo-secret gap
(see `handovers/preview-branch-cleanup-linear-api-key.md` — that one blocks the
*scripted* housekeeping path; this one blocks the *MCP tool* path that every
idea-generation role and the Issue Cap pre-flight depend on).
**Action:** Re-authorize the Linear connector for whatever account/integration runs
scheduled idea-sweep sessions (claude.ai connector settings, or `claude mcp` /
`/mcp` in an interactive session per this session's own instructions), then
re-run the idea-sweep routine for Usercon.

## Payload

Per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`, the Issue Cap
pre-flight (mandatory before any idea-generation role can file issues) requires
`list_issues` filtered by Usercon's Linear Project ID
(`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` from `projects.md`). With zero Linear
tool access, that check could not run, which meant:

- **spec-drift** (`agents/spec-drift.md`): steps 0–9 (gap-filing) blocked at
  step 0; step 10 (stale-issue sweep) blocked — needs `list_issues` +
  comment-reading + posting comments.
- **bug-error** (`agents/bug-error.md`): blocked at step 0. (Also worth noting:
  Usercon's Vercel Prod entry in `projects.md` is still `TBD`, so even with
  Linear access this role would have had no production logs to read this run.)
- **market-feature** (`agents/market-feature.md`): blocked at step 0.

**What I did do without Linear access**, since it didn't require it:
- Read `openspec/project.md`, `openspec/specs/*` (7 spec areas: agent-api,
  context-graph, context-receipt, context-review, context-usage-insights,
  drive-storage, mcp-oauth, settings-screen), `PRD.md`, `NEXT.md`, and
  `HANDOFF.md` from the Usercon repo to understand current product state.
  Usercon is a mature, actively-developed project — `openspec/changes/`
  currently has **24 active (non-archived) change folders**
  (`sha-74` through `sha-243`, plus `portable-context-packet-export`), which
  strongly implies Usercon's Linear backlog already has well more than 5
  active pipeline issues. Under the Issue Cap rule this project would very
  likely have been **at or over cap anyway** even with working Linear access —
  so I deliberately did **not** draft speculative candidate issues for a human
  to file blind; doing so without dedupe-search against ~24+ known in-flight
  items would be more likely to create duplicates than real signal.
- Step 12 (OpenSpec archive housekeeping, runs in **this** repo,
  AI-Workspace, not Usercon): checked `openspec/changes/` here — only an
  `archive/` folder exists, no active change folders. Nothing to archive.
  Clean 0, not a new blocker.
- Step 11 (preview-branch cleanup): still blocked by the pre-existing,
  well-documented `LINEAR_API_KEY` repo-secret gap — see
  `handovers/preview-branch-cleanup-linear-api-key.md` for the full history
  (7 prior runs, same wall). I added a short update there rather than
  re-deriving the branch classification, since I have no Linear access this
  run to verify it either.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable this session (try `list_projects`).
2. Re-run `routines/idea-sweep.md` for Usercon from the top — this handover
   does not carry any candidate issues to file; there is no shortcut to take
   here, just re-run the routine normally.
3. If the cap check shows Usercon at/over 5 active issues (likely, per the
   24-active-openspec-changes signal above), skip straight to spec-drift
   steps 10–11 per the routine's own pre-flight rule.
4. Delete this handover file once a session with working Linear access has
   either completed a normal idea-sweep run for Usercon, or confirmed the cap
   is genuinely under 5 and a full run isn't warranted for another reason.

## Ledger

Logged this run in `data/sweep-runs.jsonl` as blocked (not a genuine clean
sweep — see that entry's `blocked`/`reason` fields). Did not run
`node scripts/generate-routine-log.mjs` (no `LINEAR_API_KEY` in this session
either, same as the already-documented gap).
