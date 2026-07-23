## Why

Agents that hit a hard tool-access wall (no Linear MCP, no push access to a private target repo, etc.) have independently invented two ad hoc handover patterns (`handovers/*.md` with inconsistent filenames, and `delivery/<issue-id>/`). Without a single convention, each blocked session fragments institutional memory and forces the next agent to reverse-engineer intent.

## What Changes

- Add a **Blocked-agent handover** section to `agents/shared/conventions.md` — standard location, filename shape, required header fields, body sections, and session steps for blocked and receiving agents.
- Reference the convention from every role file that can hit a hard tool-access block: builder, reviewer, spec-conversation, spec-drift, bug-error, market-feature.
- Add a delta to `openspec/specs/shared-conventions/spec.md` requiring the handover convention when an agent is blocked by missing tools.

## Capabilities

### New Capabilities

_None — handover is a cross-cutting convention, not a new capability._

### Modified Capabilities

- `shared-conventions`: Agents blocked by missing tool access MUST write a handover file at the standard path with required fields, comment on the Linear issue with the link, and refresh the Status Snapshot.

## Impact

- `agents/shared/conventions.md` — new section
- `agents/builder.md`, `agents/reviewer.md`, `agents/spec-conversation.md`, `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md` — short pointer to the convention
- `openspec/specs/shared-conventions/spec.md` — new requirement (via delta)
