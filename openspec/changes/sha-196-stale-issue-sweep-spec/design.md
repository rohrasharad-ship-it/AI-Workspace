## Context

The stale-issue sweep is already implemented in `agents/spec-drift.md` step 10. This change only syncs the OpenSpec capability spec to match — no agent instruction changes.

## Goals / Non-Goals

- **Goals:** Capture sweep eligibility, caps, cooldown, comment template, and comment-only behavior in `idea-generation/spec.md`.
- **Non-Goals:** Change sweep behavior, modify `agents/spec-drift.md`, or add new automation.

## Decisions

- Place the requirement under the existing spec-drift section of `idea-generation` since the sweep is a spec-drift responsibility that runs even when gap-filing is skipped (e.g. at issue cap).

## Risks / Trade-offs

- None — documentation-only alignment with existing behavior.
