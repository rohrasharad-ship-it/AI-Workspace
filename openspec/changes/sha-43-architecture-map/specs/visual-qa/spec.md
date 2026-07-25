## MODIFIED Requirements

### Requirement: Spec-preview sandbox hosted on Vercel
AI-Workspace MUST maintain a static Vercel project (`ai-workspace-blond.vercel.app`) that deploys any pushed branch so `previews/*.html` files are reachable at predictable URLs.

#### Scenario: Preview file deployed
- **WHEN** `previews/SHA-44-v1.html` is pushed to a branch
- **THEN** it is accessible at `<branch-deployment-url>/previews/SHA-44-v1.html`

#### Scenario: Bare deployment URL
- **WHEN** someone opens the bare `*.vercel.app` root
- **THEN** they see the PM OS architecture map (`index.html`) showing roles, shared modules, and routines — not a product app

#### Scenario: Architecture map interactivity
- **WHEN** a user clicks a role, shared module, or routine node on the homepage map
- **THEN** connected nodes and edges highlight and a detail panel shows the node's trigger or file path
