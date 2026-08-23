# Handover: idea-sweep (AI Landscape 2026) blocked — no Linear MCP this session

**For:** Any agent with Linear MCP access
**From:** Claude Code cloud session, idea-sweep routine run, 2026-08-23
**Blocked by:** Linear MCP server unavailable — this session's Linear connector
requires an interactive OAuth authorization that a non-interactive/scheduled
session cannot perform. No `LINEAR_API_KEY` was present in the environment
either, so the `agents/shared/issue-cap.md` fallback (direct API call) and the
`cleanup-preview-branches.sh` / `generate-routine-log.mjs` scripts (which also
need `LINEAR_API_KEY`) were equally unavailable.
**Action:** Re-run the `idea-sweep` routine for **AI Landscape 2026** from a
session that has working Linear MCP access (or `LINEAR_API_KEY`), following
`routines/idea-sweep.md` exactly.
**Issue:** N/A — this handover blocks the routine's own Issue Cap pre-flight,
before any issue exists to link.

---

## Payload

Trigger that fired this session:

```
Run the "idea-sweep" routine for AI landscape
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

Target project (resolved from `projects.md`):

| Field | Value |
|---|---|
| Project | AI Landscape 2026 |
| Repo | rohrasharad-ship-it/ai-landscape |
| Linear Project | AI Landscape |
| Linear Project ID | `4ef7d096-f5bb-44f4-bac5-417e4488cdb8` |
| Slack Channel | #ai-landscape (not used by this routine) |
| Prod URL | https://rohrasharad-ship-it.github.io/ai-landscape/ |

**What did not run, and why:**

1. **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — could not call
   `list_issues` against the Linear Project ID above. Cap status for this
   project this cycle is **unknown**, not confirmed clean.
2. **spec-drift steps 1–9** (gap-filing) — skipped; gated on the cap check
   above and on Linear search/create access, neither available.
3. **spec-drift step 10** (stale-issue sweep / comments) — skipped; needs
   Linear MCP to list/read/comment on issues.
4. **spec-drift step 11** (preview-branch cleanup) — skipped; the cleanup
   script requires `LINEAR_API_KEY`, not present in this session's
   environment.
5. **spec-drift step 12** (OpenSpec archive sweep) — **not attempted** this
   run. This step doesn't need Linear, but it commits directly against
   AI-Workspace `main`-adjacent history and a weekly GitHub Action
   (`.github/workflows/openspec-archive.yml`) already covers it as a
   structural backup — skipped in favor of not making an unreviewed push from
   a session that has no way to verify Linear-side state for the rest of the
   run anyway.
6. **bug-error** and **market-feature** — skipped entirely; both gate on the
   same Issue Cap check and both need Linear to search-before-create and file.

Nothing in this session touched `rohrasharad-ship-it/ai-landscape` — no repo
read, no screenshots, no OpenSpec read. The blocker hit before any of that
would have mattered (cap check is step 0, before all substantive work).

## Instructions for receiving agent

1. Confirm Linear MCP is connected (or `LINEAR_API_KEY` is set) in your
   session before starting.
2. Run the Issue Cap pre-flight for **AI Landscape 2026** using Linear Project
   ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8` per `agents/shared/issue-cap.md`.
3. If under cap, run `agents/spec-drift.md`, `agents/bug-error.md`, and
   `agents/market-feature.md` in full against this project, per
   `routines/idea-sweep.md`.
4. Append the sweep-runs.jsonl ledger line for this project once the run
   actually completes (see `routines/idea-sweep.md` Output section) — the
   line this session appended (same date) records the block, not a
   completed run; don't treat it as this cycle's real result.
5. Delete this handover file once a real run for AI Landscape 2026 has
   completed for this cycle.
