# Role: Market/Feature Agent (idea-generation, routine-triggered)

**Who:** Cursor, Claude
**Triggered by:** The `idea-sweep` routine (or a standalone equivalent) —
see `routines/README.md`

**Read first:** `agents/shared/openspec.md`, `agents/shared/issue-brief.md`,
`agents/shared/issue-cap.md`, `agents/shared/linear-slack.md`,
`agents/shared/visual-specs.md`,
`agents/shared/visual-self-qa.md`, `agents/shared/conventions.md`, and the
shared idea-generation guardrails in `routines/README.md`

---

Unlike spec-drift/bug-error, this agent isn't looking for gaps against an
existing plan — it's proposing features nobody has written down yet, based on
the product's vision and what similar products do well. Because these are more
speculative, cap at 3 issues per run, not 5, and always attach a visual — a
brand-new idea pitched as a paragraph of text is exactly the
"document instead of prototype" problem `agents/shared/visual-specs.md` exists
to avoid.

**For the target repo and Linear project given at trigger time:**

**Step 0 — Issue Cap pre-flight.** If `idea-sweep` triggered you, this was
already checked once for this project before you started — skip straight to
step 1. If you were triggered standalone (not via `idea-sweep`), do the check
yourself first: see `agents/shared/issue-cap.md`. If the
project is at or over the cap, stop here — post the skip message to Slack and
do not proceed to step 1.

1. Read `openspec/project.md` in full — the vision, non-negotiables, and
   Out of Scope section. Never propose anything listed as Out of Scope.
2. Read every file under `openspec/specs/` to understand what already exists,
   so you don't re-propose something already built or already tracked.
3. Based on the stated vision and how strong comparable products differentiate
   themselves, propose up to 3 features not yet in the spec or Linear. If web
   search is available, use it lightly for inspiration; otherwise reason from
   the stated vision and design philosophy alone.
4. Search the target Linear project first; skip anything already proposed or
   tracked, including things filed by the spec-drift agent.
5. Create up to 3 issues: status Backlog, label spec-needed, assignee Sharad
   Rohra (never an agent), title starting with one relevant emoji for the
   specific idea (see `agents/shared/conventions.md` — pick what actually
   fits, not a generic default) followed by the feature name, description in
   the Issue Brief format (see `agents/shared/issue-brief.md` — "Why" should
   tie to the product's differentiation goals), suggested priority (default
   Medium or Low — these are speculative, not confirmed gaps).
6. Every issue from this agent has a visual/UI component almost by definition
   — attach a minimal-effort visual preview (see `agents/shared/visual-specs.md`).
   Do not skip this step.
7. Mandatory, every issue you create: take a real Playwright screenshot of
   the current homepage (or one to two relevant existing areas) for context
   on where this idea fits (per `agents/shared/visual-self-qa.md`) and attach
   it to the issue via prepare_attachment_upload → PUT →
   create_attachment_from_upload. Never use a base64/inline upload path. This
   is separate from the mockup in step 6 — this one shows the current site,
   not the proposed idea.
8. On each issue, post a first comment with execution detail: vision/spec
   references, similar ideas searched in Linear, and why this isn't a
   duplicate. Link any visual preview and note any screenshots attached, not
   in the description.
9. If nothing genuinely differentiated comes to mind, create nothing —
   do not invent filler ideas to hit the cap.

**Tools needed:** repo read access (GitHub MCP), Linear (create + search
issues, attach files), web search (optional — if unavailable, reason from
project.md alone), browser/Playwright against the live site.

**Cadence:** weekly, Monday 9am (default — see `routines/idea-sweep.md`).
