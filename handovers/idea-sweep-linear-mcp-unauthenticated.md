# Handover: idea-sweep routine blocked — Linear MCP not authenticated in this session

**For:** Sharad, or any agent picking this up after Linear connector access is restored
**From:** idea-sweep routine run, Application Agent, 2026-08-24 (Claude Code, cloud/scheduled session)
**Blocked by:** Linear MCP connector requires authentication and this session has no OAuth
flow available (non-interactive/scheduled session) — no `mcp__Linear__*` tools are exposed
at all, not even read-only ones.
**Action:** Re-authorize the Linear connector for this account (claude.ai → Settings →
Connectors), then re-run: "Run the idea-sweep routine for Application Agent."
**Issue:** No driving Linear issue — this is an infra blocker on the routine itself, not
work on an existing issue.

## What happened

The scheduled trigger fired `idea-sweep` for **Application Agent**
(`rohrasharad-ship-it/Application-Agent`, Linear Project ID
`7dc5202c-a586-4bed-b2d3-fba10f2dd913`). Per `routines/idea-sweep.md`, every one of the
three roles (spec-drift, bug-error, market-feature) requires the Issue Cap pre-flight
(`agents/shared/issue-cap.md`) before doing anything else, and that pre-flight is a Linear
`list_issues` call. This session's tool list shows Linear under "requires authentication
before its tools can be used" — no Linear tool schema is available to call at all, so the
cap count could not be performed for this project.

Because the cap check is the mandatory first gate for all three roles, **none of
spec-drift's steps 1–9, bug-error, or market-feature could run** this cycle. Spec-drift's
steps 10–11 (stale-issue sweep, preview-branch housekeeping) are independent of the cap but
both still need Linear (comment on issues / look up issue status by branch) or
`LINEAR_API_KEY` (for `scripts/cleanup-preview-branches.sh`) — also unavailable here for the
same reason, so those were skipped too rather than run against stale/incomplete data.

This is **not** the same issue as the long-running `LINEAR_API_KEY` GitHub Actions secret
gap tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that one is about the
housekeeping *script* lacking a repo secret; this one is the Linear MCP *connector* itself
being unauthenticated for this session type). Both need to be fixed independently.

Separately, and not the blocking factor this run: this session's toolset also has no
browser/Playwright tool at all, so even if Linear had been available, the mandatory
screenshot-attach step (`agents/shared/visual-self-qa.md`, required on every issue any of
these three roles create) could not have been completed either. Worth checking whether
scheduled/cloud idea-sweep sessions reliably get a Playwright-capable tool — if not, that's
a second structural gap to fix alongside the Linear connector, on the next run where Linear
is available.

## What was and wasn't done this run

- GitHub read access worked fine (repo browsing, `projects.md`, all role/shared module
  files) — the blocker is Linear-specific, not a general tool outage.
- No Linear reads, writes, comments, or attachments were attempted or fabricated.
- No entry was added to `data/sweep-runs.jsonl` for this run — that ledger's `filed` counts
  and `clean` flag both assume the roles actually ran; a fake `clean:true, filed:0` entry
  would misrepresent "nothing was checked" as "checked and found nothing." Once Linear
  access is restored, the next real run for Application Agent should log normally.

## Instructions for receiving agent/human

1. Confirm the Linear connector is authorized for this account (claude.ai connector
   settings, or `/mcp` in an interactive Claude Code session) and that `mcp__Linear__*`
   tools appear in a fresh session's tool list.
2. Re-run the trigger: "Run the idea-sweep routine for Application Agent. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly."
3. If Linear tools are present but a browser/Playwright tool is still missing, that's a
   separate, second gap — file it the same way (or note it inline) rather than skipping
   Visual Self-QA silently.
4. Delete this handover file once a clean or filed run for Application Agent lands in
   `data/sweep-runs.jsonl` — at that point this blocker is confirmed resolved.
