# Handover: idea-sweep for Usercon — Linear MCP not connected in this session (fully blocks the routine, not just LINEAR_API_KEY)

**For:** Any agent/human who can authorize the Linear connector for this account
**From:** idea-sweep routine run (Claude Code, non-interactive scheduled session), 2026-08-23
**Blocked by:** No Linear MCP tool access at all in this session — the harness reported Linear as "requires authentication before its tools can be used" and explicitly noted this session is non-interactive and cannot run the OAuth flow. No `LINEAR_API_KEY` env var either (checked, empty).
**Action:** Authorize the Linear MCP connector for this Claude account (via claude.ai connector settings, or `claude mcp` / `/mcp` in an interactive session), so a future scheduled `idea-sweep` run actually has Linear tool access.
**Issue:** none created — the routine could not get far enough to check the issue cap, so no Linear issue exists for this yet. (See "Why no issue was filed for this" below.)

## Payload

This run was triggered as: `Run the "idea-sweep" routine for Usercon. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`

Read `routines/idea-sweep.md`, `routines/README.md`, `projects.md`, `agents/shared/issue-cap.md`, `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`, and the other shared modules — all fine, all via GitHub MCP (`get_file_contents`), which works in this session. Resolved Usercon → repo `rohrasharad-ship-it/Usercon`, Linear project `UserCon`, Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`.

The routine's own first mandatory step — the Issue Cap pre-flight (`agents/shared/issue-cap.md`) — requires calling Linear's `list_issues` to count active pipeline issues for the project. This session has **no Linear MCP tool at all** (distinct from the already-documented `LINEAR_API_KEY` gap in `handovers/preview-branch-cleanup-linear-api-key.md`, which is about the *shell script* used by spec-drift step 11/12 — that handover's sessions still had working Linear MCP for reads/writes, they just lacked the raw API key for the bash script). Here, nothing Linear-shaped is reachable: no cap check, no dedupe search, no issue creation, no comments, no stale-issue sweep (spec-drift step 10).

**This means every one of the three roles' core steps (1–9) is blocked for every role, and spec-drift step 10 (stale-issue sweep) is blocked too** — not just the housekeeping steps (11/12) that were already known to be blocked by the missing `LINEAR_API_KEY`.

### What I could still check without Linear

- **Spec-drift step 12 (OpenSpec archive housekeeping, lives in AI-Workspace, not project-specific):** `openspec/changes/` in AI-Workspace currently contains only an `archive/` subdirectory — no active (non-archived) change folders. This matches the last several runs' notes in `handovers/preview-branch-cleanup-linear-api-key.md` — a clean 0, not a new blocker, and nothing to archive this run.
- **Spec-drift step 11 (preview-branch cleanup):** still blocked, same root cause already fully documented in `handovers/preview-branch-cleanup-linear-api-key.md` (missing `LINEAR_API_KEY` repo secret + proxy blocks mutating git/REST ref-delete paths). Did not re-verify the proxy behavior — that file explicitly says re-verifying wastes tokens with no new information, and I have no LINEAR_API_KEY either way. **Fix for that item is unchanged and already tracked there — don't duplicate it, just also get this new Linear-connector gap fixed.**

### Why no issue was filed for this

Filing a Linear issue about this would itself require Linear access, which is exactly what's missing. This handover file + a comment are the fallback per `agents/shared/conventions.md` → Blocked-agent handover. Once Linear MCP is authorized, whoever picks this up can decide whether it's worth a formal `PM OS` infra issue (recommend: yes, low/no priority — "idea-sweep scheduled runs need Linear MCP" — since this is a recurring scheduled trigger and will hit the same wall every time until fixed) or just fixing the connector is enough.

## Instructions for receiving agent

1. Confirm Linear MCP tools (e.g. `list_issues`, `create_issue`, `create_comment`) are actually callable in a session for this account.
2. Re-run the `idea-sweep` routine for Usercon from the top (`routines/idea-sweep.md`) — nothing from this run can be reused, since the pre-flight cap check never completed.
3. Do not treat this file as evidence Usercon is "clean" — no role actually ran. `data/sweep-runs.jsonl` was deliberately **not** updated with a `clean: true` entry for this run, to avoid implying the sweep executed and found nothing.
4. Delete this handover file once a future run completes normally (cap check succeeds) — that's the confirmation the connector fix worked.
