# Handover: idea-sweep (Resume Website) — Linear MCP unavailable this session, no issues filed

**For:** Any agent/session with Linear MCP tool access
**From:** idea-sweep routine run, Resume Website, 2026-09-03 (Claude Code, scheduled trigger)
**Blocked by:** This session's Linear MCP connector requires authentication and the session is non-interactive, so no Linear tool schema was even loadable — not merely a missing `LINEAR_API_KEY` shell env var (that's a separate, pre-existing blocker already tracked in `handovers/preview-branch-cleanup-linear-api-key.md`, 7+ consecutive hits). No Linear tool of any kind (list issues, create issue, comment, search) was available, so the Step 0 Issue Cap pre-flight could not be performed, and none of spec-drift steps 1–9, bug-error, or market-feature could run.
**Action:** Once a session with real Linear MCP access picks this up, re-run the `idea-sweep` routine for Resume Website per `routines/idea-sweep.md`, starting with the Issue Cap check below — the project is very likely already at or over cap.
**Issue:** N/A — this handover isn't tied to one Linear issue; it's a routine-run blocker, not a bug in the target product.

## Payload

**Issue Cap — likely already at or over cap.** I could not query Linear directly, but `resume-website/openspec/changes/` currently holds 7 active (non-archived) change proposals, each of which normally corresponds to a Backlog + `spec-needed` Linear issue under this repo's workflow:
- `fix-mobile-voice-audio`
- `journey-chapter-scrubber`
- `mobile-qa-pass` (SHA-12)
- `save-contact-vcard`
- `social-share-preview`
- `suggested-prompt-chips`
- `warmer-chatbot-avatar`

The cap is 5 active pipeline issues (Backlog/Todo/In Progress/In Review) per `agents/shared/issue-cap.md`. 7 active change proposals strongly suggests Resume Website is already at or over cap. **First action for the receiving agent: run the real Issue Cap check** using Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d` (from `projects.md`). If at/over cap, per `routines/idea-sweep.md` pre-flight, only run spec-drift steps 10–11 (stale-issue sweep + preview-branch housekeeping) this cycle — do not add an 8th proposal on top of these 7.

**bug-error: confirmed clean, independent of the Linear blocker.** Checked Vercel runtime errors directly (`get_runtime_errors`, project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, last 24h): **no runtime errors found**. This part of the routine needs no re-run soon — it's a genuine 0, not a Linear-blocked gap.

**spec-drift / market-feature: not attempted, by design.** The 7 already-active proposals above already cover most obvious near-term gaps and feature ideas (mobile voice bug, Journey navigation, mobile QA, contact save, social share metadata, engagement via prompt chips, agent tone/avatar warmth). Rather than guess at an 8th/9th/10th candidate I have no way to dedupe against Linear — "search Linear first, skip anything already tracked" is a hard guardrail in `routines/README.md` — I left fresh ideation to the Linear-capable agent. If the cap check above comes back under 5, re-read `openspec/project.md` + `openspec/specs/*` fresh before proposing anything new; they may have moved since these 7 proposals were written.

**Housekeeping actually completed this run (needs no Linear tool):**
- Step 12 (OpenSpec archive sweep) — ran `bash scripts/archive-merged-openspec-changes.sh --sweep` in AI-Workspace, per the literal instruction in `agents/spec-drift.md` step 12 (which points at AI-Workspace's own `openspec/changes/`, not the target project's — flagging in case that's meant to target the project repo instead, since Resume Website keeps its own `openspec/changes/` locally with the 7 live proposals above). Result: `sweep: no completed active changes` — nothing to archive.
- Step 11 (preview-branch cleanup) — **not run**, correctly: `scripts/cleanup-preview-branches.sh` hard-requires `LINEAR_API_KEY` as a shell env var (the separate, pre-existing blocker in `handovers/preview-branch-cleanup-linear-api-key.md`). Checked anyway: `git branch -r` on AI-Workspace currently shows **zero** `preview/*` branches, so there is nothing to clean up right now regardless of that blocker.

**Ledger:** appended a `data/sweep-runs.jsonl` line for this run with `"clean": false` and a `"blocked"` note, rather than a bare `filed: 0/0` — `generate-routine-log.mjs` currently treats `filed === 0` as clean regardless of the `clean` flag (line ~164, `if (rest.clean || filed === 0) return {...rest, clean:true, ...}`), so a blocked run and a genuinely clean run are indistinguishable on the dashboard today. Not fixing that script here (out of scope for this handover), just flagging it — worth a look given how many recent ledger lines are `filed:0, clean:true` across projects. Did **not** run `node scripts/generate-routine-log.mjs` — also needs `LINEAR_API_KEY`, unavailable this session.

## Instructions for receiving agent

1. Run the Issue Cap check for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) per `agents/shared/issue-cap.md`.
2. If at/over cap: run spec-drift steps 10–11 only (stale-issue sweep on the existing Backlog issues; preview-branch cleanup, though per the note above there are currently no `preview/*` branches to clean). Do not file new issues.
3. If under cap: re-run spec-drift steps 1–9 and market-feature fresh, with a real Linear search for dedup against the 7 items listed above. bug-error can be skipped unless meaningful time has passed since 2026-09-03 (confirmed clean above).
4. Once any Linear-dependent step runs, also run `LINEAR_API_KEY=... node scripts/generate-routine-log.mjs` to refresh the dashboard — it's been stale across multiple blocked runs.
5. Delete this handover once a Linear-capable session has completed the cap check and either confirmed at-cap (skip) or filed/dedup'd properly.
