# Handover: idea-sweep for AI Workspace (PM OS) — blocked on Linear access, research done

**For:** Any agent/session with Linear MCP access (or a `LINEAR_API_KEY` env var)
**From:** idea-sweep routine run, AI Workspace (PM OS), 2026-09-18
**Blocked by:** This session has no Linear MCP tools available (the connector requires
OAuth authorization that can't be completed in a non-interactive/scheduled session) and
no `LINEAR_API_KEY` env var either. Every idea-sweep step that touches Linear — the
Issue Cap pre-flight, dedupe search, issue creation, comments, and the stale-issue
sweep — was impossible this run.
**Action:** Once Linear access exists, run the Issue Cap check for PM OS (Linear
Project ID `3703a715-c49d-4b9e-b6f1-5975d3ebe39a`), then use the research below to
either file the one recommended issue directly or confirm it's already tracked, and
re-run the stale-issue sweep (step 10) and preview-branch/LINEAR_API_KEY-dependent
housekeeping (step 11), neither of which this session could do either.
**Issue:** N/A — this run was triggered by the `idea-sweep` routine (see
`routines/idea-sweep.md`), not by a specific Linear issue assignment, so there is no
single driving issue to comment on. This file is the record instead.

---

## What this session *could* still verify without Linear

### Bug-error (step 1–2): clean
Checked Vercel production for `ai-workspace-blond.vercel.app` (project
`prj_iDnY3CHqZIZaId6RTJINJZjZnsMB`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`):
`get_runtime_errors` and `get_runtime_logs` (level error/fatal) both returned nothing
for the last 24h. Expected — per `openspec/project.md` this is a static spec-preview
sandbox with effectively no serverless surface. **Nothing to file.**

### Spec-drift gaps (steps 1–3): clean, no new gaps
Read `openspec/project.md` and all 9 files under `openspec/specs/` (agent-dispatch,
build-loop, design-reference, idea-generation, integrations, routines,
shared-conventions, spec-conversation, visual-qa) and compared against the actual
repo: `agents/*.md` + `agents/shared/*.md` (all role/shared files specced exist),
`design/` (README, resources.md, workflow.md, snippets/), `routines/*.md`,
`scripts/*.sh` + `generate-routine-log.mjs`, `.github/workflows/*.yml`, and
`index.html` (confirmed the visual-qa spec's clickable-node + animated-walkthrough
requirements are actually implemented — `selectNode`, `drawEdges`/highlight,
`animateDot`, `highlightStep`, and the two `▶ Build loop` / `▶ Idea sweep` play
buttons are all present in the JS, not just described). No specced capability is
missing or half-built this cycle.

**One real gap found, but it's process/infra, not a code gap — recommend filing:**

> 🔧 [Infra] Add `LINEAR_API_KEY` repo secret — two structural backups have failed
> every run for 2+ months
>
> **In short:** The GitHub Action secret `LINEAR_API_KEY` was never added to this
> repo, so both `preview-branch-cleanup.yml` and the routine-log dashboard refresh
> (`scripts/generate-routine-log.mjs`) have failed on every single run since at least
> 2026-07-21.
> **Problem:** `agents/shared/conventions.md` and `openspec/specs/shared-conventions/spec.md`
> both specify this Action as the non-agent-dependent structural backup for
> preview-branch cleanup — but it has never once succeeded, and the gap has been
> invisible in Linear because it's only ever been documented in a growing git
> handover file (`handovers/preview-branch-cleanup-linear-api-key.md`, now 7
> independent-session updates over a month, all re-confirming the same root cause:
> the repo also blocks mutating `git push --delete` / GitHub REST ref-deletes through
> its network proxy, so no agent session can work around the missing secret either).
> **Solution:** Add `LINEAR_API_KEY` as a repository secret (Settings → Secrets and
> variables → Actions), then re-run `preview-branch-cleanup.yml` via
> `workflow_dispatch` and `node scripts/generate-routine-log.mjs` once locally to
> confirm both succeed.
> **Why:** Without it, ~120+ orphaned `preview/*` branches never get cleaned up
> automatically, and `data/routine-log.json` (the sandbox dashboard's data source)
> has been stale since 2026-07-27 — nearly two months, despite idea-sweep running
> weekly.
> **What it looks like:** No UI change; a green Action run and a refreshed
> `/routine-log.html` are the visible confirmation.
> Suggested priority: High. Label `spec-needed`, assignee Sharad Rohra (this is a
> one-time human action — adding a repo secret — not something to hand to a
> builder agent).
>
> **Dedupe note for the filing agent:** search Linear for "LINEAR_API_KEY" /
> "preview-branch-cleanup" first — none of the 7 prior handover updates mention an
> actual Linear issue existing for this, only the git handover file, so it's
> likely genuinely untracked, but confirm before filing.

### Stale-issue sweep (step 10): blocked, not run
Needs Linear (list Backlog issues, read/post comments). Skipped entirely this run.

### Preview-branch housekeeping (step 11): blocked, not run
Same root cause as the recommended issue above — no `LINEAR_API_KEY` in this
session's environment either, so `scripts/cleanup-preview-branches.sh` can't run
here. See `handovers/preview-branch-cleanup-linear-api-key.md` for the full,
already-verified branch classification (101 safe-to-delete / 20 keep, as of
2026-08-12) — no need to re-derive it, just needs the secret + a real git push
(this session's proxy also blocks `git push --delete`, consistent with every prior
session).

### OpenSpec archive sweep (step 12): clean, ran without needing Linear
`openspec/changes/` contains only the `archive/` subfolder — no active (non-archived)
change folders exist. Nothing to archive. (Verified directly via directory listing;
didn't need to invoke `npx openspec` since the answer was already unambiguous.)

### Market-feature (steps 1–3): one candidate, speculative
Read `openspec/project.md` vision + Out of Scope (ruled out proposing the "Capture
agent" Slack/voice-note feeder — it's explicitly listed as Out of Scope, not just
unbuilt) and all capability specs.

> 🗂️ [Feature] Surface open `handovers/*.md` blockers on the PM OS dashboard
>
> **In short:** Add a small "Blocked handovers" panel to `routine-log.html` (or the
> `index.html` architecture map) listing open files under `handovers/`, their age,
> and their `Blocked by:` line.
> **Problem:** Handovers are currently invisible except by reading git directly —
> this run is itself an example: the `LINEAR_API_KEY` blocker above has now been
> independently re-discovered and re-documented by 7+ separate idea-sweep sessions
> over a month, each spending tokens re-verifying a blocker a dashboard glance could
> have surfaced instantly.
> **Solution:** A build step (or the existing `generate-routine-log.mjs` refresh)
> parses `handovers/*.md` headers (`For:`/`From:`/`Blocked by:`) and lists them.
> **Why:** Directly serves this project's own vision — visibility into the AI-first
> loop — and prevents the exact token waste observed this run.
> **What it looks like:** A small card list, same visual language as the existing
> per-project sweep cards on `routine-log.html`.
> Suggested priority: Low/Medium — speculative, not a confirmed gap.
>
> **Dedupe note:** search Linear for "handover" / "dashboard" before filing —
> not yet in `openspec/specs/` or (as far as this session could tell without
> Linear access) tracked as an issue.

## Instructions for receiving agent

1. Get Linear access (MCP or `LINEAR_API_KEY`).
2. Run the Issue Cap check for PM OS (`3703a715-c49d-4b9e-b6f1-5975d3ebe39a`) — if
   at/over cap (5), skip filing both candidates above this cycle (housekeeping
   steps below still apply).
3. Search Linear per the dedupe notes above; file whichever candidate(s) aren't
   already tracked, following Issue Brief format and New Issue Conventions.
4. Run the stale-issue sweep (spec-drift step 10) for PM OS.
5. If `LINEAR_API_KEY` is now available, run `scripts/cleanup-preview-branches.sh`
   and `node scripts/generate-routine-log.mjs`; if git push is still blocked by a
   network proxy in your session, note that in the existing
   `handovers/preview-branch-cleanup-linear-api-key.md` file rather than opening a
   new one.
6. Delete this file once both candidates above are filed or confirmed duplicate,
   and the stale-issue sweep has run — the sweep-ledger line for this date already
   records the run as blocked, no need to keep this file once the follow-up work
   above is complete.
