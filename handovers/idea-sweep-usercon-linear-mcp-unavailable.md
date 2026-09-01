# Handover: idea-sweep for Usercon could not run — Linear MCP tool not connected at all this session

**For:** Any agent/human that can authorize the Linear connector for this account, or a future session where Linear MCP tools are actually loaded
**From:** idea-sweep routine run for Usercon (Claude Code, scheduled trigger), 2026-09-01
**Blocked by:** No Linear MCP tools are available in this session at all — not a missing-secret issue like the shell-script blocker below, but the connector itself. The session's own tool-availability notice states: "The following MCP servers require authentication before their tools can be used: Linear" and "this session is non-interactive, so Claude cannot run the OAuth flow here." A live `ToolSearch` for `list_issues`/`create_issue`/any Linear tool returned zero Linear results (GitHub and Slack tools only).
**Action:** Authorize the Linear connector for this account (per claude.ai Settings → Connectors, or however this org's Linear MCP server is configured), then re-run `idea-sweep` for Usercon. No other fix is possible from inside a session — every step below needs a live Linear MCP call.
**Issue:** No Linear issue could be created or referenced for this handover itself, for the same reason it exists — no Linear MCP access this run.

## Payload

`routines/idea-sweep.md` was read in full, along with `routines/README.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`,
`agents/shared/issue-cap.md`, and `agents/shared/conventions.md`. Every one of
the three idea-generation roles' first real step needs a working Linear MCP
call:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`, gates all three
  roles) needs `list_issues` filtered by Usercon's Linear Project ID
  (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` per `projects.md`) — could not run.
- **spec-drift** steps 4–9 (dedupe search, file, comment) and step 10
  (stale-issue sweep — list + comment on open issues) — could not run.
- **bug-error** steps 3–7 (dedupe search, file, comment) — could not run.
  (Also would have needed Vercel prod logs, not attempted since it's moot
  without Linear to file into or dedupe against.)
- **market-feature** steps 4–8 (dedupe search, file, comment) — could not run.
- **spec-drift step 11** (preview-branch cleanup) is *separately* already
  blocked, independent of this — see
  `handovers/preview-branch-cleanup-linear-api-key.md` (missing
  `LINEAR_API_KEY` repo secret for the script, plus a proxy that blocks
  `git push --delete`/ref-delete REST calls, confirmed across 7 prior runs).
  That file's fix (add the repo secret) does not fix *this* blocker — this
  one is the interactive Linear MCP connector for the session itself, not the
  Action's secret.
- **spec-drift step 12** (OpenSpec archive sweep) does **not** need Linear —
  checked manually via GitHub MCP: `openspec/changes/` in AI-Workspace
  currently contains only `archive/`, no active change folders. Clean 0,
  consistent with every recent handover update. No action needed.

No Linear search, cap check, issue creation, or comment happened this run —
none of the "nothing found" bullets below are genuine sweep results, they are
"could not check." I did not write a `clean: true` entry to
`data/sweep-runs.jsonl` for this reason: that field means a real sweep ran and
found nothing, and a false `clean` entry would hide this blocker from the
`/routine-log.html` dashboard and make Usercon look up to date when it has
not actually been swept.

## Instructions for receiving agent

1. Get the Linear connector authorized for this account (a human step —
   claude.ai Settings → Connectors, or the org's MCP config; not something an
   agent session can self-serve).
2. Once Linear MCP tools are loaded (verify with a trivial call like
   `list_issues` against Usercon's project ID), re-run
   `routines/idea-sweep.md` for Usercon from the top — Issue Cap pre-flight,
   then all three roles.
3. This handover file's job is done once a real idea-sweep run for Usercon
   completes (filed issues or a genuine `clean: true`) — delete it then.
4. Do not treat the absence of a `sweep-runs.jsonl` entry for this date as
   "nothing to do" — it means the run was blocked, not clean.
