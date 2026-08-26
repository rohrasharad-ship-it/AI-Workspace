# Handover: idea-sweep for Resume Website — Linear connector not authorized in this session

**For:** Any agent/session with Linear MCP access (or Sharad, to authorize the connector)
**From:** idea-sweep routine run for Resume Website, 2026-08-26 (Claude Code, cloud/scheduled session)
**Blocked by:** Linear MCP server requires OAuth authorization this session does not have. `ToolSearch` for Linear tools returns nothing, and the session's own tool-availability notice explicitly lists Linear under "MCP servers require authentication before their tools can be used" — non-interactive sessions cannot run the OAuth flow. No `LINEAR_API_KEY` env var is set either, so there is no fallback path (checked with `env | grep -i linear`, empty).
**Action:** Authorize the Linear connector for Claude (claude.ai → Settings → Connectors → Linear), or re-run this routine from a session that already has Linear MCP access. Once authorized, re-run `idea-sweep` for Resume Website — nothing below needs to be re-derived except the bug-error window (see Payload).

## Why this is a different blocker than the existing Linear handovers

`handovers/preview-branch-cleanup-linear-api-key.md` documents a *different* problem:
those sessions **had** Linear MCP (they ran `list_issues`, read statuses/labels) but
couldn't `git push --delete` a branch or run the shell cleanup script (needs
`LINEAR_API_KEY` as a raw secret, and the proxy blocks ref-deletion mutations). That
blocker is already well-documented across 7+ runs — no need to re-verify it here.

This run's blocker is upstream of that one: **no Linear MCP tool access at all**, for
any project, for any purpose (read, search, or write). That blocks every step of
`routines/idea-sweep.md` that touches Linear — the mandatory Issue Cap pre-flight
(`agents/shared/issue-cap.md`), all three roles' dedupe search, all issue creation,
and spec-drift's stale-issue comment sweep (step 10).

## What ran anyway (no Linear needed)

- **Issue Cap pre-flight:** Could not count active pipeline issues for Resume Website
  (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`). Treated this the same as
  "at cap" for safety — **no issues were filed** by any of the three roles this run,
  since filing without a dedupe search would risk duplicates the routine explicitly
  forbids.
- **Bug-error's actual signal (Vercel), checked directly:** `get_runtime_errors` on
  the Resume Website Vercel project (`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team
  `team_P5vgMhFNfh2d4fCe2YkRLjey`), window `since=24h` as of 2026-08-26T23:40 UTC —
  **no runtime errors returned.** If Linear had been available, bug-error would have
  filed nothing this run regardless — genuinely clean, not just blocked.
- **Step 12 (OpenSpec archive housekeeping, AI-Workspace-wide, no Linear needed):**
  `openspec/changes/` in AI-Workspace contains only the `archive/` subdirectory — no
  active change folders. Clean 0, nothing to archive. Consistent with prior sessions'
  notes in `preview-branch-cleanup-linear-api-key.md`.
- **Step 11 (preview-branch cleanup):** Not re-attempted — already exhaustively
  confirmed blocked (missing `LINEAR_API_KEY` repo secret + proxy blocks ref deletion
  via both git and REST) across 7 independent prior runs in
  `handovers/preview-branch-cleanup-linear-api-key.md`. Re-verifying adds no new
  information; see that file's fix (add the repo secret) if still unresolved.

## What did NOT run (needs Linear, not attempted to avoid wasted/stale work)

- Spec-drift steps 1–9 (OpenSpec-vs-codebase gap analysis for Resume Website) —
  not attempted. Unlike the branch-cleanup cross-reference, a gap list produced
  without being able to search Linear for existing coverage has a real risk of
  duplicating open issues, and this role runs weekly — cheap to just re-run properly
  once Linear is back rather than pre-computing a payload that would need re-checking
  anyway.
- Spec-drift step 10 (stale-issue sweep) — needs to read/comment on existing issues.
- Market-feature (all steps) — same reasoning as spec-drift 1–9.

## Instructions for receiving agent

1. Confirm Linear MCP is available (`list_issues` or equivalent responds).
2. Re-run `routines/idea-sweep.md` for **Resume Website** from the top, including the
   Issue Cap pre-flight (project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) — nothing
   here is a substitute for that pre-flight.
3. Bug-error may reuse the "clean, no runtime errors in the 24h before
   2026-08-26T23:40 UTC" finding above only if the re-run happens within a few hours
   of that timestamp; otherwise pull a fresh window — production logs move fast.
4. Delete this handover file once a Linear-capable session has completed the run (or
   confirmed the connector is authorized going forward).
