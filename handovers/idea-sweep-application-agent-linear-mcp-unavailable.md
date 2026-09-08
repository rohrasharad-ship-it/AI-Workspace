# Handover: idea-sweep routine (Application Agent) — no Linear access this session

**For:** Any agent/session with working Linear MCP access
**From:** Claude Code cloud session running the `idea-sweep` routine for Application Agent, 2026-09-08 (scheduled trigger)
**Blocked by:** Linear MCP is not connected in this session at all — the harness reports "Linear" as an MCP server requiring OAuth authorization, and this is a non-interactive session that cannot complete that flow. There is no fallback (no `LINEAR_API_KEY` env var either).
**Action:** Once Linear MCP (or a `LINEAR_API_KEY`) is available, run the Issue Cap pre-flight for **Application Agent** (Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`), then execute `agents/spec-drift.md`, `agents/bug-error.md`, and `agents/market-feature.md` per `routines/idea-sweep.md`, using the groundwork below so the work already done this session isn't repeated.
**Issue:** No Linear issue exists yet — this handover is itself the record of the blocked run.

---

## Why this is worse than the existing `preview-branch-cleanup-linear-api-key.md` blocker

That handover tracks a narrower problem: the `preview-branch-cleanup.yml` GitHub Action and
`scripts/generate-routine-log.mjs` lack the `LINEAR_API_KEY` **repo secret**, but prior
idea-sweep sessions still had **Linear MCP tool access** and could search/file/comment
directly (see the sweep-runs.jsonl `"clean":true` entries for Application Agent on
2026-07-11, 2026-08-06, 2026-08-19 — those runs completed steps 1–10 fine and only
step 11/12 housekeeping was blocked).

This session has **no Linear MCP tools at all** — not a missing bash-script secret, a
missing OAuth grant for the MCP connector itself. That blocks every step that needs Linear:
the Issue Cap pre-flight (step 0 of every role), search-before-file (step 4/3/4), issue
creation, first comments, and spec-drift's stale-issue sweep (step 10). None of the three
idea-generation roles could run this cycle. I did **not** write a `"clean":true` line to
`data/sweep-runs.jsonl` — that would misrepresent "couldn't check" as "checked, found
nothing." Treat this run as not having happened for ledger purposes; the next successful
run should log normally.

## Second, separate issue: this routine's tooling assumes a web app — Application Agent isn't one

Independent of the Linear blocker, two more routine assumptions don't fit this project,
worth flagging to Sharad once someone has Linear access:

- **`agents/bug-error.md` needs a Vercel prod URL to read runtime logs.** `projects.md`
  lists Application Agent's Vercel Prod as `TBD`, and the project itself
  (`openspec/project.md`, `README.md`) is a Python CLI + always-on cloud service +
  Slack bot with no web frontend — there may never be a Vercel deployment to point this
  role at. Bug-error should probably read something else for this project (e.g. the
  cloud service's own logs, once it has a hosting target) — or be marked N/A here.
- **The mandatory Visual Self-QA screenshot** (`agents/shared/visual-self-qa.md`,
  required on every issue any of the three roles create) assumes a live site a
  Playwright browser can screenshot. Application Agent's only user-facing surfaces are
  Slack messages and a local CLI — there's no URL to screenshot. Spec-drift and
  market-feature issues for this project will need a documented exception (e.g. a
  terminal/Slack-message screenshot in lieu of a browser one) or the mandate doesn't
  apply cleanly here.

Consider filing a PM OS issue about both of these (similar in spirit to
`handovers/linear-issue-vercel-preview-blocker.md`, which documented a comparable
routine-vs-reality mismatch) once Linear access exists.

## Groundwork already done this session (spec-drift candidates — NOT deduped against Linear)

I read `openspec/project.md` and every file under `openspec/specs/` in
`rohrasharad-ship-it/Application-Agent`, and the corresponding code under
`src/application_agent/`. This repo's specs are unusually well-maintained — each one
carries a `Status` and `Open / Next` section that already tracks what's unshipped, so
the real gaps are mostly self-documented rather than requiring a line-by-line code diff.
**None of the below has been searched against Linear for duplicates** (Application Agent
also auto-creates a Linear issue per job-application capture per
`openspec/specs/integrations/spec.md` Phase 1b — SHA-108 — so the project's Linear
project may already contain related engineering issues under different titles; dedupe
carefully). Do not paste these straight in — verify each one is still open and not
already tracked before filing.

1. **In short:** Slack-triggered laptop fill
   **Problem:** Starting a form fill still requires typing a command on the laptop CLI (`application-agent fill --id <app-id>`) — there's no way to kick it off from the Slack thread where the rest of the workflow lives.
   **Solution:** A Slack thread command (e.g. "fill this one") that queues the laptop fill session for when the user is next at their laptop.
   **Why:** Both `openspec/specs/browser/spec.md` ("Open / Next") and `openspec/specs/orchestrator/spec.md` ("Open / Next") independently list this as outstanding — it's the one piece connecting the Slack control surface to the laptop fill step that the orchestrator's own flow diagram assumes exists.
   **What it looks like:** N/A (no UI — Slack command + confirmation message).
   Source: `openspec/specs/browser/spec.md` § Open/Next, `openspec/specs/orchestrator/spec.md` § Open/Next.

2. **In short:** Cloud low-stakes auto-submit
   **Problem:** Low-stakes items (events/hackathons/workshops with explicit per-item opt-in) are speced to auto-submit headlessly in the cloud, but `openspec/specs/browser/spec.md` still lists "Mode 2" (cloud headless auto-submit) as planned, not shipped — only Mode 1 (laptop collaborative CDP fill) has code (`src/application_agent/browser/fill_session.py`, `cdp.py`, `discovery.py`, `fill.py`, `snapshot.py`, `guard.py` — all laptop-CDP-flavored; no headless-cloud submit path visible).
   **Solution:** Build the declared-but-missing headless Playwright path for low-stakes opt-in items.
   **Why:** It's one of the two modes the `browser` capability's spec explicitly defines as in-scope, and the project's whole pitch is removing manual grind — this half is currently 100% manual.
   **What it looks like:** N/A (backend-only; no UI).
   Source: `openspec/specs/browser/spec.md` (Mode 2 section + Status line).

3. **In short:** Verify PDF resume export status
   **Problem:** `openspec/specs/generation/spec.md` § Open/Next still lists "PDF export for tailored resumes" as unbuilt, but `src/application_agent/generation/resume_export.py` (10KB) already exists and looks substantial enough that this may already be shipped and the spec just wasn't updated (spec drift in the literal sense, not a code gap).
   **Solution:** Not a feature ask — have someone with the full picture (or the next agent with repo + Linear access) check whether `resume_export.py` already satisfies this and, if so, update the spec's Status/Open-Next instead of filing a build issue.
   **Why:** Filing a duplicate "build PDF export" issue when it may already be done would waste a Linear slot and confuse triage.
   **What it looks like:** N/A — a spec correction, not a feature.
   Source: `openspec/specs/generation/spec.md` § Open/Next vs `src/application_agent/generation/resume_export.py`.

No market-feature candidates are included — per `agents/market-feature.md` step 9,
nothing genuinely differentiated came to mind on a light read of `openspec/project.md`'s
vision/non-negotiables, and this is a personal internal tool (not a product with
external users to differentiate against), so speculative filler would be low-value.
Someone with full context on Sharad's actual day-to-day friction using this tool would
do better here than a cold read of the spec.

No bug-error candidates — see "second, separate issue" above; there is no known prod
surface to read logs from.

## Instructions for receiving agent

1. Confirm Linear MCP (or `LINEAR_API_KEY`) now works.
2. Run the Issue Cap pre-flight for Application Agent (`agents/shared/issue-cap.md`,
   project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`). If at/over cap, stop per that
   module's rules (skip filing, spec-drift still does its housekeeping steps).
3. If under cap: search Linear for each of the 3 candidates above (and anything the
   SHA-108 per-application auto-sync may have created under a different title) before
   filing anything. File only what's genuinely new, in Issue Brief format
   (`agents/shared/issue-brief.md`), Backlog + `spec-needed`, assignee Sharad Rohra.
4. Decide/confirm the Visual Self-QA exception for this project (see above) before
   attaching screenshots — don't skip the requirement silently, and don't block filing
   on it either; use judgment or ask Sharad.
5. Run spec-drift steps 10–12 (stale-issue sweep, preview-branch housekeeping,
   OpenSpec archive sweep) — independent of the above and not blocked by anything
   this session found new.
6. Append a `data/sweep-runs.jsonl` line for this project once the above actually runs
   (this session intentionally did not, per the reasoning above).
7. Delete this handover file once resolved, per the standard convention.
