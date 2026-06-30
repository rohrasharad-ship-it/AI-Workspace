# PM OS — Agent Operating Instructions

This file is the single source of truth for how AI agents operate across all of Sharad's projects.
Every agent (Cursor, Claude, Codex, or otherwise) reads this before starting work.

---

## The Loop

```
[Issue lands in Backlog — thin title + one sentence]
    → Sharad reviews priority on mobile
    → Sharad assigns to an agent (still in Backlog)
    → Agent enters SPEC MODE: drafts spec as Linear comment, asks questions
    → Back-and-forth in Linear comments until spec is right
    → SHARAD moves issue to Todo (this is the only build trigger)
    → Agent sees Todo → enters BUILD MODE → codes → opens PR
    → Vercel auto-generates preview URL on PR
    → Slack notifies Sharad with preview URL
    → Sharad taps URL on phone — reviews visually, not code
    → Sharad comments "approved" on Linear issue
    → Agent merges PR
    → Vercel deploys to production
    → Agent runs openspec archive, moves issue to Done
```

**The only action that starts coding: Sharad moves status to Todo.**
**The only review surface: Vercel preview URL on Sharad's phone.**

---

## Status Meanings and Who Controls Each

| Status | Meaning | Who can move here |
|---|---|---|
| Backlog | Idea exists, spec being drafted | Agent (creates), Sharad (from triage) |
| Todo | Spec approved — build it | **Sharad only. Agents never move here.** |
| In Progress | Agent is actively coding | Agent (auto, when it starts after Todo) |
| In Review | PR open, Vercel preview ready | Agent (auto, on PR creation) |
| Done | Merged and live in production | Agent (auto, after merge) |

**Agents are permitted to move: Backlog → In Progress → In Review → Done.**
**Agents are never permitted to move anything to Todo. That is Sharad's gate.**

---

## The Spec Layer: OpenSpec

Every repo uses OpenSpec to keep a living spec in sync with what's actually built.

**Setup (agent does this once per repo, on first task):**
```bash
npm install --save-dev @fission-ai/openspec@latest
npx openspec init   # select cursor as assistant
```

This creates `openspec/project.md` — the project's constitution. The agent populates it on init.

**`openspec/project.md` template:**
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
- Every PR must include a Vercel preview URL
- No new dependencies without proposing first

## Out of Scope
<What this product will never do>
```

**Three commands — all run by the agent, never Sharad:**
- `npx openspec propose "<title>"` — generates proposal.md, design.md, tasks.md
- `npx openspec apply` — implements the approved spec
- `npx openspec archive` — folds delta back into openspec/project.md after merge

---

## Roles

### Role 1: Builder Agent
**Who:** Cursor (primary), Claude, Codex

**Triggered by:** Linear issue assigned to the agent

---

#### SPEC MODE — when issue status is Backlog

This is the only thing the agent does while an issue is in Backlog. No code.

1. Read the issue title and description
2. Read `openspec/project.md` for project context
3. Run `npx openspec propose "<issue title>"` to generate structured spec artifacts
4. Post a comment on the Linear issue in this format:

```
Here's my understanding of what we're building:

What: [one sentence]

How: [key technical choices]

Tasks I'm planning:
- [ ] task 1
- [ ] task 2
- [ ] task 3

Questions / assumptions:
- [anything that might be wrong or needs Sharad's input]

Reply to refine this, or move to Todo when the spec looks right.
```

5. When Sharad replies — update the issue description with the refined spec, ask follow-up questions if needed.
6. Keep iterating in comments until Sharad is satisfied.
7. **Do not write any code. Do not create any branch. Wait for Todo status.**

---

#### BUILD MODE — when issue status changes to Todo

Status changed to Todo = spec is approved = build it now.

1. Run `npx openspec apply` — implement all tasks from the approved spec
2. Open a PR using the repo's `.github/pull_request_template.md`
3. PR description must include: what was built, **Vercel preview URL**, how to verify in 3 steps
4. Move Linear issue to `In Review`

**Vercel preview URL is the most important thing in the PR.** It is what Sharad reviews. Without it, the review cannot happen.

---

**Never (ever):**
- Write code while issue is in Backlog
- Move an issue to Todo
- Merge your own PR
- Push directly to main
- Add dependencies not in `openspec/project.md` without a new spec proposal

---

### Role 2: Reviewer Agent
**Who:** Cursor, Claude

**Triggered by:** PR opened on GitHub

**Decision tree:**
```
Is CI green?
  No  → Comment on PR with what failed. Do not merge. Notify Slack.
  Yes →
    Is this a trivial change? (typo, copy, config, single-line)
      Yes → Merge immediately.
            Post to Slack: "[Project] ✅ [feature] merged. Deploying."
      No  →
            Post to #[project-slack-channel]:
              "Ready for your review:
               Feature: [title]
               Preview: [Vercel URL] ← tap this
               What changed: [2 sentences]
               CI: ✅ green
               Approve: reply 'approved' on [Linear issue link]"

            Wait for Sharad to comment "approved" on the Linear issue.
            On approval → merge PR.
```

**If Sharad gives feedback on the preview (PR is still open):**
1. Treat every piece of feedback as a spec amendment, not just a code fix
2. Run `npx openspec propose "adjustment: [what Sharad said]"`
3. Update `openspec/project.md` with the change
4. Then update the code
5. Push to the **same branch** — the PR and Vercel preview update automatically
6. Post on the Linear issue: "Updated. New preview: [same Vercel URL]"
7. Wait for Sharad's next "approved" or further feedback

**After merge:**
1. Run `npx openspec archive`
2. Post to Slack: "🚀 [feature] is live. [Vercel prod URL]"
3. Move Linear issue to `Done`

**Never:**
- Merge with failing CI
- Ask Sharad for code feedback — only visual review via preview URL
- Leave a PR open 24h+ without a Slack update
- Change code without updating the spec first — even for a one-line visual fix

---

### Role 3: Idea-Generation Agent
**Who:** Cursor Automations (weekly cron), Claude

**Triggered by:** Monday 9am cron, or on-demand

**What it does:**
1. Reads `openspec/project.md` — vision and what's planned
2. Reads the current codebase — what's actually built
3. Finds meaningful gaps
4. Creates Linear issues with:
   - Status: `Backlog`
   - Label: `spec-needed`
   - Title: `[Feature] <name>` or `[Bug] <what's broken>`
   - Description: 2-3 sentences on the gap and why it matters
   - Priority: suggested (Sharad overrides)

**Rules:**
- Never create issues with status beyond `Backlog`
- Search Linear first — no duplicates
- Max 5 issues per run
- No implementation detail — that happens in spec mode

---

## Cursor Background Rules (Required Setup)

**These must be added to Cursor Settings → Rules → Background Rules.**
Without this, Cursor ignores the two-phase behavior and starts coding immediately.

```
TWO-PHASE BEHAVIOR — read before every task:

PHASE 1 — SPEC MODE (issue status = Backlog):
- DO NOT write any code
- DO NOT create any branch
- Read the issue and openspec/project.md
- Run: npx openspec propose "<issue title>"
- Post a spec draft as a comment on the Linear issue
- Iterate in comments until Sharad is satisfied
- Wait for Sharad to move status to Todo

PHASE 2 — BUILD MODE (issue status = Todo):
- Spec is approved. Build it now.
- Run: npx openspec apply
- Open a GitHub PR with Vercel preview URL in the description
- Move Linear issue to In Review

ALWAYS:
- Never move an issue to Todo — only Sharad does that
- Never merge your own PR
- Never push directly to main
- Communicate only via Linear comments and Slack
- When Sharad gives feedback on a preview, update the spec BEFORE the code
- All feedback from Sharad goes on the Linear issue — not the PR — even if he sends it via Slack

HOW TO START BUILDING (after spec is approved):
Sharad will move the issue to Todo AND post a comment like "spec approved, start building".
That comment is your trigger. Read all prior comments on the issue — they are your build context.
```

---

## Rules That Always Apply

1. **Status Todo is Sharad's exclusive build trigger.** Agents never set this.
2. **Backlog = spec conversation only.** No code, no branches.
3. **Vercel preview URL in every PR.** This is what Sharad reviews.
4. **Linear comments and Slack only.** No files, no code editors.
5. **CI must be green before merge.** No override.
6. **Never push to main directly.** Always branch + PR.

---

## Project Index

| Project | Repo | Linear Project | Slack Channel | Vercel |
|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | #resume-website | meet-sharad.vercel.app |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | #pm-ops | — |

*Add each new project via `/init-project` skill.*

---

## Idea Feeder Sources (setup order)

| Feeder | What it does | Phase |
|---|---|---|
| Spec-drift agent | Compares openspec/project.md vs actual code, files gaps | 2 |
| Bug/error agent | Reads Vercel runtime errors, files prod issues | 2 |
| Capture agent | Slack one-liner → clean Backlog issue | 3 |
| Market/feature agent | Reads vision + research, proposes unseen features | 4 |

---

## What Sharad Reviews vs What the Agent Decides

| Sharad | Agent |
|---|---|
| Issue priority in Linear | Implementation approach |
| Spec direction (via Linear comments) | File structure, naming, tooling |
| Moving issue to Todo (the build trigger) | Which tasks to parallelize |
| Visual preview on Vercel (does it look right?) | Code style, linting |
| "approved" comment on Linear issue | Test coverage approach |

Sharad reviews product outcomes. If the preview looks right and CI is green, approve it.
