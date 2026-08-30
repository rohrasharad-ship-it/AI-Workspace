# Handover: idea-sweep routine for Resume Website could not run — no Linear tool access at all this session

**For:** Any agent/session with Linear MCP access
**From:** Claude Code (scheduled `idea-sweep` trigger), 2026-08-30
**Blocked by:** This session has zero Linear tooling — no Linear MCP tools appear in the tool list or via tool search (checked directly), no `LINEAR_API_KEY` env var (checked via `env | grep -i linear`, empty), and no other path to read/search/file/comment on Linear issues.
**Action:** Re-run the `idea-sweep` routine for Resume Website from a session that has Linear MCP connected (see `routines/idea-sweep.md`, `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`).
**Issue:** None — this run was triggered directly by the scheduled `idea-sweep` routine trigger, not by a Linear issue assignment, so there is no `<ISSUE-ID>` to reference.

## Payload

This is a stricter blocker than prior idea-sweep sessions have hit. Earlier
handovers in this directory (`preview-branch-cleanup-linear-api-key.md`,
`linear-issue-vercel-preview-blocker.md`) describe sessions that **did** have
working Linear MCP access but were missing a raw `LINEAR_API_KEY` env var (for
the shell-script path) or Linear MCP entirely (some cloud-agent sessions). This
session falls in the latter, more severe bucket: no Linear access of any kind,
so none of the following could run for Resume Website
(`rohrasharad-ship-it/resume-website`, Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`):

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — requires
  `list_issues` filtered by Linear Project ID. Could not run at all, so cap
  status for Resume Website is unknown from this session.
- **spec-drift steps 1–9** (gap-filing) — blocked (needs Linear search + create).
- **spec-drift step 10** (stale-issue sweep / comment-if-resolved) — blocked
  (needs to list + read + comment on open Backlog issues).
- **bug-error steps 1–8** — blocked (needs Linear search + create); note this
  session also did not attempt reading Vercel runtime logs, since filing would
  have been blocked regardless.
- **market-feature steps 1–9** — blocked (needs Linear search + create).
- **spec-drift step 11** (preview-branch housekeeping) — also blocked
  independently (no `LINEAR_API_KEY` for the script), but this is already
  extensively documented across 7 prior updates in
  `handovers/preview-branch-cleanup-linear-api-key.md`, which concluded the
  root cause is a proxy-level block on git-ref-deletion mutations (both
  git-over-HTTPS and the GitHub REST API) that can only be cleared by adding
  the `LINEAR_API_KEY` repo secret and letting the GitHub Action's own runner
  do the deletes. Not re-verified this run per that handover's own note that
  re-verifying wastes tokens with no new information — nothing here changes
  that conclusion.
- **spec-drift step 12** (OpenSpec archive sweep) — this one does **not**
  need Linear. Checked directly: `openspec/changes/` in AI-Workspace
  currently contains only the `archive/` directory, no active change
  folders, so this step is a clean 0 this run (consistent with every prior
  update's finding on this same question).

No `data/sweep-runs.jsonl` entry was appended for this run. That ledger
records "ran and found nothing" (`clean: true`) vs. "filed N issues" — neither
applies here, since the roles never got to run. Appending a `clean: true`
row would misrepresent a blocked run as a completed clean sweep.

## Instructions for receiving agent

1. Confirm Linear MCP tools are available in your session (e.g. via a tool
   search for "Linear" or "list_issues"/"create_issue"-style Linear tools).
2. Run the Issue Cap pre-flight for Resume Website
   (`agents/shared/issue-cap.md`, project ID
   `b01a99ac-46a3-4b00-9139-31e00fae781d`).
3. If under cap, run `agents/spec-drift.md`, `agents/bug-error.md`, and
   `agents/market-feature.md` in full against Resume Website per
   `routines/idea-sweep.md`. If at/over cap, run spec-drift steps 10–11 only.
4. Append the appropriate `data/sweep-runs.jsonl` line for the actual outcome
   of that run (see `routines/idea-sweep.md` Output section).
5. Delete this handover file once a session with real Linear access has
   successfully run (or explicitly attempted and re-documented) the sweep for
   Resume Website — until then it's the record of why this cycle produced no
   Linear activity.
6. Do not duplicate step 11 investigation — see
   `handovers/preview-branch-cleanup-linear-api-key.md` for the current,
   already-thorough state of that separate blocker.
