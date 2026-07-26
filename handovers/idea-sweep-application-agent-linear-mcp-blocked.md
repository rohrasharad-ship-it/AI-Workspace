# Handover: idea-sweep routine for Application Agent could not run — Linear MCP unauthenticated

**For:** Any agent/session with an authenticated Linear MCP connection
**From:** Scheduled `idea-sweep` routine run, Application Agent project, 2026-07-26
**Blocked by:** Linear MCP server requires OAuth authorization; this session is
non-interactive (scheduled trigger) and cannot complete the authorization flow.
No `LINEAR_API_KEY` is set in the environment either, so there is no fallback
path for the script-based steps.
**Action:** Once Linear is authorized (via claude.ai connector settings or
`/mcp` in an interactive session), re-run: "Run the 'idea-sweep' routine for
Application Agent. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md
exactly."
**Issue:** none — this is a routine-level blocker, not tied to a single Linear issue.

## Payload

Per `routines/idea-sweep.md`, every step that could run before touching Linear
was blocked at the very first gate:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) requires
  `list_issues` against the Application Agent Linear Project ID
  (`7dc5202c-a586-4bed-b2d3-fba10f2dd913`) — not callable.
- **spec-drift** steps 1–9 (gap filing) need Linear search/create; step 10
  (stale-issue sweep) needs Linear issue read/comment; step 11
  (preview-branch cleanup script) needs `LINEAR_API_KEY` for label/state
  lookups — none available. Step 12 (OpenSpec archive sweep) doesn't need
  Linear, but running it in isolation, out of order, without also being able
  to act on anything it surfaces felt like busywork rather than routine
  compliance, so it was left for the actual sweep run.
- **bug-error**: also blocked on Linear for filing/dedup. Separately,
  `projects.md` lists Application Agent's Vercel Prod as `TBD` — there is no
  deployed URL yet, so there are no production runtime logs for this role to
  read regardless of Linear access.
- **market-feature**: also blocked on Linear for filing/dedup.

### What was done instead (read-only, no Linear needed)

Confirmed the repo is real and active: `openspec/project.md` and 6 specs
(`profile`, `generation`, `tracker`, `integrations`, `browser`, `orchestrator`)
exist, plus ~12 non-archived folders under `openspec/changes/` (e.g.
`cdp-fill-session`, `ats-screening-answers`, `slack-only-lead-ingestion`,
`company-context-brief`) suggesting active in-flight spec work. `src/application_agent/`
has matching top-level modules (`browser/`, `generation/`, `integrations/`,
`orchestrator/`, `profile/`, `tracker/`, plus `cli.py`, `models.py`). A real
spec-drift pass (specced-vs-built, line-level) was **not** done — it would be
wasted effort without the ability to dedupe against existing Linear issues or
file anything found, and re-reading everything again once Linear is back
online is cheap relative to guessing now and risking stale/duplicate findings.

## Instructions for receiving agent

1. Confirm Linear MCP is authenticated (a simple `list_issues` call against
   the Application Agent project ID above should succeed).
2. Re-run the idea-sweep routine for Application Agent from scratch, following
   `routines/idea-sweep.md` exactly — start at the Issue Cap pre-flight.
3. For bug-error specifically: check whether `projects.md`'s Vercel Prod entry
   for Application Agent is still `TBD`. If a prod URL now exists, update
   `projects.md` first; if it's still TBD, bug-error has nothing to read and
   should report "clean, nothing filed" for that reason rather than skip
   silently.
4. Delete this handover file once a real idea-sweep run has completed for
   this project (per `agents/shared/conventions.md` — handovers are deleted
   only once the blocked work is fully complete and tracked elsewhere).
5. Do not assume the read-only notes above are a substitute for steps 1–3 of
   spec-drift/market-feature — they are orientation only, not a completed gap
   analysis.
