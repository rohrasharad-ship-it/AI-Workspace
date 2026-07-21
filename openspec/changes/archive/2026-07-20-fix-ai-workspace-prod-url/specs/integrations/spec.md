## MODIFIED Requirements

### Requirement: PM OS project registered
AI-Workspace (PM OS) MUST be registered in `projects.md` with Linear project "PM OS", Slack `#pm-ops`, and Vercel sandbox URL `ai-workspace-blond.vercel.app`.

#### Scenario: Idea-sweep on PM OS
- **WHEN** idea-sweep runs against PM OS
- **THEN** spec-drift can read this repo's `openspec/` and compare against the instruction files in the codebase
