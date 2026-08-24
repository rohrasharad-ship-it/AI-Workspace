# Handover: idea-sweep routine has no Linear MCP access in this session — entire routine blocked

**For:** Any agent/human who can either (a) re-authorize the Linear connector for
scheduled/headless Claude Code sessions, or (b) pick up this run's idea-sweep
work once Linear access is restored
**From:** Claude Code (scheduled `idea-sweep` trigger, session started
non-interactively), run for **Resume Website**, 2026-08-24
**Blocked by:** The Linear MCP connector is installed and enabled for this
session (`ListConnectors` reports `installState: "unknown"`, `enabledInChat:
true`, `isAuthless: false`) but no Linear tools (`mcp__Linear__*`) ever
surfaced via `ToolSearch`. The system reminder for this session states
explicitly: *"This session is non-interactive, so Claude cannot run the OAuth
flow here... these servers need to be authorized... via claude.ai connector
settings."* Linear is OAuth/interactively-authenticated, and this run is a
scheduled (cron-triggered) session with no human present to complete that
flow.
**Action:** Re-authorize the Linear connector so it survives scheduled/cron
session starts (claude.ai → Settings → Connectors → Linear → reconnect, or
confirm whatever token Linear's connector uses has a refresh path that works
headlessly) — then re-run `idea-sweep` for Resume Website (and any other
project whose scheduled run landed in the same window) to actually do the
work described below.

---

## Why this is a new/distinct blocker (not the same as the known `LINEAR_API_KEY` issue)

`handovers/preview-branch-cleanup-linear-api-key.md` already tracks 7
consecutive runs blocked because `scripts/cleanup-preview-branches.sh` (step
11) and `scripts/generate-routine-log.mjs` need a **`LINEAR_API_KEY` env var /
repo secret** for direct Linear REST calls from a shell script. That blocker
is still live (confirmed again this run — no `LINEAR_API_KEY` in this
session's environment either) and doesn't need a new file; see the update I
added there.

This handover is about something upstream and more severe: **this session had
no Linear MCP tools at all**, not even the `list_issues`/search/create/comment
calls that every prior idea-sweep session (Cursor and Claude Code alike) used
successfully. Every one of those prior sessions' handovers assumes Linear MCP
*works* and only shell-script/git-push paths are blocked. This run, none of
the Linear-dependent steps could even start:

- **Step 0 (Issue Cap pre-flight)** — needs `list_issues` filtered by Linear
  Project ID. Could not run.
- **spec-drift steps 4–9** (dedupe search, create issues, comment) — all
  Linear MCP calls. Could not run.
- **bug-error steps 3–7** — same. Could not run.
- **market-feature steps 4–8** — same. Could not run.
- **spec-drift step 10 (stale-issue sweep)** — needs `list_issues` +
  read/post comments. Could not run.
- **spec-drift step 11 (preview-branch cleanup)** — separately blocked by
  missing `LINEAR_API_KEY` (see above); would also need Linear MCP or the API
  key either way.
- **spec-drift step 12 (openspec archive sweep)** — the one step that doesn't
  need Linear. I ran the check: `openspec/changes/` in AI-Workspace currently
  has no active (non-archived) folders, so this is a clean 0, not a new
  blocker.

In short: **zero issue-cap checking, zero dedupe search, zero issue creation,
zero comments** were possible this run, for Resume Website or (if the same
schedule fired for other projects) any other project. This is a total outage
of the routine's actual output, not a partial degradation.

## What I did instead

1. Read `routines/idea-sweep.md`, `routines/README.md`,
   `agents/shared/issue-cap.md`, `agents/spec-drift.md`, `agents/bug-error.md`,
   `agents/market-feature.md`, and `agents/shared/conventions.md` in full.
2. Confirmed via `ToolSearch` that no `mcp__Linear__*` tools exist in this
   session's toolset (GitHub MCP, Slack MCP, and Vercel MCP tools did load).
3. Confirmed via `ListConnectors` that the Linear connector is installed and
   `enabledInChat: true` at the account level, but its auth state is
   `"unknown"` — consistent with the OAuth-token-not-available-headlessly
   explanation above, not a project misconfiguration.
4. Checked for a `LINEAR_API_KEY` env var as a fallback path for at least the
   housekeeping scripts — not set.
5. Ran the one step that doesn't require Linear (step 12, openspec archive
   sweep, in AI-Workspace) — clean, nothing to archive.
6. Did **not** attempt any gap-finding/log-reading/feature-brainstorming work
   for Resume Website (spec-drift step 1–3, bug-error step 1–2, market-feature
   step 1–3 are Linear-independent reads) because doing that analysis without
   being able to run the Issue Cap check or dedupe search first would risk
   producing candidate issues that either exceed the cap or duplicate
   something already tracked — and I'd have nowhere safe to file the results
   anyway (this isn't a multi-project run, so there's no grouping-candidate
   ledger to append to per `agents/shared/cross-project-grouping.md`).
7. Did **not** write a `data/sweep-runs.jsonl` entry for this run — the ledger
   schema (`filed`, `clean`) represents "roles ran and found N (or 0)", which
   would misrepresent what happened. A run that never started is not the same
   as a clean run.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable in a fresh session (interactive or
   scheduled) before doing anything else — try `list_issues` against the
   Resume Website Linear Project ID (`b01a99ac-46a3-4b00-9139-31e00fae781d`
   from `projects.md`).
2. If reachable, re-run `idea-sweep` for Resume Website from scratch per
   `routines/idea-sweep.md` — do not assume anything from this aborted run;
   nothing was cached or partially filed.
3. If still unreachable, escalate the connector-auth question to Sharad
   directly rather than writing another handover — this is a session/account
   configuration issue, not something any agent session can self-serve fix
   from inside the sandbox.
4. Delete this file once a scheduled idea-sweep run completes successfully
   with real Linear MCP access (confirms the fix held).
