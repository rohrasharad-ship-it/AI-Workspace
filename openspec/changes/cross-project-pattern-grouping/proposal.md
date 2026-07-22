## Why

When idea-sweep runs against multiple projects in one trigger, each role files separate Backlog issues per project even when the underlying gap is identical. Sharad then triages the same problem N times instead of once.

## What Changes

- Add `agents/shared/cross-project-grouping.md` — matching rules, deferred filing, grouped issue format, and which Linear project receives cross-repo issues.
- Update `routines/idea-sweep.md` and `routines/README.md` — multi-project runs collect gap candidates per role, group matches at end of run, then file once.
- Update spec-drift, bug-error, and market-feature role files — during multi-project idea-sweep, defer Linear creation and hand candidates to the orchestrator grouping step (single-project runs unchanged).
- Update OpenSpec `routines` and `idea-generation` specs with grouping requirements.

## Capabilities

### New Capabilities

_None — grouping is a refinement of existing idea-sweep orchestration._

### Modified Capabilities

- `routines`: Multi-project idea-sweep MUST group matching gaps before filing; single-project runs behave as today.
- `idea-generation`: Roles MUST defer per-project filing during multi-project sweeps and supply grouping candidates to the orchestrator.

## Impact

- `agents/shared/cross-project-grouping.md` — new shared module
- `routines/idea-sweep.md`, `routines/README.md` — orchestration flow
- `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md` — defer-filing step
- `openspec/specs/routines/spec.md`, `openspec/specs/idea-generation/spec.md` — requirement deltas
- `previews/SHA-175-v1.html` — reference mockup from spec phase
