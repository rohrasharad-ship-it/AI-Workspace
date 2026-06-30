# PM OS — Agent Operating Instructions

This file is the single source of truth for how AI agents operate across all of Sharad's projects.
Every agent (Cursor, Claude, Codex, or otherwise) reads this before starting work.

---

## The Loop

```
[Linear issue created — thin title + one sentence]
    → Sharad triages and prioritizes on mobile
    → Sharad assigns issue to an agent
    → Builder Agent runs /opsx:propose
    → Builder Agent posts proposal summary as a Linear comment
    → Sharad thumbs-up (or corrects) on mobile
    → Builder Agent runs /opsx:apply → opens PR on GitHub
    → Reviewer Agent checks PR automatically
    → Reviewer Agent decides: trivial → merge | needs-approval → post Slack with Vercel preview URL
    → Sharad taps Vercel preview on phone, approves merge via Linear comment
    → Reviewer Agent merges PR
    → Vercel auto-deploys to production
    → /opsx:archive folds the change into the living spec
```

Sharad's only inputs: triage priority, proposal thumbs-up, and visual merge approval. No code editor ever.

---

## Roles

### Role 1: Builder Agent
**Who uses this:** Cursor (primary), Claude, Codex

**Triggered by:** Linear issue assigned to the agent

**Step 1 — Propose, don't build yet:**
1. Read the Linear issue
2. Read `openspec/project.md` in the target repo
3. Run `/opsx:propose "<issue title>"`
4. Read the generated `proposal.md`, `design.md`, `tasks.md`
5. Post a Linear comment on the issue in this format:

```
Planning to build: [one sentence what you understood]

Tech approach: [key choices]

Tasks:
- [ ] task 1
- [ ] task 2
- [ ] task 3

Assumptions: [anything you assumed that could be wrong]

Reply with ✅ to start building, or correct anything above.
```

6. **Wait for Sharad's reply before running `/opsx:apply`.**

**Step 2 — Build (after confirmation):**
1. Run `/opsx:apply`
2. Implement all tasks
3. Open a PR using the repo's `.github/pull_request_template.md`
4. PR description must include: what was built, Vercel preview URL, how to verify in 3 steps
5. Update Linear issue status to `In Review`

**Never:**
- Start coding before the proposal confirmation
- Merge your own PR
- Add dependencies not mentioned in `openspec/project.md` without a new proposal

---

### Role 2: Reviewer Agent
**Who uses this:** Cursor, Claude

**Triggered by:** PR opened on GitHub

**Decision tree:**
```
Is CI green?
  No → Post comment: what failed, what Sharad should know. Do not merge.
  Yes →
    Is this trivial? (copy fix, config tweak, style-only, single-line)
      Yes → Merge immediately. Post to Slack: "[Project] [issue title] merged to main. Vercel deploying."
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
1. Run `/opsx:archive` in the repo
2. Post to Slack: "[Project] [feature] is live on prod. [Vercel prod URL]"
3. Move Linear issue to `Done`

**Do not:**
- Merge anything with failing CI
- Ask for code-level feedback from Sharad — he reviews the preview, not the diff
- Leave a PR open for more than 24 hours without a Slack update

---

### Role 3: Idea-Generation Agent
**Who uses this:** Cursor Automations (weekly cron), Claude

**Triggered by:** Monday 9am cron, or on-demand

**What it does:**
1. Reads `openspec/project.md` — the product vision and what's planned
2. Reads current codebase — what's actually built
3. Reads recent Vercel runtime errors — what's broken
4. Compares gaps
5. Creates Linear issues for each gap with:
   - Status: `Triage`
   - Label: `spec-needed`
   - Title: `[Feature] <descriptive name>` or `[Bug] <what's broken>`
   - Description: 2-3 sentences on what the gap is and why it matters

**Rule:** Never create issues beyond `Triage`. Sharad is the filter. Generate, don't prioritize.

**Do not:**
- Create duplicate issues (search Linear before creating)
- Create more than 5 issues per run (quality over quantity)
- Add implementation details — that happens at proposal time

---

## Rules That Always Apply (All Agents)

1. **Communicate through Linear and Slack, never through files.** Sharad reads comments on mobile, not markdown files.
2. **One proposal before every build.** No exceptions, even for tiny features.
3. **CI must be green before merge.** No override.
4. **Every PR follows `.github/pull_request_template.md`.** No freeform descriptions.
5. **When genuinely unsure, ask via Linear comment.** Don't guess and build 200 lines of wrong code.
6. **Never push directly to `main`.** Always a branch + PR.

---

## Project Index

| Project | Repo | Linear Project | Slack Channel | Vercel URL |
|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | #resume-website | sharad.pm |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | #pm-ops | — |

*Add each new project here when it's onboarded.*

---

## Idea Feeder Sources (in order of setup priority)

| Feeder | What it does | When to add |
|---|---|---|
| Spec-drift agent | Compares project.md vs actual code, files missing features | Phase 2 |
| Bug/error agent | Reads Vercel runtime errors, files issues for prod problems | Phase 2 |
| Capture agent | Voice note / Slack one-liner → clean Triage issue | Phase 3 |
| Reviewer spillover | PR reviewer notices a gap → new Triage issue, PR still merges | Phase 3 |
| Market/feature agent | Reads vision + does research, proposes features you haven't thought of | Phase 4 |

**Phase 1 goal: get the basic loop working on resume-website without any of these feeders. Sharad manually creates the first 5 issues.**

---

## OpenSpec Quick Reference

```bash
openspec init              # run once per project, select cursor as assistant
/opsx:propose "<name>"     # builder runs this first, before any code
/opsx:apply                # builder runs this after Sharad confirms
/opsx:archive              # reviewer runs this after merge
```

The `openspec/project.md` file is the project's constitution. Write it manually after init. Every proposal inherits its context. An agent without a good `project.md` will drift.

---

## What Sharad Reviews vs What the Agent Decides

| Sharad reviews | Agent decides |
|---|---|
| Proposal plan (thumbs-up or correction) | Implementation approach |
| Visual preview on Vercel (does it look right?) | File structure, naming |
| Issue priority in Linear | Which tasks to parallelize |
| Merge approval | Code style, test coverage |
| Whether a feature enters a cycle | Linting, formatting |

Sharad is a product judge. If the preview looks right and CI is green, that is sufficient to merge.
