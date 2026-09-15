# Handover: idea-sweep routine for Application Agent could not run — no Linear access in this (scheduled) session

**For:** Any agent session with live Linear MCP access (or a `LINEAR_API_KEY` secret) for `rohrasharad-ship-it/Application-Agent`
**From:** idea-sweep routine run (all three roles: spec-drift, bug-error, market-feature), triggered as a scheduled/automated task, 2026-09-15
**Blocked by:** Linear MCP server requires OAuth in this session; the session is non-interactive (scheduled trigger) so the OAuth flow can't run. No `LINEAR_API_KEY` env var is set as a fallback either (checked — absent).
**Action:** Once Linear access exists, run the issue-cap pre-flight and all applicable idea-sweep steps for Application Agent (Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`), using the pre-researched candidates below as a starting point — not a checklist to file blindly.
**Issue:** none — this is a routine-level blocker, not tied to one Linear issue.

## Payload

### Root cause (affects every scheduled idea-sweep run, not just this project)

This session had Linear listed under "MCP servers that require authentication before
their tools can be used," with an explicit note that non-interactive sessions can't
complete OAuth. `env | grep -i linear` also came back empty, so the script-based
fallback (`LINEAR_API_KEY`, used by `cleanup-preview-branches.sh` and
`generate-routine-log.mjs`) isn't available either. That second gap is already tracked
in depth — see `handovers/preview-branch-cleanup-linear-api-key.md` (7 independent
sessions have hit it since 2026-08-02; root cause confirmed as a proxy policy blocking
git-ref deletes and GitHub REST writes for git operations, not something this session
should re-verify). **This handover is about the first gap** — Linear MCP OAuth itself
being unavailable to scheduled/cron-triggered sessions, which is a broader problem: even
if the `LINEAR_API_KEY` secret above gets fixed, a scheduled idea-sweep session still
can't do anything Linear-related (issue cap check, search, file, comment) unless
something durable (an API key available to scheduled sessions, or a persisted OAuth
grant) is wired up. Worth flagging to whoever owns the co-work/cron scheduling setup —
this isn't fixable from inside a routine run.

### What this blocked, concretely

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — mandatory before any
  filing, requires `list_issues`. Not done.
- **spec-drift steps 1–9** (gap-filing) — steps 1–3 (read openspec + propose gaps) were
  done as research only, below; steps 4–9 (Linear dedupe search, filing, screenshots,
  comments) not done.
- **spec-drift step 10** (stale-issue sweep) — requires `list_issues` + comments. Not done.
- **spec-drift step 11** (preview-branch housekeeping) — script hard-requires
  `LINEAR_API_KEY`; already tracked, see above. Not attempted again here.
- **spec-drift step 12** (OpenSpec archive sweep) — doesn't need Linear, but needs a
  local clone of AI-Workspace with `npx openspec`/`jq`, which this session doesn't have
  (no working directory git repo). Not attempted; needs a session with shell + repo access.
- **bug-error** (all steps) — blocked twice over. Linear access aside, `projects.md`
  lists Application Agent's Vercel Prod as `TBD`. Worth a second look at whether "Vercel
  Prod" is even the right signal for this project: per `openspec/project.md`, Application
  Agent's runtime is a Slack bot + Python cloud service + laptop CLI, not a Vercel web
  app like the other rows in `projects.md` — hosting is listed as "cloud always-on
  service (TBD)." Someone should decide the real error/log source for this project
  (structured logs from wherever the always-on service ends up hosted, Sentry, etc.)
  rather than leaving bug-error permanently pointed at a Vercel URL that may never exist.
- **market-feature steps 1–3** (read vision, propose ideas) — done as research only,
  below; steps 4–9 (dedupe, filing, visuals, screenshots, comments) not done.

### Context: prior runs

`data/sweep-runs.jsonl` shows three prior clean idea-sweep runs for Application Agent
(2026-07-11, 2026-08-06, 2026-08-19 — all `filed: {bugs:0, features:0}, clean:true`).
Those sessions evidently had working Linear access and still filed nothing, which is
useful context for the candidates below: several of them are things the project's own
spec files already list under "Open / Next," so a prior clean run may well have already
considered and consciously deferred them as roadmap items rather than drift. Treat the
candidates below as leads to check against Linear, not a pre-approved filing list —
**do not file all of them just to use them up.**

### Pre-researched spec-drift candidates (read openspec/project.md + all 6
openspec/specs/*/spec.md files; did not read `src/` in depth — verify against actual
code before filing)

**Higher confidence — direct spec inconsistency, not just a roadmap note:**

1. **Follow-up dates aren't tracked anywhere.** `openspec/project.md`'s own one-line
   description of `tracker` says it's "an audit log of every application/email/event
   plus follow-up dates." `openspec/specs/tracker/spec.md` has no mention of a
   follow-up-date field, schedule, or reminder anywhere in Status, Storage, Status
   lifecycle, or Requirements. Looks like a real gap between the stated charter and the
   spec/implementation, not a deferred roadmap item.
2. **Tracker lifecycle stops at `submitted`/`skipped` — no post-submission outcome.**
   `tracker/spec.md`'s Non-Negotiables say tracker "alone must justify the project's
   existence" and "treat logging completeness as a hard requirement," but the lifecycle
   (`captured → prepping → ready → in_progress → submitted | skipped`) never records
   what happened after submission (interview, offer, rejection). For a project whose
   core value proposition is the audit trail, this seems like a meaningful, not cosmetic, gap.

**Lower confidence — already self-documented as "Open / Next" in the specs, so likely
already seen and possibly intentionally deferred; only file if Linear confirms it's not
already tracked or consciously parked:**

3. Indeed MCP integration for job discovery (`integrations/spec.md` Status: "Indeed …
   remain planned").
4. Slack command to trigger laptop fill remotely — currently local-CLI-only
   (`application-agent fill`); listed in both `browser/spec.md` and
   `orchestrator/spec.md` Open/Next.
5. Cloud headless Mode 2 (low-stakes auto-submit for events/hackathons opted in) —
   `browser/spec.md` Status: "Cloud headless Mode 2 remains planned."

### Pre-researched market-feature candidate (speculative — not implied by any existing
spec; needs full Linear dedupe before filing; cap for this role is 3, only proposing 1
since I couldn't verify it's genuinely novel without searching Linear)

1. **Weekly Slack pipeline digest.** `/queue` (existing, shipped) is an on-demand,
   ephemeral pull. Nothing proactively summarizes pipeline health over time — e.g. a
   Monday recap of "N captured, N ready-but-untouched >3 days, N submitted this week."
   Ties directly to the project's differentiation goal (removing manual grind) without
   touching anything out-of-scope (no LinkedIn, no auto-submit, no Gmail). Needs a
   visual mockup of the Slack message per `agents/shared/visual-specs.md` before filing.

## Instructions for receiving agent

1. Get Linear access (MCP or `LINEAR_API_KEY`) working for a session that can also
   reach `rohrasharad-ship-it/Application-Agent` and `rohrasharad-ship-it/AI-Workspace`.
2. Run the Issue Cap pre-flight for Application Agent (`agents/shared/issue-cap.md`,
   project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`). If at/over cap, stop per the
   routine's own rules (still run spec-drift steps 10–11 if a working `LINEAR_API_KEY`
   is available for step 11's script).
3. If under cap: for each candidate above, search Linear first. File only the ones that
   are (a) not already tracked and (b) still look like real gaps on a fresh read of
   `src/` — don't file #3–5 without checking they weren't deliberately deferred.
4. Do the stale-issue sweep (step 10) and, if `LINEAR_API_KEY` is fixed by then, the
   housekeeping scripts (step 11 — but see the existing handover first, don't
   re-diagnose) and step 12 (needs a real clone + `npx openspec`, not Linear-gated).
5. Decide what to do about bug-error's missing target (see the Vercel Prod / hosting
   note above) — either register a real log source in `projects.md` or explicitly note
   bug-error is N/A for this project until a deployment exists.
6. Once this handover's guidance has been acted on (candidates evaluated, sweep run),
   delete this file — it's not meant to persist as a permanent artifact.
