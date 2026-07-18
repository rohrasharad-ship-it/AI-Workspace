# Shared Module: Conventions & Rules That Always Apply

Referenced by: every role in `agents/`. Every agent reads this file regardless
of role — it is the one exception to "only read what your role needs."

## New Issue Conventions (applies to every issue any agent creates, anywhere)

Whether it's reviewer spillover, an idea-generation routine, or any future
issue-creating path — every new Linear issue follows all of these, no exceptions:

1. **Assignee is always Sharad Rohra.** Never assign an agent directly at
   creation time, and never set a `delegate`. Sharad decides who (if anyone)
   works the issue, and when — that decision happens later, not at creation.
2. **Title starts with one relevant emoji, then the rest of the title as
   usual.** e.g. `🎬 [Feature] Project video card shell`, `📱 [Feature] Mobile
   QA pass`, `🔗 [Feature] LinkedIn Open Graph meta tags`. One emoji is enough
   — pick the single most relevant one, don't decorate the whole title with
   several. Sharad is visual; he wants to recognize an issue type at a glance
   in a list, not read a sentence to know what it's about.
3. **Description uses the Issue Brief format** — five scannable one-liners
   (`In short`, `Problem`, `Solution`, `Why`, `What it looks like`). No long
   paragraphs at creation time. Full template, rules, and examples:
   `agents/shared/issue-brief.md`.

## Cursor Rules (Fallback — Now Confirmed Needed, Not Just Hypothetical)

AGENTS.md is the single source of truth and is a convention Cursor, Claude, and
Codex all read automatically at the start of a session — including cloud/background
sessions triggered by Linear assignment. Duplicating the full ruleset into Cursor
Settings → Rules creates a second copy that will drift the moment this file changes.
Don't do that.

**This has now been directly observed** (Cursor's builder agent skipping the
move-to-`In Review` step — see `agents/builder.md` step 8), not just a
hypothetical. Add exactly this one line as a fallback in Cursor Settings → Rules now:

```
Before starting any task, read and follow AGENTS.md in the repo root. Treat it as
mandatory instructions, not optional context.
```

Nothing more. If it still gets skipped after that, that's a signal to
investigate further — not to paste more rules in.

### Structural backup for the `In Review` transition specifically

Don't rely solely on an agent remembering one API call at the right moment —
add a second, non-agent-dependent path: in Linear, go to **Settings →
Integrations → GitHub** and enable the built-in workflow automation that moves
an issue's status based on its linked PR's state (open PR → `In Review`,
PR merged → `Done`). This is a native Linear feature, not something any agent
has to execute — once configured, the status updates correctly even if the
agent's own step 8 is skipped. Keep the agent instruction above as well; the
two paths don't conflict, whichever fires first wins and both land on the
same correct status.

### Structural backup for preview-branch pileup

The per-issue cleanup rules in `agents/shared/visual-specs.md` (delete the
previous iteration's branch, delete on spec-lock) rely on an agent
remembering what it created. `agents/spec-drift.md` step 9 adds a periodic
sweep to the weekly spec-drift routine run: list all remote `preview/*`
branches, check each one's issue via the branch name
(`preview/<issue-id>-v<n>`), and delete any branch whose issue is no longer
`spec-needed` (i.e. it's `agent-ready`, `In Review`, `Done`, or canceled) or
that isn't the highest version number for that issue. This catches orphans
regardless of which session created them.

## Rules That Always Apply

1. **Assignment wakes an agent; the `agent-ready` label decides whether it builds.** Status is never the gate — Linear auto-flips it to In Progress on assignment.
2. **`spec-needed` = discuss only, no code.** `agent-ready` = build.
3. **The `agent-ready` label only changes as a direct, same-turn consequence
   of Sharad's explicit approval** (see `agents/spec-conversation.md`, steps
   6-7) — never on an agent's own inferred judgment that agreement was
   reached, and never at any other time. Sharad's job is to type the
   approval; the agent's job is to execute the mechanical label/assignee
   change — not to decide independently that approval happened.
4. **Every PR waits for Sharad's explicit "@<agent> approved" before merging.** No auto-merge, no size-based exception — a typo fix and a new feature both wait the same way.
5. **Vercel preview URL is the only review surface.** Sharad never sees code.
6. **All Sharad feedback goes on the Linear issue** — not the PR, even if he sends it via Slack.
7. **Spec update before code change** — always, even for a one-line fix.
8. **Checks (Vercel build + any CI) must be green before any merge.**
9. **Never push to main directly. Never delete anything but a `preview/*`
   branch** — either one you created this session, or, for the weekly
   spec-drift routine's housekeeping sweep, an orphaned `preview/*` branch
   whose issue is no longer `spec-needed` (see the Cursor Rules backup
   section above).
10. **Every new issue is assigned to Sharad Rohra, never an agent, its title starts with one relevant emoji, and its description uses the Issue Brief format.** See New Issue Conventions above.
11. **Build must always succeed before any PR opens.** Existing tests (if the repo has any) run only for changes touching shared/critical surface — never required to exist, never run wholesale for every small change.
12. **Visual Self-QA is mandatory for the builder role and all idea-generation routines** — a real screenshot, actually looked at, attached to the Linear issue via the signed-upload flow (never base64). This is not optional and not skippable to save tokens.
13. **Moving an issue to `In Review` happens immediately when a PR opens — never gated on Vercel, screenshots, or anything downstream.** A step failing later must not silently undo or block what already succeeded earlier.
14. **Never go silent.** If the preview URL can't be obtained after reasonable polling, post what you have (the PR link) rather than posting nothing at all.
15. **Keep the Status Snapshot block at the top of every issue description
    current on every touch** (see `agents/shared/status-snapshot.md`) —
    Sharad should be able to read the description alone and know the current
    phase, without opening comments.
16. **For visual or motion UI work, start at `design/README.md`** — copy-paste
    from the resource catalog or local snippets (`design/snippets/`) rather
    than inventing animations from scratch. See `design/workflow.md`.

## What Sharad Does vs What Agents Do

| Sharad | Agents |
|---|---|
| @mentions agents on `spec-needed` issues to refine spec | Draft spec, ask questions, refresh Status Snapshot every reply |
| Replies with any affirmative once the spec looks ready (see `agents/spec-conversation.md`) | Finalizes spec text, swaps label to `agent-ready`, assigns itself, and builds — no manual label/assignee work for Sharad |
| Views Vercel preview URL on phone | Verify build + tests pass before opening any PR |
| Comments feedback on Linear issue | Update spec then code, refresh preview |
| Comments "@<agent> approved" | Merge, archive spec, move to Done, notify Slack |
| Overrides issue priority | Everything else |
