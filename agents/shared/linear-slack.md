# Shared Module: Linear → Slack Notifications

Referenced by: `routines/README.md`, `routines/idea-sweep.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`,
`.claude/commands/init-project.md`

Idea-generation routines surface work in Slack through **two independent
channels**. Both should work; neither replaces the other.

## Two notification paths

| Path | Who posts | When | What Sharad sees |
|---|---|---|---|
| **Routine summary** | The orchestrating agent (via Slack tool) | End of each `idea-sweep` run | One consolidated message: how many issues filed per role, links, or a skip notice |
| **Per-issue bell** | Linear's Slack integration (automatic) | Each new issue created in the project | Linear bot card in the project channel — title, description snippet, link |

**Agents do not post per-issue Slack messages for routine-created issues.**
The routine summary is the agent's job; per-issue cards are Linear's job.

## Setup (once per Linear project)

1. **Connect Slack at workspace level** — Linear Settings → Integrations →
   Slack → Authorize (if not already connected).
2. **Open the Linear project** — e.g. Resume Website.
3. **Bell icon** — top right of the project page → **Configure** next to
   *Slack channel notifications*.
4. **Pick the channel** — match `projects.md` (`#resume-website` for Resume
   Website, `#pm-ops` for PM OS, etc.).
5. **Enable events** — at minimum **Issue created**. Optionally: comments,
   status changes.
6. **Confirm in Slack** — Linear posts a confirmation like "Notifications for
   *Resume Website* are now enabled" in the channel.

Repeat for every row in `projects.md` when onboarding a new project
(`/init-project` Step D).

**Do not enable the Slack tool on idea-generation automations** — the routine
summary is posted by the orchestrator at the end of the run, not by each
sub-role. Per-issue notifications come from Linear's bell, not from agents.

## Smoke test

After configuring the bell (or when verifying SHA-15-style cron health):

1. Create a throwaway issue manually in the Linear project (Backlog,
   `spec-needed`, assignee Sharad Rohra).
2. Within ~1 minute, confirm a Linear bot card appears in the project's Slack
   channel (not just the routine summary — this is a manual test issue).
3. Delete or cancel the test issue.

If step 2 fails, the bell is not wired correctly — fix before blaming the cron.

## Common failure modes

| Symptom | Likely cause |
|---|---|
| Routine summaries arrive but no per-issue Linear cards | Project bell not configured, or "Issue created" event not enabled. Bell was added after the last cron run that filed issues — still unverified. |
| Nothing in Slack at all | Slack integration disconnected at workspace level, or Linear bot not invited to the channel. |
| Only `@Linear` manual creates show up | Channel has the Linear app but project bell notifications are off — manual `@Linear` and project bell are different features. |
| Idea-sweep says "skipped" every day | Issue cap hit (5+ open issues per project) — no issues created, so no Linear per-issue notifications to test. Triage backlog first. |

## Phase 2 cron verification checklist

After standing up `idea-sweep` for resume-website, confirm each row once (re-run
after any prompt or tool-grant change):

| Check | Pass criteria |
|---|---|
| Routine fires on schedule | External trigger shows successful runs at expected cadence. |
| Issue fields | Backlog, `spec-needed`, assignee Sharad Rohra — never `agent-ready`, never an agent assignee. |
| No duplicates | Second run on same codebase/logs does not re-file already-tracked gaps. |
| Description shape | Issue Brief format — five scannable one-liners, no implementation detail (`agents/shared/issue-brief.md`). |
| Execution detail | First comment on each issue has evidence (spec refs, search terms, log excerpts). |
| Routine Slack summary | End-of-run message in `#resume-website` (filed N issues, or skip notice). |
| Linear per-issue bell | New issue triggers a Linear bot card in `#resume-website` within ~1 min (bell configured + smoke-tested). |
| Screenshots | Live-site screenshot attached per `agents/shared/visual-self-qa.md`. |

If the routine-summary row passes but the Linear-bell row fails, fix the
project bell — not the cron prompts.
