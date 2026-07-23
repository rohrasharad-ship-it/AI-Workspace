## Context

Two prior blocked sessions left handover notes in incompatible shapes:

| Pattern | Location | Example |
|---|---|---|
| Action handover | `handovers/<descriptive-name>.md` | `handovers/linear-sha-25-resume-handoff.md` |
| Artifact bundle | `delivery/<ISSUE-ID>/README.md` | `delivery/SHA-53/README.md` |

Both carry the same intent — preserve work for an agent with different tool access — but differ in path, naming, and required fields.

## Decision

Unify under **`handovers/`** in AI-Workspace (always, even when work targets another project):

1. **Action handover** — `handovers/<ISSUE-ID>-<short-slug>.md` when the receiver must *do* something (create/cancel a Linear issue, post a comment, enable infra).
2. **Artifact bundle** — `handovers/<ISSUE-ID>/README.md` (+ files alongside) when the receiver must *apply* code the blocked agent could not push to the target repo.

Required header block (five fields + issue link) and two body sections (Payload, Instructions for receiving agent) are mandatory for both kinds.

Legacy `delivery/` paths and pre-convention `handovers/linear-*` filenames are historical only — do not copy their shape for new handovers.

## Alternatives considered

- **Keep two top-level directories** (`handovers/` + `delivery/`) — rejected; the issue explicitly asks for one convention.
- **Linear comment only, no git file** — rejected; comments lack versioned artifacts and are hard to forward to agents without MCP.

## Risks

- Existing links to `delivery/SHA-53/` remain valid; no migration required for this change.
