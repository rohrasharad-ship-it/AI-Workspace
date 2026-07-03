# Shared Module: Conventions & Rules That Always Apply

Referenced by: every role in `agents/`. Every agent reads this file regardless
of role — it is the one exception to "only read what your role needs."

## New Issue Conventions (applies to every issue any agent creates, anywhere)

Whether it's reviewer spillover, an idea-generation routine, or any future
issue-creating path — every new Linear issue follows both of these, no exceptions:

1. **Assignee is always Sharad Rohra.** Never assign an agent directly at
   creation time, and never set a `delegate`. Sharad decides who (if anyone)
   works the issue, and when — that decision happens later, not at creation.
2. **Title starts with one relevant emoji, then the rest of the title as
   usual.** e.g. `🎬 [Feature] Project video card shell`, `📱 [Feature] Mobile
   QA pass`, `🔗 [Feature] LinkedIn Open Graph meta tags`. One emoji is enough
   — pick the single most relevant one, don't decorate the whole title with
   several. Sharad is visual; he wants to recognize an issue type at a glance
   in a list, not read a sentence to know what it's about.

## Cursor Rules (Optional Safety Net — Not Required Right Now)

AGENTS.md is the single source of truth and is a convention Cursor, Claude, and
Codex all read automatically at the start of a session — including cloud/background
sessions triggered by Linear assignment. Duplicating the full ruleset into Cursor
Settings → Rules creates a second copy that will drift the moment this file changes.
Don't do that.

If — and only if — Cursor's automation-triggered agent is ever observed skipping
AGENTS.md (this has not been confirmed; the one time it happened, AGENTS.md didn't
exist in the repo yet), add exactly this one line as a fallback in Cursor Settings → Rules:

```
Before starting any task, read and follow AGENTS.md in the repo root. Treat it as
mandatory instructions, not optional context.
```

Nothing more. If it still gets skipped after that, that's a signal to investigate
further — not to paste more rules in.

## Rules That Always Apply

1. **Assignment wakes an agent; the `agent-ready` label decides whether it builds.** Status is never the gate — Linear auto-flips it to In Progress on assignment.
2. **`spec-needed` = discuss only, no code.** `agent-ready` = build.
3. **Only Sharad adds or removes the `agent-ready` label.**
4. **Every PR waits for Sharad's explicit "@<agent> approved" before merging.** No auto-merge, no size-based exception — a typo fix and a new feature both wait the same way.
5. **Vercel preview URL is the only review surface.** Sharad never sees code.
6. **All Sharad feedback goes on the Linear issue** — not the PR, even if he sends it via Slack.
7. **Spec update before code change** — always, even for a one-line fix.
8. **Checks (Vercel build + any CI) must be green before any merge.**
9. **Never push to main directly. Never delete anything but a `preview/*` branch you created.**
10. **Every new issue is assigned to Sharad Rohra, never an agent, and its title starts with one relevant emoji.** See New Issue Conventions above.
11. **Build must always succeed before any PR opens.** Existing tests (if the repo has any) run only for changes touching shared/critical surface — never required to exist, never run wholesale for every small change.
12. **Visual Self-QA is mandatory for the builder role and all idea-generation routines** — a real screenshot, actually looked at, attached to the Linear issue via the signed-upload flow (never base64). This is not optional and not skippable to save tokens.
13. **Moving an issue to `In Review` happens immediately when a PR opens — never gated on Vercel, screenshots, or anything downstream.** A step failing later must not silently undo or block what already succeeded earlier.
14. **Never go silent.** If the preview URL can't be obtained after reasonable polling, post what you have (the PR link) rather than posting nothing at all.

## What Sharad Does vs What Agents Do

| Sharad | Agents |
|---|---|
| @mentions agents on `spec-needed` issues to refine spec | Draft spec, ask questions, update issue description (only when asked) |
| Swaps label to `agent-ready`, then assigns (assignment wakes the agent) | Check label first, refuse if `spec-needed`, build if `agent-ready` |
| Views Vercel preview URL on phone | Verify build + tests pass before opening any PR |
| Comments feedback on Linear issue | Update spec then code, refresh preview |
| Comments "@<agent> approved" | Merge, archive spec, move to Done, notify Slack |
| Overrides issue priority | Everything else |
