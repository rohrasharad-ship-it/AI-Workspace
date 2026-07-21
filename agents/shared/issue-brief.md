# Shared Module: Issue Brief (Scannable Description Format)

Referenced by: `agents/spec-drift.md`, `agents/bug-error.md`,
`agents/market-feature.md`, `agents/reviewer.md`, `agents/spec-conversation.md`,
`routines/README.md`

Every agent that **creates** a Linear issue writes the description in this
format. Sharad should understand the issue in under 10 seconds — no long
paragraphs, no implementation detail, no jargon.

The **Status Snapshot** block (see `agents/shared/status-snapshot.md`) still
goes at the very top when present. The Issue Brief follows immediately below
it.

## Template

```markdown
**In short:** <3–4 plain words — the gist at a glance>

**Problem:** <one sentence — what's wrong or missing today>

**Solution:** <one sentence — what we'd build or change>

**Why:** <one sentence — why it matters now>

**What it looks like:** <one sentence — plain-language picture of the result;
link to a visual preview here when the issue has a UI component>
```

## Rules

1. **Each field is exactly one line.** No bullet lists, no multi-sentence
   paragraphs, no sub-bullets inside a field.
2. **Plain language.** Write for a PM scanning a backlog on a phone — not for
   another engineer. No file paths, no function names, no framework terms.
3. **"In short" is 3–4 words max.** Noun-verb or adjective-noun is fine:
   `Add PDF download`, `Fix mobile overlap`, `Highlight project videos`.
4. **"Problem" = user pain or gap.** What someone experiences or can't do —
   not "the component lacks X prop."
5. **"Solution" = outcome, not implementation.** "A download button saves a
   PDF" — not "add an API route and react-pdf."
6. **"Why" = urgency or value.** Why bother now? One concrete reason.
7. **"What it looks like" = a picture in words.** For visual issues, one
   sentence plus the preview link from `agents/shared/visual-specs.md`. For
   non-visual issues (bugs in logs, backend gaps), describe the expected
   behavior after the fix.
8. **Idea-generation issues stay high-level.** Spec-drift, bug-error, and
   market-feature file Backlog + `spec-needed` issues — the brief is enough
   for triage. Deeper spec detail belongs in the later spec-conversation
   phase, not at creation time.
9. **Execution detail goes in the first comment, not the description.** After
   creating the issue, post a comment with evidence: spec file references,
   codebase areas checked, Linear dedupe search terms, error log excerpts,
   screenshot notes, visual-preview links. Sharad triages from the Issue
   Brief; digs into the comment when he wants proof. See the first-comment
   step in each idea-generation role file.
10. **Title and "In short" should align.** The title (with its leading emoji —
   see `agents/shared/conventions.md`) can expand slightly on "In short," but
   they should describe the same thing.

## Examples

### Spec-drift (missing feature)

```markdown
**In short:** Add PDF download

**Problem:** Visitors can't save your resume without screenshotting the page.

**Solution:** A clear download button that saves a clean PDF copy.

**Why:** Recruiters ask for a PDF attachment in almost every outreach email.

**What it looks like:** A "Download PDF" button below the resume header on desktop and mobile.
```

### Bug/error

```markdown
**In short:** Fix contact form crash

**Problem:** Submitting the contact form shows a blank error page about half the time.

**Solution:** The form should always confirm submission or show a clear retry message.

**Why:** You're losing inbound messages you never know were attempted.

**What it looks like:** After submit, a green "Message sent" confirmation — or a red inline error with a retry button, never a crash page.
```

### Market/feature (new idea)

```markdown
**In short:** Project video cards

**Problem:** Your best work is buried in long text blocks that people skim past.

**Solution:** Each project gets a short video preview card on the homepage.

**Why:** Video thumbnails get 3–5× more engagement than text-only project lists on comparable portfolio sites.

**What it looks like:** A grid of cards with a looping 5-second clip, project title, and one-line tagline — see preview link below.
```

### Reviewer spillover

```markdown
**In short:** Empty state message

**Problem:** The projects page shows a blank white area when there are no projects yet.

**Solution:** A friendly placeholder explaining projects are coming soon.

**Why:** A blank page looks broken to first-time visitors.

**What it looks like:** Centered text: "Projects coming soon" with a subtle illustration.
```
