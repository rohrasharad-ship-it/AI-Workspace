## Why

The idea-sweep issue cap currently counts every non-terminal Linear issue in a project. That is too broad — issues in unexpected workflow states (or miscounted across projects) can block new ideas or let sweeps run when the real backlog is full. The cap should only reflect active pipeline work: Backlog, Todo, In Progress, and In Review.

## What Changes

- Tighten `agents/shared/issue-cap.md` so only issues in the four active workflow stages count toward the cap of 5.
- Require project scoping via Linear Project ID **and** verify each issue's `projectId` matches before counting.
- Update `routines/README.md` summary to match the narrower count rule.
- Update OpenSpec requirements in `idea-generation` and `integrations` specs.

## Capabilities

### New Capabilities

_None — this refines existing issue-cap behavior._

### Modified Capabilities

- `idea-generation`: Issue cap counts only Backlog, Todo, In Progress, and In Review issues for the target project.
- `integrations`: Issue cap check scenario updated to describe the stage-based count.

## Impact

- `agents/shared/issue-cap.md` — primary counting procedure
- `routines/README.md` — pre-flight summary
- `openspec/specs/idea-generation/spec.md` — requirement text
- `openspec/specs/integrations/spec.md` — scenario text
