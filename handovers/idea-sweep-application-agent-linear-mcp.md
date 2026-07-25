# Handover: idea-sweep for Application Agent could not file issues — Linear MCP unauthenticated

**For:** Any agent/session with an authenticated Linear MCP connection
**From:** Claude (scheduled `idea-sweep` routine run), 2026-07-25
**Blocked by:** Linear MCP tools require OAuth authorization that this non-interactive
scheduled session cannot complete (`/mcp` flow needs a human). No `LINEAR_API_KEY`
env var is set either, so even the shell-script fallback (`cleanup-preview-branches.sh`)
can't run.
**Action:** Run the Issue Cap pre-flight for **Application Agent**
(Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`), then — if under cap —
search Linear to dedupe and file the candidate issues below.
**Issue:** N/A — this handover originates from a scheduled `idea-sweep` routine run,
not an existing Linear issue. No Linear issue exists yet for this blocker.

---

## What happened

`routines/idea-sweep.md` was triggered for **Application Agent**
(`rohrasharad-ship-it/Application-Agent`). All three idea-generation roles
(`spec-drift`, `bug-error`, `market-feature`) need Linear MCP for their very first
mandatory step — the Issue Cap pre-flight (`agents/shared/issue-cap.md`) — which
this session could not perform:

- Linear MCP tools are listed as requiring authentication; this session is a
  non-interactive scheduled run, so the OAuth flow could not be completed.
- `LINEAR_API_KEY` is not set in this session's environment, so the housekeeping
  script fallback (`scripts/cleanup-preview-branches.sh`, spec-drift step 11) also
  hard-fails (`error: LINEAR_API_KEY is required`).

Per `agents/shared/conventions.md` → **Blocked-agent handover** (this is one of the
named example triggers: "no Linear MCP"), this session did the read-only work that
doesn't require Linear and stopped short of filing anything, rather than guessing
at dedupe or skipping silently.

## What was still done (no Linear required)

1. **Vercel check** — `list_projects` for the account's only team
   (`team_P5vgMhFNfh2d4fCe2YkRLjey`) returns only `ai-workspace`, `usercon`,
   `resume-website`, `ai-landscape`. **No Vercel project exists for Application
   Agent** — matches `projects.md`'s "TBD" prod URL. **bug-error has nothing to
   read this cycle** — not "clean," just not deployed yet. Skip it until a prod
   URL exists.
2. **Spec-drift reading** (steps 1–3, no Linear) — read `openspec/project.md` and
   all six capability specs (`profile`, `generation`, `tracker`, `integrations`,
   `browser`, `orchestrator`) in the Application-Agent repo. Each spec's own
   `Status` / `Open / Next` sections self-report shipped vs. planned (with SHA
   references), which is what the candidate gaps below are drawn from. **This is
   not a full code-vs-spec diff** — a receiving agent should do a quick source
   check (`src/`) before filing, per spec-drift step 2, since specs could be
   stale in either direction.
3. **Market-feature reading** (steps 1–2, no Linear) — read the vision, Build
   Order, and Out-of-Scope list in `openspec/project.md` to reason about
   genuinely new features.
4. **Steps not attempted**: spec-drift step 10 (stale-issue sweep — needs
   Linear), step 11 (preview-branch cleanup — needs `LINEAR_API_KEY`), step 12
   (OpenSpec archive sweep — doesn't need Linear, but does need the `gh` CLI for
   safe open-PR detection, which this session doesn't have; skipped rather than
   risk archiving a change with an open PR. This already runs weekly via
   `.github/workflows/openspec-archive.yml`, so nothing here needs the manual
   sweep to compensate).

## Payload — candidate issues to file (once cap-checked and Linear-deduped)

**None of these have been filed. None have been checked against Linear for
duplicates. Do the Issue Cap check and a Linear search first** — some may already
be tracked.

### Spec-drift candidates (real planned-but-unbuilt gaps, cap 5)

1. **📥 Indeed MCP job-discovery integration** — `integrations/spec.md` lists
   Indeed as "Planned Integrations... remains planned"; `orchestrator/spec.md`
   assumes it ("Indeed MCP may supplement discovery but does not auto-start prep
   without a capture") but no MCP wiring exists yet.
2. **🌐 Cloud headless Mode 2 (low-stakes auto-submit)** — `browser/spec.md`
   Status: "Cloud headless Mode 2 remains planned." Events/hackathons with
   explicit per-item opt-in have no implementation yet, only the CDP
   laptop-fill mode (Mode 1) is built.
3. **💬 Slack command to trigger laptop fill remotely** — listed as Open/Next in
   *both* `browser/spec.md` and `orchestrator/spec.md`. Today fill only starts
   via local CLI (`application-agent fill --id <app-id>`); the "Slack is the
   remote-control surface for everything except fill/submit" promise in
   `project.md` is only half true until this exists.
4. **📅 Follow-up date tracking on tracker entries** — `openspec/project.md`'s
   own one-line description of the `tracker` capability says it is "an audit log
   of every application/email/event plus follow-up dates," but
   `tracker/spec.md`'s actual schema/status lifecycle has no follow-up-date
   field or behavior anywhere. This is a drift between the top-level vision doc
   and the capability's own spec — worth confirming whether it was quietly
   dropped or just never written down.
5. **📄 PDF export for tailored resumes** — `generation/spec.md` Open/Next:
   "PDF export for tailored resumes — writes `data/artifacts/{app_id}/` and
   stores path on `FillCompanion`." Not shipped; resumes are currently `.docx`
   only per `profile/spec.md`.

### Market-feature candidates (genuinely new, cap 3 — only 2 proposed; see note)

1. **🎤 Post-submission interview support** — every capability's lifecycle stops
   at `submitted`/`skipped` (`tracker/spec.md` status lifecycle has no stage
   past `submitted`). The product already builds a company-context brief
   (`generation` SHA-189) and a portfolio blurb (SHA-190) per application —
   extending that into an interview-prep pack (likely questions, talking
   points drawing from `profile/projects.yaml` + the existing company brief)
   would carry the differentiation from "get the application out the door" to
   "help win the offer," without touching the no-auto-submit non-negotiable.
2. **📊 Outreach-effectiveness digest** — the tracker already correlates cold
   outreach (Apollo contacts, SHA-116) with application outcomes in one JSON
   store, but nothing surfaces that correlation back to the user. A periodic
   Slack digest ("cold emails to hiring managers had a 2x reply rate vs.
   recruiters this month") would use data the system already collects and
   differentiate from plain trackers (Huntr/Teal) that don't link outreach to
   outcome.

   *Only two proposed, not three — no third idea felt genuinely differentiated
   rather than filler; per `agents/market-feature.md` step 9, better to under-fill
   than invent one.*

### Structural note (not an issue, just flag for the receiving agent)

Application Agent has **no web frontend** — it's a Slack bot + CLI backend, and
its Vercel prod URL is "TBD" (not deployed). The shared idea-generation
guardrails mandate a real Playwright screenshot of "the live site" for every
issue created (`agents/shared/visual-self-qa.md`) and a visual preview for
UI-bearing issues (`agents/shared/visual-specs.md`) — neither maps cleanly onto
a product whose only user-facing surface is Slack messages. Worth a short
conversation with Sharad on what "visual QA" means here (e.g. a screenshot of
the rendered Slack thread/fill-companion message) before the receiving agent
tries to force a live-URL screenshot that doesn't exist.

## Instructions for receiving agent

1. Run the Issue Cap pre-flight for Application Agent
   (`7dc5202c-a586-4bed-b2d3-fba10f2dd913`) per `agents/shared/issue-cap.md`.
   If at/over cap (5), stop — post the skip message to `#application-agent` and
   do not file any of the candidates above.
2. If under cap, search Linear first for each candidate above — several may
   already be duplicates of open work; skip any that are.
3. For survivors, do a quick `src/` check to confirm each is genuinely unbuilt
   (specs can drift in either direction), then file per each role's own
   Instructions (`agents/spec-drift.md` step 5, `agents/market-feature.md`
   step 5) — Backlog, `spec-needed`, assignee Sharad Rohra, emoji title,
   Issue Brief description, first-comment execution detail citing this
   handover and the spec file(s) referenced above.
4. Resolve the visual-QA structural note above (either with Sharad or by
   using a rendered Slack-message mock) before attaching screenshots.
5. Post the consolidated per-project Slack summary to `#application-agent`
   per `routines/idea-sweep.md` once filing is done (or confirm the skip
   message already covers it if at cap).
6. Delete this handover file once Application Agent's idea-sweep has fully
   caught up (either these issues are filed, or explicitly declined) and that
   is tracked elsewhere.
