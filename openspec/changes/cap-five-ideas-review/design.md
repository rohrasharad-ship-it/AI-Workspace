## Context

Idea-generation routines (`idea-sweep`) gate on a per-project cap of 5 open issues before filing new ideas. SHA-136 fixed project filtering (use Linear Project ID, not display name). SHA-167 narrows *which* issues within that project count.

Linear workflow states on Sharad's team:

| Status | `statusType` |
|---|---|
| Backlog | `backlog` |
| Todo | `unstarted` |
| In Progress | `started` |
| In Review | `started` |
| Done | `completed` |
| Canceled | `canceled` |
| Duplicate | `duplicate` |

The MCP `list_issues` response exposes `status` (display name) and `statusType`. Two active stages share `statusType: started` (In Progress, In Review), so counting by `statusType` alone is insufficient.

## Goals / Non-Goals

**Goals:**
- Count only issues in Backlog, Todo, In Progress, or In Review.
- Count only issues belonging to the target project (`projectId` matches `projects.md`).
- Keep pagination, sanity-check, and skip-message behavior unchanged.

**Non-Goals:**
- Changing the cap number (still 5).
- Filtering by label (`spec-needed` vs `agent-ready`) — stage is the gate, not label.
- Adding executable code; agents follow markdown instructions.

## Decisions

### Decision: Match on `status` display name, not `statusType`

Use case-insensitive match against: `Backlog`, `Todo` (also accept `To Do`), `In Progress`, `In Review`. This is explicit, matches Sharad's workflow names, and avoids counting any future custom non-terminal states.

**Alternatives considered:**
- `statusType` not in (`completed`, `canceled`, `duplicate`) — current rule; too broad.
- `statusType` in (`backlog`, `unstarted`, `started`) — lumps In Review with In Progress correctly but would also count any future `started` custom state.

### Decision: Belt-and-suspenders `projectId` check

Even when filtering `list_issues` by project UUID, verify each returned issue's `projectId` equals the target ID before incrementing. Guards against MCP quirks or mis-assigned issues.

## Risks / Trade-offs

- **Team-specific status names** → Document accepted aliases (`To Do` / `Todo`). If a project team renames states, update the allowlist in `issue-cap.md`.
- **Slightly lower counts** → Projects with issues in other non-terminal states no longer block idea-sweep; intentional per spec.

## Migration Plan

Docs-only change. No deploy or data migration. Takes effect on next idea-sweep run.
