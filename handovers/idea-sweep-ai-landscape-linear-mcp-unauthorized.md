# Handover: idea-sweep routine (AI Landscape 2026) could not run — Linear MCP is unauthorized in this session

**For:** Any agent/human who can authorize the Linear connector for this account, or any future idea-sweep session that runs with Linear MCP access already granted
**From:** Claude Code (scheduled `idea-sweep` trigger), AI Landscape 2026, 2026-08-29
**Blocked by:** The Linear MCP server is listed as requiring authentication before its tools can be used in this session. This session is a non-interactive scheduled run — it cannot complete an OAuth flow, and per its own operating instructions must not ask anyone for authorization codes, tokens, or callback URLs. No Linear tool of any kind (`list_issues`, `create_issue`, `save_issue`, comment tools, etc.) is reachable at all — not even present in the deferred-tool list.
**Action:** Authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear, or `claude mcp` / `/mcp` in an interactive session), then re-run (or wait for the next scheduled firing of) the `idea-sweep` routine for AI Landscape 2026.
**Issue:** N/A — this is a routine trigger (`routines/idea-sweep.md`), not an issue-driven session. No Linear issue could be created or referenced because Linear itself is the blocked tool.

## How this differs from the existing `preview-branch-cleanup-linear-api-key.md` handover

That handover documents sessions that **did** have Linear MCP tool access (they used it to run the stale-issue sweep, dedupe searches, and issue creation) but lacked a `LINEAR_API_KEY` shell env var for the `cleanup-preview-branches.sh` / `generate-routine-log.mjs` scripts, plus a proxy that blocks `git push --delete`. That is a narrower, already-diagnosed blocker limited to steps 11/12 housekeeping.

This session's blocker is upstream of that one and total: the **Linear MCP connector itself is not authorized**, so every step of `idea-sweep` that touches Linear was unreachable this run — not just the housekeeping scripts. That includes:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — could not count active pipeline issues for AI Landscape 2026 (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
- **spec-drift** steps 4–5, 7–10 (dedupe search, issue creation, comment, stale-issue sweep) — none run.
- **bug-error** steps 3–4, 7 (dedupe search, issue creation, comment) — none run. (Also did not pull Vercel runtime logs first, since any candidate found would have been un-dedupeable and un-fileable without Linear.)
- **market-feature** steps 4–5, 8 (dedupe search, issue creation, comment) — none run.
- Steps 11–12 (preview-branch cleanup, openspec archive sweep) were not attempted either, since 11 also needs Linear issue-status lookups and both are independent of the specific project targeted this run.

**No issues were created, no Linear searches were performed, no comments were posted, and `data/sweep-runs.jsonl` was deliberately left untouched** — appending a `{"clean":true}` line would misrepresent this run as "checked, found nothing" when in fact nothing could be checked at all. Do not backfill a ledger entry for this date/project until a session with real Linear access confirms what, if anything, should be filed.

## Instructions for receiving agent

1. Authorize the Linear MCP connector for this account (see **Action** above). This session cannot self-serve this — it requires a human or an interactive session.
2. Once authorized, re-run `routines/idea-sweep.md` for **AI Landscape 2026** from the top, including the Issue Cap pre-flight — nothing from this attempt can be reused since no Linear-side work happened.
3. If the receiving session also hits the separate, already-diagnosed `LINEAR_API_KEY` / proxy blocker on steps 11–12, don't re-litigate it — see `handovers/preview-branch-cleanup-linear-api-key.md`, which has that fully documented across 7 prior runs.
4. Delete this handover file once a session with working Linear access has successfully run idea-sweep for AI Landscape 2026 (or confirms the connector is authorized going forward, even if that particular run finds nothing to file).
