# Handover: idea-sweep for Application Agent could not run — Linear MCP not authorized this session

**For:** Any agent/human who can authorize the Linear connector for this Claude Code account (claude.ai → Settings → Connectors), or who has a working Linear MCP session
**From:** idea-sweep routine run (scheduled), Application Agent, 2026-09-10
**Blocked by:** The Linear MCP server is listed by the harness as "requires authentication before its tools can be used" — no Linear tool (`list_issues`, `search_issues`, `create_issue`, comment tools, etc.) is callable at all this session. This is a session/account authorization gap, not the previously-documented `LINEAR_API_KEY` shell-script issue (see `handovers/preview-branch-cleanup-linear-api-key.md`, which is about a missing repo secret for the GitHub Action / cleanup script and is a separate, narrower problem).
**Action:** Authorize the Linear connector for this account (claude.ai Settings → Connectors → Linear), then re-run the `idea-sweep` routine for Application Agent from scratch — nothing from this run can be reused since no reading, searching, or filing against Linear happened.
**Issue:** none — this run never got far enough to touch a specific Linear issue.

## Payload

`routines/idea-sweep.md` requires, before anything else, a mandatory per-project **Issue
Cap pre-flight** (`agents/shared/issue-cap.md`) via `list_issues` filtered by the Linear
Project ID (`7dc5202c-a586-4bed-b2d3-fba10f2dd913` for Application Agent). With zero Linear
tool access, this pre-flight cannot run, which blocks every downstream step for all three
roles:

- **spec-drift** (`agents/spec-drift.md`) steps 1–9 need Linear search (dedupe) and issue
  creation; step 10 (stale-issue sweep) needs to list and comment on open issues. None of
  this is possible. Steps 11–12 (preview-branch cleanup / OpenSpec archive housekeeping)
  are AI-Workspace-wide, not Application-Agent-specific, and are already tracked as blocked
  by a different, narrower cause in `handovers/preview-branch-cleanup-linear-api-key.md` —
  no need to re-attempt or re-document those here.
- **bug-error** (`agents/bug-error.md`) needs the cap check, then Linear search/create.
  Also independently blocked on its own: Application Agent's `Vercel Prod` field in
  `projects.md` is still `TBD`, so there is no production URL to pull runtime logs from
  even if Linear were available.
- **market-feature** (`agents/market-feature.md`) needs the cap check, then Linear
  search/create.

I confirmed (via Bash) there is no `LINEAR_API_KEY` or Vercel token available as a raw env
var in this session either, so there is no fallback path to hit the Linear API directly
outside the MCP tool. GitHub MCP access and general network egress both work fine (verified
`curl` to api.github.com succeeds) — this is specifically a Linear-connector authorization
gap for this session, nothing broader.

No OpenSpec/codebase reading was attempted for Application Agent this run either: without
Linear to dedupe-search or file against, reading the repo first would just be wasted
analysis that couldn't lead to any filed issue — better to hand that off cleanly than
produce gap-analysis that has to be redone anyway once Linear works.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually callable (e.g. a trivial `list_issues` call)
   before starting — don't assume authorization based on this file alone.
2. Re-run `idea-sweep` for Application Agent from `routines/idea-sweep.md` step 1
   (pre-flight cap check), in full — spec-drift, bug-error, market-feature.
3. `agents/bug-error.md` will still be blocked separately until Application Agent's Vercel
   prod URL is filled in in `projects.md` (currently `TBD`) — that's a pre-existing gap,
   not something this handover introduces.
4. Delete this file once a full idea-sweep run for Application Agent completes
   successfully end-to-end (or is confirmed clean).
