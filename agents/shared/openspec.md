# Shared Module: The Spec Layer (OpenSpec)

Referenced by: `agents/builder.md`, `agents/reviewer.md`, `agents/spec-conversation.md`,
`agents/spec-drift.md`, `agents/market-feature.md`

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

When bootstrapping a new project, do **not** start from empty placeholder
stubs if the app already has shipped features. First inspect the codebase,
identify what is already built, and write those existing capabilities into the
baseline OpenSpec files. New issues are for gaps beyond that baseline, not for
re-describing working behavior.

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

## Who reads how much (this is the rule that actually prevents waste)

| Agent | What it reads | Why |
|---|---|---|
| **Idea-Generation (spec-drift, market-feature)** | `project.md` + **all** capability spec files | Its job is finding gaps across the whole product — full breadth is correct here, not a mistake |
| **Builder / Spec Conversation on a single issue** | `project.md` + **only the one relevant capability's** `spec.md` | It's working one feature — reading unrelated capabilities wastes tokens and adds irrelevant context that can cause drift |

If a builder or spec-conversation agent finds itself reading the entire
`openspec/specs/` tree for a single-capability task, something is wrong —
either the capability split doesn't exist yet (fix it, see above) or the task
genuinely spans multiple capabilities (rare — flag it to Sharad rather than
silently reading everything).
