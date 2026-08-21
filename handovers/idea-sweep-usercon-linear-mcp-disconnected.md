# Handover: idea-sweep routine for Usercon could not run — Linear MCP tools never loaded this session

**For:** Any agent/human who can confirm or restore Linear MCP connectivity for this account's sessions
**From:** idea-sweep routine run for Usercon (Claude Code, scheduled trigger), 2026-08-21
**Blocked by:** No `mcp__Linear__*` tools were exposed in this session at any point, despite Linear being listed as a "connecting" MCP server at session start. `ListConnectors` confirms the Linear connector is installed and `enabledInChat: true` (`installState: "unknown"`) — so this is a runtime connection failure, not a missing/disabled integration. Every step of `routines/idea-sweep.md` (issue-cap pre-flight, dedupe search, `create_issue`, comments, spec-drift's stale-issue sweep) requires Linear MCP, so nothing in the routine's actual output — no issue filing, no cap check, no stale-issue comments — could execute.
**Action:** Retry the `idea-sweep` routine for Usercon once `mcp__Linear__*` tools are confirmed present (check via a tool search before starting any role). If this recurs across sessions, the Linear connector's OAuth/session state likely needs a human to re-authorize it in claude.ai connector settings.
**Issue:** N/A — this run was routine-triggered (`idea-sweep` cron), not driven by a specific Linear issue.

## Payload

- Read `routines/idea-sweep.md`, `routines/README.md`, and all three role files
  (`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`)
  plus their shared modules — routine understood correctly, this is a pure
  tool-access blocker, not a comprehension gap.
- Confirmed via `ToolSearch` (multiple queries: `"Linear list_issues create issue"`,
  `"+linear create_issue"`, `"select:mcp__Linear__create_issue,..."`, bare `"Linear"`)
  that zero Linear-prefixed tools exist in this session's toolset.
- This is notable because **prior idea-sweep sessions for Usercon did have working
  Linear MCP** — see the 2026-08-08 and 2026-08-12 updates in
  `handovers/preview-branch-cleanup-linear-api-key.md`, which used `list_issues`
  and issue status lookups successfully. So this is a session-specific/transient
  connection failure, not a structural change to the project.
- Per `projects.md`, Usercon's Vercel Prod is currently `TBD` (no deployed URL) —
  independent of the Linear blocker, the bug-error role has no production
  target to read logs from yet. Worth fixing in `projects.md` once Usercon has
  a live deployment, but not something this session could act on either way.
- Did **not** attempt housekeeping steps 11–12 (preview-branch cleanup,
  OpenSpec archive sweep) — those are already exhaustively documented as
  blocked by a missing `LINEAR_API_KEY` repo secret *and* a proxy-level block
  on mutating git operations, confirmed independently across 7 prior sessions
  in `handovers/preview-branch-cleanup-linear-api-key.md`. That handover's own
  2026-08-12 update says re-verifying wastes tokens with no new information —
  deferring to it rather than repeating the probe.
- Did **not** write a sweep-ledger line to `data/sweep-runs.jsonl` — the ledger
  schema only has `filed` counts and `clean: true/false` (roles ran and found
  nothing), neither of which honestly describes "roles could not run at all."
  Fabricating a `clean: true` entry would misrepresent this run as a completed
  sweep. Leave the ledger untouched; the next successful run's entry should be
  the authoritative record for this cycle instead.

## Instructions for receiving agent

1. Before running any idea-generation role, verify `mcp__Linear__*` tools are
   actually loaded (e.g. `ToolSearch` for `"Linear list_issues"`) — do not
   assume the connector being "connecting" at session start means it will
   resolve.
2. If tools are present: run `idea-sweep` for Usercon fresh per
   `routines/idea-sweep.md` — issue-cap pre-flight, then spec-drift →
   bug-error → market-feature, single-project (file directly, no grouping
   needed).
3. If tools are still absent: do not retry the probing already done here —
   this file already confirms it's a connectivity issue, not a config one.
   Flag to Sharad that the Linear connector may need re-authorization.
4. Delete this handover once a session successfully completes an idea-sweep
   run for Usercon with working Linear MCP access.
