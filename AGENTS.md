# PM OS — Agent Operating Instructions

This file is the single source of truth for how AI agents operate across all of Sharad's projects.
Every agent (Cursor, Claude, Codex, or otherwise) reads this before starting work.

---

## Core Concept: Trigger vs Gate

Two different things, often confused:

- **Trigger** = what *wakes* an agent. Assigning an issue to an agent, or
  @mentioning it in a comment, starts a fresh agent session. This is the only
  way an agent starts working — nothing else wakes it (a plain comment with no
  @mention wakes no one; a status change wakes no one).
- **Gate** = what the woken agent *checks before proceeding*. This is the
  `agent-ready` label. The agent wakes on assignment, then reads the label to
  decide whether to build or refuse.

So the build flow is always: **assignment wakes the agent → the agent checks the
label → builds if `agent-ready`, refuses if `spec-needed`.**

### Why the label, not the status

Linear automatically flips an issue's status to "In Progress" the instant you
assign it to an agent — core to Linear's native agent-assignment feature, not
configurable. By the time an agent's session starts, status has already left
Backlog whether or not the spec is ready. So **status can never be the gate.**

- `spec-needed` — spec not yet approved. Agent refuses to build.
- `agent-ready` — spec approved by Sharad. Agent may build.

Status is cosmetic — it reflects Linear's automation, not a signal agents act on.

## The Loop

```
SPEC PHASE (issue labeled spec-needed — no agent assignment yet)
  Sharad @mentions an agent in a Linear comment: "@cursor what do you think about..."
  Agent replies in comments, refines the spec
  Back-and-forth until Sharad is satisfied
  Agent updates the issue DESCRIPTION only when Sharad explicitly says so
  No code. No branches. No assignment.

BUILD TRIGGER
  Sharad swaps the label from spec-needed to agent-ready, then assigns to an agent
  (assignment wakes the agent; the agent-ready label is what tells it to proceed)

BUILD PHASE
  Agent's first action: check the label, not the status
  If spec-needed → refuse (see Role 1) and stop
  If agent-ready → proceed:
    Clean up any leftover preview/<issue-id>-* branch from the spec phase
    Read full issue: finalized description = spec, comments = context
    Run OpenSpec, implement, open PR
    Wait for Vercel preview URL on the PR (~60s)
    Decide: trivial change or significant change?
      TRIVIAL (copy, config, meta, styling, bug fix <50 lines):
        Enable GitHub auto-merge → merges itself when checks are green
        Slack: "⚡ Auto-merged: [feature]. Live: [prod URL]"
        Run openspec archive, move issue to Done
      SIGNIFICANT (new component/page/flow, notable UI change):
        Move issue to In Review
        Slack: "🔍 [feature] ready. Preview: [URL]. Approve with '@<agent> approved' on [Linear link]"
        STOP. The session ends here — nothing watches for approval automatically.

APPROVAL (significant changes only)
  Sharad taps the preview URL on his phone, reviews visually
  Either:
    Feedback → comments on the Linear issue (spec change first, then code — see Role 2)
    Approved → comments "@<agent> approved" (the @mention re-wakes the agent)
  On approval, the re-woken agent: merges → openspec archive → moves to Done → Slack "🚀 live"
```

---

## The Spec Layer: OpenSpec

Every repo uses OpenSpec to keep a living spec in sync with what's actually built.
**The whole point of OpenSpec — not optional, not a nice-to-have — is that the
spec is split by capability so agents only read what's relevant to the task in
front of them.** A single flat spec file (however well organized with headers)
defeats this: every agent ends up reading the entire thing for every task,
which wastes tokens and increases the chance of drift/confusion on unrelated
sections.

**Setup (agent does this once per repo, on first task — verify it actually ran,
don't just assume from a prior AGENTS.md instruction):**
```bash
npm install --save-dev @fission-ai/openspec@latest
npx openspec init   # select cursor as assistant
```

**Required structure after init:**
```
openspec/
├── project.md              — small constitution, ~1 page, always read
├── specs/
│   ├── <capability-a>/spec.md    — e.g. hero, journey, voice-agent, contact
│   ├── <capability-b>/spec.md
│   └── ...
└── changes/
    └── <change-id>/proposal.md, tasks.md   — one small delta per active change
```

If a repo currently has a single flat spec file (e.g. a pre-existing `SPEC.md`
from before OpenSpec was adopted), **that must be split into per-capability
files under `openspec/specs/`** as part of running `openspec init` properly —
not left as-is with OpenSpec layered awkwardly on top. Natural capability
boundaries are usually the site's own sections (hero, journey/timeline, about,
contact, voice-agent, etc.) — split along those lines, don't invent new ones.

**`openspec/project.md` template (agent fills this on init):**
```markdown
# Project: <Name>

## What This Is
<One sentence: what the product does and who it's for>

## Tech Stack
- Framework: 
- Styling: 
- Backend/DB: 
- Hosting: Vercel
- Language: TypeScript

## Non-Negotiables
- <Rules the agent must never break>
- Every PR must include the Vercel preview URL
- No new dependencies without a spec proposal first

## Out of Scope
<What this product will never do>

## Capabilities
<List of capability names and which openspec/specs/<name>/spec.md file covers
each one — this is the index an agent uses to find the ONE file it needs>
```

**Three commands — all run by the agent, never Sharad:**
- `npx openspec propose "<title>"` — generates proposal artifacts before coding
- `npx openspec apply` — implements the approved spec
- `npx openspec archive` — folds delta back into the relevant capability's
  `spec.md` after merge — **not** into one giant file

### Who reads how much (this is the rule that actually prevents waste)

| Agent | What it reads | Why |
|---|---|---|
| **Idea-Generation (spec-drift, Role 4)** | `project.md` + **all** capability spec files | Its job is finding gaps across the whole product — full breadth is correct here, not a mistake |
| **Builder / Spec Conversation (Roles 1 & 3) on a single issue** | `project.md` + **only the one relevant capability's** `spec.md` | It's working one feature — reading unrelated capabilities wastes tokens and adds irrelevant context that can cause drift |

If a builder or spec-conversation agent finds itself reading the entire
`openspec/specs/` tree for a single-capability task, something is wrong —
either the capability split doesn't exist yet (fix it, see above) or the task
genuinely spans multiple capabilities (rare — flag it to Sharad rather than
silently reading everything).

---

## Visual Specs: When Text Isn't Enough

PMs today pitch features with a prototype, not a document. This project follows
the same rule: **any time an agent proposes something with a meaningful visual
or motion component — whether during an active spec conversation (Role 3) or
while auto-generating a brand-new idea (Role 4, spec-drift or market/feature) —
it attaches a visual, not just text.** Sharad should never have to imagine what
"the emoji tilts 20 degrees on scroll" or "add a rocket sticker near the hero
CTA" looks like from a sentence.

**Skip this entirely** for changes with no visual/UI component — logic, config,
copy-only changes, backend behavior. Text is genuinely enough there; don't
manufacture a visual to check a box.

**Mechanism (same for every use, only the effort tier changes):**
1. Build a **single standalone HTML/CSS/JS file** — no framework, no build step,
   just the element/interaction in question, or a rough page-outline showing
   roughly where it would sit. Do not touch the real project repo.
2. Save it to `rohrasharad-ship-it/AI-Workspace`, path `previews/<issue-id>-v<n>.html`
   (e.g. `previews/SHA-13-v1.html`)
3. Push to a branch named `preview/<issue-id>-v<n>` (e.g. `preview/SHA-13-v1`).
   **Do not open a PR** — Vercel deploys a preview for any pushed branch, PR or not.
4. Before pushing, **delete the previous iteration's branch** for this issue
   (`git push origin --delete preview/<issue-id>-v<n-1>`). Only one preview
   branch should ever exist per issue at a time.
5. Look up the deployment URL for the new branch. **The Vercel project's output
   directory is the repo root**, so the bare deployment URL just shows the
   placeholder homepage — link the actual file path:
   `<deployment-url>/previews/<issue-id>-v<n>.html`. Paste that full path
   alongside the spec text, not the bare deployment URL.
6. **When the idea is dropped or the spec is finalized** (`agent-ready` label,
   or Sharad rejects it in triage), delete the remaining preview branch. No
   preview branch should survive past that point.

**Two effort tiers — same mechanism, different investment:**

| Tier | When | Effort |
|---|---|---|
| **Full** | Role 3 — Sharad is already actively discussing this issue with you | Build the real interaction if motion matters (e.g. an actual scroll-linked emoji tilt) — this is a live candidate for building |
| **Minimal** | Role 4 — you're auto-generating a brand-new idea Sharad hasn't seen yet | A single static frame is enough: show the emoji itself, roughly where it would sit on the page, or a plain annotated mockup. No interactivity, no polish. Most auto-generated ideas get triaged out — don't over-invest before Sharad has even looked at it. |

**Branch safety — never touch `main`:** only ever run
`git push origin --delete preview/<issue-id>-v<n>` — a fully qualified branch
name with the `preview/` prefix. Never run a bare or wildcard delete command.
`main` is additionally protected at the GitHub level against deletion, but
agents must never attempt to delete anything other than a `preview/*` branch
they created themselves.

---

## Roles

### Role 1: Builder Agent
**Who:** Cursor (primary), Claude, Codex
**Triggered by:** Assigned to an issue

**FIRST ACTION ON ANY ASSIGNMENT — check the label, never the status:**
Status will already say "In Progress" by the time you read this — that is
Linear's automatic behavior on assignment, not a signal that the spec is ready.
Ignore it. Check labels instead.

**If the issue is labeled `spec-needed` (not `agent-ready`):**
Do not build. Post this comment on the Linear issue and stop:

```
⚠️ Spec not confirmed.

This issue is still labeled spec-needed — the spec hasn't been approved yet.
I can't start building.

Please review and refine the spec with me in the comments below, then:
1. Swap the label from spec-needed to agent-ready
2. Re-assign me (or just comment to ping me again)

I'll start the moment I see the agent-ready label.
```

**If the issue is labeled `agent-ready`:**
1. **Cleanup:** delete any leftover `preview/<issue-id>-*` branch from the spec
   phase (`git push origin --delete preview/<issue-id>-vN`). These are scratch
   demos from Role 3 and must not survive into the build.
2. Read the full Linear issue: the finalized description is the spec, comments are context
3. Ensure OpenSpec is installed: `npm install --save-dev @fission-ai/openspec@latest`
4. Run `npx openspec propose "<issue title>"` (base it on the finalized description)
5. Run `npx openspec apply` — implement
6. Open a PR using `.github/pull_request_template.md`, Vercel preview URL in the body
7. Wait up to 90 seconds for Vercel to post the preview URL to the PR
8. **Decide trivial vs significant, then act — no separate reviewer, no extra labels:**

   **TRIVIAL** (copy edit, config, meta tags, styling tweak, bug fix under 50 lines):
   - Enable GitHub native auto-merge on the PR (merges automatically once checks pass)
   - Once merged: run `npx openspec archive`, move issue to `Done`
   - Slack: `⚡ Auto-merged: [title]. Live: [prod URL]`

   **SIGNIFICANT** (new visible component, new page, new user flow, notable UI change):
   - Move issue to `In Review`
   - Slack: the review post below
   - **Stop.** This session ends. Sharad's `@<agent> approved` comment re-wakes an
     agent to finish the merge (see Role 2). Nothing watches automatically.

**Slack post (significant / needs review):**
```
🔍 Ready for your review
Feature: [issue title]
Preview: [Vercel preview URL] ← tap this
What changed: [2 sentences]
Checks: ✅ passing
Approve: comment "@<agent> approved" on [Linear issue URL]
```

**Never:**
- Write any code on an issue labeled `spec-needed` — check the label every time, regardless of status
- Add or remove the `agent-ready` label yourself — only Sharad does that
- Merge a significant PR without Sharad's "approved" — only auto-merge the trivial class
- Push directly to main
- Change code without updating the spec first
- Leave a `preview/*` branch alive once you start building

---

### Role 2: Review & Merge (on approval)
**Who:** Cursor, Claude — whichever agent Sharad @mentions
**Triggered by:** Sharad commenting on the Linear issue while a significant PR is open

There is no always-on autonomous reviewer — that would add cost with no clean
trigger for a solo setup. Instead, the open PR simply waits. Sharad's comment on
the Linear issue re-wakes an agent to act. His comment is one of two kinds:

**A. Feedback ("make the button red", "the animation is too fast"):**
1. Every piece of feedback = spec amendment first
2. Run `npx openspec propose "adjustment: [what Sharad said]"`, update `openspec/project.md`
3. Then update the code
4. Push to the **same branch** — PR and Vercel preview auto-refresh
5. Comment on the Linear issue: "Updated — preview refreshed at the same URL"
6. Stop. Wait for the next comment (more feedback, or approval).

**B. Approval ("@<agent> approved", "@<agent> lgtm"):**
1. Confirm checks are green (Vercel build + any CI). If red, say so and stop.
2. Merge the PR
3. Run `npx openspec archive`
4. Move the Linear issue to `Done`
5. Slack: "🚀 [feature] is live. [prod URL]"

**Spillover — gaps noticed while building or reviewing:**
If you notice a gap out of scope for the current issue (missing error state, no
empty state, accessibility, mobile handling), don't block. File a new Linear
issue (`Backlog`, `spec-needed`, title + 2-sentence description — see the
**New Issue Conventions** rule below for assignee and title format) and note it
in a comment: "Noticed [gap] — filed SHA-XX separately. Not blocking this."

**Never:**
- Merge with failing checks
- Merge a significant PR without an explicit "approved" from Sharad
- Show Sharad code — only preview URLs
- Change code without updating the spec first

---

### Role 3: Spec Conversation Agent
**Who:** Cursor, Claude — @mentioned in Linear comments while issue is labeled `spec-needed`

**This role has no assignment. It is triggered by @mentions in Linear comments.**

When @mentioned on an issue labeled `spec-needed`:
1. Read the issue title, description, and all prior comments
2. Read `openspec/project.md` from the repo for project context
3. Reply in the Linear comment thread:
   - What you understand the feature to be
   - Questions or concerns about the approach
   - Alternative approaches if relevant
   - **A spec-preview link, if the feature is visual or motion-based** — see
     "Visual Specs" below, **full-effort tier** (Sharad is actively engaged already)
4. **Only update the issue description when Sharad explicitly says so** — e.g. "update the issue with this", "finalize the spec", "go ahead and lock this in". Until he says that, keep discussing in comments only.
5. The updated description is what the builder agent will read when assigned

Do not write code in the real project repo. Do not run openspec commands during spec phase.
Do not update the issue description on your own judgment that "agreement was reached" — wait for Sharad's explicit word.

---

## New Issue Conventions (applies to every issue any agent creates, anywhere)

Whether it's Role 2's spillover, Role 4's crons, or any future issue-creating
path — every new Linear issue follows both of these, no exceptions:

1. **Assignee is always Sharad Rohra.** Never assign an agent directly at
   creation time, and never set a `delegate`. Sharad decides who (if anyone)
   works the issue, and when — that decision happens later, not at creation.
2. **Title starts with one relevant emoji, then the rest of the title as
   usual.** e.g. `🎬 [Feature] Project video card shell`, `📱 [Feature] Mobile
   QA pass`, `🔗 [Feature] LinkedIn Open Graph meta tags`. One emoji is enough
   — pick the single most relevant one, don't decorate the whole title with
   several. Sharad is visual; he wants to recognize an issue type at a glance
   in a list, not read a sentence to know what it's about.

---

### Role 4: Idea-Generation Agents (cron-triggered)

Three scheduled agents keep the Backlog self-filling so Sharad triages instead
of inventing work from scratch. All three are set up as **Cursor Automations**
against the project repo. All three obey the same guardrails:

- Create issues only as `Backlog` + `spec-needed` — **never `agent-ready`**
- Assignee is always Sharad Rohra, never an agent (see New Issue Conventions above)
- Title starts with one relevant emoji (see New Issue Conventions above)
- Search Linear first — skip anything already tracked (open or recently closed)
- Max 5 issues per run (4c: max 3 — see below); if nothing real is found, create nothing
- No implementation detail — that belongs to the later spec conversation
- Suggest a priority; Sharad overrides
- **If the proposed issue has a meaningful visual/UI component, attach a visual
  preview per the "Visual Specs" section above, minimal-effort tier, and link
  it in the issue description alongside the text.** This applies to all three
  variants below, not just 4c — a spec-drift gap like "add a rocket sticker
  near the hero CTA" needs a visual just as much as a market/feature idea does.

**4a — Spec-Drift Agent** (weekly, Monday 9am)
Exact prompt to paste into the Cursor Automation:
```
You are the Spec-Drift Idea-Generation Agent from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (Role 4). Read that file first and
follow its guardrails exactly, including the Visual Specs rule and the New
Issue Conventions rule (assignee always Sharad Rohra, title starts with one
relevant emoji).

Repo: rohrasharad-ship-it/resume-website. Linear project: Resume Website.
1. Read openspec/project.md and every file under openspec/specs/ to see what
   is planned/specced.
2. Read the current codebase to see what is actually built.
3. Find meaningful gaps — planned things missing or only half-built. Ignore
   cosmetic nitpicks.
4. Search the Linear "Resume Website" project first; skip anything already tracked.
5. Create up to 5 issues for real gaps: status Backlog, label spec-needed,
   assignee Sharad Rohra (never an agent), title "🔧 [Feature] <name>" — pick
   one relevant emoji, not literally 🔧 every time — 2-3 sentence description
   of the gap and why it matters, suggested priority.
6. If the gap has a visual/UI component, attach a minimal-effort visual
   preview (see Visual Specs section) and link it in the issue description.
7. If nothing meaningful is found, create nothing.
```
Tools to enable: repo (automatic), Linear (create + search issues).

**4b — Bug/Error Agent** (daily, 9am)
Exact prompt to paste into the Cursor Automation:
```
You are the Bug/Error Idea-Generation Agent from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (Role 4). Read that file first and
follow its guardrails exactly, including the Visual Specs rule and the New
Issue Conventions rule (assignee always Sharad Rohra, title starts with one
relevant emoji).

Repo: rohrasharad-ship-it/resume-website, deployed at meet-sharad.vercel.app.
1. Read the Vercel production runtime logs/errors from the last 24 hours.
2. Keep only real, actionable errors — drop one-off network blips, bot noise,
   and anything that self-resolved.
3. Search the Linear "Resume Website" project first; skip anything already tracked.
4. Create up to 5 issues: status Backlog, label spec-needed, assignee Sharad
   Rohra (never an agent), title "🐛 [Bug] <what's broken>" — pick one relevant
   emoji, 🐛 is just the default for a generic bug — 2-3 sentence description
   with the error and when it fires. Priority High if it hits a core flow
   (voice agent, hero, contact), Medium otherwise.
5. If the bug is visual (layout, overlap, broken animation), attach a
   minimal-effort visual preview showing the problem.
6. If the site is clean, create nothing.
```
Tools to enable: repo (automatic), Linear (create + search issues), Vercel
(read deployment logs — add a Vercel API token as an automation secret if
Cursor has no native Vercel integration in your setup).

**4c — Market/Feature Agent** (weekly, Monday 9am — the "suggest brand-new specs" cron)
Unlike 4a/4b, this agent isn't looking for gaps against an existing plan — it's
proposing features nobody has written down yet, based on the product's vision
and what similar products do well. Because these are more speculative, cap at
3 issues per run, not 5, and always attach a visual — a brand-new idea pitched
as a paragraph of text is exactly the "document instead of prototype" problem
this whole section exists to avoid.

Exact prompt to paste into the Cursor Automation:
```
You are the Market/Feature Idea-Generation Agent from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (Role 4). Read that file first and
follow its guardrails exactly, including the Visual Specs rule and the New
Issue Conventions rule (assignee always Sharad Rohra, title starts with one
relevant emoji).

Repo: rohrasharad-ship-it/resume-website. Linear project: Resume Website.
1. Read openspec/project.md in full — the vision, non-negotiables, and
   Out of Scope section. Never propose anything listed as Out of Scope.
2. Read every file under openspec/specs/ to understand what already exists,
   so you don't re-propose something already built or already tracked.
3. Based on the stated vision (a PM's portfolio that itself demonstrates
   product thinking) and how strong portfolio/personal sites differentiate
   themselves, propose up to 3 features not yet in the spec or Linear. If web
   search is available, use it lightly for inspiration; otherwise reason from
   the stated vision and design philosophy alone.
4. Search the Linear "Resume Website" project first; skip anything already
   proposed or tracked, including things filed by the spec-drift agent.
5. Create up to 3 issues: status Backlog, label spec-needed, assignee Sharad
   Rohra (never an agent), title starting with one relevant emoji for the
   specific idea (e.g. 🎯 for a targeting/segmentation feature, 🎚️ for a
   slider tool — pick what actually fits, not a generic default) followed by
   "[Feature] <name>", 2-3 sentence description of the idea and why it fits
   the portfolio's differentiation goals, suggested priority (default Medium
   or Low — these are speculative, not confirmed gaps).
6. Every issue from this agent has a visual/UI component almost by definition
   — attach a minimal-effort visual preview (see Visual Specs section) and
   link it in the issue description. Do not skip this step for this agent.
7. If nothing genuinely differentiated comes to mind, create nothing —
   do not invent filler ideas to hit the cap.
```
Tools to enable: repo (automatic), Linear (create + search issues), web search
(optional — if unavailable, the agent reasons from project.md alone).

---

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

---

## Rules That Always Apply

1. **Assignment wakes an agent; the `agent-ready` label decides whether it builds.** Status is never the gate — Linear auto-flips it to In Progress on assignment.
2. **`spec-needed` = discuss only, no code.** `agent-ready` = build.
3. **Only Sharad adds or removes the `agent-ready` label.**
4. **Only trivial changes self-merge.** Significant changes wait for Sharad's "@<agent> approved".
5. **Vercel preview URL is the only review surface.** Sharad never sees code.
6. **All Sharad feedback goes on the Linear issue** — not the PR, even if he sends it via Slack.
7. **Spec update before code change** — always, even for a one-line fix.
8. **Checks (Vercel build + any CI) must be green before any merge.**
9. **Never push to main directly. Never delete anything but a `preview/*` branch you created.**
10. **Every new issue is assigned to Sharad Rohra, never an agent, and its title starts with one relevant emoji.** See New Issue Conventions.

---

## Distribution: One AGENTS.md, Not Copy-Pasted

This file lives once, in `rohrasharad-ship-it/AI-Workspace`. Every project repo
gets a **thin pointer file** instead of a full copy — while this process is still
evolving, staying in one place beats syncing N copies by hand.

**Thin `AGENTS.md` template for a new project repo:**
```markdown
# Agent Instructions — <Project Name>

STEP 0 — before doing anything else: fetch and follow the full process from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (main branch). Treat it as mandatory,
not optional context. This file only adds project-specific facts.

## Project Facts
- Repo: <owner/repo>
- Linear project: <name>
- Slack channel: <#channel>
- Tech stack: <one line>
```

**Why this works:** an agent's GitHub tool (or a raw-content web fetch, if the
AI-Workspace repo is public) can pull that file in under a second for roughly
800-1000 tokens — negligible, and it happens once per task, not per turn.

**One requirement:** AI-Workspace must be reachable by whatever agent is doing
the fetch. Since this file has no secrets in it, keep AI-Workspace **public** so
any agent (Cursor cloud agent, Claude, Codex via GitHub Action) can fetch it with
zero special repo grants. If AI-Workspace must stay private, use a git submodule
in each project repo instead — more setup, but works without a public repo.

**When to stop pointing and start copying:** once this process is stable and
you're no longer editing it weekly, bake a static copy into each repo. Fetching
a stable file forever is unnecessary overhead — the pointer is a convenience
during active iteration, not a permanent architecture.

---

## Project Index

| Project | Repo | Linear Project | Slack Channel | Vercel Prod |
|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | #resume-website | meet-sharad.vercel.app |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | #pm-ops | ai-workspace.vercel.app (spec-preview sandbox — set up once via Vercel dashboard "Add New Project", see Spec Previews section) |

*Add new projects via `/init-project` skill.*

---

## Idea Feeder Sources (setup order)

| Feeder | What it does | Trigger | Status |
|---|---|---|---|
| Spec-drift agent (4a) | Reads openspec/specs/ vs actual code, files issues for what's specced but unbuilt | Weekly cron (Mon 9am) — **Sharad sets up in Cursor Automations** | Active |
| Bug/error agent (4b) | Reads Vercel runtime errors + logs, files issues for what's breaking in prod | Daily cron — **Sharad sets up in Cursor Automations** | Active |
| Market/feature agent (4c) | Reads project vision, proposes brand-new features not yet in the spec or Linear, always with a visual | Weekly cron (Mon 9am) — **Sharad sets up in Cursor Automations** | Active |
| Spillover | Agent notices a gap while building or reviewing, files a new Backlog issue, doesn't block current work | Per-issue (built into Roles 1 & 2) | Already in loop |
| Capture agent | Sharad drops a Slack message or voice note → becomes a clean Backlog issue | On-demand — **Sharad sets up Slack workflow** | Not yet built |

**Done:** Manual issues, spec-drift, bug/error, market/feature — all three crons have exact prompts in Role 4.
**Remaining:** Capture agent — the only feeder left. Low priority, build when the others feel routine.

---

## What Sharad Does vs What Agents Do

| Sharad | Agents |
|---|---|
| @mentions agents on `spec-needed` issues to refine spec | Draft spec, ask questions, update issue description (only when asked) |
| Swaps label to `agent-ready`, then assigns (assignment wakes the agent) | Check label first, refuse if `spec-needed`, build if `agent-ready` |
| Views Vercel preview URL on phone | Decide trivial (self-merge) vs significant (wait for approval) |
| Comments feedback on Linear issue | Update spec then code, refresh preview |
| Comments "@<agent> approved" | Merge, archive spec, move to Done, notify Slack |
| Overrides issue priority | Everything else |
