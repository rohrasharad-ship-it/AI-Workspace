# Handover: idea-sweep session has no Linear MCP tools at all

**For:** Any agent/human who can restore Linear MCP access for scheduled idea-sweep sessions, or Sharad directly
**From:** idea-sweep routine run for Resume Website, Claude Code (web/scheduled trigger), 2026-08-28
**Blocked by:** This session's toolset has no Linear MCP server connected — not even read-only. `ToolSearch` for any Linear-related tool (list_issues, create_issue, search_issues, comments, etc.) returns nothing; the session's own system reminder explicitly lists `Linear` under "MCP servers require authentication before their tools can be used" and states this is a non-interactive session that cannot run the OAuth flow.
**Action:** Re-authorize the Linear MCP connector for whatever account/environment runs scheduled `idea-sweep` triggers (claude.ai connector settings, per the session's own guidance), so future scheduled runs have working Linear access again.
**Issue:** none — this is a routine-triggered session, not an issue-driven one.

## Payload

This is a **new, more severe** blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`. That file documents prior
sessions having working Linear MCP (able to do the Issue Cap check, search,
create issues, comment) but lacking the separate `LINEAR_API_KEY` env var
needed only by the `cleanup-preview-branches.sh` shell script. This session has
neither — no Linear MCP tools of any kind, and no `LINEAR_API_KEY` env var
either (checked directly: unset).

Effect on this run (`idea-sweep` for **Resume Website**, single-project
trigger):

- **Step 0 (Issue Cap pre-flight)** — could not run. `list_issues` filtered by
  the Resume Website Linear Project ID (`b01a99ac-46a3-4b00-9139-31e00fae781d`
  per `projects.md`) is a Linear MCP call; no such tool exists in this
  session's toolset.
- **spec-drift steps 1–9, bug-error, market-feature** — all skipped. Every one
  of these requires searching Linear before proposing/filing (dedupe) and
  filing requires `create_issue`/`save_issue`, neither available.
- **spec-drift step 10 (stale-issue sweep)** — skipped. This step normally
  runs even when a project is at the issue cap (cap only blocks *new* filing),
  but it still needs Linear reads (list open issues, read comments, post a
  comment) which are unavailable here. This is the part that's new relative
  to a normal at-cap skip: past at-cap runs (see git log, e.g. Resume Website
  2026-08-05) always still completed the stale-issue sweep. This run could
  not.
- **spec-drift step 11 (preview-branch cleanup)** — already known-blocked on
  missing `LINEAR_API_KEY`, unrelated to this session's own toolset; see the
  existing handover. Did not re-verify the proxy-level git-push block — that
  file's 2026-08-12 update already says re-verifying wastes tokens with no
  new information, and nothing about this run changes that finding.
- **spec-drift step 12 (openspec archive housekeeping)** — ran. `openspec/changes/`
  in AI-Workspace currently contains only the `archive/` directory, no active
  (non-archived) change folders, so there was nothing to archive. Clean 0,
  not a new blocker (this step doesn't touch Linear).

No Linear issues were searched, created, or commented on this run. No
Resume Website content was assessed for gaps/bugs/feature ideas, since doing
that research without being able to check the issue cap or dedupe against
existing Linear issues risks producing candidates that duplicate what's
already tracked or ignore an already-full backlog.

## Instructions for receiving agent

1. Confirm whether Linear MCP is supposed to be connected for the
   account/environment that runs scheduled `idea-sweep` triggers. If it was
   working through at least 2026-08-19 (see git log — AI Workspace (PM OS)
   run that day did complete a real stale-issue sweep) and is now entirely
   absent, something in the connector authorization lapsed or was
   reconfigured — check claude.ai connector settings for the Linear
   connector's status.
2. Once Linear MCP access is confirmed working again, just let the next
   scheduled `idea-sweep` trigger for Resume Website run normally — no
   backlog of specific findings to replay from this handover, since none
   were produced.
3. Delete this file once a subsequent `idea-sweep` run (any project) confirms
   Linear MCP tools are reachable again.
