## Why

`projects.md` lists `ai-workspace.vercel.app` as the PM OS production sandbox URL, but that domain serves an unrelated React app. The real Vercel project domain is `ai-workspace-blond.vercel.app`, which serves the correct "PM OS — Spec Preview Sandbox" placeholder. Wrong links send routines and humans to the wrong site.

## What Changes

- Update `projects.md` Vercel Prod column for AI Workspace (PM OS) to `ai-workspace-blond.vercel.app`
- Update `openspec/project.md` hosting line to match
- Update integrations and visual-qa spec requirements that reference the stale domain
- Clarify `agents/shared/status-snapshot.md` that `ai-workspace.vercel.app` is a wrong/stale domain, not the sandbox

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `integrations`: PM OS project registration URL
- `visual-qa`: Spec-preview sandbox hosted on Vercel domain

## Impact

- `projects.md` — registry row for AI Workspace
- `openspec/project.md` — tech stack hosting line
- `openspec/specs/integrations/spec.md` — PM OS registration requirement
- `openspec/specs/visual-qa/spec.md` — sandbox domain requirement
- `agents/shared/status-snapshot.md` — production-domain guidance
