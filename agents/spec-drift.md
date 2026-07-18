# Role: Spec-Drift Agent (idea-generation, routine-triggered)

**Who:** Cursor, Claude
**Triggered by:** The `idea-sweep` routine (or a standalone equivalent) —
see `routines/README.md`

**Read first:** `agents/shared/openspec.md`, `agents/shared/issue-brief.md`,
`agents/shared/visual-specs.md`, `agents/shared/visual-self-qa.md`,
`agents/shared/conventions.md`, and the shared idea-generation guardrails in
`routines/README.md`

---

**Job:** find meaningful gaps between what's planned (OpenSpec) and what's
actually built, and file them as Backlog issues for Sharad to triage. This is
full-breadth reading by design — see the "who reads how much" table in
`agents/shared/openspec.md`.

**For the target repo and Linear project given at trigger time:**

**Step 0 — Issue Cap pre-flight.** If `idea-sweep` triggered you, this was
already checked once for this project before you started — skip straight to
step 1. If you were triggered standalone (not via `idea-sweep`), do the check
yourself first: see "Pre-flight: Issue Cap" in `routines/README.md`. If the
project is at or over the cap, stop here — post the skip message to Slack and
do not proceed to step 1.

1. Read `openspec/project.md` and every file under `openspec/specs/` to see what
   is planned/specced.
2. Read the current codebase to see what is actually built.
3. Find meaningful gaps — planned things missing or only half-built. Ignore
   cosmetic nitpicks.
4. Search the target Linear project first; skip anything already tracked.
5. Create up to 5 issues for real gaps: status Backlog, label spec-needed,
   assignee Sharad Rohra (never an agent), title starting with one relevant
   emoji (see `agents/shared/conventions.md` — pick what fits, not literally
   🔧 every time), description in the Issue Brief format (see
   `agents/shared/issue-brief.md`), suggested priority.
6. If the gap has a visual/UI component, attach a minimal-effort visual
   preview (see `agents/shared/visual-specs.md`) and link it in the issue
   description.
7. Mandatory, every issue you create: take a real Playwright screenshot of
   the live site area related to this gap (per `agents/shared/visual-self-qa.md`)
   and attach it to the issue via prepare_attachment_upload → PUT →
   create_attachment_from_upload. Never use a base64/inline upload path.
8. If nothing meaningful is found, create nothing.
9. **Housekeeping (runs every time, independent of 1-8):** list all remote
   `preview/*` branches in the target repo. For each, parse the issue ID from
   the branch name (`preview/<issue-id>-v<n>`) and look up that issue in
   Linear. Delete the branch if the issue is no longer labeled `spec-needed`
   (i.e. it moved to `agent-ready`, `In Review`, `Done`, or was
   canceled/duplicated), or if it's an older version number than the latest
   branch for that issue. Report the count deleted at the end of the run.
   This is the structural backup for preview-branch pileup — see
   `agents/shared/conventions.md`'s Cursor Rules section for why it exists.

**Tools needed:** repo read access (GitHub MCP, including branch delete),
Linear (create + search issues, attach files, read issue status/labels),
browser/Playwright against the live site.

**Cadence:** weekly, Monday 9am (default — see `routines/idea-sweep.md`).
