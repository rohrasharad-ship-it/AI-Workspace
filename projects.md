# Project Index

Every project any agent or routine operates on, in one place. Routines
(`routines/*.md`) resolve a project name given at trigger time against this
table to get its repo, Linear project, Slack channel, and prod URL.

| Project | Repo | Linear Project | Linear Project ID | Slack Channel | Vercel Prod |
|---|---|---|---|---|---|
| Resume Website | rohrasharad-ship-it/resume-website | Resume Website | b01a99ac-46a3-4b00-9139-31e00fae781d | #resume-website | meet-sharad.vercel.app |
| AI Workspace (PM OS) | rohrasharad-ship-it/AI-Workspace | PM OS | 3703a715-c49d-4b9e-b6f1-5975d3ebe39a | #pm-ops | ai-workspace.vercel.app (spec-preview sandbox — set up once via Vercel dashboard "Add New Project", see `agents/shared/visual-specs.md`) |
| AI Landscape 2026 | rohrasharad-ship-it/ai-landscape | AI Landscape | 4ef7d096-f5bb-44f4-bac5-417e4488cdb8 | #ai-landscape | https://rohrasharad-ship-it.github.io/ai-landscape/ |
| Application Agent | rohrasharad-ship-it/Application-Agent | Application Agent | 7dc5202c-a586-4bed-b2d3-fba10f2dd913 | #application-agent | TBD |
| Usercon | rohrasharad-ship-it/Usercon | UserCon | 47ebefac-a4f4-4bdd-a382-4506f7e79b6b | #usercon | TBD |

**Linear Project ID** is the UUID used for `list_issues` project filtering and
other Linear MCP calls. Display names are for humans; IDs are required for
reliable queries (see `agents/shared/issue-cap.md`).

*Add new projects via `/init-project` skill — include the Linear Project ID
when registering a row (from Linear → Project → … → Copy project ID, or
`list_projects` via MCP).*
