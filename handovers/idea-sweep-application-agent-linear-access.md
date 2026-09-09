# Handover: Linear MCP not connected this session — idea-sweep could not check the cap, dedupe, or file for Application Agent

**For:** Any agent/session with Linear MCP tool access, or a human who can authorize the Linear connector (claude.ai → Settings → Connectors) for future sessions
**From:** `idea-sweep` routine run (spec-drift + bug-error + market-feature), Application Agent, 2026-09-09
**Blocked by:** Linear MCP is not authenticated in this session — no `mcp__Linear__*` tools were loadable at all (confirmed via tool search; the session's own tool listing explicitly flags Linear as requiring authorization). No `LINEAR_API_KEY` env var is set either (checked `env | grep -i linear`, empty).
**Action:** Once Linear access exists, run the Issue Cap pre-flight, then dedupe-search and file the draft candidates below for **Application Agent** (Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`) per `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`.

This is a **different** blocker from the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one is about the missing
`LINEAR_API_KEY` **repo secret** used by `scripts/cleanup-preview-branches.sh` and
`scripts/generate-routine-log.mjs`, run from a shell). Every session that hit *that*
blocker still had working **Linear MCP** tool access (they used `list_issues` etc. to
build their payloads). This session has neither — no MCP, no raw key — so it could not
even do the mandatory Issue Cap count (`agents/shared/issue-cap.md`) before proceeding,
let alone search for duplicates or create/comment on issues. Both point at the same root
gap (no durable Linear credential available to non-interactive/background sessions) but
need different fixes: the script needs the repo secret; interactive sessions need the
Linear connector authorized for this account. Worth fixing both at once if convenient.

## What I could and couldn't do this run

- **Issue Cap pre-flight (mandatory before any filing):** could not run — no `list_issues`
  access. Did not file anything, in case the project is already at/over the 5-issue cap.
- **Spec-drift steps 1–9 (gap-filing):** read `openspec/project.md` and all 6
  `openspec/specs/*/spec.md` files plus the `src/application_agent/` tree structure.
  Candidates below are drafted but **not** deduped against Linear — do that before filing.
- **Spec-drift steps 10–11 (stale-issue sweep, preview-branch housekeeping):** could not
  run — both need Linear MCP (list open issues / look up issue status). Step 11's
  script also needs `LINEAR_API_KEY` regardless (see the other handover).
- **Spec-drift step 12 (openspec archive sweep):** not attempted — `scripts/archive-merged-openspec-changes.sh`
  needs repo git access this session doesn't have for AI-Workspace beyond the GitHub MCP
  content API; also secondary to the Linear blocker above. Note in passing:
  `openspec/changes/` in Application-Agent currently has 13 non-archived change folders
  (`ats-screening-answers`, `cdp-fill-session`, `company-context-brief`,
  `draft-quality-self-critique`, `event-blurb-generation`, `online-resume-website`,
  `portfolio-blurb-generation`, `profile-foundation-files`, `replace-capture-attachments`,
  `resume-file-export`, `resume-master-docx-export`, `save-flagged-screening-policy`,
  `slack-only-lead-ingestion`), several of which correspond to capabilities each spec.md
  already marks "shipped (SHA-xxx)" — worth a look next time the archive sweep can run,
  independent of the Linear blocker.
- **Bug-error:** not blocked by Linear — checked Vercel directly (`list_teams` →
  `list_projects`) and confirmed there is **no Vercel project for Application Agent**
  (only `milletmate`, `ai-workspace`, `resume-website`, `usercon`, `ai-landscape` exist
  under the account). Matches `projects.md`'s "Vercel Prod: TBD" — this project is a
  Python/Slack service with no deployed web frontend yet, so there are no runtime
  logs/errors to read. Nothing to file; re-check once a prod deployment exists.
- **Market-feature:** read `openspec/project.md` in full (vision, non-negotiables, Out of
  Scope) plus all 6 spec files for existing coverage. Candidates below are genuinely new
  (not already in a spec's own "Open / Next" list) but **not** checked against Linear.

## Payload — spec-drift candidates (drawn from each spec's own "Open / Next"; real
planned-vs-built gaps, but likely already partially known/tracked — verify via Linear
search before filing any of these, per the "search first, skip anything tracked" rule)

1. **In short:** Low-stakes auto-submit mode
   **Problem:** The architecture promises headless, opt-in auto-submit for low-stakes
   items (events/workshops/hackathons), but only the laptop CDP fill mode is built.
   **Solution:** Ship the cloud headless Playwright path for explicitly opted-in items.
   **Why:** It's one of the three architecture surfaces in `project.md` and currently
   0% built — a real gap between the stated design and what exists.
   **What it looks like:** An opt-in low-stakes lead runs fully hands-off; tracker shows
   it submitted with no laptop session.
   *Source:* `openspec/specs/browser/spec.md` "Open / Next" + `project.md` architecture table.

2. **In short:** Slack-triggered laptop fill
   **Problem:** The two-way Slack control promise ("remote control for everything except
   fill/submit") doesn't yet cover starting the fill step itself — it's CLI-only today.
   **Solution:** A Slack thread command (e.g. "fill this") that queues the laptop fill
   session for the next time the CLI polls/runs.
   **Why:** Closes the one gap in the "Slack controls everything but the physical
   fill/submit act" story.
   **What it looks like:** Replying "fill this" in an application thread marks it
   ready-to-fill; next `application-agent fill` run picks it up first.
   *Source:* both `browser/spec.md` and `orchestrator/spec.md` list this in "Open / Next".

3. **In short:** Indeed job discovery
   **Problem:** All leads currently require a manual Slack `/capture` — there's no
   supplementary discovery feed even though one was planned.
   **Solution:** Wire the Indeed MCP path so it surfaces candidate postings the user can
   `/capture` from, without auto-starting prep on its own.
   **Why:** Named explicitly in `project.md` integrations and still unstarted.
   **What it looks like:** A periodic Slack digest of matching Indeed postings the user
   can tap to capture.
   *Source:* `integrations/spec.md` "Planned Integrations" (still 0% built).

4. **In short:** Tailored resume PDF export
   **Problem:** Fill companions currently carry tailored resume text/diffs but no
   downloadable PDF artifact.
   **Solution:** Export each tailored resume to `data/artifacts/{app_id}/` as a PDF and
   link it on `FillCompanion`.
   **Why:** Called out as open work in the generation spec; needed before a resume file
   can be attached during laptop fill/upload.
   **What it looks like:** A "Download tailored resume (PDF)" link in the Slack fill
   companion message.
   *Source:* `generation/spec.md` "Open / Next".

5. **In short:** Ghost-job / posting quality score
   **Problem:** No signal today distinguishes a healthy posting from a stale/ghost one
   before time is spent prepping it.
   **Solution:** A lightweight A–F score (inspired by `career-ops`) surfaced at capture
   time.
   **Why:** Explicitly called out as an open idea inspired by prior art already reviewed
   for this project.
   **What it looks like:** Capture confirmation shows a quality grade next to the job
   title; low grades get a one-line caution note.
   *Source:* `generation/spec.md` "Open / Next" (marked optional there).

## Payload — market-feature candidates (genuinely new, not in any spec's Open/Next; cap
per role is 3, proposing 2 since a 3rd didn't feel differentiated enough to justify —
verify via Linear search before filing)

1. **In short:** Stale-lead follow-up nudges
   **Problem:** Once a fill companion is posted, nothing proactively reminds the user if
   an application sits in `ready`/`in_progress` for a long time with no follow-up.
   **Solution:** A periodic Slack nudge (e.g. weekly) listing applications past a
   configurable "no movement" threshold, pulled from tracker's own status lifecycle.
   **Why:** The product's differentiator is being a co-pilot that doesn't let things
   fall through the cracks — a spreadsheet tracker can't proactively remind; this can.
   **What it looks like:** A Friday Slack message: "3 applications haven't moved in
   10+ days: [Company A], [Company B], [Company C] — still pursuing these?"

2. **In short:** Interview-prep companion
   **Problem:** The product's lifecycle stops at `submitted`/`skipped` — there's no
   generation support for the next real-world step, interview prep, even though the
   same truthfulness-attributed project data (`profile/projects.yaml`) that powers
   resumes/cover letters is exactly what a talking-points brief would need.
   **Solution:** When a tracker entry is manually marked "interview scheduled," generate
   a short talking-points brief (likely questions for the role + 2–3 attributable
   project stories) using the existing generation pipeline and attribution rules.
   **Why:** Extends the "career co-pilot" vision past the application step, which is
   where most comparable tools (resume builders, autofill extensions) stop entirely.
   **What it looks like:** A Slack message with 3–5 talking points, each tagged
   🟢/🟠/⚠️ the same way cover letters are today.

**Visual-preview note for whoever files these:** this product has no live web UI — it's a
Slack bot + local CLI, and Vercel Prod is TBD (confirmed above, nothing deployed). The
usual `agents/shared/visual-specs.md` mockup-branch convention is built for web-UI
projects; for Application Agent, a mocked-up Slack message screenshot (or a plain text
block quoting the proposed message) is the closest sensible substitute for "what it looks
like" — use judgment rather than forcing a `preview/<issue-id>-vN` branch that has no
site to deploy.

## Instructions for receiving agent

1. Confirm Linear MCP access (or `LINEAR_API_KEY`) is now available.
2. Run the Issue Cap pre-flight for Application Agent (`7dc5202c-a586-4bed-b2d3-fba10f2dd913`)
   per `agents/shared/issue-cap.md`. If at/over cap, stop — do not file, per the routine.
3. If under cap: search Linear for each candidate above before filing (some may already be
   tracked — none of this was deduped). File only the ones that are genuinely new, up to 5
   spec-drift + 3 market-feature, in the Issue Brief format with the first-comment
   execution detail called for in each role file.
4. Also run spec-drift steps 10–12 (stale-issue sweep, preview-branch housekeeping,
   openspec archive sweep) for this project while you're in — none of that ran this
   session either.
5. Delete this handover file once Application Agent's idea-sweep has actually run end to
   end with real Linear access — until then it's the record of what this session found.
