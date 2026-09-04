# Handover: idea-sweep routine for Application Agent could not run — no Linear MCP access in this session

**For:** Any agent/session with working Linear MCP access
**From:** Claude Code (scheduled `idea-sweep` trigger), Application Agent project, 2026-09-04
**Blocked by:** This session has zero Linear MCP tools available — the connector requires authorization the non-interactive scheduled session cannot grant (per this session's own tooling: "The following MCP servers require authentication before their tools can be used: Linear"). No `list_issues`, `search_issues`, `create_issue`, `add_comment`, or any other Linear call was reachable at all.
**Action:** Once Linear MCP (or a valid `LINEAR_API_KEY`) is available to a scheduled/cloud session, re-run the `idea-sweep` routine for **Application Agent** from scratch — nothing from this attempt can be resumed, because no step that touches Linear ran.
**Issue:** none — this blocker occurs before any issue exists (pre-flight, before step 1 of any role)

---

## Payload

Trigger was: `Run the "idea-sweep" routine for Application Agent.` per `routines/idea-sweep.md`.

I read `routines/idea-sweep.md`, `routines/README.md`, `projects.md`, and `agents/spec-drift.md` to confirm scope. Application Agent resolves to:
- Repo: `rohrasharad-ship-it/Application-Agent`
- Linear Project: Application Agent
- Linear Project ID: `7dc5202c-a586-4bed-b2d3-fba10f2dd913`
- Slack: `#application-agent` (moot — idea-sweep posts no Slack summary anyway)

**Why nothing could run, not even partially:**

1. **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`, mandatory before any role starts) requires `list_issues` filtered by Linear Project ID. Not callable — no Linear MCP tool exists in this session's toolset at all (confirmed via tool search, not just "returned an error").
2. Because the cap check couldn't run, I could not determine whether to run steps 1–9 (gap-filing) or fall back to steps 10–11 only per the routine's pre-flight rule — both branches assume Linear is reachable.
3. **spec-drift steps 1–9** (gap-filing) need Linear search (dedupe) and issue creation — blocked.
4. **spec-drift step 10** (stale-issue sweep) needs `list_issues` + reading/posting comments on Backlog issues — blocked.
5. **spec-drift steps 11–12** (preview-branch + OpenSpec archive housekeeping, AI-Workspace-side scripts) both require `LINEAR_API_KEY` as a shell env var — confirmed **not set** in this session (`echo $LINEAR_API_KEY` empty). This is the *same* unresolved blocker already tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (7 prior independent hits, root cause: repo secret `LINEAR_API_KEY` was never added, and even with a token the network proxy rejects `git push --delete` and the GitHub REST ref-delete endpoint). I did not re-verify the proxy behavior — that file already documents it exhaustively and says re-checking wastes tokens. I'm only recording here that Application Agent's run hit the same wall, for completeness of that file's per-project history, without duplicating its content.
6. **bug-error** and **market-feature** roles also require Linear (dedupe search + issue creation) — blocked identically; I did not attempt Vercel-log or vision-doc reading for them since filing is impossible regardless of what's found, and doing that reading without being able to act on it would just burn tokens for no output.

**No Linear issues were searched, created, or commented on. No branches were deleted. No files were archived. No sweep-ledger line was appended** — I deliberately did not write a `data/sweep-runs.jsonl` entry, because every shape the schema allows (`"clean": true` with zero counts, or real counts) would misrepresent what happened: the roles never ran, they weren't run-and-found-nothing.

## Instructions for receiving agent

1. Confirm Linear MCP is reachable (or `LINEAR_API_KEY` is set for the housekeeping scripts) in the session that picks this up.
2. Re-run `idea-sweep` for **Application Agent** from the top: pre-flight cap check, then spec-drift → bug-error → market-feature per `routines/idea-sweep.md`. Nothing here needs replaying — no partial state exists to reconcile.
3. For the housekeeping steps specifically (spec-drift 11–12), check whether `handovers/preview-branch-cleanup-linear-api-key.md` has been resolved first; if not, that file's fix (add the `LINEAR_API_KEY` repo secret) unblocks this too and this handover file can simply be deleted once a normal run succeeds.
4. Do not treat this file as requiring a Linear comment — there is no issue to comment on. Delete this file once a subsequent Application Agent idea-sweep run completes normally (with real Linear access).
