## Context

AI-Workspace is a documentation-only meta-repo with no application runtime. It mandates OpenSpec for all product repos via `agents/shared/openspec.md` and `/init-project`, but had no `openspec/` folder of its own. Spec-drift sweeps against PM OS could not compare planned vs built.

## Goals / Non-Goals

**Goals:**
- Bootstrap full OpenSpec structure matching the mandated pattern (`project.md` + per-capability `specs/`)
- Document all nine existing capabilities from the shipped instruction files
- Enable `npm run build` to validate spec structure
- Unblock idea-generation sweeps on this repo

**Non-Goals:**
- Changing any agent instruction behavior
- Adding application code or test suites
- Modifying product repos

## Decisions

1. **Nine capability boundaries** — split along natural module boundaries already present in the repo (`agents/`, `routines/`, `design/`, shared modules) rather than one spec per role file. Keeps spec-drift scans manageable while matching how agents already read selectively.

2. **Baseline specs written directly** — since this is greenfield bootstrap with no prior specs to delta against, requirements are written directly into `openspec/specs/<capability>/spec.md` documenting existing behavior.

3. **OpenSpec CLI init with Cursor** — `npx openspec init --tools cursor` for standard tooling; build script runs `openspec validate --specs`.

## Risks / Trade-offs

- **[Risk] Spec drift from instruction files** → Mitigation: specs derived directly from current `agents/` and `routines/` content; spec-drift will flag future gaps
- **[Risk] Capability boundaries too coarse** → Mitigation: index in `project.md` makes it easy to split later via a dedicated change
