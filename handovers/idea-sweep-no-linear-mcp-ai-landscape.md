# Handover: idea-sweep routine for AI Landscape 2026 — blocked, no Linear MCP in session

**For:** Any agent/human who can confirm or restore Linear MCP connector access for scheduled idea-sweep sessions
**From:** idea-sweep routine run for AI Landscape 2026, 2026-09-13 (Claude Code, scheduled trigger)
**Blocked by:** The Linear MCP server was listed as requiring authentication in this session — no Linear tool of any kind was available (confirmed via tool search; only GitHub MCP tools resolved). This is a session-connector problem, not a code/repo problem.
**Action:** Reconnect/authorize the Linear MCP connector for whatever account or integration backs scheduled `idea-sweep` sessions (claude.ai connector settings, per the standard reauthorization flow), then either re-run this cycle's idea-sweep for AI Landscape manually or wait for the next scheduled firing.
**Issue:** None — this blocks before any Linear issue exists to link.

## Payload

`routines/idea-sweep.md` was followed for target project **AI Landscape 2026**
(repo `rohrasharad-ship-it/ai-landscape`, Linear Project ID
`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`). Prior runs in `data/sweep-runs.jsonl`
(2026-08-02 through 2026-08-15) show Linear MCP normally works for this
routine — this looks like a one-off session/connector issue, not a
structural regression, but it's worth confirming nothing changed on the
Linear-connector side for scheduled sessions specifically.

What could **not** run, in order:

1. **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs
   `list_issues` filtered by Linear Project ID. Not run.
2. **spec-drift steps 1–9** (gap-filing) — needs Linear search + issue
   creation. Not run.
3. **spec-drift step 10** (stale-issue sweep) — needs Linear issue listing +
   commenting. Not run.
4. **bug-error** (all steps) — needs Linear search + issue creation. Not run.
5. **market-feature** (all steps) — needs Linear search + issue creation. Not run.

What **did** run, without needing Linear:

- **spec-drift step 12** (OpenSpec archive housekeeping) — checked
  `openspec/changes/` in AI-Workspace directly via GitHub MCP: only the
  `archive/` subdirectory exists, no active (non-archived) change folders.
  Clean, nothing to archive this run.
- **spec-drift step 11** (preview-branch cleanup) — not attempted here. This
  has been a known, separately-documented blocker since 2026-08-02 (missing
  `LINEAR_API_KEY` repo secret — see
  `handovers/preview-branch-cleanup-linear-api-key.md`, 7 consecutive
  confirmations through 2026-08-12, which explicitly asks future sessions not
  to re-verify it again). Not re-verified here; same root cause class
  (missing Linear credential) but a distinct blocker from this handover
  (that one is a missing GitHub Actions secret for a shell script; this one
  is the Linear MCP connector itself being unauthenticated in a live
  session).

## Instructions for receiving agent

1. Confirm whether Linear MCP is expected to be available to scheduled
   `idea-sweep` sessions triggered this way, and if so, reauthorize it
   (claude.ai connector settings — this cannot be done from inside a
   non-interactive session).
2. Once Linear access is confirmed working, re-run `idea-sweep` for
   **AI Landscape 2026** — steps 1–10 above have not run yet for this cycle,
   so nothing has been skipped as "already checked," it's simply pending.
3. Do not duplicate `handovers/preview-branch-cleanup-linear-api-key.md` —
   that blocker is tracked separately and explicitly asks not to be
   re-verified every run.
4. Delete this handover file once a future idea-sweep run for AI Landscape
   confirms Linear MCP access works again.
