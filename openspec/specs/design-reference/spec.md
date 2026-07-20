## Purpose

A catalog of external UI animation sources and local snippets agents copy-paste instead of writing animations from scratch.

## Requirements

### Requirement: Design folder is the UI starting point
Agents building or speccing visual/motion features MUST read `design/README.md` first and use cataloged sources rather than inventing animations from scratch.

#### Scenario: Builder implements animated hero
- **WHEN** an issue requires scroll-linked text reveal
- **THEN** the builder checks `design/resources.md` for React Bits, Aceternity UI, or local snippets before writing custom animation code

#### Scenario: Backend-only change
- **WHEN** an issue touches only config or API logic
- **THEN** the design reference capability is not required reading

### Requirement: Resource catalog maintained
`design/resources.md` MUST catalog external copy-paste sources (React Bits, Aceternity UI, Anime.js, UI Verse, Animista, etc.) with guidance on when to use each.

#### Scenario: Agent needs hover effect
- **WHEN** a spec requires a spotlight hover interaction
- **THEN** `design/resources.md` points to the appropriate source and `design/snippets/spotlight-hover.html` provides a local reference

### Requirement: Local snippets as plain HTML references
`design/snippets/` MUST contain standalone HTML/CSS/JS reference implementations agents can adapt without a build step.

#### Scenario: Snippet referenced in spec preview
- **WHEN** SHA-44 compared Anime.js vs React Bits patterns
- **THEN** `previews/SHA-44-v1.html` demonstrates both approaches side by side

### Requirement: Copy-paste workflow documented
`design/workflow.md` MUST document the step-by-step process: find source → copy component → adapt to project stack → add only required peer deps.

#### Scenario: React/Next.js project
- **WHEN** adapting a React Bits component
- **THEN** the agent follows shadcn/ui as foundation, copies specific component source, and installs only needed peer deps (usually `motion`)

### Requirement: Default stack hierarchy
For React/Next.js projects, the default priority MUST be: shadcn/ui (foundation) → React Bits or Aceternity UI (effects) → Motion (custom React) → Anime.js (vanilla/SVG only).

#### Scenario: Standard form component needed
- **WHEN** a feature needs a dialog or dropdown
- **THEN** shadcn/ui is the first choice, not a custom build or pre-installing every animation library
