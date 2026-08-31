# Handover: idea-sweep routine blocked — Linear MCP not authenticated in this session

**For:** Sharad (or any human with access to this account's connector settings)
**From:** idea-sweep routine, triggered for "AI Workspace" (PM OS), 2026-08-31
**Blocked by:** the Linear MCP server requires authentication before its tools can be
used. `ToolSearch` for `list_issues` / `create_issue` / project queries returned only
GitHub, Vercel, and Slack tools — no `mcp__Linear__*` tool exists in this session's tool
set at all. `ListConnectors` shows the Linear connector as `enabledInChat: true` but
`installState: "unknown"` — it is toggled on for chat but not actually authenticated, so
no tool schema is exposed.

## This is a long-running, unresolved recurrence — not a one-off

`git log --all --oneline | grep -ic "linear mcp"` currently returns **51** near-identical
blocked-run commits across dozens of unmerged session branches, dating back to at least
July 2026, across every project in `projects.md` (AI Workspace, Resume Website, AI
Landscape, Application Agent, Usercon). None of these fixes or handovers have ever been
merged into `main` — each scheduled session hits the same wall, writes a new handover on
its own throwaway branch, and the branch is never merged, so the next session finds no
trace of it and re-documents from scratch. This file itself is a recreation of one first
written in commit `219db5e` (2026-08-25) and re-created again in `67d6c53` (2026-08-29) —
both on branches that never reached `main`.

**This will keep recurring on every scheduled idea-sweep firing until a human
authorizes the Linear connector at the account level.** No amount of retrying or
re-documenting from inside a session fixes it — the OAuth flow cannot run
non-interactively here.

## Action needed (one-time, by a human)

Authorize the Linear connector for this account via claude.ai connector settings
(Settings → Connectors → Linear → reconnect/authorize). This session cannot do this
itself. Once authorized, the next scheduled or manual `idea-sweep` firing picks it up
with no other change needed — no code or routine file needs editing.

## What did and didn't run this session

- Read `routines/idea-sweep.md`, `routines/README.md`, and `projects.md` and resolved
  the target: **AI Workspace (PM OS)** — repo `rohrasharad-ship-it/AI-Workspace`,
  Linear Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`.
- Could not perform the mandatory pre-flight Issue Cap check (`agents/shared/issue-cap.md`)
  because it requires `list_issues` filtered by Linear Project ID — no Linear tool
  available to call.
- Because pre-flight itself couldn't run, none of spec-drift, bug-error, or
  market-feature executed — including spec-drift steps 10–11 (stale-issue sweep,
  preview-branch housekeeping), which the routine says to run even when a project is at
  cap. Those steps also depend on Linear reads.
- Did **not** write a `data/sweep-runs.jsonl` entry for this run — every existing entry
  in that ledger represents a run that actually queried Linear, and writing one here
  would misrepresent a blocked run as a completed sweep.

## Recommendation

Given 51 prior occurrences with zero resolution via in-session handovers, further
per-run handover files add no new information. Treat this file as the canonical,
up-to-date record — no need to write another one until either (a) the connector is
fixed, or (b) a session finds this file already reflects a stale date and updates it in
place instead of creating a new one.

## Instructions for the next agent/human

1. Authorize the Linear MCP connector for this account (claude.ai connector settings).
2. Re-run: "Run the idea-sweep routine for AI Workspace. Follow
   `rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md` exactly."
3. Once Linear reads succeed, this file can be deleted.
