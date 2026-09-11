# Handover: idea-sweep routine for AI Workspace (PM OS) blocked — no Linear MCP access

**For:** Any agent/session with Linear MCP access authorized
**From:** idea-sweep routine orchestrator, scheduled run, 2026-09-11
**Blocked by:** Linear MCP server requires authorization in this session
(listed as "requires authentication before its tools can be used") and no
`LINEAR_API_KEY` is present in the environment. No Linear tools were
reachable via tool search, so no Linear read or write calls could be made.
**Action:** Re-run the `idea-sweep` routine for AI Workspace (PM OS) once
Linear MCP is authorized (claude.ai connector settings, or `claude mcp` /
`/mcp` in an interactive session).
**Issue:** N/A — this handover is not tied to a specific Linear issue; it
blocks the routine run itself before any issue could be created or read.

## Payload

Target project resolved from `projects.md`:
- **Project:** AI Workspace (PM OS)
- **Repo:** `rohrasharad-ship-it/AI-Workspace`
- **Linear Project:** PM OS
- **Linear Project ID:** `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`
- **Slack Channel:** #pm-ops (not used by this routine — Linear-only output)
- **Vercel Prod:** ai-workspace-blond.vercel.app (spec-preview sandbox)

Per `routines/idea-sweep.md`, this run should have:
1. Done the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Linear
   Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a` — **not done**, requires
   `list_issues` via Linear MCP.
2. If under cap, run `agents/spec-drift.md`, `agents/bug-error.md`,
   `agents/market-feature.md` in order — **none run**, all three need Linear
   MCP (search for dedupe, file issues, or both).
3. Run spec-drift steps 10–11 (stale-issue sweep, preview-branch
   housekeeping) even at cap — **not done**. Step 10 needs Linear MCP
   directly; step 11 (`scripts/cleanup-preview-branches.sh`) needs
   `LINEAR_API_KEY` for issue label/state lookup, also unavailable.
4. Append a sweep-ledger line to `data/sweep-runs.jsonl` — **skipped
   deliberately**: filed counts and the `clean` flag would be fabricated
   without having actually run the cap check or the three roles.

No codebase reading, spec-drift gap analysis, Vercel log review, or Linear
searching was attempted, since every downstream step in this routine
ultimately depends on Linear MCP (either to check the cap, dedupe, file, or
comment) — there was no partial work possible.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable (e.g. `list_issues`,
   `create_issue`, `search_issues` equivalents) or that `LINEAR_API_KEY` is
   set in the environment.
2. Re-run the routine from scratch: `routines/idea-sweep.md` for "AI
   Workspace" — do the Issue Cap pre-flight first, then the three roles (or
   just steps 10–11 if at cap).
3. Delete this handover file once that run completes (whether it files
   issues or finds nothing) — this file is the source of truth for the
   missed run until then.
4. Do not backfill a `data/sweep-runs.jsonl` entry for 2026-09-11 with
   invented counts; the next real run's own ledger line is sufficient.
