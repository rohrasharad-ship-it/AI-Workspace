# Handover: idea-sweep routine blocked for Application Agent — no Linear MCP in session

**For:** Any agent/session with Linear MCP access
**From:** Claude cloud session running `routines/idea-sweep.md` for Application Agent, 2026-09-22
**Blocked by:** No Linear MCP server connected in this session (confirmed via tool search — zero `mcp__linear__*` tools present, and no `LINEAR_API_KEY` in env). This blocks every Linear read/write the routine needs: the Issue Cap pre-flight, `list_issues` search-before-file, `save_issue`/create, comments, and attachments.
**Action:** Run the Issue Cap pre-flight for Application Agent, then review and file the candidate issues below (or re-run the three roles fresh) per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`.
**Issue:** N/A — this is a routine trigger ("Run the idea-sweep routine for Application Agent"), not an issue-driven session.

---

## What could and couldn't run this cycle

| Step | Status | Why |
|---|---|---|
| Issue Cap pre-flight (`agents/shared/issue-cap.md`) | **Not run** | Needs `list_issues` against Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913` — no Linear MCP. **The candidates below have NOT been checked against the cap or against existing Linear issues — do that before filing anything.** |
| spec-drift steps 1–3 (read specs vs code, find gaps) | **Done** (read-only) | No Linear needed for reading |
| spec-drift steps 4–9 (dedupe search + file) | **Not run** | Needs Linear search + `save_issue` |
| spec-drift step 10 (stale-issue sweep) | **Not run** | Needs Linear `list_issues` + comment |
| spec-drift step 11 (preview-branch cleanup) | **Not run** | `scripts/cleanup-preview-branches.sh` hard-requires `LINEAR_API_KEY` (checked script source — it exits immediately without it), not set in this session |
| spec-drift step 12 (openspec archive sweep) | **Not run** | `npx openspec` isn't resolvable in this sandbox without a network install (`@fission-ai/openspec` not present in `node_modules`, `npx openspec` fails with "could not determine executable to run"). Separately, without a `gh` binary the script's `has_open_pr_for_change` check silently degrades to "no open PR" on failure rather than skipping — **do not run `--sweep` without `gh` available**, it could archive a change folder that still has an open PR referencing it. |
| bug-error (all steps) | **Not run** | Application Agent's Vercel Prod in `projects.md` is `TBD` — no prod URL/logs source exists yet, independent of the Linear blocker |
| market-feature steps 1–3 (read vision, propose) | **Done** (read-only) | No Linear needed for reading |
| market-feature steps 4–9 (dedupe search + file) | **Not run** | Needs Linear search + `save_issue` |

**Recurring-pattern note:** `data/sweep-runs.jsonl` shows Application Agent runs on 2026-07-11, 2026-08-06, and 2026-08-19 all logged as `"clean":true`. It's worth double-checking whether those were genuinely clean runs or also silently hit this same missing-Linear-MCP wall and got logged as clean by mistake — this session did not verify that either way.

---

## Payload — candidate issues (unverified against Linear, do not file blind)

Read: `openspec/project.md`, all six `openspec/specs/*/spec.md` files, all active (non-archived) `openspec/changes/*` proposals, and `src/application_agent/**` (profile, generation, tracker, integrations/{slack,linear,apollo}, browser, orchestrator, cli.py). Everything below was verified against actual code, not invented — but still needs the search-before-file dedupe step against current Linear state, since some may already be tracked as active `openspec/changes/*` work that later gets its own Linear issue via other agent activity.

### Spec-drift candidates (max 5, suggested)

1. **🐛 Slack "updated resume" inbound path doesn't exist**
   - Problem: project.md + orchestrator/spec.md + profile/spec.md describe posting an updated resume to `#application-agent` as a live profile-update path; no such handler exists.
   - Solution: add a `file_shared` handler that validates + writes into `profile/`.
   - Why: without it, "Slack is remote control for everything except fill" is false — profile edits are file-only today.
   - What it looks like: bot acks the file, diffs against current resume, asks confirm before overwrite.
   - Checked: `openspec/project.md`, `specs/orchestrator/spec.md`, `specs/profile/spec.md` vs `src/application_agent/integrations/slack/app.py` (only `/capture`, `/outreach`, `/queue`, thread keywords, 3 buttons — no file event).
   - Suggested priority: Medium.

2. **🐛 Tracker "follow-up dates" field is undocumented vapor**
   - Problem: `tracker/spec.md` lists follow-up dates as core coverage; no such field exists on the `Application` model.
   - Solution: add `follow_up_at` + a `/queue` surface for overdue follow-ups.
   - Why: the spec's own "What This Covers" line names it as a defining feature.
   - What it looks like: tracker stores a date, Slack digest nudges on due ones.
   - Checked: `specs/tracker/spec.md` vs `src/application_agent/models.py`, `tracker/store.py` (grep for `follow_up`: zero hits).
   - Suggested priority: Medium.

3. **🐛 No real audit log, only current-state overwrite**
   - Problem: the project's own top non-negotiable ("every action written to audit log") isn't met — `Application` has one `updated_at` timestamp, overwritten each change, no per-action history.
   - Solution: append-only event log (action, actor, timestamp) alongside the state JSON.
   - Why: `tracker/spec.md` calls this "the hard requirement that alone justifies the project."
   - What it looks like: `applications.log.jsonl` or an `events` list per app.
   - Checked: `project.md` Non-Negotiables, `specs/tracker/spec.md` vs `tracker/store.py`, `models.py` (no "audit" hits in src).
   - Suggested priority: Medium.

4. **🐛 Slack channel scoping isn't enforced**
   - Problem: `integrations/spec.md` non-negotiable requires Slack inbound scoped to the designated channel; any channel the bot is in can currently trigger commands.
   - Solution: check `channel_id` against `SLACK_CHANNEL_ID` env and no-op/ack-only otherwise.
   - Why: accidental invocation in an unrelated channel could leak drafts or dedupe wrong.
   - What it looks like: one guard clause at top of each handler.
   - Checked: `specs/integrations/spec.md` vs `slack/app.py`, `slack/service.py` (no channel allow-list anywhere).
   - Suggested priority: Low.

5. **🐛 robots.txt / ToS check missing from ATS discovery**
   - Problem: `browser/spec.md` non-negotiable to respect robots.txt is unimplemented; `browser/discovery.py` fetches posting pages via raw `httpx` with no robots check.
   - Solution: fetch/parse robots.txt once per host, skip discovery if disallowed.
   - Why: explicit non-negotiable; also touches ToS risk on the companion `company_brief` fetch.
   - What it looks like: small cached robots-checker used by `discovery.py` and `company_brief.py`.
   - Checked: `specs/browser/spec.md` Non-Negotiables vs `browser/discovery.py`, `generation/company_brief.py`.
   - Suggested priority: Low.

### Market-feature candidates (max 3, suggested)

1. **✨ Interview Prep Kit**
   - Problem: the co-pilot stops helping right after apply; competitors (Simplify, Teal) do too.
   - Solution: `draft_interview_prep()` using company_brief + tailored resume + projects.yaml — likely questions + talking points.
   - Why: differentiates from pure autofill tools; reuses the existing generation pipeline/data.
   - What it looks like: Slack message posted once status reaches `ready`/`submitted`, pinned to the app thread.
   - Not in specs/changes today; draft-only, human-reviewed, no new non-negotiable risk.
   - Suggested priority: Medium.

2. **🎯 Outcome-Aware Resume Analytics**
   - Problem: user tailors multiple resume tracks but gets no feedback on which bullets/track actually convert.
   - Solution: weekly digest over tracker JSON — response rate by track, company size, keyword overlap.
   - Why: no ATS-autofill competitor closes this loop; pure use of data already collected.
   - What it looks like: scheduled Slack post, e.g. "Product track: 3/9 replies vs Chief-of-Staff 1/6."
   - Suggested priority: Low.

3. **💬 Negotiation Assistant**
   - Problem: tracker lifecycle effectively ends at `submitted`; no support through interview/offer/negotiation.
   - Solution: extend lifecycle with `interview`/`offer` stages; draft (never send) a counter-offer email from `preferences.yaml` comp range.
   - Why: matches "career co-pilot," not just "apply co-pilot"; draft-only fits the existing cold-email pattern.
   - What it looks like: Slack thread command "offer" → drafted email + 3 talking points.
   - Suggested priority: Low.

All 3 feature ideas stay draft-only/human-send, never touch LinkedIn, and don't add autonomous submission — consistent with `openspec/project.md`'s Out of Scope list.

---

## Instructions for receiving agent

1. Run the Issue Cap pre-flight for Application Agent (`agents/shared/issue-cap.md`, Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`). If at/over cap, stop — don't file.
2. For each candidate above, search the Application Agent Linear project first (title/keywords) — skip anything already tracked, including anything that shipped as a Linear issue from one of the `openspec/changes/*` proposals already in flight.
3. File survivors as Backlog + `spec-needed`, assignee Sharad Rohra, per `agents/shared/issue-brief.md` and `agents/shared/conventions.md`. Cap at 5 spec-drift + 3 market-feature, same as a normal run.
4. Visual/screenshot requirements still apply per `agents/shared/visual-self-qa.md` and `agents/shared/visual-specs.md` — note Application Agent's Vercel Prod is `TBD` in `projects.md`, so a live-site screenshot may not be possible yet; if so, follow the documented fallback (attempt honestly, note the block, defer to Sharad — never skip silently).
5. bug-error still cannot run for this project until a Vercel Prod URL exists — separately worth flagging to Sharad, not something to invent a workaround for.
6. Before running spec-drift step 11 (preview-branch cleanup), confirm `gh` is available in whatever session runs it — the archive script (step 12) silently mis-skips its open-PR safety check without `gh`.
7. Once filed, append an accurate `data/sweep-runs.jsonl` line for this cycle (this session already appended one marked `"blocked": true` for the 2026-09-22 attempt — add a new line for your own run rather than editing that one).
8. Delete this handover file once Application Agent's candidates have been triaged (filed or explicitly rejected) — until then it's the record of this cycle's findings.
