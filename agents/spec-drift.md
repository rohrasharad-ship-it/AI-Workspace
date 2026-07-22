# Role: Spec-Drift Agent (idea-generation, routine-triggered)

**Who:** Cursor, Claude
**Triggered by:** The `idea-sweep` routine (or a standalone equivalent) —
see `routines/README.md`

**Read first:** `agents/shared/openspec.md`, `agents/shared/issue-brief.md`,
`agents/shared/issue-cap.md`, `agents/shared/cross-project-grouping.md`,
`agents/shared/linear-slack.md`,
`agents/shared/visual-specs.md`, `agents/shared/visual-self-qa.md`,
`agents/shared/conventions.md`, and the shared idea-generation guardrails in
`routines/README.md`

---

**Job:** (1) find meaningful gaps between what's planned (OpenSpec) and what's
actually built, and file them as Backlog issues for Sharad to triage; (2)
cross-check existing open issues against the current codebase and comment when
one looks already resolved. Gap-finding is full-breadth reading by design —
see the "who reads how much" table in `agents/shared/openspec.md`.

**For the target repo and Linear project given at trigger time:**

**Step 0 — Issue Cap pre-flight (gap-filing only).** If `idea-sweep` triggered
you, the routine already checked the cap once for this project before you
started. If that pre-flight put the project at or over the cap, **skip steps
1–9** and go straight to step 10. Otherwise skip the cap check and go to step
1. If you were triggered standalone (not via `idea-sweep`), do the check
yourself first: see `agents/shared/issue-cap.md`. If the project is at or over
the cap, **skip steps 1–9** (do not file new issues) but still run steps 10–11
— stale-issue comments and preview-branch housekeeping help shrink the backlog
and do not count against the cap.

1. Read `openspec/project.md` and every file under `openspec/specs/` to see what
   is planned/specced.
2. Read the current codebase to see what is actually built.
3. Find meaningful gaps — planned things missing or only half-built. Ignore
   cosmetic nitpicks.
4. Search the target Linear project first; skip anything already tracked.
5. For each real gap that passes step 4 dedupe — at most 5 per run:
   **Single-project run:** create the issue in Linear (`save_issue`): status
   Backlog, label spec-needed, assignee Sharad Rohra (never an agent), title
   starting with one relevant emoji (see `agents/shared/conventions.md` — pick
   what fits, not literally 🔧 every time), description in the Issue Brief
   format (see `agents/shared/issue-brief.md`), suggested priority. Then do
   steps 6–8 for each issue.
   **Multi-project idea-sweep:** do **not** call `save_issue` — for each gap,
   append a grouping candidate to the run ledger per
   `agents/shared/cross-project-grouping.md` (title, brief, priority,
   `executionDetail`, `attachments`). Then do steps 6–8 below to populate
   `executionDetail` and `attachments` on the candidate.
6. If the gap has a visual/UI component, attach a minimal-effort visual
   preview (see `agents/shared/visual-specs.md`). **Single-project:** attach
   to the Linear issue. **Multi-project:** include in the candidate's
   `attachments`.
7. Mandatory, every gap you file: take a real Playwright screenshot of the
   live site area related to this gap (per `agents/shared/visual-self-qa.md`).
   **Single-project:** attach to the issue via prepare_attachment_upload → PUT
   → create_attachment_from_upload. Never use a base64/inline upload path.
   **Multi-project:** add to the candidate's `attachments` (do not call Linear
   attachment APIs).
8. **Single-project:** on each issue, post a first comment with execution
   detail: openspec file(s) referenced, codebase areas checked, Linear search
   terms used for dedupe, and why this isn't a duplicate. Link any visual
   preview and note any screenshots attached, not in the description.
   **Multi-project:** set `executionDetail` on the candidate with the same
   payload.
9. If nothing meaningful is found, create nothing / append no candidates.
10. **Stale-issue sweep (runs every time, independent of 1–9):** for the
   target Linear project, list open issues (paginate per
   `agents/shared/issue-cap.md` — use the **Linear Project ID** from
   `projects.md`). For each candidate issue:
   - **Include** issues in `Backlog` status (any labels). These are the usual
     stale backlog items.
   - **Skip** issues in `In Progress`, `In Review`, or `Done` — someone is
     actively working them or they are already terminal.
   - **Skip** if this issue already has a comment from a prior spec-drift run
     containing `Spec-drift check — this may already be done` posted within the
     last 30 days (read comments via Linear MCP; do not re-flag the same issue
     every week).
   - Read the issue's description and understand what it asks for. Cross-check
     against the current codebase, `openspec/specs/`, and the live site (when
     relevant). Flag only when you have **high confidence** the described work
     is already shipped — not cosmetic guesses or partial matches.
   - Post **at most 3 comments per run** (prioritize the oldest Backlog issues
     first). Use this template:
     ```
     🔍 Spec-drift check — this may already be done

     Cross-checked against the current codebase and OpenSpec on <date>.

     **What I looked at:** <openspec file(s), code paths, or live URL checked>

     **Why it looks resolved:** <one plain-language sentence>

     Is it safe to close this issue? A one-line reply is enough — no need to @mention anyone.
     ```
   - **Never close, cancel, or relabel the issue yourself** — comment only.
     Sharad decides.
   - Report the count flagged at the end of the run (0 is fine).
11. **Housekeeping (runs every time, independent of 1–9):** preview branches
   live in **AI-Workspace** (`rohrasharad-ship-it/AI-Workspace`), not in the
   target project repo — run the cleanup script there:
   ```bash
   cd AI-Workspace   # clone or use an existing checkout
   export LINEAR_API_KEY=...   # required for issue label/state lookup
   bash scripts/cleanup-preview-branches.sh
   ```
   Use `--dry-run` to report without deleting. The script parses each
   `preview/<issue-id>-v<n>` branch, looks up the issue in Linear, and deletes
   when the issue is no longer `spec-needed` (moved to `agent-ready`, `In
   Review`, `Done`, or canceled/duplicated) or when it's an older version than
   the latest branch for that issue. Report the deleted count at the end of the
   run. A scheduled GitHub Action (`.github/workflows/preview-branch-cleanup.yml`)
   runs the same script weekly as a structural backup — see
   `agents/shared/conventions.md`.

**Tools needed:** shell access to clone/run scripts in AI-Workspace (including
`git push origin --delete preview/<issue-id>-v<n>` for orphans), Linear (create
+ search issues, **comment on existing issues**, attach files, read issue
status/labels/comments), browser/Playwright against the live site.

**Cadence:** weekly, Monday 9am (default — see `routines/idea-sweep.md`).
