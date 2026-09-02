# Handover: idea-sweep routine for AI Landscape could not run — no Linear MCP access at all in this session

**For:** Any agent/session with working Linear MCP tools (or a valid `LINEAR_API_KEY`)
**From:** idea-sweep routine session (Claude Code, scheduled trigger), 2026-09-02
**Blocked by:** This session has zero Linear tool access — not the narrower "missing `LINEAR_API_KEY` shell secret" problem already tracked in `handovers/preview-branch-cleanup-linear-api-key.md`. The Linear connector shows as installed (`enabledInChat: true`) but its `installState` is `unknown` and a targeted `ToolSearch` for any `mcp__Linear__*` tool (list_issues, create_issue, search_issues, etc.) returned **no matching deferred tools** — the MCP server itself never surfaced any callable tools this session, most likely because its OAuth/auth needs to be completed by a human (this session is non-interactive and cannot run that flow). Also confirmed no `LINEAR_API_KEY` in the shell environment (`env | grep -i linear` → empty), so there was no REST-API fallback either.
**Action:** Re-run the `idea-sweep` routine for AI Landscape (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`, per `projects.md`) from a session where the Linear connector is actually authorized — either reconnect it under claude.ai Settings → Connectors, or wake this from a session type where `mcp__Linear__*` tools actually resolve.
**Issue:** N/A — this is a routine-level block before any Linear issue existed to attach a comment to.

## What this blocks

Every step of `routines/idea-sweep.md` that isn't pure repo-reading requires Linear:

- Pre-flight Issue Cap check (`agents/shared/issue-cap.md`) — needs `list_issues` filtered by Linear Project ID.
- spec-drift steps 4–9 (dedupe search, create issues, comment) — blocked.
- spec-drift step 10 (stale-issue sweep, comment on possibly-resolved Backlog issues) — blocked, needs Linear read + comment.
- spec-drift steps 11–12 (preview-branch / openspec-archive housekeeping scripts) — both scripts require `LINEAR_API_KEY` as a shell secret to look up issue labels/state; also unavailable this session (see the **separate, already-tracked** blocker in `handovers/preview-branch-cleanup-linear-api-key.md` — that one is about the missing repo secret specifically, not full Linear MCP absence; both blockers currently compound for AI Landscape).
- bug-error steps 3–8 (dedupe, create, comment) — blocked. Note: also worth flagging structurally — `projects.md` lists AI Landscape's Vercel Prod as `https://rohrasharad-ship-it.github.io/ai-landscape/` (GitHub Pages), yet the repo root also has a `vercel.json`. Confirm with Sharad which is actually authoritative before the next bug-error run reads "Vercel production runtime logs" — if it's really GitHub Pages, there is no Vercel runtime-log source for this project and step 1 of `agents/bug-error.md` may need a different signal (e.g. browser console errors captured live via Playwright instead).
- market-feature steps 4–9 (dedupe, create, comment) — blocked.

Nothing in this session could get past the Issue Cap pre-flight, so **no repo-side prep work for spec-drift/market-feature gap-finding was attempted either** — those steps explicitly require reading the whole spec surface and codebase, and any candidates found now would need re-reading anyway once Linear access exists (freshness of the dedupe check matters more than saving a re-read). The repo does have a normal `openspec/` structure (`openspec/project.md`, `openspec/specs/`, `openspec/changes/`) ready for spec-drift and market-feature to read once unblocked.

## Instructions for receiving agent

1. Confirm Linear MCP tools actually resolve in your session (`ToolSearch` for `mcp__Linear__*`, or just call `list_issues`/equivalent and see if it works) before starting — don't assume the connector being "installed" means it's usable.
2. Re-run `routines/idea-sweep.md` for **AI Landscape** from step 1 (Issue Cap pre-flight), following the routine file exactly — this handover changes nothing about the routine's own instructions, it's purely a "this session couldn't start" note.
3. While there, separately check whether `handovers/preview-branch-cleanup-linear-api-key.md` has been resolved (the `LINEAR_API_KEY` repo secret) — if still open, steps 11–12 of spec-drift will hit that second, already-documented wall even after Linear MCP itself is working.
4. Delete this handover file once a session with working Linear MCP has successfully completed an idea-sweep run for AI Landscape.
