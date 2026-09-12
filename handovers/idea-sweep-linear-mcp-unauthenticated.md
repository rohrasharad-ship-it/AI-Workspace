# Handover: idea-sweep routine cannot run — Linear MCP connector unauthenticated in this session

**For:** Sharad Rohra (connector re-auth) or any agent session confirmed to have working Linear MCP access
**From:** Claude Code idea-sweep run for Application Agent, 2026-09-12
**Blocked by:** The Linear MCP server is listed as requiring authentication in this session ("MCP servers require authentication before their tools can be used: Linear") — no Linear tool schemas are available at all, not even read-only ones like `list_issues`.
**Action:** Re-authorize the Linear connector for Claude Code sessions (claude.ai → Settings → Connectors → Linear, or `/mcp` in an interactive session), then re-run the `idea-sweep` routine for Application Agent (and any other projects that fired on the same schedule while this was broken).

---

## Payload

Triggered task: `Run the "idea-sweep" routine for Application Agent`, following
`routines/idea-sweep.md` exactly.

This blocker is upstream of everything in `routines/idea-sweep.md` and all
three role files — every one of them requires Linear MCP:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) needs `list_issues`
  filtered by Linear Project ID to count active pipeline issues. Could not run
  — so it's unknown whether Application Agent (Linear Project ID
  `7dc5202c-a586-4bed-b2d3-fba10f2dd913`) is at or under the 5-issue cap.
- **spec-drift** steps 4–5 (dedupe search + file), step 8 (comment), and step
  10 (stale-issue sweep — list + comment) all need Linear MCP.
- **bug-error** steps 3–4 (dedupe search + file) and step 7 (comment) need
  Linear MCP. (Separately, Application Agent's Vercel Prod URL is listed as
  `TBD` in `projects.md`, so this role would have had nothing to check even
  with Linear access — that's a pre-existing gap, not part of this blocker.)
- **market-feature** steps 4–5 (dedupe search + file) and step 8 (comment)
  need Linear MCP.

So this run did **not** file any issues, comment on any existing issues, or
determine cap status for Application Agent — not because nothing was found,
but because the check could not be performed at all. This is different from a
"clean" run (see `data/sweep-runs.jsonl` convention) and no `clean: true` line
was appended for this run, to avoid implying the roles actually looked and
found nothing.

**What I could still do without Linear**, since it was self-contained:

- `agents/spec-drift.md` step 12 (OpenSpec archive housekeeping, AI-Workspace,
  independent of Linear): `openspec/changes/` in this repo currently contains
  only the `archive/` folder — zero active change folders — so there was
  nothing to archive regardless of tooling. (The `npx openspec` CLI itself
  also failed to resolve in this session's environment — `npm error could not
  determine executable to run` — but it's moot here since there's nothing to
  archive either way.)
- `agents/spec-drift.md` step 11 (preview-branch cleanup): still blocked
  independently by the missing `LINEAR_API_KEY` repo secret — see
  `handovers/preview-branch-cleanup-linear-api-key.md` for the full history
  (7 consecutive prior confirmations, including that the network proxy blocks
  mutating git/GitHub-API calls even when a valid `GITHUB_TOKEN` is present).
  That is a separate, already-tracked blocker from this one and doesn't need
  re-verification here.

## Instructions for receiving agent

1. Confirm Linear MCP tools (e.g. `list_issues`, `create_issue`) are actually
   callable in a fresh session before assuming this is fixed — a connector
   can show as "connected" in settings but still fail per-session.
2. Re-run `idea-sweep` for **Application Agent** specifically (this run
   produced no output for that project — not even a `clean` sweep-runs.jsonl
   line).
3. Check whether any other scheduled `idea-sweep` firings landed in this same
   window (other projects) and re-run those too if they hit the same wall —
   worth a quick check of `data/sweep-runs.jsonl` for a gap starting around
   2026-08-19 (the last recorded entry before this run) through today.
4. Once a run completes normally, append its `data/sweep-runs.jsonl` line per
   the routine spec — do not backfill one for this run, since no roles
   actually executed.
5. Delete this handover file once a subsequent `idea-sweep` run confirms
   Linear MCP works end-to-end (cap check + search + file/comment all
   succeed).
