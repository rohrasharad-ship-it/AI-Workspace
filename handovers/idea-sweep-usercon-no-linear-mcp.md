# Handover: idea-sweep routine for Usercon could not run — no Linear MCP access this session

**For:** Any agent/human who can confirm Linear connector auth for this account, or a future idea-sweep session with working Linear MCP access
**From:** idea-sweep routine run for Usercon (Claude Code, cloud session), 2026-09-24
**Blocked by:** This session had **no Linear MCP tools available at all** — `ToolSearch` for any `mcp__Linear__*` tool (e.g. `list_issues`, `create_issue`) returned no matches, and the session's own tool listing flagged `Linear` under "MCP servers require authentication before their tools can be used," with an explicit note that a non-interactive session cannot run the OAuth flow. No `LINEAR_API_KEY` was present as a shell env var either (checked via `env | grep -i linear` — empty).
**Action:** Complete (or re-complete) Linear connector authorization for this account (via claude.ai connector settings, since this is a non-interactive session and cannot do it here), then re-run `idea-sweep` for Usercon. No code or config change is needed in this repo for the Linear-MCP side of this specific blocker.
**Issue:** None — this is a routine trigger, not an issue-driven session, so there is no Linear issue to link.

## Payload

Per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`, every step of idea-sweep
for a single project needs Linear MCP:

- **Issue Cap pre-flight** (must run once before any role) — needs `list_issues` filtered
  by Usercon's Linear Project ID (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` per `projects.md`).
  Could not run.
- **spec-drift steps 1–9** (gap-filing) — needs Linear search for dedupe + issue creation.
  Could not run.
- **spec-drift step 10** (stale-issue sweep) — needs `list_issues` + reading/posting
  comments on existing Backlog issues. Could not run.
- **bug-error** (all steps) — needs Linear search + issue creation. Could not run.
- **market-feature** (all steps) — needs Linear search + issue creation. Could not run.

This is **distinct** from the already-tracked blocker in
`handovers/preview-branch-cleanup-linear-api-key.md` (7+ prior runs): those sessions *did*
have working Linear MCP access and paginated hundreds of real issues — they were blocked
only on the shell script's `LINEAR_API_KEY` env var (for `cleanup-preview-branches.sh`) and
on a proxy that blocks git ref deletion. This session couldn't reach that point at all,
because there was no Linear access of any kind, MCP or shell key.

**Checked independently, not blocked (informational only):**
- `openspec/changes/` in this repo (AI-Workspace) currently has only an `archive/`
  subdirectory — no active (non-archived) change folders. Step 12 (OpenSpec archive
  housekeeping) would be a clean 0 even with tooling available, consistent with every prior
  run's report since 2026-08-12. Not re-running the script since it depends on the same
  environment as everything else here and has nothing to do regardless.
- Step 11 (preview-branch housekeeping) was not attempted this run — it depends on the
  same missing Linear access (for issue label/state lookup) documented exhaustively in
  `handovers/preview-branch-cleanup-linear-api-key.md`; re-attempting it here would add no
  new information.

**Not updated this run:** `data/sweep-runs.jsonl`. That ledger's schema (`filed`,
`clean`) represents a completed run's actual findings — logging `{"filed":{"bugs":0,
"features":0},"clean":true}` here would misrepresent a fully blocked run as a verified-clean
one. Leaving it out rather than recording a false "clean" entry.

## Instructions for receiving agent

1. Confirm whether the Linear connector for this account is authorized (claude.ai connector
   settings — this cannot be done from inside a non-interactive session).
2. Once confirmed working, re-run: "Run the idea-sweep routine for Usercon. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly." A fresh run will redo
   the Issue Cap pre-flight and all three roles from scratch — nothing from this session
   needs replaying, since nothing could execute.
3. Delete this handover file once a subsequent idea-sweep run for any project confirms
   Linear MCP tools are reachable in a fresh session (i.e. once this is confirmed to be a
   one-off session/auth gap, not a recurring pattern like the LINEAR_API_KEY issue).
4. Do not conflate this with `handovers/preview-branch-cleanup-linear-api-key.md` — that
   one needs a repo secret added; this one needs connector auth, a different fix in a
   different place.
