## Context

`projects.md` has six columns: Project, Repo, Linear Project, **Linear Project ID**, Slack Channel, Vercel Prod. Issue-cap pre-flight (`agents/shared/issue-cap.md`) requires the UUID for reliable `list_issues` filtering. SHA-136 backfilled IDs for existing rows, but `/init-project` Step E still documents a five-column row template that omits the ID.

## Goals / Non-Goals

**Goals:**
- Capture the Linear project UUID at creation time in Step D.
- Write all six columns in Step E, matching the live `projects.md` table format.
- Make the integrations spec scenario explicit about using the creation response ID.

**Non-Goals:**
- Retroactively fixing any already-onboarded projects missing IDs (manual/backfill if needed).
- Changing the `projects.md` table structure itself.

## Decisions

1. **Source of ID: `save_project` response** — The Linear MCP `save_project` tool returns the created project's `id` field. Store it as `$LINEAR_PROJECT_ID` immediately after Step D. Fallback: call `list_projects` and match by name if the response omits `id`.

2. **Row template matches column order** — Step E row:
   `| $PROJECT_NAME | $REPO | $PROJECT_NAME | $LINEAR_PROJECT_ID | $SLACK_CHANNEL | $VERCEL_URL |`
   This mirrors the existing table header order exactly.

## Risks / Trade-offs

- **[Risk] Agent skips capturing ID** → Mitigation: Step D explicitly says "save the returned project `id`" and Step E references `$LINEAR_PROJECT_ID` so the variable must exist before writing the row.
