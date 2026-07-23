## Why

Spec-drift's built-in stale-issue sweep (comment template, 3-per-run cap, 30-day cooldown) is implemented in `agents/spec-drift.md` step 10 but not documented in the idea-generation OpenSpec capability. OpenSpec is the living source of truth — shipped recurring behavior with no spec backing is exactly the drift this repo exists to catch.

## What Changes

- Add a **Spec-drift flags stale issues** requirement to `openspec/specs/idea-generation/spec.md` with a scenario matching the current comment template, caps, and eligibility rules from `agents/spec-drift.md` step 10.

## Capabilities

### New Capabilities

_None._

### Modified Capabilities

- `idea-generation`: Document spec-drift's stale-issue sweep — runs every time (independent of gap-filing), Backlog-only candidates, 30-day re-flag cooldown, 3 comments per run max, comment-only (never close/relabel).

## Impact

- `openspec/specs/idea-generation/spec.md` — new requirement and scenario (via delta)
