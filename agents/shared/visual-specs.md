# Shared Module: Visual Specs (mockups of proposed ideas)

Referenced by: `agents/spec-conversation.md`, `agents/spec-drift.md`,
`agents/bug-error.md`, `agents/market-feature.md`

PMs today pitch features with a prototype, not a document. This project follows
the same rule: **any time an agent proposes something with a meaningful visual
or motion component — whether during an active spec conversation or while
auto-generating a brand-new idea (spec-drift, bug/error, or market/feature) —
it attaches a visual, not just text.** Sharad should never have to imagine what
"the emoji tilts 20 degrees on scroll" or "add a rocket sticker near the hero
CTA" looks like from a sentence.

**Skip this entirely** for changes with no visual/UI component — logic, config,
copy-only changes, backend behavior. Text is genuinely enough there; don't
manufacture a visual to check a box.

**Mechanism (same for every use, only the effort tier changes):**
1. Build a **single standalone HTML/CSS/JS file** — no framework, no build step,
   just the element/interaction in question, or a rough page-outline showing
   roughly where it would sit. Do not touch the real project repo.
2. Save it to `rohrasharad-ship-it/AI-Workspace`, path `previews/<issue-id>-v<n>.html`
   (e.g. `previews/SHA-13-v1.html`)
3. Push to a branch named `preview/<issue-id>-v<n>` (e.g. `preview/SHA-13-v1`).
   **Do not open a PR** — Vercel deploys a preview for any pushed branch, PR or not.
4. Before pushing, **delete the previous iteration's branch** for this issue
   (`git push origin --delete preview/<issue-id>-v<n-1>`). Only one preview
   branch should ever exist per issue at a time.
5. Look up the deployment URL for the new branch. **The Vercel project's output
   directory is the repo root**, so the bare deployment URL just shows the
   placeholder homepage — link the actual file path:
   `<deployment-url>/previews/<issue-id>-v<n>.html`. Paste that full path
   alongside the spec text, not the bare deployment URL.
6. **When the idea is dropped or the spec is finalized** (`agent-ready` label,
   or Sharad rejects it in triage), delete the remaining preview branch. No
   preview branch should survive past that point.

**Two effort tiers — same mechanism, different investment:**

| Tier | When | Effort |
|---|---|---|
| **Full** | Sharad is already actively discussing this issue with you (spec conversation) | Build the real interaction if motion matters (e.g. an actual scroll-linked emoji tilt) — this is a live candidate for building |
| **Minimal** | You're auto-generating a brand-new idea Sharad hasn't seen yet (spec-drift, bug/error, market-feature) | A single static frame is enough: show the emoji itself, roughly where it would sit on the page, or a plain annotated mockup. No interactivity, no polish. Most auto-generated ideas get triaged out — don't over-invest before Sharad has even looked at it. |

**Branch safety — never touch `main`:** only ever run
`git push origin --delete preview/<issue-id>-v<n>` — a fully qualified branch
name with the `preview/` prefix. Never run a bare or wildcard delete command.
`main` is additionally protected at the GitHub level against deletion, but
agents must never attempt to delete anything other than a `preview/*` branch
they created themselves.
