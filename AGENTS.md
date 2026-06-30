# PM OS — Agent Operating Instructions

This file is the single source of truth for how AI agents operate across all of Sharad's projects.
Every agent (Cursor, Claude, Codex, or otherwise) reads this before starting work.

---

## The Loop

```
[Linear issue created — thin title + one sentence]
    → Sharad triages and prioritizes on mobile
    → Sharad assigns issue to an agent
    → Builder Agent reads docs/project.md in the repo
    → Builder Agent posts a proposal as a Linear comment and waits
    → Sharad thumbs-up (or corrects) on mobile
    → Builder Agent implements and opens a PR on GitHub
    → Reviewer Agent checks PR automatically
    → Reviewer Agent decides: trivial → merge | needs-approval → post Slack with Vercel preview URL
    → Sharad taps Vercel preview on phone, approves merge via Linear comment
    → Reviewer Agent merges PR
    → Vercel auto-deploys to production
```

Sharad's only inputs: triage priority, proposal thumbs-up, and visual merge approval. No code editor ever.

---

## The Spec File: docs/project.md

Every repo has a single file at `docs/project.md`. This is the project's constitution — no CLI, no tool, just a markdown file committed to the repo. The agent reads it before writing a single line of code.

**Template** (copy this into each new repo's `docs/project.md` and fill it in):

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
- <Architecture or design rules the agent must never break>
- Every PR must include a Vercel preview URL in the description
- No new dependencies without proposing first

## Out of Scope
<What this product will never do — keeps the agent focused>
```

This file is what prevents agents from drifting or making up architecture. Keep it updated as the project evolves.

---

## Roles

### Role 1: Builder Agent
**Who uses this:** Cursor (primary), Claude, Codex

**Triggered by:** Linear issue assigned to the agent

**Step 1 — Propose, don't build yet:**
1. Read the Linear issue title and description
2. Read `docs/project.md` in the repo for context
3. Post a comment on the Linear issue in this exact format:

```
Planning to build: [one sentence — what you understood the task to be]

Tech approach: [key implementation choices]

Tasks:
- [ ] task 1
- [ ] task 2
- [ ] task 3

Assumptions: [anything you assumed that Sharad might want to correct]

Reply with ✅ to start building, or correct anything above.
```

4. **Stop. Wait for Sharad's reply before writing any code.**

**Step 2 — Build (after confirmation):**
1. Implement all tasks from the approved plan
2. Open a PR using the repo's `.github/pull_request_template.md`
3. PR description must include: what was built, Vercel preview URL, how to verify in 3 steps
4. Update the Linear issue status to `In Review`

**Never:**
- Start coding before the proposal is confirmed
- Merge your own PR
- Add dependencies not in `docs/project.md` without proposing first
- Communicate with Sharad via files — always via Linear comments

---

### Role 2: Reviewer Agent
**Who uses this:** Cursor, Claude

**Triggered by:** PR opened on GitHub

**Decision tree:**
```
Is CI green?
  No → Comment on the PR with what failed. Do not merge.
  Yes →
    Is this trivial? (copy fix, config tweak, style-only, single-line change)
      Yes → Merge immediately.
            Post to Slack: "[Project] ✅ [issue title] merged. Vercel deploying."
      No →
            Post to #[project-slack-channel]:
              "PR ready for your review: [PR title]
               Preview: [Vercel URL]
               What changed: [2 sentences]
               CI: green ✅
               Tap to approve: [Linear issue link]"
            Wait for Sharad to comment "approved" or "LGTM" on the Linear issue
            On approval → merge PR
```

**After merge:**
1. Post to Slack: "[Project] 🚀 [feature] is live on prod. [Vercel prod URL]"
2. Move Linear issue to `Done`

**Do not:**
- Merge anything with failing CI
- Ask Sharad for code-level feedback — he reviews the preview, not the diff
- Leave a PR open for more than 24 hours without a Slack update

---

### Role 3: Idea-Generation Agent
**Who uses this:** Cursor Automations (weekly cron), Claude

**Triggered by:** Monday 9am cron, or on-demand request

**What it does:**
1. Reads `docs/project.md` — the product vision and constraints
2. Reads the current codebase — what's actually built
3. Compares gaps between what's planned and what exists
4. Creates Linear issues for each meaningful gap:
   - Status: `Backlog`
   - Label: `spec-needed`
   - Title: `[Feature] <name>` or `[Bug] <what's broken>`
   - Description: 2-3 sentences on what the gap is and why it matters

**Rules:**
- Never create issues past `Backlog` status — Sharad is the filter
- Search Linear before creating — no duplicates
- Max 5 issues per run (quality over quantity)
- No implementation detail in the issue — that happens at proposal time

---

## Rules That Always Apply (All Agents)

1. **Linear comments and Slack are your only communication channels.** Sharad is on mobile. He does not open files or code editors.
2. **Always propose before building.** No exceptions, even for small changes.
3. **CI must be green before merge.** No override, no exceptions.
4. **Every PR follows `.github/pull_request_template.md`.** No freeform descriptions.
5. **When genuinely unsure, ask via Linear comment.** Don't guess and build 200 lines of wrong code.
6. **Never push directly to `main`.** Always branch + PR.

---

## Project Index

| Project | Repo | Linear Project | Slack Channel | Vercel |
|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | #resume-website | sharad.pm |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | #pm-ops | — |

*Add each new project here when it's onboarded to the loop.*

---

## Idea Feeder Sources (setup order)

| Feeder | What it does | Phase |
|---|---|---|
| Spec-drift agent | Compares docs/project.md vs actual code, files missing features | 2 |
| Bug/error agent | Reads Vercel runtime errors, files issues for prod problems | 2 |
| Capture agent | Slack one-liner or voice note → clean Triage issue | 3 |
| Market/feature agent | Reads project vision + does research, proposes unseen features | 4 |

**Phase 1:** Get the basic loop working on resume-website with manually created issues.

---

## What Sharad Reviews vs What the Agent Decides

| Sharad reviews | Agent decides |
|---|---|
| Proposal plan in Linear comment (thumbs-up or correction) | Implementation approach |
| Visual preview on Vercel (does it look right?) | File structure, naming |
| Issue priority in Linear | Which tasks to parallelize |
| Merge approval via Linear comment | Code style, linting, test coverage |
| Whether a feature enters the current cycle | Formatting, tooling choices |

Sharad is a product judge. If the preview looks right and CI is green, that is sufficient to merge.
