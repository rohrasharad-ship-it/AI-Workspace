# Handover: idea-sweep routine for Usercon could not run — no Linear MCP access this session

**For:** Any agent/session with Linear MCP tool access authorized (check by confirming a `list_issues`-style Linear tool is actually callable, not just listed)
**From:** `idea-sweep` routine run for Usercon (scheduled trigger), 2026-09-27
**Blocked by:** This session has **no Linear MCP tools at all** — the Linear MCP server is listed as requiring authentication, and this is a non-interactive scheduled session so the OAuth flow can't be completed here. This is a harder/different blocker than the one already tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that one has full Linear MCP read/write but is missing the `LINEAR_API_KEY` *env var* needed by the housekeeping shell scripts and `git push --delete`). Here there is no Linear access of any kind — no `list_issues`, no `create_issue`, no `create_comment`.
**Action:** Once a session has Linear MCP authorized (the account owner needs to authorize the Linear connector — this can't be done from inside a session), re-run the `idea-sweep` routine for Usercon from `routines/idea-sweep.md` from the top. This handover deliberately does **not** hand off pre-computed gap/bug/feature candidates — see Payload for why that would be unsafe.
**Issue:** N/A — this is a routine-level blocker (idea-sweep pre-flight), not tied to one existing Linear issue.

## What this blocks, specifically

Every idea-generation role's process depends on Linear at multiple steps, all unreachable this session:

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — needs `list_issues` filtered by Usercon's Linear Project ID (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). Could not even determine whether Usercon is under or at the 5-issue cap.
- **spec-drift** steps 4–10 (search Linear before filing, create issues, first comment, stale-issue sweep + comments) — all need Linear read/write.
- **bug-error** steps 3–7 (search, create, comment) — same.
- **market-feature** steps 4–8 (search, create, comment) — same.
- spec-drift step 11 (preview-branch housekeeping) also needs `LINEAR_API_KEY` for the shell script, which this session doesn't have either (same underlying gap as the already-tracked handover above, so not re-logged there — this file is the Linear-MCP-access blocker, that one is the env-var blocker).

Only spec-drift step 12 (OpenSpec archive sweep, `scripts/archive-merged-openspec-changes.sh --sweep`) doesn't need Linear — **not run this session** because it requires shell access to a clone of AI-Workspace and this session only has GitHub MCP file/branch tools, no shell. Flagging so it isn't silently skipped twice.

## Second, independent blocker for bug-error specifically

`projects.md` lists Usercon's **Vercel Prod as `TBD`** — there is no production URL on record. Even with Linear restored, the bug-error role has nothing to read logs from and no live URL to screenshot. Whoever picks this up should also fill in the real prod URL in `projects.md` (or confirm none exists yet, in which case bug-error should keep being skipped for Usercon, not treated as a tooling failure).

## Why no gap/feature candidates are included here

I did read `openspec/project.md` and the `openspec/specs/` capability list for Usercon (read-only, no Linear needed) to see whether a partial spec-drift/market-feature pass was safe to hand off anyway. It is not: Usercon's `openspec/changes/` currently has **23 active (non-archived) change folders** —

```
portable-context-packet-export, sha-74-pending-review-actions, sha-75-context-card-metadata,
sha-139-detail-missing-fields, sha-143-agent-contribution-breakdown, sha-179-empty-lifeareas-you,
sha-180-habit-context-type, sha-181-bulk-add-context, sha-182-archived-context-purge,
sha-183-sensitivity-visibility-level, sha-184-multi-user-isolation, sha-186-login,
sha-203-stitch-visual-design, sha-204-mobile-tab-nav, sha-207-context-receipt-panel,
sha-211-context-node-detail-screen, sha-212-you-identity-card, sha-213-grouped-settings-screen,
sha-214-simplified-menu-overlay, sha-216-mcp-setup-tutorial-ui, sha-220-contextual-manual-rule-input,
sha-231-restore-archived-context, sha-243-context-item-version-history
```

That volume of in-flight change proposals (most named after `SHA-<n>` Linear issue IDs) means almost any gap or feature idea a Linear-blind pass could surface is very likely already tracked in Linear under one of these. Filing — or even just proposing for hand-off — candidates without the ability to search Linear first would directly violate the "search Linear first, skip anything already tracked" rule in `routines/README.md` and risk flooding the backlog with duplicates. Better to hand off a clean blocker than a list of probably-duplicate guesses.

## Instructions for receiving agent

1. Confirm Linear MCP is actually callable (not just listed) — try a small `list_issues` call scoped to Usercon's project ID before doing anything else.
2. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Usercon using Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`.
3. If under cap, run `routines/idea-sweep.md` for Usercon in full: spec-drift → bug-error → market-feature, per each role's own file. For bug-error, first check whether `projects.md` still says `TBD` for Usercon's Vercel Prod — if so, skip bug-error and note that in the run's output rather than treating it as blocked tooling.
4. Append the real sweep-ledger line to `data/sweep-runs.jsonl` for this run once it actually files something (or confirms clean) — do not backfill one for this blocked attempt, since no roles actually ran.
5. Delete this handover file once a real idea-sweep run for Usercon completes with Linear access restored.
