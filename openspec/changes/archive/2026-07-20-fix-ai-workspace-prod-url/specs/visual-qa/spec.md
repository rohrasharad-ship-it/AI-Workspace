## MODIFIED Requirements

### Requirement: Spec-preview sandbox hosted on Vercel
AI-Workspace MUST maintain a static Vercel project (`ai-workspace-blond.vercel.app`) that deploys any pushed branch so `previews/*.html` files are reachable at predictable URLs.

#### Scenario: Preview file deployed
- **WHEN** `previews/SHA-44-v1.html` is pushed to a branch
- **THEN** it is accessible at `<branch-deployment-url>/previews/SHA-44-v1.html`

#### Scenario: Bare deployment URL
- **WHEN** someone opens the bare `*.vercel.app` root
- **THEN** they see the placeholder `index.html` ("Spec Preview Sandbox") — not a product app
