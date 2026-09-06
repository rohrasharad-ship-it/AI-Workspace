# Handover: Linear MCP unauthenticated — idea-sweep could not run for Usercon

**For:** Sharad (connector re-auth) or any future agent session with working Linear MCP access
**From:** Claude Code, scheduled `idea-sweep` routine run for Usercon, 2026-09-06
**Blocked by:** Linear MCP tools were not loaded in this session at all — the session's own tool listing reported `Linear` as an MCP server "requiring authentication before their tools can be used," and explicitly noted this is a non-interactive session that cannot run an OAuth flow. `ToolSearch` for `linear` / `mcp__Linear` returned zero matches (no Linear tool schemas available to call, not even a search/list call). No `LINEAR_API_KEY` was present as a Bash env var either, so there was no fallback script path.
**Action:** Re-authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear → reconnect), then re-run `idea-sweep` for Usercon. No other fix is needed — this is purely an auth-session gap, not a code or repo problem.
**Issue:** none — this run has no driving Linear issue; it's the recurring `idea-sweep` routine itself that could not proceed.

---

## Why this is a new/different blocker

This is **not** the already-documented `handovers/preview-branch-cleanup-linear-api-key.md` issue (missing `LINEAR_API_KEY` repo secret blocking the housekeeping *script's* git push). That blocker assumes Linear MCP itself works for reading/searching/commenting, and only the shell-script housekeeping step (steps 11–12 in `agents/spec-drift.md`) fails. Prior idea-sweep runs for Usercon (2026-07-14, 2026-07-21, 2026-08-08, 2026-08-12 per `data/sweep-runs.jsonl` and that handover's update log) all had working Linear MCP read/search/comment access and only hit the git-push-403 wall at the very end.

This run had **no Linear access of any kind** — not read, not search, not create, not comment. That is a strictly more fundamental blocker than the documented one, and it stops the routine before step 1 of any role.

## What that means for this cycle

Per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`, the mandatory Issue Cap pre-flight (count active pipeline issues via Linear `list_issues` filtered by Usercon's Linear Project ID, `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) must run before any role creates issues. With no Linear MCP access, this pre-flight cannot be performed, so per the routine's own guardrails **no idea-generation role could safely run**:

- **spec-drift** — steps 1–3 (read `openspec/` vs. codebase) are technically doable via GitHub MCP alone, but steps 4–9 (dedupe search, file, comment) and step 10 (stale-issue sweep) all require Linear MCP — skipped entirely rather than doing partial, un-deduplicated analysis that a properly authenticated run will redo anyway.
- **bug-error** — blocked on Linear the same way; separately, Usercon's row in `projects.md` still lists Vercel Prod as `TBD`, so even with Linear working there is no production URL to pull runtime logs from for this project. That's a standing, unrelated gap — someone needs to fill in Usercon's real prod URL in `projects.md` (or confirm there isn't one yet) before bug-error can ever produce anything for this project.
- **market-feature** — same Linear blocker as spec-drift for steps 4–9.
- **Housekeeping (spec-drift steps 11–12)** — also require Linear (via `LINEAR_API_KEY` in the cleanup scripts) and are additionally blocked by the separate, already-documented git-push-403 proxy issue in `handovers/preview-branch-cleanup-linear-api-key.md` (unchanged, not re-verified this run since Linear access wasn't even available to re-derive the branch list).

No Linear issues were created, searched, or commented on this run. No ledger entry was appended to `data/sweep-runs.jsonl` for this date — this was not a "ran cleanly, found nothing" outcome, it was a "could not run" outcome, and recording it as `clean: true` would misrepresent that.

## Instructions for receiving agent / Sharad

1. Reconnect the Linear connector for this account if it has since been re-authorized, confirm with a trivial `list_projects` or `list_issues` call before trusting it.
2. Re-run `idea-sweep` for Usercon once Linear MCP access is confirmed working — nothing about Usercon's OpenSpec, codebase, or Linear backlog was touched this cycle, so a fresh run is safe and won't duplicate anything.
3. Separately (not blocking, lower priority): fill in Usercon's real Vercel Prod URL in `projects.md`, or explicitly mark it as "no prod deployment yet" if that's accurate, so future bug-error runs know whether to expect a target.
4. Delete this handover file once a subsequent idea-sweep run for Usercon completes normally with working Linear access.
