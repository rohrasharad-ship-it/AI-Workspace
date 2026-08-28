# Handover: idea-sweep routine blocked — no Linear MCP access in this session

**For:** Any agent/session with Linear MCP access
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature) for Application Agent, 2026-08-28
**Blocked by:** Linear MCP tools are unauthenticated/unreachable in this session (an automated, non-interactive scheduled run — no OAuth flow could be completed). No `list_issues`, `search_issues`, `create_issue`, or comment tool was reachable at any point in this run.
**Action:** Run the Issue Cap pre-flight, dedupe against Linear, and file (or discard) the candidates below for Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913` (Application Agent).
**Issue:** N/A — this is a routine-level block (idea-sweep trigger), not tied to one pre-existing Linear issue.

## Payload

### What this session could and couldn't do
- **Could** (no Linear needed): read `openspec/project.md`, `README.md`, all 6 capability specs (`profile`, `generation`, `tracker`, `integrations`, `browser`, `orchestrator`) and the `src/application_agent/*` directory tree in `rohrasharad-ship-it/Application-Agent` via GitHub MCP (read-only).
- **Could not**: run the Issue Cap pre-flight (`agents/shared/issue-cap.md`), search Linear for dedup, create or skip any issue, comment on existing issues, or run spec-drift's stale-issue sweep (step 10) — every one of those requires Linear MCP, which had zero tool access this run.
- **Bug-error is structurally not-applicable right now regardless of Linear access**: `projects.md` lists Application Agent's Vercel Prod as `TBD`. This project is a Python CLI/Slack agent with no deployed web surface, so there are no Vercel runtime logs to read. Worth confirming with Sharad whether `projects.md` should mark this row "N/A — no prod deployment" so future bug-error runs don't re-attempt it every cycle.
- Preview-branch housekeeping (step 11) and the OpenSpec archive sweep (step 12) both also need `LINEAR_API_KEY` as a script env var (separate from MCP) and a working `git push` — not attempted here for the same underlying reason (no Linear-side capability this session), and this repo already has a longer-running, separate handover open for the `LINEAR_API_KEY` secret itself (`handovers/preview-branch-cleanup-linear-api-key.md`) — do that one first if picking up housekeeping too.
- This session did **not** append a line to `data/sweep-runs.jsonl` — no real cap check or dedup happened, so a `"clean": true` entry would misrepresent this run as a completed sweep that found nothing. Append the real outcome once the work below is actually done.

### spec-drift candidates (pulled from each capability spec's own "Open / Next" section — not yet deduped against Linear)
These are gaps the specs already self-report as unbuilt, so search Linear first — some may already be tracked as issues:
1. Indeed + Notion MCP wiring (`integrations` spec) — both planned integrations remain unimplemented.
2. Slack command to trigger laptop fill remotely (`browser` spec **and** `orchestrator` spec both list this as the same gap — file once, not twice).
3. Cloud headless Mode 2 for low-stakes opt-in auto-submit (`browser` spec) — only Mode 1 (laptop CDP) is shipped.
4. PDF export for tailored resumes to `data/artifacts/{app_id}/` (`generation` spec).
5. Resume PDF upload automation during the laptop fill session (`orchestrator` spec).

Note: a full line-by-line code-vs-spec audit (reading every `.py` file body, not just directory listings and spec "Status" sections) was **not** performed this run — these specs are unusually well self-maintained (each capability's "Status" section already cites the shipping commit/issue, e.g. "SHA-115"), so the marginal value of a deep independent audit may be lower here than on less-disciplined projects. Recommend the next Linear-capable spec-drift run do that deeper pass rather than just filing the above at face value.

### market-feature candidates (proposed, not filed, not yet deduped against Linear)
Grounded in `openspec/project.md`'s stated vision and non-negotiables; cross-checked against `openspec/changes/` (13 non-archived change folders) and none overlap:
1. **📅 Follow-up reminder nudges** — the tracker already exists to log "follow-up dates" per the original build brief, but no spec/code path proactively surfaces them. A scheduled Slack nudge ("it's been 7 days since you applied to Acme — draft a follow-up email?") would close the loop the tracker capability was meant to justify.
2. **📊 Weekly application funnel digest** — a Slack summary (applied / responses / interviews this week) so the user can gauge search health, similar to what Teal/Huntr surface; Slack-only, so it fits the existing architecture without a new UI surface.
3. **🎤 Interview-prep companion** — a Slack thread command once an application moves past "submitted" (e.g. "got an interview") that drafts prep notes (likely questions, company-brief recap, talking points sourced from `profile/projects.yaml` attribution) — reuses the existing `company_brief.py` and `attribution.py` modules rather than new infra.

All three respect the Out of Scope list in `openspec/project.md` (no LinkedIn automation, no auto-submit, no Gmail ingestion, no mobile fill surface).

## Instructions for receiving agent
1. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) against Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`.
2. If under cap: search Linear for each candidate above; file only the ones not already tracked, following `agents/shared/issue-brief.md` (Backlog + `spec-needed`, assignee Sharad Rohra, one relevant emoji, first comment with execution detail per the role files). The three market-feature candidates are Slack-only with no visual surface yet to screenshot — note that explicitly in the issue rather than silently skipping the visual Self-QA step.
3. Run spec-drift steps 10–11 (stale-issue sweep + preview-branch housekeeping) and step 12 (OpenSpec archive sweep) for this project if no other run has covered them recently.
4. Confirm with Sharad whether the Vercel Prod `TBD` row for Application Agent in `projects.md` should be updated so bug-error stops being a no-op every cycle.
5. Append the real outcome to `data/sweep-runs.jsonl` once done.
6. Delete this handover file once the above is complete.
