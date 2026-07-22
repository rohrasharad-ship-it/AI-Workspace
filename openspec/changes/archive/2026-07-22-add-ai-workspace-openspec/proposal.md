## Why

AI-Workspace mandates OpenSpec for every project but had none of its own. Idea-generation sweeps (especially spec-drift) had nothing to check gaps against when scanning this repo.

## What Changes

- Initialize OpenSpec (`@fission-ai/openspec`, `openspec/config.yaml`, Cursor skills/commands)
- Add `openspec/project.md` — PM OS vision, non-negotiables, capability index
- Add nine per-capability baseline specs under `openspec/specs/` documenting existing shipped process
- Add `package.json` with `npm run build` that validates all specs
- Add `.gitignore` for `node_modules/`

## Capabilities

### New Capabilities

- `agent-dispatch`: AGENTS.md router, hub model, role dispatch table
- `build-loop`: Builder/reviewer roles, trigger vs gate, PR → approval flow
- `spec-conversation`: Spec-phase discussion on `spec-needed` issues
- `idea-generation`: Spec-drift, bug-error, market-feature roles
- `routines`: Named routine bundles and orchestration model
- `shared-conventions`: Issue Brief, issue cap, status snapshot, always-apply rules
- `integrations`: Project registry and Linear → Slack notifications
- `visual-qa`: Visual specs, visual self-QA, preview sandbox
- `design-reference`: UI animation catalog and copy-paste workflow

### Modified Capabilities

(none — greenfield bootstrap)

## Impact

- New files: `openspec/`, `package.json`, `package-lock.json`, `.gitignore`, `.cursor/` (OpenSpec init)
- No changes to existing agent instruction behavior — specs document what already exists
- Spec-drift can now compare this repo's instructions against its own OpenSpec baseline
