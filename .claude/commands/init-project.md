Initialize a new project into the AI-first PM loop. Run this once per new repo.

## Usage
/init-project

## What this does
1. Asks you for the project details
2. Creates AGENTS.md and .github/pull_request_template.md in the target GitHub repo
3. Creates a Linear project for it
4. Adds the project to the Project Index in AI-Workspace/AGENTS.md

## Steps

Ask the user for the following (one message, numbered list):
1. GitHub repo name (format: owner/repo, e.g. rohrasharad-ship-it/my-app)
2. Project display name (e.g. "My App")
3. One-sentence description of what the product does and who it's for
4. Tech stack (framework, styling, backend/DB if any)
5. Key non-negotiables (architecture rules the agent must never break)
6. What's out of scope (what this product will never do)
7. Slack channel name for this project (e.g. #my-app)
8. Vercel URL if known (or "TBD")

Once you have the answers, do all of the following:

### Step A — Create AGENTS.md in the target repo
Use the GitHub MCP tool to create `.github` doesn't need to be created separately — create this file at path `AGENTS.md` in the repo:

```
# Agent Instructions — $PROJECT_NAME

## Before writing any code on any issue
1. Install OpenSpec if not already in package.json: `npm install --save-dev @fission-ai/openspec@latest`
2. Run `npx openspec propose "<issue title>"` — this generates proposal.md, design.md, tasks.md
3. Read those files, then post a comment on the Linear issue in this format:

Planning to build: [one sentence]

Tech approach: [key choices]

Tasks:
- [ ] task 1
- [ ] task 2
- [ ] task 3

Assumptions: [anything Sharad might want to correct]

Reply with ✅ to start building, or correct anything above.

4. Wait for Sharad's reply before writing any code.

## After Sharad confirms
1. Run `npx openspec apply`
2. Implement all tasks
3. Open a PR — use `.github/pull_request_template.md` for the description
4. The PR description must include the Vercel preview URL
5. Set the Linear issue status to In Review

## After PR is merged
1. Run `npx openspec archive`
2. Post in $SLACK_CHANNEL Slack: "[feature name] is live. [Vercel prod URL]"
3. Set the Linear issue to Done

## Rules
- Never push directly to main
- Never merge your own PR
- Always ask via Linear comment if something is unclear — never guess
```

### Step B — Create PR template in the target repo
Create `.github/pull_request_template.md`:

```
## What This Does
<!-- Plain English — what changed, not how -->

## Preview
<!-- Vercel preview URL — paste it here -->

## How to Verify
1. 
2. 
3. 

## Linear Issue
<!-- Link to the Linear issue that drove this -->
```

### Step C — Create Linear project
Use the Linear MCP tool to create a new project with:
- Name: $PROJECT_NAME
- Team: Sharad Rohra
- Description: $ONE_SENTENCE_DESCRIPTION. Slack: $SLACK_CHANNEL. Repo: $REPO.
- Priority: Medium

### Step D — Update AI-Workspace/AGENTS.md Project Index
Read the current AGENTS.md from the AI-Workspace repo and add a new row to the Project Index table:
| $PROJECT_NAME | $REPO | $PROJECT_NAME | $SLACK_CHANNEL | $VERCEL_URL |

### Step E — Confirm to the user
Reply with:
- Links to the two files created in GitHub
- Link to the new Linear project
- "Next: add your first 3–5 issues to the Linear project in Backlog, then assign the first one to Cursor."
