# Handover: idea-sweep routine for Resume Website could not run — Linear MCP not authorized this session

**For:** Any agent/session with an authorized Linear MCP connection, or Sharad (to re-authorize the Linear connector)
**From:** Claude Code (scheduled `idea-sweep` trigger), 2026-09-12
**Blocked by:** The Linear MCP server is unauthenticated for this session (`This session is non-interactive, so Claude cannot run the OAuth flow here` — reauthorization must happen via claude.ai connector settings or `claude mcp`/`/mcp` in an interactive session). No `list_issues`, `create_issue`, `search_issues`, or comment tools were reachable at all — this is a deeper blocker than the previously-documented missing `LINEAR_API_KEY` repo secret (see `handovers/preview-branch-cleanup-linear-api-key.md`), which assumed working Linear MCP access for the agent itself and only lacked the key for the *shell script* run by step 11.
**Action:** Re-authorize the Linear connector for this account (or run the sweep from a session where it's already authorized), then re-run `idea-sweep` for **Resume Website**.
**Issue:** N/A — this is a routine trigger (`routines/idea-sweep.md`), not an issue-driven session. No Linear issue exists to comment on.

---

## Payload

Target project resolved from `projects.md`:

| Field | Value |
|---|---|
| Project | Resume Website |
| Repo | `rohrasharad-ship-it/resume-website` |
| Linear Project | Resume Website |
| Linear Project ID | `b01a99ac-46a3-4b00-9139-31e00fae781d` |
| Prod URL | `meet-sharad.vercel.app` |

`routines/idea-sweep.md` requires, in order, per project: an Issue Cap
pre-flight (`agents/shared/issue-cap.md`, needs `list_issues` filtered by the
Linear Project ID above), then `agents/spec-drift.md`,
`agents/bug-error.md`, `agents/market-feature.md` — every one of which
searches, creates, or comments on Linear issues as its core mechanism. With
zero Linear MCP tool access, **none of steps 0 through 10 across all three
roles could be attempted** — not "found nothing," but genuinely unable to
check the cap, search for dupes, file anything, or run the stale-issue
sweep.

**Step 11 (preview-branch cleanup)** — separately still blocked per the
standing handover at `handovers/preview-branch-cleanup-linear-api-key.md`
(no `LINEAR_API_KEY` repo secret; 7+ consecutive prior runs confirmed this).
Also newly confirmed this run: no `LINEAR_API_KEY` env var is present in this
session's shell either (checked directly), and this session had no Linear
MCP tool to substitute for it, so the branch classification step couldn't
even be attempted this time (previous sessions could at least classify
branches via Linear MCP even without the script secret).

**Step 12 (openspec archive sweep)** — deliberately **not run** this
session, for a separate reason: `scripts/archive-merged-openspec-changes.sh`
shells out to `gh` to check whether a change still has an open PR
(`has_open_pr_for_change`), and this session has no `gh` CLI. Reading the
script, when `gh` is missing it prints a warning and returns non-zero from
that check, which the caller may read as "no open PR" — i.e. running it here
risked archiving an active change that still has an open PR, since the
safety check silently degrades instead of failing loudly. `resume-website`
currently has 7 non-archived folders under `openspec/changes/`
(`journey-chapter-scrubber`, `social-share-preview`, `suggested-prompt-chips`,
`save-contact-vcard`, `mobile-qa-pass`, `fix-mobile-voice-audio`,
`warmer-chatbot-avatar`) — did not check which, if any, are `complete` per
`npx openspec list --json`, since that's moot without the PR-check being
trustworthy. This is a clean skip, not a failure to resolve — the weekly
GitHub Action (`.github/workflows/openspec-archive.yml`) covers this as a
structural backup and runs with real `gh` access.

## Instructions for receiving agent

1. Confirm Linear MCP is authorized (try a trivial `list_issues` call scoped
   to the Resume Website Linear Project ID above).
2. Re-run `routines/idea-sweep.md` for Resume Website from the top: Issue Cap
   pre-flight, then spec-drift → bug-error → market-feature in order.
3. Once Linear MCP access is confirmed, also re-attempt spec-drift step 11
   for this project if the `LINEAR_API_KEY` repo secret has since been added
   (check `handovers/preview-branch-cleanup-linear-api-key.md` first — don't
   duplicate that investigation if it's still open).
4. Append the real sweep-runs.jsonl line for Resume Website once the roles
   actually run (this session logged a `"blocked"` line instead — see
   `data/sweep-runs.jsonl`, entry dated 2026-09-12 — not a real "clean" pass).
5. Delete this handover file once a real idea-sweep run for Resume Website
   has completed (or once Linear MCP is confirmed working and a fresh run is
   in progress, whichever the receiving agent judges is the actual
   resolution).
