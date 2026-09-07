# Handover: idea-sweep could not run — Linear MCP unauthenticated this session

**For:** Any agent/session confirmed to have a working, authenticated Linear MCP connection
**From:** idea-sweep routine (orchestrating session, Claude Code scheduled run), triggered for Application Agent, 2026-09-07
**Blocked by:** The Linear MCP server is present in this session's tool roster but requires
OAuth authorization that a non-interactive scheduled session cannot perform — no
`mcp__Linear__*` tool schema is loadable at all this run (confirmed via a tool search: only
GitHub/Slack/Vercel tools matched issue/comment-related queries, zero Linear results). This
is a different, more fundamental blocker than the one tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (repeated across ~7 prior runs): that
file's sessions all had **working** Linear MCP tool calls (`list_issues`, label/status
reads) and were only blocked on the raw `LINEAR_API_KEY` env var needed by the *shell
scripts* (`cleanup-preview-branches.sh`, `generate-routine-log.mjs`) plus a proxy-level
block on git ref deletion. This session has neither Linear MCP access nor a
`LINEAR_API_KEY` env var (checked, unset), so **no step of any idea-generation role that
touches Linear could run** — not just housekeeping.
**Action:** Once a session with real Linear MCP access (or the `LINEAR_API_KEY` secret) picks
this up, run the full `idea-sweep` routine for **Application Agent** from scratch — nothing
below is pre-computed, because the Issue Cap pre-flight itself requires Linear and could not
be checked.
**Issue:** N/A — routine-level blocker, not tied to a single Linear issue.

## What could and could not run this session

| Step | Status |
|---|---|
| Issue Cap pre-flight (`agents/shared/issue-cap.md`) | **Blocked** — requires `list_issues` against Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`. Not run. Cap status for Application Agent is unknown as of this run. |
| spec-drift steps 1–9 (gap-filing) | **Blocked** — step 4 (dedupe search) and step 5 (file issue) both need Linear. Did not read `openspec/specs/` or the codebase for gap-finding either, since any candidate found could not be deduped or filed anyway (see note below on repo state). |
| spec-drift step 10 (stale-issue sweep) | **Blocked** — needs to list/comment on existing Linear issues. |
| spec-drift step 11 (preview-branch housekeeping) | **Blocked** — no `LINEAR_API_KEY`; also see the pre-existing, still-unresolved handover `handovers/preview-branch-cleanup-linear-api-key.md` for the separate git-ref-deletion proxy block that affects this step even when the key exists. |
| spec-drift step 12 (openspec archive sweep) | **Not attempted** — the script requires a local clone with `npx openspec`, `jq`, and `gh` CLI; this session has GitHub-MCP-only tooling per its own operating instructions (no `gh` CLI permitted) and no local checkout. Per `agents/shared/conventions.md`, this is also covered by a weekly scheduled GitHub Action in AI-Workspace as a structural backup, so it is not solely dependent on idea-sweep sessions. |
| bug-error (all steps) | **Blocked, and separately not applicable yet** — needs Linear for dedupe/filing (blocked), *and* `projects.md` lists Application Agent's Vercel Prod as `TBD`. Confirmed by reading the repo: Application Agent (`rohrasharad-ship-it/Application-Agent`) is a Python CLI/agent project (`pyproject.toml`, `src/application_agent/`, no web app, no Vercel config found) — there is currently no production deployment for this role to read runtime logs from. |
| market-feature steps 1–2 (read vision/specs) | Readable without Linear — see notes below. Steps 3+ (propose, dedupe, file) blocked. |

## Repo context gathered (for the receiving agent's head start)

Read via GitHub MCP, no Linear needed:

- `openspec/project.md` — not yet read in full this session (deprioritized once the Linear
  block made filing impossible either way); do this first on the next run.
- `openspec/specs/` has 6 spec areas: `browser`, `generation`, `integrations`,
  `orchestrator`, `profile`, `tracker` — matches the module breakdown in `README.md`.
- `openspec/changes/` currently has **13 active (non-archived) change folders** in flight:
  `ats-screening-answers`, `cdp-fill-session`, `company-context-brief`,
  `draft-quality-self-critique`, `event-blurb-generation`, `online-resume-website`,
  `portfolio-blurb-generation`, `profile-foundation-files`, `replace-capture-attachments`,
  `resume-file-export`, `resume-master-docx-export`, `save-flagged-screening-policy`,
  `slack-only-lead-ingestion`. This is an unusually large number of concurrent proposals —
  **the next spec-drift run should read all 13 before proposing new gaps**, since several
  plausible "missing feature" candidates (e.g. resume export, event blurbs, ATS screening)
  are very likely already covered by one of these in-flight changes and would be false
  positives for both spec-drift and market-feature.
- This project has no Vercel deployment (`projects.md` correctly lists `TBD`) — bug-error
  should be treated as structurally not-yet-applicable for Application Agent, not just
  blocked, until a prod deployment exists. Worth flagging to Sharad separately (not done
  here — that itself would require Linear or Slack, and this is out of scope for a
  tool-access handover).

## Instructions for receiving agent

1. Confirm Linear MCP actually works this session (e.g. a trivial `list_issues` call)
   before relying on anything else in this file.
2. Run the Issue Cap pre-flight for Application Agent fresh (Linear Project ID
   `7dc5202c-a586-4bed-b2d3-fba10f2dd913`) — nothing here assumes an answer.
3. If under cap, run spec-drift steps 1–9, bug-error (skip — no prod URL exists; do not
   invent one), and market-feature per their own files, reading all 13 in-flight
   `openspec/changes/` entries first to avoid duplicate proposals.
4. Backfill `data/sweep-runs.jsonl` for this project/date with the real outcome once the
   role(s) actually run — the entry this session appended (`"blocked": true`) is a
   placeholder, not a clean-run result, and should not be mistaken for one.
5. Delete this handover file once a session has successfully completed a real
   Application Agent idea-sweep (cap check + all applicable roles), since its only job is
   to prevent the next session from assuming "clean" when nothing was actually checked.
