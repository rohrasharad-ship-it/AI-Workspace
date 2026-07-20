Initialize a new project into the AI-first PM loop. Run this once per new repo.

## Usage
/init-project

## What this does
1. Asks you for the project details
2. Creates AGENTS.md and .github/pull_request_template.md in the target GitHub repo
3. Initializes OpenSpec properly with per-capability spec files — NOT a flat spec doc
   and NOT empty placeholder stubs if the project already has shipped features
4. Creates a Linear project for it
5. Adds the project to the Project Index in AI-Workspace/projects.md

Because the target repo's AGENTS.md is only a thin pointer into
AI-Workspace/AGENTS.md (see "Hub model" there), the project gets every role
(`agents/*.md`) and every routine (`routines/*.md`) for free the moment it's
added to `projects.md` — no extra setup needed to make idea-generation
routines like `idea-sweep` work against it.

## Steps

Ask the user for the following (one message, numbered list):
1. GitHub repo name (format: owner/repo, e.g. rohrasharad-ship-it/my-app)
2. Project display name (e.g. "My App")
3. Tech stack (framework, styling, backend/DB if any) — one line
4. Slack channel name for this project (e.g. #my-app)
5. The product's natural capability breakdown — e.g. "hero, journey, about,
   contact, voice-agent" for a portfolio site, or the equivalent sections for
   whatever this product is. If the user isn't sure yet, 3-5 rough guesses are
   fine — this can be refined later, but it must exist from day one so no
   agent ever has to read one giant flat spec file.

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

### Step C — Initialize OpenSpec with per-capability structure (not a flat file)
In the target repo, create:
```
openspec/project.md
openspec/specs/<capability-1>/spec.md
openspec/specs/<capability-2>/spec.md
... one per capability from the user's answer above
```
`openspec/project.md` uses the template from
AI-Workspace/agents/shared/openspec.md, including the `## Capabilities` index
listing each capability name and its file path. Each `openspec/specs/<capability>/spec.md`
must describe the capability that already exists in the codebase if that
feature is already shipped. Inspect the repo first, then convert the live
product into the baseline spec. If a capability is genuinely new or not yet
implemented, the file can start as a short stub, but do not leave shipped
behavior undocumented.

The point at this stage is the STRUCTURE existing from day one and the
current product faithfully captured in OpenSpec — not placeholder content. A
project that starts with the right shape and the right baseline never needs the
retrofit resume-website needed.

### Step D — Create Linear project
Use the Linear MCP tool to create a new project with:
- Name: $PROJECT_NAME
- Team: Sharad Rohra
- Description: $ONE_SENTENCE_DESCRIPTION. Slack: $SLACK_CHANNEL. Repo: $REPO.
- Priority: Medium
- After creating the project, configure Linear → Slack bell notifications to
  $SLACK_CHANNEL (see `agents/shared/linear-slack.md` — enable "Issue created"
  and run the smoke test).

### Step E — Update AI-Workspace/projects.md
Read the current `projects.md` from the AI-Workspace repo and add a new row to
the Project Index table:
| $PROJECT_NAME | $REPO | $PROJECT_NAME | $SLACK_CHANNEL | $VERCEL_URL |

### Step F — Confirm to the user
Reply with:
- Links to the files created in GitHub (AGENTS.md, PR template, openspec/ structure)
- Link to the new Linear project
- "Next: add your first 3–5 issues to the Linear project in Backlog, then assign the first one to Cursor."
