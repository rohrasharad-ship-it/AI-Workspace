## Why

New projects onboarded via `/init-project` get a `projects.md` row missing the Linear Project ID column, so issue-cap counting silently returns zero and idea-generation can flood an already-loaded backlog. SHA-136 fixed this for existing projects; every future onboarded project hits the same failure mode until init-project captures the ID at creation time.

## What Changes

- Update `/init-project` Step D to capture the Linear project UUID from the `save_project` MCP response (or `list_projects` fallback).
- Update `/init-project` Step E `projects.md` row template to include all six columns, with the Linear Project ID as the fourth column.
- Align the integrations spec scenario with the corrected onboarding flow.

## Capabilities

### New Capabilities

_None — this refines existing onboarding behavior._

### Modified Capabilities

- `integrations`: Clarify that `/init-project` MUST write the Linear Project ID from project creation into `projects.md`, not rely on manual follow-up.

## Impact

- `.claude/commands/init-project.md` — primary fix
- `openspec/specs/integrations/spec.md` — delta spec (already states the requirement; tighten onboarding scenario wording if needed)
