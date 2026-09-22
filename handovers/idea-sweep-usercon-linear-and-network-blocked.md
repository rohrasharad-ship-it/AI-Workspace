# Handover: idea-sweep for Usercon — Linear MCP unavailable + network policy blocks live screenshots this session

**For:** Any agent/session with Linear MCP access and unrestricted outbound HTTPS
**From:** Scheduled `idea-sweep` routine run, Claude Code cloud session, 2026-09-22
**Blocked by:** (1) No Linear MCP tool access this session — the connector requires an OAuth authorization this non-interactive scheduled session cannot perform (confirmed: no `mcp__Linear__*` tools appear anywhere in the tool list or via tool search). (2) The session's egress proxy rejects outbound HTTPS to essentially all external hosts except a small allowlist (npm/pypi/anthropic registries) — confirmed via `curl` (`connect_rejected`, "organization policy") against `usercon.vercel.app`, `vercel.com`, and `github.com` alike. This is the exact "network-policy fallback" scenario documented in `agents/shared/visual-self-qa.md`.
**Action:** Once a session has Linear MCP connected (or Sharad forwards this to one that does), re-run `idea-sweep` for Usercon from scratch — this run made no Linear-side progress at all, so nothing here is "resume from," just "start over."

---

## What did and didn't run

| Role | Step 0 (cap check) | Result |
|---|---|---|
| **bug-error** | Not needed — this role's outcome doesn't depend on the cap | **Ran cleanly, no blocker.** `mcp__Vercel__get_runtime_errors` (project `prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`, `since: 7d`) returned **zero runtime errors**. Per role step 8, "if the site is clean, create nothing" — correctly nothing to file, no Linear access even needed for this outcome. |
| **spec-drift** | Blocked | Could not run the Issue Cap pre-flight (`agents/shared/issue-cap.md` needs `list_issues` by Linear Project ID) or search Linear for dedupe, so steps 1–9 could not proceed. Did not attempt gap analysis against `openspec/` vs codebase — even if real gaps were found, they can't be filed or dedupe-checked, and the mandatory Visual Self-QA screenshot (conventions.md rule 12) can't be taken either (see network blocker below). Steps 10–11 (stale-issue sweep, preview-branch housekeeping) also need Linear read access — skipped for the same reason. |
| **market-feature** | Blocked | Same as spec-drift: cap check and Linear dedupe search both impossible. Did not attempt feature ideation for the same reason — un-filable, un-screenshottable output has no value and would just go stale. |

## Signal worth knowing before the next run

Usercon's repo currently has **23 unarchived `openspec/changes/` folders** (`sha-74` through `sha-243`, e.g. `sha-179-empty-lifeareas-you`, `sha-231-restore-archived-context`, `sha-243-context-item-version-history`, ...). That's a strong signal the project's active Linear pipeline is well above the 5-issue cap already — the next session should expect **spec-drift steps 1–9 and all of market-feature to skip immediately at the cap check**, with only spec-drift steps 10–11 (stale sweep + housekeeping) actually running. Budget accordingly rather than being surprised.

Also: the existing handover `handovers/preview-branch-cleanup-linear-api-key.md` documents a **separate, long-standing** blocker — the `LINEAR_API_KEY` repo secret is still missing on `AI-Workspace`, so even a session with Linear MCP access cannot complete spec-drift step 11 (branch cleanup) end-to-end; git push to delete branches is also proxy-blocked from every session tried so far (7 independent confirmations as of 2026-08-12). That issue is unrelated to this one (this session never got far enough to hit it) but will resurface the moment Linear access is restored.

## Fixed this run (not blocked, no Linear needed)

`projects.md`'s Usercon row had **Vercel Prod: TBD**. Resolved via Vercel MCP:
- Project: `usercon` (`prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`)
- Production domain: `usercon.vercel.app`
- `passwordProtection.enabled: false`, `ssoProtection.enabled: false` — the domain itself is not access-gated (unlike the AI-Workspace preview-protection issue in `handovers/linear-issue-vercel-preview-blocker.md`). This session just couldn't reach it due to its own egress policy, which is a session-local restriction, not a property of the deployment.
- Updated `projects.md` accordingly so future runs don't need to re-derive this.

## Evidence: network policy blocks outbound HTTPS this session

```
$ curl -sI https://usercon.vercel.app/   → connect_rejected (gateway 403 to CONNECT, "organization policy")
$ curl -sI https://vercel.com/          → connect_rejected, same cause
$ curl -sI https://github.com/          → connect_rejected, same cause (only api.anthropic.com / package registries allowlisted per proxy status)
```

Per `agents/shared/visual-self-qa.md` → "Network-policy fallback": this is exactly the documented trigger (outbound HTTPS blocked *before* reaching the target site, reproduced against multiple unrelated hosts). No screenshot was fabricated; none was attempted past this proof, since the same proxy would block Playwright identically.

## Instructions for receiving agent

1. Confirm Linear MCP is connected in your session (`list_issues` or similar succeeds).
2. Confirm outbound HTTPS works (quick `curl -I https://usercon.vercel.app/` should return `200`, not a proxy rejection).
3. Re-run `idea-sweep` for **Usercon** per `routines/idea-sweep.md` from step 0 — do the Issue Cap pre-flight fresh; expect it to likely already be at/over cap given the 23 open change folders noted above.
4. If at cap: run spec-drift steps 10–11 only, per the routine's pre-flight rule. Check `handovers/preview-branch-cleanup-linear-api-key.md` first — step 11 will hit that same wall again unless `LINEAR_API_KEY` has been added as an AI-Workspace repo secret in the meantime.
5. Delete this handover once a future run either completes cleanly or supersedes these notes.
