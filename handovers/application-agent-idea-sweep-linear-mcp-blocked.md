# Handover: idea-sweep routine blocked for Application Agent — no Linear MCP in this session

**For:** Any agent/session with Linear MCP access
**From:** Scheduled `idea-sweep` routine run, Application Agent, 2026-09-16 (this session had no Linear connector)
**Blocked by:** Linear MCP server is not authorized in this session (`ReadNotifications`/tool listing marked it "requires authentication before its tools can be used" — no `mcp__Linear__*` tools were ever exposed to try). No Playwright/browser tool was available either.
**Action:** Re-run `idea-sweep` for **Application Agent** from a session that has Linear MCP + Playwright, using the research below as a head start, then do the Issue Cap pre-flight and dedup search before filing anything.
**Issue:** none (this is a routine-level blocker, not a single Linear issue)

---

## Payload

### What actually blocked this run

Followed `routines/idea-sweep.md` exactly. Read `routines/README.md`, `agents/spec-drift.md`,
`agents/bug-error.md`, `agents/market-feature.md`, `agents/shared/issue-cap.md`,
`agents/shared/conventions.md`, and `projects.md`. Target resolved to:

| Field | Value |
|---|---|
| Repo | `rohrasharad-ship-it/Application-Agent` |
| Linear Project | Application Agent |
| Linear Project ID | `7dc5202c-a586-4bed-b2d3-fba10f2dd913` |
| Slack Channel | #application-agent (not used — idea-generation is Linear-only) |
| Vercel Prod | `TBD` in `projects.md` |

Every one of the three roles needs Linear MCP for its very first mandatory step
(Issue Cap pre-flight — `agents/shared/issue-cap.md`) before anything else can run.
This session had no Linear connector at all, so:

- **Issue Cap pre-flight**: could not be done — don't know if Application Agent is
  at/under the 5-issue cap.
- **spec-drift**: could do the reading (steps 1–3, see below) but not step 4
  (dedup search), step 5 (create), or steps 10–12 (stale-issue sweep, preview-branch
  housekeeping, openspec-archive housekeeping all read/write Linear issue state).
- **bug-error**: additionally blocked structurally — `projects.md` lists Vercel Prod
  as `TBD` for Application Agent. This is a Python CLI/agent project (see
  `README.md`/`openspec/project.md`) with no web deployment yet, so there is no
  production URL or Vercel log source to read regardless of Linear access. This
  role is **not applicable** to this project right now, not just blocked.
- **market-feature**: could do the reading (steps 1–2) but not the dedup search or
  filing.
- No Playwright/browser tool was available in this session either, so even if
  Linear worked, the mandatory Visual Self-QA screenshot step (every role) and any
  visual-preview step could not have been completed.

**Net result: nothing was filed, nothing was searched for duplicates, and the
stale-issue/branch/openspec housekeeping sweeps did not run this cycle.** This is
not a "clean" run in the `data/sweep-runs.jsonl` sense — it's a blocked one. See
ledger entry appended below.

### Research already done (to save the next agent a pass)

Read `README.md`, `openspec/project.md`, and every `openspec/specs/*/spec.md`
capability file, plus the `src/application_agent/*` module listing, for
Application Agent. Notes below are **candidates only** — the next agent must
still search Linear for dedup (title/keywords) per `agents/shared/issue-brief.md`
and `agents/shared/conventions.md` before filing anything, and must run the
Issue Cap pre-flight first.

#### Spec-drift candidates — explicit "Open / Next" items each capability spec already flags as unbuilt

These are the project's own admission of planned-but-not-shipped work, pulled
straight from each spec's `## Open / Next` section as of commit on `main`
(`openspec/specs/*/spec.md`):

- **browser** (`openspec/specs/browser/spec.md`):
  - Slack command to trigger laptop fill remotely (orchestrator currently requires
    a local CLI invocation — `application-agent fill`).
  - Cloud headless Mode 2 for low-stakes opt-in submits (events/hackathons) — spec
    describes it but `src/application_agent/browser/` only has `cdp.py`,
    `discovery.py`, `fill.py`, `fill_session.py`, `guard.py`, `snapshot.py` — no
    headless-cloud submit path visible in the file list.
  - ATS-specific selector fallbacks as patterns emerge (open-ended, low priority).
- **generation** (`openspec/specs/generation/spec.md`):
  - Ghost-job / low-quality posting scoring (optional, inspired by `career-ops`
    prior art) — no scoring module in `src/application_agent/generation/`.
  - **Caution**: the spec also lists "PDF export for tailored resumes" under
    Open/Next, but `src/application_agent/generation/resume_export.py` (10KB)
    already exists — this looks like a **stale spec note**, not a real gap. Worth
    a spec-drift "already done?" check/comment rather than a new issue.
- **integrations** (`openspec/specs/integrations/spec.md`):
  - MCP wiring for **Indeed** (job search) and **Notion** (optional profile/tracker
    mirror) — confirmed unbuilt: `src/application_agent/integrations/` only has
    `apollo/`, `linear/`, `slack/` subdirectories, no `indeed` or `notion`.
  - Slack bot/app event-subscription setup — partially ambiguous since
    `integrations/slack/` already exists; verify against the live Slack app config
    before filing (may already be done).
- **orchestrator** (`openspec/specs/orchestrator/spec.md`):
  - Slack command to trigger laptop fill from a thread (same underlying gap as the
    browser one above — likely **one issue, not two**, if filing both).
  - Resume PDF upload automation during the fill session.

None of these were checked against Linear for existing tracking — that's the
required next step, not a step this session could take.

#### Market-feature seed ideas (unvalidated — need Linear dedup + a visual before filing)

Speculative, not yet checked against `openspec/project.md`'s Out of Scope list
(re-verify — nothing here should conflict with "no fully-autonomous submission",
"never touch linkedin.com", or "no background email polling"):

1. **Application funnel dashboard** — `tracker` already has a full status lifecycle
   (`captured → prepping → ready → in_progress → submitted/skipped`) and per-track
   resume data; a simple view of conversion rate by resume track / by source could
   differentiate this from generic ATS-autofill tools, ties directly to the
   product's "tracker is the asset" priority in `README.md` §3.
2. **Pre-prep fit/comp check** — before running the full generation pipeline on a
   captured lead, do a cheap check of posting comp/location against
   `profile/preferences.yaml` deal-breakers and flag likely-mismatch postings in
   the Slack capture thread, so prep isn't spent on postings the user would skip
   anyway.
3. **Follow-up reminder nudges** — `tracker` spec mentions "follow-up dates" as
   part of the audit log's job, but no spec or module surfaced a follow-up
   scheduling/reminder mechanism; a Slack nudge N days after `submitted` with no
   response could close that loop.

These are ideas only — the market-feature role's own job (steps 3–9) still needs
to run for real: web search for comparable products, Linear dedup, cap check,
and the mandatory visual preview + screenshot.

### Ledger

Per `routines/idea-sweep.md` Output section, appended this line to
`data/sweep-runs.jsonl` (this session, via GitHub API — see commit history):

```json
{"at":"2026-09-16T00:00:00Z","project":"Application Agent","filed":{"bugs":0,"features":0},"clean":false,"blocked":"no-linear-mcp-in-session"}
```

Note the added `blocked` field is non-standard (the routine's schema only defines
`at`/`project`/`filed`/`clean`) — flagging it here so whoever runs
`scripts/generate-routine-log.mjs` next knows this line represents a blocked run,
not a genuine "swept and found nothing" result, and can decide whether the
dashboard/script needs to handle that distinction.

## Instructions for receiving agent

1. Confirm Linear MCP tools and a Playwright/browser tool are actually available
   in your session before starting (don't assume — check the tool list first).
2. Do the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Application
   Agent (`7dc5202c-a586-4bed-b2d3-fba10f2dd913`) — paginate `list_issues`,
   filter by project ID not name.
3. If under cap: run spec-drift steps 1–9 using the candidates above as a
   starting point (still re-read the specs yourself — this list is not
   exhaustive and the spec files may have changed since this was written),
   dedup-search Linear, then file. Also run steps 10–12 (stale-issue sweep,
   preview-branch housekeeping, openspec-archive housekeeping) regardless of cap.
4. If under cap: run market-feature steps 1–9 using the seed ideas above,
   with a real web search and a real visual preview + screenshot.
5. Treat bug-error as **not applicable** for Application Agent until
   `projects.md`'s Vercel Prod field is filled in with a real deployment — don't
   spend time on it, and don't file a "blocked" note for it (it's a project-config
   gap, not a tool-access gap).
6. Once real issues are filed (or a clean "nothing found" run completes), replace
   the ledger line above with a normal `clean:true`/counts line reflecting the
   actual outcome, and run `node scripts/generate-routine-log.mjs` (needs
   `LINEAR_API_KEY`) to refresh `data/routine-log.json`.
7. Delete this handover file once Application Agent's idea-sweep has actually run
   to completion — until then it's the record of why this cycle produced nothing.

## Also worth flagging to Sharad (not actionable by an agent)

There are ~29 open `claude/festive-goodall-*` branches on this repo from prior
scheduled `idea-sweep` runs (branch-per-run, never merged/cleaned up), plus this
run's own `claude/festive-goodall-jcvd8k`. Separately, `data/sweep-runs.jsonl`
shows three prior Application Agent runs (2026-07-11, 2026-08-06, 2026-08-19)
logged as `clean:true` — if those also lacked Linear MCP, that history may be
overstating how many real sweeps have happened for this project. Worth checking
whether the scheduled trigger's session is missing the Linear connector
consistently, not just this one time.
