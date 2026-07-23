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
remembering what it created. Two backups catch orphans regardless of which
session created them:

1. **Scheduled GitHub Action** — `.github/workflows/preview-branch-cleanup.yml`
   in AI-Workspace runs `scripts/cleanup-preview-branches.sh` weekly (Monday
   9am UTC). Requires `LINEAR_API_KEY` as a repo secret.
2. **Spec-drift housekeeping** — `agents/spec-drift.md` step 11 runs the same
   script during each idea-sweep (preview branches live in AI-Workspace, not
   project repos).

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
12. **Visual Self-QA is mandatory for the builder role and all idea-generation routines** — a real screenshot, actually looked at, attached to the Linear issue via the signed-upload flow (never base64). This is not optional and not skippable to save tokens. If session network policy blocks outbound HTTPS, follow the documented fallback in `agents/shared/visual-self-qa.md` — attempt honestly, comment with the block details, defer visual QA to Sharad; never skip silently.
13. **Moving an issue to `In Review` happens immediately when a PR opens — never gated on Vercel, screenshots, or anything downstream.** A step failing later must not silently undo or block what already succeeded earlier.
14. **Never go silent.** If the preview URL can't be obtained after reasonable polling, post what you have (the PR link) rather than posting nothing at all.
15. **Keep the Status Snapshot block at the top of every issue description
    current on every touch** (see `agents/shared/status-snapshot.md`) —
    Sharad should be able to read the description alone and know the current
    phase, without opening comments.
16. **For visual or motion UI work, start at `design/README.md`** — copy-paste
    from the resource catalog or local snippets (`design/snippets/`) rather
    than inventing animations from scratch. See `design/workflow.md`.
17. **Blocked by missing tool access → write a standard handover** (see
    Blocked-agent handover below). Do not invent a new note location or filename
    shape.

## Blocked-agent handover

When an agent hits a **hard tool-access wall** — it cannot finish assigned
work because a required integration is definitively unavailable (no Linear MCP,
no push access to the target repo, no Vercel API token, etc.) — it must **not**
improvise a new "leave a note for the next agent" pattern. Use this convention
instead.

### When to use

Use a handover when you have done everything your session *can* do and the
remaining work requires tools you lack — not when you are merely uncertain or
waiting on Sharad's input.

### Location and naming

All handovers live in **AI-Workspace** under `handovers/`, even when the work
targets another project repo.

| Kind | Path | Use when |
|---|---|---|
| **Action handover** | `handovers/<ISSUE-ID>-<short-slug>.md` | Blocked agent needs another agent (with different tool access) to *do* something: create or cancel a Linear issue, post a comment, enable infra, etc. |
| **Artifact bundle** | `handovers/<ISSUE-ID>/README.md` (+ files alongside) | Blocked agent finished implementation locally but cannot push to the target repo — leave apply instructions and any patch/source files. |

`<ISSUE-ID>` is the Linear issue driving the session (e.g. `SHA-53`).
`<short-slug>` is 2–4 kebab-case words describing the handover (e.g.
`linear-mcp`, `repo-push-blocked`).

**Do not** create `delivery/` directories or ad hoc `handovers/` filenames —
those predate this convention. Existing `handovers/linear-*` and
`delivery/<issue-id>/` paths are historical examples only; new handovers MUST
follow the table above.

### Required header (both kinds)

Every handover MUST start with this block:

```markdown
# Handover: <one-line summary>

**For:** <who should pick this up — e.g. "Any agent with Linear MCP access">
**From:** <agent role + issue ID + approximate date>
**Blocked by:** <specific missing access — e.g. "No Linear MCP in cloud session">
**Action:** <imperative one-liner — what the receiver must accomplish>
**Issue:** [<ISSUE-ID>](<Linear issue URL>)
```

### Required body sections

1. **Payload** — everything the receiver needs without re-reading the session
   (issue fields to create, code locations, apply steps, links).
2. **Instructions for receiving agent** — numbered checklist of exact steps;
   end with what *not* to do when applicable.

### Session steps (blocked agent)

1. Write the handover file at the path above on your working branch.
2. **Comment on the Linear issue** with: blocker summary, link to the handover
   file on GitHub (branch or PR URL), and what you completed vs what remains.
3. **Refresh the Status Snapshot** — Phase stays at the current stage; `Last
   update` must mention the blocker and handover link.
4. **Do not go silent** — if you cannot open a PR, still commit and push your
   branch when possible; Sharad or the next agent needs the handover in git.

### Receiving agent

1. Read the handover file from the linked path.
2. Execute **Instructions for receiving agent**.
3. Comment on the original issue when done.
4. Delete the handover file only once the blocked work is fully complete and
   tracked elsewhere — until then, it is the source of truth.

## What Sharad Does vs What Agents Do

| Sharad | Agents |
|---|---|
| @mentions agents on `spec-needed` issues to refine spec | Draft spec, ask questions, refresh Status Snapshot every reply |
| Replies with any affirmative once the spec looks ready (see `agents/spec-conversation.md`) | Finalizes spec text, swaps label to `agent-ready`, assigns itself, and builds — no manual label/assignee work for Sharad |
| Views Vercel preview URL on phone | Verify build + tests pass before opening any PR |
| Comments feedback on Linear issue | Update spec then code, refresh preview |
| Comments "@<agent> approved" | Merge, archive spec, move to Done, notify Slack |
| Overrides issue priority | Everything else |
