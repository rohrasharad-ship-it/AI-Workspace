# Shared Module: Issue Cap Pre-flight

Referenced by: `routines/README.md`, `routines/idea-sweep.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`

Before any idea-generation role creates issues for a project, count that
project's **active pipeline issues**. If the count is **5 or more**, do not run
idea-generation for that project this cycle.

## What counts toward the cap

An issue counts only when **all** of the following are true:

1. **Same project** — `projectId` on the issue matches the **Linear Project
   ID** from `projects.md` for the target project.
2. **Active workflow stage** — `status` (display name, case-insensitive) is one
   of:
   - `Backlog`
   - `Todo` or `To Do`
   - `In Progress`
   - `In Review`

Issues in **Done**, **Canceled**, **Duplicate**, or any other status do **not**
count — even if `statusType` is not terminal.

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
4. **Count active pipeline issues:** for each issue, increment only when:
   - `projectId` equals the target Linear Project ID from step 1, **and**
   - `status` matches one of the four active stages above (case-insensitive;
     treat `To Do` and `Todo` as the same stage).
5. If the count is **≥ 5**, the project is at cap — post the skip message below
   and stop **creating new issues** for this project. Spec-drift still runs its
   stale-issue sweep and preview-branch housekeeping (steps 10–11 in
   `agents/spec-drift.md`) even at cap.
6. **Sanity check:** if the count is **0** but the project should have open
   work, call `list_projects` and confirm the ID in `projects.md` still
   matches. Update `projects.md` if Linear was reorganized, then recount once.

## Skip message

Post to the project's Slack channel from `projects.md`:

```
⛔ Idea-sweep skipped — [Project Name from projects.md]
Linear already has [N] active pipeline issues (cap: 5 per project). Triage the backlog
before more get added.
```

**Check once per project per routine run** — if `idea-sweep` is running all
three roles, do this a single time before any of them start.
