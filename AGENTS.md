# PM OS — Agent Operating Instructions

This file is the single source of truth for how AI agents operate across all of Sharad's projects.
Every agent (Cursor, Claude, Codex, or otherwise) reads this before starting work.

---

## The Loop

```
SPEC PHASE (issue in Backlog — no agent assignment yet)
  Sharad @mentions an agent in a Linear comment: "@cursor what do you think about..."
  Agent replies in comments, refines the spec
  Back-and-forth until Sharad is satisfied
  Agent updates the issue DESCRIPTION with the final agreed spec
  No code. No branches. No assignment.

BUILD TRIGGER
  Sharad moves issue to Todo
  Sharad assigns to Cursor (or Claude/Codex)
  Sharad comments: "spec approved, start building"
  ← this comment is the actual trigger

BUILD PHASE
  Agent reads full issue: description + all comments = build context
  Agent runs OpenSpec, implements, opens PR
  Agent waits for Vercel to post preview URL to PR (60s)
  Agent self-labels issue: auto-merge or review-required
  Agent posts to Slack with result

REVIEW (if review-required)
  Slack: "Ready for review: [feature]. Preview: [Vercel branch URL]. Approve: [Linear link]"
  Sharad taps URL on phone — reviews visually
  Feedback → comments on Linear issue (not the PR)
  Agent updates spec first, then code, pushes to same branch
  Vercel preview auto-refreshes on same URL
  Repeat until Sharad comments "approved"
  Agent merges

AUTO-MERGE (if auto-merge)
  Agent merges immediately after CI green
  Slack: "✅ [feature] auto-merged. Live: [prod URL]"

AFTER MERGE
  Agent runs openspec archive
  Agent moves Linear issue to Done
```

---

## The Spec Layer: OpenSpec

Every repo uses OpenSpec to keep a living spec in sync with what's actually built.

**Setup (agent does this once per repo, on first task):**
```bash
npm install --save-dev @fission-ai/openspec@latest
npx openspec init   # select cursor as assistant
```

This creates `openspec/project.md` — the project's constitution.

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
```

**Three commands — all run by the agent, never Sharad:**
- `npx openspec propose "<title>"` — generates proposal artifacts before coding
- `npx openspec apply` — implements the approved spec
- `npx openspec archive` — folds delta back into openspec/project.md after merge

---

## Roles

### Role 1: Builder Agent
**Who:** Cursor (primary), Claude, Codex
**Triggered by:** Assigned to issue with status Todo + "spec approved" comment from Sharad

**On trigger:**
1. Read the full Linear issue: description is the spec, comments are context
2. Ensure OpenSpec is installed: `npm install --save-dev @fission-ai/openspec@latest`
3. Run `npx openspec propose "<issue title>"`
4. Run `npx openspec apply` — implement
5. Open a PR using `.github/pull_request_template.md`
6. Wait up to 90 seconds for Vercel to post the preview URL to the PR
7. Extract the Vercel preview URL from the PR checks
8. Self-label the Linear issue based on what was built:
   - `review-required` if: new visible component, new page, significant UI change, new user flow
   - `auto-merge` if: copy edit, config, meta tags, bug fix under 50 lines, styling tweak
9. Post to Linear issue and Slack (see templates below)
10. Move Linear issue to `In Review`

**Slack post (review-required):**
```
🔍 Ready for your review
Feature: [issue title]
Preview: [Vercel branch URL] ← tap this
What changed: [2 sentences]
CI: ✅ green
Approve: reply "approved" on [Linear issue URL]
```

**Slack post (auto-merge):**
```
⚡ Auto-merged: [issue title]
Live: [Vercel prod URL]
```

**Never:**
- Write any code while issue is in Backlog — spec phase only, via @mentions in comments
- Move an issue to Todo — only Sharad does that
- Merge your own PR
- Push directly to main
- Change code without updating the spec first

---

### Role 2: Reviewer Agent
**Who:** Cursor, Claude
**Triggered by:** PR opened on GitHub

**Step 1 — Check CI:**
- CI failing → comment on PR with what failed, notify Slack, do not merge

**Step 2 — Check label on Linear issue:**

If `auto-merge`:
- CI must be green
- Merge immediately
- Post to Slack: "⚡ Auto-merged: [title]. Live: [prod URL]"
- Run `npx openspec archive`
- Move issue to Done

If `review-required`:
- Get Vercel preview URL from PR checks
- Post to #[project-slack-channel] using the review template above
- Wait for Sharad to comment "approved" on the Linear issue
- On approval → merge → archive → Done → Slack "🚀 live"

**If Sharad gives feedback on the preview (PR still open):**
1. Every piece of feedback = spec amendment first
2. Run `npx openspec propose "adjustment: [what Sharad said]"`
3. Update `openspec/project.md`
4. Update code
5. Push to same branch (PR and Vercel preview auto-refresh)
6. Comment on Linear issue: "Updated — preview refreshed at same URL"
7. Wait for next "approved" or more feedback

**Never:**
- Merge with failing CI
- Show Sharad code — only preview URLs
- Leave a PR open 24h+ without a Slack update
- Change code without updating spec first

---

### Role 3: Spec Conversation Agent
**Who:** Cursor, Claude — @mentioned in Linear comments during Backlog phase

**This role has no assignment. It is triggered by @mentions in Linear comments.**

When @mentioned on a Backlog issue:
1. Read the issue title, description, and all prior comments
2. Read `openspec/project.md` from the repo for project context
3. Reply in the Linear comment thread:
   - What you understand the feature to be
   - Questions or concerns about the approach
   - Alternative approaches if relevant
4. When the conversation reaches agreement, **update the issue description** with the final spec
5. The updated description is what the builder agent will read when assigned

Do not write code. Do not create branches. Do not run openspec commands.

---

### Role 4: Idea-Generation Agent
**Who:** Cursor Automations (weekly cron), Claude
**Triggered by:** Monday 9am cron, or on-demand

**What it does:**
1. Reads `openspec/project.md` — vision and constraints
2. Reads current codebase — what's actually built
3. Finds meaningful gaps (missing features, broken things, spec drift)
4. Creates Linear issues:
   - Status: `Backlog`
   - Label: `spec-needed`
   - Title: `[Feature] <name>` or `[Bug] <what's broken>`
   - Description: 2-3 sentences — what the gap is and why it matters
   - Priority: suggested (Sharad overrides)

**Rules:**
- Never create issues past Backlog
- Search Linear first — no duplicates
- Max 5 issues per run
- No implementation detail in the issue — that belongs in the spec conversation

---

## Cursor Background Rules (paste into Cursor Settings → Rules)

```
SPEC PHASE — when I am @mentioned on a Backlog issue (not assigned):
- Do NOT write code
- Do NOT create branches
- Read the issue and openspec/project.md
- Reply in the Linear comment with my understanding, questions, suggestions
- Update the issue description with the agreed spec when conversation concludes

BUILD PHASE — when I am assigned to an issue with status Todo:
- Read the full issue: description = spec, comments = context
- Install OpenSpec if needed: npm install --save-dev @fission-ai/openspec@latest
- Run: npx openspec propose "<title>" then npx openspec apply
- Open a GitHub PR with Vercel preview URL in the description
- Wait for Vercel preview URL (up to 90s) from PR checks
- Self-label the Linear issue: review-required or auto-merge
- Post to Slack with preview URL if review-required
- Move issue to In Review

FEEDBACK DURING REVIEW — when Sharad comments on the Linear issue while PR is open:
- Update spec first (npx openspec propose "adjustment: ...")
- Then update code
- Push to same branch — preview auto-refreshes

ALWAYS:
- Never move an issue to Todo — only Sharad does that
- Never merge my own PR
- Never push directly to main
- All communication via Linear comments and Slack
- Spec update before code change — always
```

---

## Rules That Always Apply

1. **Backlog = spec conversation only.** @mentions, no assignment, no code.
2. **Todo + "spec approved" comment = build trigger.**
3. **Vercel preview URL is the only review surface.** Sharad never sees code.
4. **All Sharad feedback goes on the Linear issue** — not the PR, even if he sends it via Slack.
5. **Spec update before code change** — always, even for a one-line fix.
6. **CI must be green before any merge.**
7. **Never push to main directly.**

---

## Project Index

| Project | Repo | Linear Project | Slack Channel | Vercel Prod |
|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | #resume-website | meet-sharad.vercel.app |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | #pm-ops | — |

*Add new projects via `/init-project` skill.*

---

## Idea Feeder Sources (setup order)

| Feeder | What it does | Phase |
|---|---|---|
| Spec-drift agent | Compares openspec/project.md vs code, files gaps | 2 |
| Bug/error agent | Reads Vercel runtime errors, files prod issues | 2 |
| Capture agent | Slack one-liner → clean Backlog issue | 3 |
| Market/feature agent | Reads vision + research, proposes new features | 4 |

---

## What Sharad Does vs What Agents Do

| Sharad | Agents |
|---|---|
| @mentions agents in Backlog comments to refine spec | Draft spec, ask questions, update issue description |
| Moves issue to Todo (the only build trigger) | Build, PR, self-label, post preview |
| Views Vercel preview URL on phone | Decide auto-merge vs review-required |
| Comments feedback on Linear issue | Update spec then code, refresh preview |
| Comments "approved" | Merge, archive spec, notify Slack |
| Overrides issue priority | Everything else |
