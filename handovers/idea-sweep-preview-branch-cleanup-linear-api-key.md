# Handover: Preview-branch cleanup blocked — LINEAR_API_KEY not available in session

**For:** Any agent/session with `LINEAR_API_KEY` available as a shell env var and git push access to `rohrasharad-ship-it/ai-workspace`
**From:** spec-drift role, idea-sweep routine run for project "AI Landscape" (Linear project `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`), 2026-07-27
**Blocked by:** `scripts/cleanup-preview-branches.sh` hard-requires `LINEAR_API_KEY` (`error: LINEAR_API_KEY is required`) and this session's shell environment does not have it set (checked via `env | grep -i linear` — no match). GitHub push/clone access via the session's local git proxy works fine; Linear MCP tool access also works fine — only the raw API key needed by the shell script for direct GraphQL calls is missing.
**Action:** Run `bash scripts/cleanup-preview-branches.sh` (optionally `--dry-run` first) from a checkout of `rohrasharad-ship-it/ai-workspace` with `LINEAR_API_KEY` exported, and report the deleted/kept/skipped counts.
**Issue:** No single Linear issue drives this — this is routine housekeeping (`agents/spec-drift.md` step 11), not itself a product gap. Do not file a Linear issue against the AI Landscape project for this; it's an automation/infra gap.

## Payload

- This session confirmed real git clone + push capability to `rohrasharad-ship-it/ai-workspace` works (via the sandbox's local git credential proxy) and `npx openspec` runs fine after a local `npm install` — those parts of the toolchain are healthy.
- `gh` CLI is **not** installed in this sandbox either (`which gh` → not found), which also affects `scripts/archive-merged-openspec-changes.sh`'s optional open-PR check in `--sweep` mode (that script degrades gracefully with a warning when `gh` is missing — not a hard blocker there, just noted for awareness).
- As of this run, `origin` on `rohrasharad-ship-it/ai-workspace` has **~95 `preview/*` branches**, ranging from `preview/SHA-18-v1` through at least `preview/SHA-94-v1` (full list obtainable via `git branch -r --list 'origin/preview/*'` or `list_branches` on GitHub MCP).
- Spot-checking the corresponding Linear issues for the AI Landscape project (`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) during this same run showed **every current issue in that project is `Done`, `Canceled`, or `Duplicate` — none are `Backlog`/`spec-needed`**. That strongly suggests most/all `preview/SHA-*` branches tied to AI Landscape issues are now orphaned and eligible for deletion under the script's own rules (issue state `completed`/`canceled`/`duplicate`, or no longer labeled `spec-needed`).
- This is a rough read from one project's issues only, not a substitute for running the actual script, which also handles other projects' `SHA-*` issues in the same shared Linear team and the "older version than latest branch for that issue" rule.

## Instructions for receiving agent

1. Get `LINEAR_API_KEY` into your shell env (repo secret / local credential — not something this session had access to).
2. `git clone https://github.com/rohrasharad-ship-it/ai-workspace.git && cd ai-workspace`
3. Run `bash scripts/cleanup-preview-branches.sh --dry-run` first, review the planned deletions, then run without `--dry-run` to execute for real.
4. Report the final `deleted`/`kept`/`skipped` counts wherever this routine's results are being tracked.
5. Delete this handover file once the cleanup has actually run successfully — until then it documents the open gap.

**Do not** hand-roll the branch-deletion logic outside the script (e.g. by using Linear MCP tools to approximate the safety check and then running raw `git push origin --delete`) — the script is the single reviewed source of truth for this decision and mixing an ad hoc check with real deletions risks removing a branch that's still legitimately `spec-needed` for a different project.
