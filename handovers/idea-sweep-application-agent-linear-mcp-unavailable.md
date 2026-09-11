# Handover: idea-sweep for Application Agent blocked — Linear MCP unauthenticated this session

**For:** Any agent/session with authenticated Linear MCP access (or a human with Linear access)
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature), Application Agent, 2026-09-11
**Blocked by:** The Linear MCP server is unauthenticated in this session — the harness reported it explicitly ("The following MCP servers require authentication before their tools can be used: Linear") and this is a non-interactive scheduled session, so the OAuth flow can't be run to unblock it. No `LINEAR_API_KEY` env var is present either, so there is no fallback path (raw GraphQL via curl, as other blocked sessions have used) for this session.
**Action:** Once Linear MCP is authenticated (or `LINEAR_API_KEY` is available) for a session running this routine, use the Payload below to run the Issue Cap pre-flight, dedupe-search, and file the candidate issues per `agents/spec-drift.md` and `agents/shared/issue-cap.md` — don't re-derive the gap analysis, it's already done.

This is a different, more severe blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one is specifically about the
`preview-branch-cleanup.yml` GitHub Action missing a repo secret, and is unrelated to whether
an idea-sweep session itself can read/write Linear). That handover's own conclusion — "no
further action needed... re-verifying wastes tokens" — still holds; I did not re-touch it or
re-verify its branch list this run. **This session had no Linear access at all**, which is a
step further back: previous idea-sweep sessions (see that file's update log) could at least
call `list_issues`/`list_projects` via Linear MCP, they just couldn't push branch-deletion
commits. This session couldn't do the Linear read/write calls either — so steps 0 (Issue Cap),
1–9 (gap filing), and 10 (stale-issue sweep) in `agents/spec-drift.md` were all skipped, not
just step 11.

## What I could and couldn't do this run

- **Could:** clone/read both repos locally (already checked out on their designated
  branches), read `openspec/project.md` + all 6 capability specs + the codebase for
  Application Agent, cross-check against recent commit history.
- **Could not:** call any Linear MCP tool (`list_issues`, `create_issue`, `create_comment`,
  etc.) — auth required, no interactive session to grant it. So I could not: check the
  Issue Cap, search for existing/duplicate issues, file new issues, or run the stale-issue
  sweep (step 10).
- **Also structurally blocked regardless of Linear:** `agents/spec-drift.md` step 11
  (preview-branch cleanup) and step 12 (openspec archive sweep) both need `LINEAR_API_KEY`
  as a shell env var — not set in this session either. Step 11 is the same pre-existing
  blocker tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (not re-verified,
  see above). Step 12's script (`scripts/archive-merged-openspec-changes.sh`) does **not**
  actually need `LINEAR_API_KEY` (confirmed by reading it) — but see the separate open
  question about it below.
- **bug-error role is inapplicable regardless of any blocker:** `projects.md` lists
  Application Agent's Vercel Prod as `TBD` — there is no deployed prod URL, so there are no
  Vercel runtime logs to read. bug-error has nothing to do for this project until it has a
  real prod deployment target; this isn't something a Linear fix resolves.

## Payload — spec-drift candidate gaps (for the receiving agent to dedupe-check and file)

Application Agent's six capability specs (`openspec/specs/*/spec.md`) each keep their own
`Open / Next` section, and the codebase is unusually well-aligned with them (12 of the repo's
own `openspec/changes/*` proposals show all tasks checked off and match shipped commits). I
cross-checked every `Open / Next` line against `src/application_agent/` and recent commits
rather than re-deriving gaps from scratch. Two of those Open/Next lines are actually stale
(already shipped, spec just wasn't updated — see below); the following four are real,
still-unbuilt gaps:

1. **Cloud headless auto-submit for low-stakes items (browser Mode 2).** `browser/spec.md`
   describes this as a distinct, in-scope mode (events/hackathons/workshops with explicit
   per-item opt-in, no laptop required) and it's referenced as a non-negotiable capability,
   but `src/application_agent/browser/` only contains CDP/laptop-fill code
   (`cdp.py`, `fill.py`, `fill_session.py`, `discovery.py`, `guard.py`, `snapshot.py`) — no
   headless/cloud auto-submit path exists yet. Suggested title: `🎫 Cloud auto-submit for
   low-stakes event registrations`. Suggested priority: Medium.
2. **Slack command to trigger laptop fill remotely.** Called out as Open/Next in both
   `browser/spec.md` and `orchestrator/spec.md`. Today, laptop fill is CLI-only
   (`application-agent fill --id <app-id>`) — there's no Slack thread command that queues or
   triggers it. Suggested title: `💬 Slack command to trigger laptop fill session`. Suggested
   priority: Medium.
3. **Indeed MCP integration (job search).** Called out as planned in `integrations/spec.md`
   since early specs; no `indeed` module exists under `src/application_agent/integrations/`
   (only `apollo/`, `linear/`, `slack/`). Still explicitly "remains planned" per the spec's own
   Status line. Suggested title: `🔍 Indeed MCP integration for job discovery`. Suggested
   priority: Low (Slack `/capture` already covers primary lead intake; this is supplemental).
4. **Notion sync for profile/tracker (optional mirror).** Called out in `profile/spec.md`
   Open Decision and `integrations/spec.md` Planned Integrations; no Notion code exists.
   Explicitly framed as optional in the spec itself. Suggested title: `📝 Optional Notion sync
   for profile/tracker`. Suggested priority: Low.

**Not filed as gaps** (already shipped, but the spec's own Open/Next section wasn't updated —
this is spec-drift in the *other* direction, a documentation cleanup, not a Backlog issue; flag
to Sharad or fix directly in a spec-edit PR rather than a Linear issue):
- `generation/spec.md` Open/Next still lists "PDF export for tailored resumes" as unbuilt —
  it shipped (`resume_export.py`, `resume-file-export` and `resume-master-docx-export` changes,
  both fully archived-eligible with all tasks checked, commits #31/#28 in the log).
- `orchestrator/spec.md` Open/Next still lists "Resume PDF upload automation during fill
  session" as unbuilt — it shipped per `browser/spec.md`'s own Mode 1 description
  ("SHA-157... propose an upload action for resume/CV file inputs") and commit `5a8400c`.

**Did not evaluate as market-feature candidates** — with zero Linear access there was no way
to dedupe-search first, and this product has no live web frontend to screenshot for the
mandatory Visual Self-QA step (it's a Slack-native agent, not a website — Vercel Prod is
`TBD`/none). Rather than propose ideas nobody can verify aren't already tracked or attach a
required screenshot for, market-feature was skipped entirely this run rather than half-done.
Worth flagging separately: `agents/shared/visual-self-qa.md`'s "real Playwright screenshot"
requirement doesn't map cleanly onto a Slack-only product with no prod URL — may be worth a
project-type exception in that shared module (a Slack conversation screenshot/transcript in
place of a browser screenshot?) rather than leaving future runs to skip market-feature by
default for this project.

## Separate open question (not a blocker, just worth a human decision)

`agents/spec-drift.md` step 12 says to run the openspec archive sweep by `cd AI-Workspace` and
running `scripts/archive-merged-openspec-changes.sh --sweep` **there** — but Application
Agent's own `openspec/changes/` (in the Application-Agent repo, not AI-Workspace) currently has
12 change folders with all tasks checked off and matching shipped commits, and would be the
actual target of a sweep for this project. Application-Agent has no copy of this script or its
GitHub Action (confirmed: no `scripts/`, no `.github/workflows/`). Running the script from
within `AI-Workspace` only ever touches AI-Workspace's own `openspec/changes/` — it has no
effect on Application-Agent's backlog of unarchived-but-complete changes. I did not run the
script against Application-Agent myself (that would mean improvising past what step 12 actually
says, and committing/pushing to the Application-Agent branch on a judgment call I'd rather a
human confirm first). Two ways to resolve, Sharad's call:
- Copy `scripts/archive-merged-openspec-changes.sh` + `.github/workflows/openspec-archive.yml`
  into Application-Agent (and every other per-project repo) so each repo can sweep its own
  `openspec/changes/`, matching what AI-Workspace does for itself; or
- Clarify in `agents/spec-drift.md` that step 12 is AI-Workspace-specific housekeeping only
  and doesn't apply per-project (in which case each project repo needs its own equivalent
  step documented somewhere).

Completed-but-unarchived change folders in Application-Agent as of this run (all tasks
checked, all correspond to already-merged PRs): `ats-screening-answers`, `cdp-fill-session`,
`event-blurb-generation`, `portfolio-blurb-generation`, `profile-foundation-files`,
`replace-capture-attachments`, `resume-file-export`, `resume-master-docx-export`,
`save-flagged-screening-policy`, `slack-only-lead-ingestion`. (`company-context-brief`,
`draft-quality-self-critique`, `online-resume-website` also match shipped commits but have no
`tasks.md` to confirm completion mechanically — worth a quick manual check before archiving
those three specifically.)

## Instructions for receiving agent

1. Confirm Linear MCP is authenticated (or `LINEAR_API_KEY` is set) in your session.
2. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Application Agent
   (Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`, from `projects.md`).
3. If under cap, dedupe-search the four candidate gaps above against the Application Agent
   Linear project, then file whichever aren't already tracked, following
   `agents/spec-drift.md` steps 5–8 (Issue Brief format, first-comment execution detail,
   visual preview only where genuinely applicable — these are backend/integration gaps,
   likely no UI screenshot needed for most of them).
4. Run the stale-issue sweep (step 10) against Application Agent's open Backlog issues.
5. Decide the openspec-archive-script question above (with Sharad) before archiving
   Application Agent's completed change folders.
6. Delete this handover file once steps 2–4 are done and tracked in Linear — the analysis
   above is a one-time snapshot, not something to keep re-deriving each run.
