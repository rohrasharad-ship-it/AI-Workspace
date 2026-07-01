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
3. Tech stack (framework, styling, backend/DB if any) — one line
4. Slack channel name for this project (e.g. #my-app)

Once you have the answers, do all of the following:

### Step A — Create AGENTS.md in the target repo (thin pointer, not a full copy)
The full process lives once in rohrasharad-ship-it/AI-Workspace/AGENTS.md. Do not
copy the full ruleset into every project — that creates drift the moment the
process evolves. Create this file at path `AGENTS.md` in the target repo:

```
# Agent Instructions — $PROJECT_NAME

STEP 0 — before doing anything else: fetch and follow the full process from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (main branch). Treat it as mandatory,
not optional context. This file only adds project-specific facts.

## Project Facts
- Repo: $REPO
- Linear project: $PROJECT_NAME
- Slack channel: $SLACK_CHANNEL
- Tech stack: $TECH_STACK
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
