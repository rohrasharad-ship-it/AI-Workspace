# Handover: idea-sweep routine for Application Agent — no Linear MCP access in this session

**For:** Any agent/session with Linear MCP access
**From:** idea-sweep routine run (Claude Code cloud session), 2026-08-29
**Blocked by:** This session has GitHub MCP (read + write) and Vercel MCP tools, but no Linear MCP tools at all — the Linear connector is unauthenticated and this is a non-interactive session, so the OAuth flow can't be completed here. Every step of `routines/idea-sweep.md` needs Linear: the mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`, `list_issues`), dedupe search before filing, issue creation, and first-comment posting.
**Action:** Run the Issue Cap check for **Application Agent** (Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`, from `projects.md`), then file whichever of the candidates below still make sense (search first — some time has passed since this research) as Backlog + `spec-needed` issues per `agents/shared/issue-brief.md` and `agents/shared/conventions.md`.
**Issue:** N/A — this is a routine run, not a single driving issue.

## Context: this is a repeat of a known, unresolved pattern

This is not a one-off. `handovers/linear-issue-vercel-preview-blocker.md` (July 2026) already opens with "Cloud agent sessions do not have Linear MCP connected," and `handovers/preview-branch-cleanup-linear-api-key.md` logs 7 consecutive idea-sweep runs (across three different projects, 2026-08-02 through 2026-08-12) all hitting Linear-adjacent access walls (missing `LINEAR_API_KEY` secret, git-push-delete blocked by the proxy). Both of those are still open on `main`, unresolved, months later. Worth surfacing to Sharad directly: **idea-sweep as currently designed may not be runnable end-to-end by any session type that actually gets triggered for it** — every recorded run either has no Linear MCP (this one, the Vercel-blocker one) or has Linear MCP but not the shell/secret access the housekeeping steps need. If that's still true, it may be worth Sharad wiring up a persistent Linear OAuth grant for scheduled/cloud sessions specifically, rather than relying on each run's ad hoc handover.

## What I could and couldn't do this run

- **Could not** run the Issue Cap pre-flight (needs `list_issues`) — so per `agents/shared/issue-cap.md`, no issue should be filed blind without it.
- **Could not** search Linear for existing/duplicate issues.
- **Could not** create issues, attach screenshots, or post comments.
- **Bug-error role is not currently actionable anyway**: `projects.md` lists Application Agent's Vercel Prod as `TBD`, and `openspec/project.md`'s own tech-stack section describes hosting as "cloud always-on service (TBD)" — there is no production URL to pull runtime logs from. Nothing to hand over for that role beyond this note.
- **Did do** the read-only research both spec-drift and market-feature would normally act on — see Payload below — so the receiving agent can go straight to the cap check + filing instead of re-reading the whole repo.

## Payload: candidate issues (verify + dedupe before filing — do not file as-is without a fresh Linear search)

Researched via GitHub MCP against `rohrasharad-ship-it/Application-Agent`: `openspec/project.md`, all 6 spec files (`browser`, `generation`, `integrations`, `orchestrator`, `profile`, `tracker`), all `openspec/changes/` proposals (active + archived, to exclude in-flight work), and the full `src/application_agent/` tree + `tests/`.

### Spec-drift candidates (up to 5, cap per `agents/spec-drift.md`)

1. **No Indeed integration** — `integrations/spec.md` and `project.md` both list Indeed as a planned job-search source; `src/application_agent/integrations/` only has `apollo/`, `linear/`, `slack/`. Proposed: an Indeed MCP/API client that feeds the existing `/capture` prep pipeline (never auto-starts it).
2. **No Notion sync for profile/tracker** — both specs list it as an optional mirror; zero `notion` references anywhere in `src/` or `openspec/changes/`. Proposed: thin, env-var-gated optional sync client, repo files remain source of truth (per spec).
3. **Cloud headless Mode 2 (low-stakes auto-submit) unbuilt** — `browser/spec.md` defines two architectural modes; only the laptop/CDP mode (`cdp.py`, `discovery.py`, `fill.py`, `fill_session.py`, `guard.py`, `snapshot.py`) exists. Spec itself says "Cloud headless Mode 2 remains planned." Proposed: `browser/headless.py`-style cloud runner gated by the per-item opt-in flag already modeled in `tracker`.
4. **No Slack-triggered remote laptop fill** — both `browser/spec.md` and `orchestrator/spec.md` list this as open; `integrations/slack/app.py` has `/capture`, `/outreach`, `/queue`, thread keywords, and the `app_start/app_skip/app_submitted` buttons, but nothing invokes fill (fill is CLI-only via `cli.py`). Proposed: a Slack action that queues a fill request the laptop CLI picks up on next poll — no change to the "human clicks submit" non-negotiable.
5. **No follow-up-date tracking** — `project.md` itself describes the tracker as "the audit log of every application/email/event plus follow-up dates," but there's no such field; `search_code` for `follow_up` returns zero hits repo-wide. Proposed: `follow_up_at` field on `Application`, set on status transitions, surfaced via `/queue`.

### Market/feature candidates (up to 3, cap per `agents/market-feature.md` — none of these are in `openspec/project.md`'s Out of Scope section)

1. **Audit-log analytics view** — the tracker's audit log sits unused as pure history; `tracker/spec.md` says this log "alone must justify the project's existence." Proposed: lightweight CLI/Slack `/stats` report (response rate, time-to-response, outcomes by resume track/channel).
2. **Interview-prep generator** — pipeline stops at "Ready to apply," nothing helps once a reply arrives. Proposed: on marking an app interview-stage, draft likely questions + STAR-style talking points from `profile/projects.yaml` and the existing `company_brief`, reusing the truthfulness-attribution machinery already built for cover letters.
3. **Recruiter-reply draft assistant** — no help for post-apply back-and-forth. Proposed: Slack command where the user pastes a recruiter's message and gets a draft reply (schedule/negotiate/decline) — manual paste-in only, stays clear of the Gmail-ingestion Out-of-Scope item, mirrors the existing cold-email drafting pattern.

## Instructions for receiving agent

1. Run the Issue Cap check for Application Agent (`agents/shared/issue-cap.md`, project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`). If at/over 5 active pipeline issues, stop — do not file any of the below this cycle.
2. If under cap: search the Application Agent Linear project for each candidate above; drop any already tracked (including anything filed since 2026-08-29).
3. File the survivors per `agents/shared/conventions.md` + `agents/shared/issue-brief.md` (Backlog, `spec-needed`, assignee Sharad Rohra, emoji-led title, Issue Brief description, first comment with the spec/code refs noted above, screenshot per `agents/shared/visual-self-qa.md`).
4. Also run spec-drift steps 10–12 (stale-issue sweep + preview-branch/OpenSpec-archive housekeeping) for Application Agent if not already done elsewhere this cycle — this handover only covers steps 1–9 (gap-filing) and the market-feature role.
5. Append the sweep-ledger line to `data/sweep-runs.jsonl` per `routines/idea-sweep.md` once filing is done, and run `node scripts/generate-routine-log.mjs`.
6. Consider flagging the "Context" section above (repeat Linear-access pattern across cloud sessions) to Sharad directly, separate from this specific project's issues — it's a process gap, not something to file as a normal Application Agent issue.
7. Delete this handover file once filing is complete and the ledger is updated.
