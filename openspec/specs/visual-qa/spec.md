## Purpose

Two complementary visual verification systems: spec previews (proposed ideas) and self-QA screenshots (live deployed results).

## Requirements

### Requirement: Visual specs for proposed UI ideas
Any agent proposing a feature with a meaningful visual or motion component MUST attach a standalone HTML preview — not just text. Non-visual changes (logic, config, copy-only) MUST skip this.

#### Scenario: Market-feature proposes UI idea
- **WHEN** market-feature files a new visual feature
- **THEN** it creates `previews/<issue-id>-v<n>.html`, pushes to `preview/<issue-id>-v<n>` branch (no PR), and links `<deployment-url>/previews/<issue-id>-v<n>.html`

#### Scenario: Full-effort vs minimal-effort tier
- **WHEN** spec-conversation discusses a visual feature (full tier) vs idea-generation auto-files one (minimal tier)
- **THEN** full tier builds real interaction; minimal tier shows a static frame or annotated mockup

### Requirement: Preview branch lifecycle
Only one `preview/<issue-id>-*` branch MUST exist per issue at a time. Previous iterations MUST be deleted before pushing a new one. Preview branches MUST be deleted when spec is finalized (`agent-ready`) or idea is dropped.

#### Scenario: New preview iteration
- **WHEN** an agent creates `preview/SHA-40-v2`
- **THEN** it deletes `preview/SHA-40-v1` first

#### Scenario: Builder starts on agent-ready
- **WHEN** a builder begins implementation
- **THEN** any remaining `preview/<issue-id>-*` branch for that issue is deleted

### Requirement: Visual self-QA mandatory for builder and idea-generation
Agents MUST capture real Playwright screenshots of live deployed URLs, actually view them, and attach to Linear issues via signed upload — never base64 inline.

#### Scenario: Builder before PR
- **WHEN** a builder finishes implementation on a product repo
- **THEN** it screenshots the changed area on the Vercel preview at desktop and mobile viewports and attaches both to the Linear issue

#### Scenario: AI-Workspace infra change
- **WHEN** a builder changes instruction files only (no UI)
- **THEN** visual self-QA is N/A; Status Snapshot shows Preview: N/A

### Requirement: Spec-preview sandbox hosted on Vercel
AI-Workspace MUST maintain a static Vercel project (`ai-workspace.vercel.app`) that deploys any pushed branch so `previews/*.html` files are reachable at predictable URLs.

#### Scenario: Preview file deployed
- **WHEN** `previews/SHA-44-v1.html` is pushed to a branch
- **THEN** it is accessible at `<branch-deployment-url>/previews/SHA-44-v1.html`

#### Scenario: Bare deployment URL
- **WHEN** someone opens the bare `*.vercel.app` root
- **THEN** they see the placeholder `index.html` ("Spec Preview Sandbox") — not a product app

### Requirement: SSO/login redirect detection
Before claiming a preview is ready or attaching screenshots, agents MUST check that the URL does not redirect to Vercel SSO/login pages.

#### Scenario: Deployment protection enabled
- **WHEN** a preview URL redirects to `vercel.com/sso-api`
- **THEN** the agent reports access-gated status instead of claiming preview is ready
