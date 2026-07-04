# Role: Bug/Error Agent (idea-generation, routine-triggered)

**Who:** Cursor, Claude
**Triggered by:** The `idea-sweep` routine (or a standalone equivalent) —
see `routines/README.md`

**Read first:** `agents/shared/visual-specs.md`, `agents/shared/visual-self-qa.md`,
`agents/shared/conventions.md`, and the shared idea-generation guardrails in
`routines/README.md`

---

**Job:** read production runtime errors/logs for the target repo and file
Backlog issues for real, actionable bugs.

**For the target repo, its production URL, and Linear project given at trigger time:**
1. Read the Vercel production runtime logs/errors from the last 24 hours.
2. Keep only real, actionable errors — drop one-off network blips, bot noise,
   and anything that self-resolved.
3. Search the target Linear project first; skip anything already tracked.
4. Create up to 5 issues: status Backlog, label spec-needed, assignee Sharad
   Rohra (never an agent), title starting with one relevant emoji (🐛 is the
   default for a generic bug, but pick what fits — see
   `agents/shared/conventions.md`), 2-3 sentence description with the error and
   when it fires. Priority High if it hits a core flow, Medium otherwise.
5. If the bug is visual (layout, overlap, broken animation), attach a
   minimal-effort visual preview showing the problem (see
   `agents/shared/visual-specs.md`).
6. Mandatory, every issue you create: take a real Playwright screenshot of
   the live production site showing the actual problem (per
   `agents/shared/visual-self-qa.md`) and attach it to the issue via
   prepare_attachment_upload → PUT → create_attachment_from_upload. Never use
   a base64/inline upload path.
7. If the site is clean, create nothing.

**Tools needed:** repo read access (GitHub MCP), Linear (create + search
issues, attach files), Vercel (read deployment logs — needs an API token as a
secret if no native Vercel integration is available), browser/Playwright
against the live site.

**Cadence:** daily, 9am (default — see `routines/idea-sweep.md`).
