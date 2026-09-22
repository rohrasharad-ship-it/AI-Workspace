# Handover: idea-sweep for AI Workspace (PM OS) blocked — no Linear MCP in this session at all

**For:** Any agent/human who can authorize the Linear MCP connector for this account, or who has a session with working Linear MCP access
**From:** idea-sweep routine run for AI Workspace (PM OS), triggered 2026-09-22
**Blocked by:** This cloud session has **no Linear MCP tool registered at all** — not a missing API key, the connector itself is unauthorized. A tool search for "Linear" returned no matching deferred tools, and the environment explicitly states the Linear MCP server "require[s] authentication before their tools can be used" and that OAuth cannot run in a non-interactive session.
**Action:** Authorize the Linear MCP connector for this account (via claude.ai connector settings, or `claude mcp` / `/mcp` in an interactive session), then re-run `idea-sweep` for AI Workspace (PM OS): `Run the "idea-sweep" routine for AI Workspace. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`
**Issue:** none — this run never reached the point of resolving/creating a Linear issue.

## Why this is a new/different blocker than the existing LINEAR_API_KEY handover

`handovers/preview-branch-cleanup-linear-api-key.md` documents 7 prior consecutive hits
where **Linear MCP tool access worked fine** (`list_issues` paginated across the whole
workspace successfully) but the *shell script* `scripts/cleanup-preview-branches.sh` (and
`scripts/generate-routine-log.mjs`) failed because they call the Linear GraphQL API
directly and need `LINEAR_API_KEY` as a raw env var, which was never set as a repo/session
secret.

This run is different and more severe: **there is no Linear MCP tool at all** in this
session's toolset. That blocks everything routines/idea-sweep.md needs from Linear, not
just the two shell scripts:

- `routines/README.md` Issue Cap pre-flight (`list_issues` by Linear Project ID) — cannot run
- `agents/spec-drift.md` steps 1–9 (search Linear, file gap issues) — cannot run
- `agents/spec-drift.md` step 10 (stale-issue sweep: list + read comments on open issues) — cannot run
- `agents/bug-error.md` and `agents/market-feature.md` (both search Linear first, then file) — cannot run

Only the two steps that never touch Linear MCP (they use `LINEAR_API_KEY` directly, or
nothing) were attempted, with these results:

- **Step 11 (preview-branch cleanup):** still blocked — `LINEAR_API_KEY` env var not set
  in this session either, so `scripts/cleanup-preview-branches.sh --dry-run` fails
  immediately with `error: LINEAR_API_KEY is required` (8th consecutive independent hit;
  see the other handover file for full branch-classification history — nothing to add,
  I couldn't re-verify it without Linear access this run).
- **Step 12 (openspec archive sweep):** ran successfully, no Linear needed.
  `npx openspec list --json` shows zero active (non-archived) changes, so
  `bash scripts/archive-merged-openspec-changes.sh --sweep --dry-run` reported "no
  completed active changes" — clean 0, matching the state noted in prior handover
  updates.
- `node scripts/generate-routine-log.mjs` also still fails with the same
  `LINEAR_API_KEY is required` error — the routine-log dashboard (`/routine-log.html`)
  is stale as of this run and could not be refreshed.

## Payload

Nothing to file, comment, or clean up this run — the blocker is total for every
Linear-dependent step. `projects.md` resolves AI Workspace (PM OS) to Linear Project ID
`3703a715-c49d-4b9e-b6f1-5975d3ebe39a` for whoever picks this up.

## Instructions for receiving agent

1. Get Linear MCP authorized for the session that will pick this up (connector settings,
   or `/mcp` interactively) — this alone unblocks the Issue Cap check, spec-drift 1–10,
   bug-error, and market-feature.
2. Separately (unrelated fix, tracked in the other handover file): add the
   `LINEAR_API_KEY` repository secret so `preview-branch-cleanup.yml`,
   `scripts/cleanup-preview-branches.sh`, and `scripts/generate-routine-log.mjs` stop
   failing. Do not assume fixing Linear MCP auth also sets this env var — they are
   different credentials.
3. Once Linear MCP works, re-run: `Run the "idea-sweep" routine for AI Workspace. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`
4. Delete this handover file once a full idea-sweep run for AI Workspace (PM OS)
   completes end to end (issue cap check + all three roles ran, one way or another).
