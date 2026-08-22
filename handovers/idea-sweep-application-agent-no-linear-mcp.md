# Handover: idea-sweep routine (Application Agent) could not run — Linear MCP unauthenticated this session

**For:** Any agent/session with working Linear MCP access
**From:** Claude Code, scheduled `idea-sweep` trigger for Application Agent, 2026-08-22
**Blocked by:** The Linear MCP server was reported by the harness as requiring authentication ("These servers require authentication before their tools can be used: Linear") — a non-interactive/scheduled session cannot run the OAuth flow to clear this. No Linear tools of any kind were available; this is not the already-tracked `LINEAR_API_KEY`-for-scripts issue (see `handovers/preview-branch-cleanup-linear-api-key.md`) — that one affects only the housekeeping shell script's env var, while this session had **zero** Linear MCP tool access for anything (search, create, comment, list_issues).
**Action:** Re-run the `idea-sweep` routine for **Application Agent** (`routines/idea-sweep.md`) from a session where the Linear connector is authorized, or have Sharad authorize the Linear connector for scheduled/cloud sessions so this doesn't recur on every scheduled firing.
**Issue:** No Linear issue could be created or referenced to link this handover — that's exactly what's blocked.

## What could and couldn't run this session

Followed `routines/idea-sweep.md` exactly, resolving **Application Agent** against
`projects.md` (repo `rohrasharad-ship-it/Application-Agent`, Linear Project ID
`7dc5202c-a586-4bed-b2d3-fba10f2dd913`, Vercel Prod `TBD`).

| Step | Status |
|---|---|
| Issue Cap pre-flight (`agents/shared/issue-cap.md`) | **Blocked** — needs `list_issues` via Linear MCP; unavailable |
| spec-drift steps 1–9 (gap-filing) | **Blocked** — needs Linear search + `save_issue` |
| bug-error steps 1–8 (bug-filing) | **Blocked** — same |
| market-feature steps 1–9 (feature-filing) | **Blocked** — same |
| spec-drift step 10 (stale-issue sweep) | **Blocked** — needs `list_issues` + comment-posting via Linear MCP |
| spec-drift step 11 (preview-branch cleanup, AI-Workspace-wide) | **Not attempted** — already confirmed blocked 7 consecutive prior runs by the missing `LINEAR_API_KEY` repo secret and a proxy that rejects mutating git/REST calls (see `handovers/preview-branch-cleanup-linear-api-key.md`); re-attempting would add no new information |
| spec-drift step 12 (OpenSpec archive housekeeping, AI-Workspace-wide) | **Ran** — `openspec/changes/` in AI-Workspace contains only the `archive/` folder, no active change folders. Clean 0, consistent with every prior run's report. |

Because **nothing could be checked or filed** (not even a cap count), no
`data/sweep-runs.jsonl` line was appended — the ledger's `"clean": true` shape
means "checked, found nothing," which would misrepresent what actually
happened ("could not check at all"). Do not infer from a missing ledger entry
that this cycle was skipped for capacity reasons; it wasn't a cap skip, it was
a total tool-access block.

## Instructions for receiving agent

1. Confirm Linear MCP tools are available in your session (try `list_issues`
   against the Application Agent project ID above).
2. Re-run `idea-sweep` for **Application Agent** per `routines/idea-sweep.md`
   from the top, including the Issue Cap pre-flight — do not assume this
   session's partial step-12 result needs to be redone (it doesn't), but do
   redo everything Linear-dependent since none of it ran.
3. If Linear MCP is still unavailable, do not create a duplicate handover for
   the same root cause — update this file with a new dated section instead
   (matching the pattern in `handovers/preview-branch-cleanup-linear-api-key.md`).
4. Once a run completes successfully (or confirms clean), this handover file
   can be deleted.
