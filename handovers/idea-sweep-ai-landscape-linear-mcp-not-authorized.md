# Handover: idea-sweep routine blocked — Linear MCP not authorized in this session

**For:** Any agent/session confirmed to have working Linear MCP tool access
**From:** Claude (Claude Code cloud session), idea-sweep routine run for AI Landscape 2026, 2026-09-20
**Blocked by:** The Linear MCP server was listed as requiring authentication/OAuth for this
session, with zero Linear tools available (no `list_issues`, `list_projects`, `create_issue`,
`add_comment`, etc.) — not even read-only calls worked. This session is a non-interactive
scheduled trigger, so it cannot run the OAuth flow itself.
**Action:** Someone with access to this account's Linear connector needs to authorize it for
scheduled/automated sessions (via claude.ai connector settings, per the standard non-interactive
MCP auth guidance), or a session that already has Linear MCP authorized should pick up this run.
Once Linear MCP works, re-run the `idea-sweep` routine for AI Landscape 2026 per
`routines/idea-sweep.md`.
**Issue:** N/A — routine trigger, no driving Linear issue.

---

## Why this is a new/different blocker (not a duplicate of existing handovers)

`handovers/preview-branch-cleanup-linear-api-key.md` and
`handovers/idea-sweep-preview-branch-cleanup-blocked.md` both document **narrower** problems
from prior idea-sweep runs for AI Landscape and other projects: those sessions had **working
Linear MCP access** (they ran full paginated `list_issues` sweeps, cross-referenced ~270+
issues, posted/skipped stale-issue comments, etc.) and only got stuck on (a) the
`LINEAR_API_KEY` shell env var needed by `scripts/cleanup-preview-branches.sh`, and (b) a
proxy policy blocking `git push --delete` / REST ref-deletion.

This session's blocker is upstream of all of that: **Linear MCP itself never connected**, so
none of steps 0–10 in `agents/spec-drift.md` / `agents/bug-error.md` / `agents/market-feature.md`
could even start — not just the housekeeping tail end (steps 11–12).

## What this session did

1. Read `routines/idea-sweep.md`, `routines/README.md`, `projects.md`,
   `agents/shared/issue-cap.md`, `agents/spec-drift.md`, `agents/bug-error.md`,
   `agents/market-feature.md`, `agents/shared/conventions.md` per the routine.
2. Resolved the target project: **AI Landscape 2026** — repo
   `rohrasharad-ship-it/ai-landscape`, Linear project "AI Landscape", Linear Project ID
   `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`, Slack `#ai-landscape` (not used — routine is
   Linear-only), prod `https://rohrasharad-ship-it.github.io/ai-landscape/`.
3. Confirmed via the session's tool listing that the Linear MCP server requires
   authorization and exposes no tools at all in this session.
4. Because the mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`) requires
   `list_issues` against Linear, it could not be performed. Per `routines/README.md` and
   `agents/shared/issue-cap.md`, that check must happen before any role creates issues —
   so spec-drift steps 1–9, bug-error steps 1–7, and market-feature steps 1–8 were all
   skipped rather than run uncapped.
5. Spec-drift step 10 (stale-issue sweep) also needs Linear MCP (list/read/comment) —
   skipped for the same reason.
6. Spec-drift step 11 (preview-branch housekeeping): checked this session's environment
   for `LINEAR_API_KEY` — not set — so `scripts/cleanup-preview-branches.sh` could not run
   either. (This matches the still-open, separately-tracked blocker in
   `handovers/preview-branch-cleanup-linear-api-key.md` — no new information added there.)
7. Spec-drift step 12 (OpenSpec archive sweep) does not need Linear. This session cloned
   `AI-Workspace` successfully and confirmed shell/git read access works. However,
   `scripts/archive-merged-openspec-changes.sh --sweep`'s safety check
   (`has_open_pr_for_change`) depends on the `gh` CLI, which this session does not have
   (GitHub access here is GitHub-MCP-only, no `gh`/`git push` credential exercised). Running
   the sweep with that check silently disabled risks archiving a change that still has an
   open PR. Since `.github/workflows/openspec-archive.yml` already runs the same sweep
   weekly as a structural backup with real `gh` access, this session deferred to that
   scheduled Action rather than run the sweep manually with a degraded safety check.
8. No Linear issues were searched, created, or commented on this run. No `sweep-runs.jsonl`
   entry was appended — no role actually executed, so a `"clean": true` entry would
   misrepresent this as a completed no-op sweep rather than a blocked one.

## Instructions for receiving agent / human

1. If you are a human with claude.ai connector access: authorize the Linear MCP connector
   for this account so scheduled/cloud sessions can use it (Settings → Connectors, or
   wherever the Linear connector is managed). If you are an agent: verify your own session
   actually has working Linear tools before relying on this handover (try a cheap
   `list_projects` call first).
2. Once Linear MCP is confirmed working, run the Issue Cap pre-flight from
   `agents/shared/issue-cap.md` for AI Landscape 2026 (Linear Project ID
   `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
3. If under cap, run spec-drift, bug-error, and market-feature per `routines/idea-sweep.md`
   against `rohrasharad-ship-it/ai-landscape`. If at/over cap, run spec-drift steps 10–11
   only.
4. Append the `data/sweep-runs.jsonl` entry and regenerate `data/routine-log.json` per the
   routine's Output section once a role actually runs.
5. This handover is independent of `handovers/preview-branch-cleanup-linear-api-key.md` —
   do not close/delete that one based on this file; it tracks a still-open, separate
   `LINEAR_API_KEY` secret problem.
6. Delete this handover file once a run with working Linear MCP has completed (or explicitly
   found AI Landscape 2026 at cap) for this project.
