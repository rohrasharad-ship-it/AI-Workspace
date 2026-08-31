# Handover: File idea-sweep candidates for Application Agent (Linear MCP unavailable)

**For:** Any agent/session with Linear MCP access (or a valid `LINEAR_API_KEY`)
**From:** `idea-sweep` routine run, Claude (scheduled trigger), 2026-08-31
**Blocked by:** Linear MCP requires OAuth in this session; the session is
non-interactive (scheduled task) so the auth flow can't run. No
`LINEAR_API_KEY` env var is set either, so there is no fallback path. This
blocks: the Issue Cap pre-flight, Linear dedupe search, issue creation,
first-comments, and the spec-drift stale-issue sweep/comments — i.e. every
Linear-touching step of `routines/idea-sweep.md` for every one of the three
roles (spec-drift, bug-error, market-feature).
**Action:** Run the Issue Cap pre-flight for **Application Agent**
(project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`, see `agents/shared/issue-cap.md`);
if under cap, dedupe-search and file the candidate issues below (up to 5
spec-drift + up to 3 market-feature, both already capped in this handover);
if any turn out to already be tracked, skip that one and file the rest.
**Issue:** None — this run was triggered by the `idea-sweep` schedule, not by
an existing Linear issue.

---

## What this session *could* and *couldn't* do

- **bug-error**: Application Agent has no live deployment (`projects.md` lists
  its Vercel Prod as `TBD` — it's a Slack/CLI backend agent, not a hosted
  site). There is nothing to pull runtime errors from. Nothing to hand off
  here; this role is a legitimate no-op for this project, not a blocker.
- **spec-drift / market-feature research (steps 1-3 of each role)**: done in
  full — see Payload below. This required no Linear access, only GitHub read
  access to `rohrasharad-ship-it/Application-Agent`.
- **Issue Cap pre-flight, Linear dedupe search, `save_issue`, first-comments,
  stale-issue sweep (spec-drift step 10), preview-branch/openspec-archive
  housekeeping (spec-drift steps 11-12)**: none of this ran. Steps 11-12 also
  need `LINEAR_API_KEY` (step 11) and/or `gh` CLI (the archive script's
  `has_open_pr_for_change` check), neither of which is available in this
  session regardless of the Linear MCP gap.
- **No visual previews / screenshots were attempted.** Application Agent has
  no UI surface to screenshot (see bug-error note above) — every candidate
  below is backend/process, so `agents/shared/visual-self-qa.md` doesn't
  apply here. Do not treat the missing screenshots as a shortcut taken; there
  is nothing to screenshot for this project.

## Payload — candidate issues to file

Evidence below refers to files in `rohrasharad-ship-it/Application-Agent` at
`main` as of this run (commit `25260a2569121cd3a3df260d488912b542ba64ff`).
Re-verify against current `main` before filing, and run the dedupe search
per `agents/shared/issue-cap.md` / `routines/README.md` before creating each
one — these were reasoned from spec-vs-code comparison only, not checked
against Linear.

### Spec-drift candidates (up to 5, cap: 5)

**1. 🐛 Job updates post twice in the same Slack thread**
- In short: Duplicate Slack messages on capture
- Problem: When a new job link is captured, the ready-to-apply package
  (company summary, cover letter, resume, contact suggestions) gets posted
  once in the immediate reply, then posted again as separate follow-up
  messages in the same thread — including a second, extra set of action
  buttons.
- Solution: Post the ready-to-apply package exactly once per captured job.
- Why: This happens on every normal capture today, so it clutters the one
  channel the user relies on daily and makes it unclear which buttons to
  click.
- What it looks like: Capturing a job link produces one clean thread with the
  summary, drafts, and one row of action buttons — no repeats.
- Suggested priority: High
- Evidence: `openspec/specs/integrations/spec.md` ("Fill companion (Ready
  gate)" section) vs. `src/application_agent/integrations/slack/service.py`
  (`handle_capture` already embeds the full ready-package in its response)
  and `src/application_agent/integrations/slack/app.py` (`_respond_capture`
  posts that response, then unconditionally calls `bind_thread`, which
  re-posts the same package as separate thread replies).
- Why not already tracked: none of the 12 active `openspec/changes/*`
  proposals touch Slack message composition or the capture response flow;
  closest is `company-context-brief` (builds the brief content, not the
  posting/de-dup logic).

**2. 🐛 Saving a flagged answer as a reusable policy silently discards its quality-check notes**
- In short: Edited answers lose quality flags
- Problem: When the user answers a previously-flagged screening question and
  saves it for reuse, the system quietly forgets whether that answer passed
  or failed the built-in quality check, and forgets the earlier draft it was
  compared against.
- Solution: Saving an answer should keep its quality information attached,
  not reset it.
- Why: Quality badges are how the user spot-checks drafts before submitting;
  silently blanking them for edited fields removes that safety net exactly
  where a human already had to step in.
- What it looks like: After saving a policy answer, its quality badge and
  history still show correctly instead of reverting to "not checked."
- Suggested priority: Medium
- Evidence: `FillField` fields described in
  `openspec/specs/generation/spec.md` (draft-quality-self-critique section)
  vs. `models.py`'s `FillField` dataclass (`quality_status`, `quality_note`,
  `original_value`) vs. `tracker/store.py`'s `update_fill_field()`, which
  rebuilds `FillField` using only `label`, `value`, `needs_human`,
  `policy_topic` — dropping the quality fields on save.
- Why not already tracked: `save-flagged-screening-policy` added the save
  flow and `draft-quality-self-critique` added the quality fields separately;
  neither change's task list covers the interaction between the two, so the
  gap fell between them.

**3. 🔧 No way to safely auto-submit low-stakes items like event or hackathon sign-ups**
- In short: Low-stakes auto-submit not built
- Problem: The product's own design says small, low-risk sign-ups (events,
  workshops, hackathons) should be able to submit themselves once the user
  gives a one-time yes — but nothing in the system can currently perform that
  submission at all, even after opt-in.
- Solution: Build the piece that actually performs the low-stakes submission
  in the cloud once the user has opted in.
- Why: Without it, every event/hackathon registration still needs the same
  manual laptop step as a real job application, defeating the point of
  treating them differently.
- What it looks like: For an event the user has approved for auto-submit, the
  system registers them and logs it, with no laptop step required.
- Suggested priority: Medium
- Evidence: `openspec/specs/browser/spec.md` ("Mode 2: Cloud — headless
  auto-submit") describes this as still open; no cloud/headless module exists
  under `src/application_agent/browser/` (only laptop-focused `cdp.py`,
  `fill.py`, `fill_session.py`, `snapshot.py`, `guard.py`, `discovery.py`).
- Why not already tracked: none of the 12 active changes target
  headless/cloud submission; closest is `event-blurb-generation`, which only
  drafts text for events, not submission.

**4. 🔧 Follow-up reminders aren't tracked anywhere**
- In short: No follow-up date tracking
- Problem: The tracker is supposed to record follow-up dates for every
  application and outreach, but currently stores no follow-up dates at all.
- Solution: Add a way to record and later see follow-up dates per
  application.
- Why: The tracker is described as the one thing this project has to get
  right, and follow-ups are explicitly part of that job — losing track of
  when to nudge a recruiter or check back defeats the point of a career
  co-pilot.
- What it looks like: Each tracked application can carry a follow-up date
  that shows up when reviewing the pipeline.
- Suggested priority: Medium
- Evidence: `openspec/specs/tracker/spec.md` ("What This Covers") states the
  tracker covers "the audit log... plus follow-up dates," but no
  follow-up-date field exists in `models.py`'s `Application`/`FillCompanion`
  dataclasses or in `tracker/store.py`.
- Why not already tracked: none of the 12 active changes mention follow-up
  dates or reminders.

No 5th spec-drift candidate met the bar — everything else flagged as unbuilt
in the specs (Indeed integration, Notion sync, ghost-job scoring) is already
honestly labeled "planned"/"Open-Next" in the specs themselves, not drift.

### Market/feature candidates (up to 3, cap: 3)

**1. 📋 Weekly Slack digest with stale-application nudges**
- In short: Pipeline health digest
- Problem: Nothing proactively tells the user when an application has sat
  untouched, or gives a weekly view of how the whole pipeline is doing.
- Solution: A periodic Slack summary of the pipeline (counts by stage, plus a
  call-out for anything stuck too long), posted automatically.
- Why: Comparable tools (Teal, Huntr) lead with a dashboard view; a
  Slack-first tool's equivalent is a digest message, and it directly
  supports the project's own "tracker is the whole point" priority.
- What it looks like: Every week, a message lands in the channel showing how
  many applications are in each stage and which ones haven't moved in a
  while.
- Suggested priority: Medium
- Reasoning: not present in any spec.md; consistent with the Slack-as-
  remote-control architecture in `openspec/project.md`; doesn't touch any
  non-negotiable (notifications only, no auto-action).

**2. 🔧 Resume-to-posting match score shown before drafting**
- In short: Resume match score
- Problem: The user can't see at a glance how well their resume lines up
  with a posting's language before the tailored draft is generated.
- Solution: Show a simple before/after match indicator between resume and
  posting.
- Why: A well-liked feature in tools like Jobscan; gives the user a fast,
  non-scary way to sanity-check tailoring quality without reading the whole
  draft.
- What it looks like: Alongside the usual cover letter and resume draft, a
  short line shows which important posting terms are and aren't reflected in
  the resume.
- Suggested priority: Medium
- Reasoning: not present in any spec.md (`generation/spec.md` covers
  tailoring and truthfulness but no match/coverage scoring); purely
  informational, so it doesn't conflict with the never-fabricate or
  human-review non-negotiables.

**3. 🔧 Optional interview-prep handoff after marking an application submitted**
- In short: Post-submit interview prep
- Problem: Once an application is marked submitted, the co-pilot's
  involvement ends, even though the same company research it already
  gathered would be useful again at the interview stage.
- Solution: When the user marks an application submitted, offer a one-tap
  way to turn the existing company/role research into a starting
  interview-prep note.
- Why: Reuses information the system already collected instead of making the
  user start over elsewhere, extending the tool's value past the application
  step.
- What it looks like: After marking submitted, a Slack message offers "want
  a prep brief for this one?" and, if accepted, posts a short one based on
  what's already known about the company and role.
- Suggested priority: Low
- Reasoning: not present in any spec.md or the 12 active changes; strictly
  opt-in and additive, so it doesn't touch the auto-submit, LinkedIn, or
  credential-storage non-negotiables.

## Separate observation (not a Linear-issue candidate, FYI only)

Three of the 12 currently-active `openspec/changes/*` proposals in
Application-Agent — `save-flagged-screening-policy`, `cdp-fill-session`,
`slack-only-lead-ingestion` — have every task in their `tasks.md` checked off,
with matching spec text and code already present. They read as fully shipped
work sitting in the active-changes folder rather than genuinely in-flight, and
would normally be caught by spec-drift step 12's OpenSpec archive
housekeeping. That step's instructions run
`scripts/archive-merged-openspec-changes.sh --sweep` from inside an
**AI-Workspace** checkout, which only archives AI-Workspace's *own*
`openspec/changes/` — it has no path for sweeping a *different* target
repo's changes folder, and its PR check depends on the `gh` CLI, which this
session doesn't have either. This looks like a real gap in
`agents/spec-drift.md` step 12 (it doesn't say how to point the sweep at a
non-AI-Workspace target repo) worth flagging to Sharad separately, alongside
whoever picks up this handover filing the four spec-drift issues above.

## Instructions for receiving agent

1. Read `agents/shared/issue-cap.md` and run the Issue Cap pre-flight for
   **Application Agent** (project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`).
   If at/over cap (5 active pipeline issues), stop — do not file any of the
   candidates below this cycle.
2. If under cap, search the Application Agent Linear project for each
   candidate title/topic above. Skip any that are already tracked (open or
   recently closed).
3. File the remaining candidates as Backlog + `spec-needed`, assignee Sharad
   Rohra, title as given (emoji + text), description in Issue Brief format
   (already written above — paste as-is), suggested priority as given. Stop
   at 5 total for spec-drift and 3 total for market-feature, per
   `agents/spec-drift.md` / `agents/market-feature.md`.
4. Post the first comment on each created issue per
   `agents/shared/issue-brief.md` rule 9: reference the spec file(s) and code
   paths in the Evidence line above, note this was filed via handover (link
   this file), and state the dedupe search terms you used.
5. No screenshots/visual previews needed — this project has no UI surface
   (see "What this session could and couldn't do" above).
6. Update `data/sweep-runs.jsonl` with a corrected line reflecting what was
   actually filed (bugs=0 always for this project unless you also ran
   bug-error against a since-added prod URL; features = spec-drift + market
   combined), replacing the placeholder line this run added.
7. Delete this handover file once filing is complete and reflected in Linear.
8. Do not action the "Separate observation" section above yourself unless you
   also have `gh` CLI or another way to check open-PR status safely — it's
   informational, not a filing task.
