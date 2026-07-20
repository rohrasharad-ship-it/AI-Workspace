# Shared Module: Issue Cap Pre-flight

Referenced by: `routines/README.md`, `routines/idea-sweep.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`

Before any idea-generation role creates issues for a project, count that
project's **open Linear issues**. If the count is **5 or more**, do not run
idea-generation for that project this cycle.

## What counts as "open"

Every issue whose `statusType` is **not** `completed`, `canceled`, or
`duplicate`. That includes Backlog, spec-needed, agent-ready, In Progress, In
Review, and any other non-terminal state.

## How to count (Linear MCP)

**Do not filter `list_issues` by project display name.** For some projects
(AI Landscape and Usercon are confirmed examples) the Linear MCP returns an
empty list with no error when `project` is set to the human-readable name —
which makes the cap look like zero and lets idea-generation flood an already
overloaded backlog.

Always use the **Linear Project ID** (UUID) from `projects.md`.

### Steps

1. Look up the target project row in `projects.md` and copy its **Linear
   Project ID**.
2. Call `list_issues` with `project: "<Linear Project ID>"` and `limit: 250`.
3. **Paginate:** while the response has `hasNextPage: true`, call again with
   the `cursor` from the previous page. Collect issues from every page.
4. **Count open:** increment for each issue whose `statusType` is not
   `completed`, `canceled`, or `duplicate`.
5. If the count is **≥ 5**, the project is at cap — post the skip message below
   and stop **creating new issues** for this project. Spec-drift still runs its
   stale-issue sweep and preview-branch housekeeping (steps 10–11 in
   `agents/spec-drift.md`) even at cap.
6. **Sanity check:** if the count is **0** but the project should have open
   work, call `list_projects` and confirm the ID in `projects.md` still
   matches. Update `projects.md` if Linear was reorganized, then recount once.

## Skip message

Post to the project's Slack channel from `projects.md`.

When **spec-drift steps 10–11 will still run** (`idea-sweep` pre-flight at cap,
or spec-drift triggered standalone):

```
⛔ Issue cap reached — [Project Name from projects.md]
Linear already has [N] open issues (cap: 5 per project). No new issues will be
filed this cycle — triage the backlog before more get added. Stale-issue sweep
and preview-branch cleanup still run.
```

Otherwise (bug-error or market-feature standalone at cap):

```
⛔ Issue cap reached — [Project Name from projects.md]
Linear already has [N] open issues (cap: 5 per project). No new issues will be
filed this cycle — triage the backlog before more get added.
```

**Check once per project per routine run** — if `idea-sweep` is running all
three roles, do this a single time before any of them start.
