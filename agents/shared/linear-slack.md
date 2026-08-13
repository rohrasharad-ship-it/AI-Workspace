# Shared Module: Linear → Slack Notifications

Referenced by: `routines/README.md`, `routines/idea-sweep.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`,
`.claude/commands/init-project.md`

**Idea-generation routines do not post to Slack.** Agents file and update
Linear issues only — no end-of-run summary, no cap-skip notice. Linear is the
full record of what a run did.

## Linear's own per-issue bell (separate, optional, not agent-controlled)

Linear projects can optionally be configured (in Linear's own UI, not by any
agent or prompt in this repo) to post a bot card to Slack whenever a new
issue is created — this is Linear's project "bell" integration, independent
of anything these routines do. If a project's bell is enabled, creating
issues via `idea-sweep` will still trigger those Linear-side notifications
even though the agent itself sends nothing.

If you want **zero** Slack messages from idea-generation right now, check
whether the project bell is on: open the Linear project → bell icon (top
right) → *Slack channel notifications*. Turning it off there stops the
per-issue cards; nothing in this repo needs to change for that.

### Setup (if/when you want the bell back on)

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

**Do not enable the Slack tool on idea-generation automations** — agents
never post to Slack for routine-created issues, whether or not the bell is
on.

## Smoke test (only relevant if the bell is intentionally on)

1. Create a throwaway issue manually in the Linear project (Backlog,
   `spec-needed`, assignee Sharad Rohra).
2. Within ~1 minute, confirm a Linear bot card appears in the project's Slack
   channel.
3. Delete or cancel the test issue.

If step 2 fails, the bell is not wired correctly.

## Common failure modes

| Symptom | Likely cause |
|---|---|
| Getting Slack messages you don't want | Project bell is enabled — turn it off in Linear (see above); it's independent of the routine. |
| Nothing in Slack at all | Expected — agents don't post, and either the bell is off or Slack integration is disconnected. |
| Only `@Linear` manual creates show up | Channel has the Linear app but project bell notifications are off — manual `@Linear` and project bell are different features. |
