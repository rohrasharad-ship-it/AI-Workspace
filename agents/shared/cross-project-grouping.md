# Shared Module: Cross-Project Pattern Grouping

Referenced by: `routines/idea-sweep.md`, `routines/README.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`

When idea-sweep runs against **two or more projects** in one trigger, matching
gaps found across repos in the same run are filed as **one Linear issue** (not
one per repo). Single-project sweeps are unchanged — roles file immediately in
that project's Linear project.

## When grouping applies

| Trigger | Behavior |
|---|---|
| One project (e.g. "Resume Website") | No grouping — file issues directly as today |
| Two or more projects, or "all projects" | Defer filing → group matches → file once per group |

## Deferred filing (multi-project runs only)

During multi-project sweeps, idea-generation roles **do not** call Linear
`save_issue` while scanning each project. Instead, for each real gap that
passes per-project dedupe, append a **candidate** to the run ledger:

| Field | Contents |
|---|---|
| `role` | `spec-drift`, `bug-error`, or `market-feature` |
| `project` | Display name from `projects.md` (e.g. "Resume Website") |
| `title` | Emoji + gap title (same as would-be issue title) |
| `brief` | Full Issue Brief fields (`In short`, `Problem`, `Solution`, `Why`, `What it looks like`) |
| `executionDetail` | Payload for the first comment (spec refs, log excerpts, dedupe terms) |
| `attachments` | Screenshots and visual previews collected for this project |
| `priority` | Suggested priority |

After a role finishes **all** projects in the run, the orchestrator groups that
role's candidates and files the resulting issues (see below). Repeat for each
role in idea-sweep order: spec-drift → bug-error → market-feature.

## Match criteria

Candidates from the **same role** in the **same run** match when they describe
the same underlying gap:

1. **Strong match** — any of:
   - Identical normalized title (lowercase, strip leading emoji, collapse whitespace)
   - Identical **In short** field (3–4 words, case-insensitive)
2. **Judgment match** — same user-visible problem and same intended fix outcome,
   even if wording differs slightly. Document why grouped in the filed issue's
   first comment.

**Never group across roles.** Spec-drift, bug-error, and market-feature
candidates stay separate even if descriptions overlap.

**When in doubt, do not group** — two issues is safer than hiding distinct gaps.

## Where grouped issues are filed

| Candidate count after grouping | Linear project |
|---|---|
| One project in the group | That project's Linear project (from `projects.md`) |
| Two or more projects in the group | **PM OS** (AI-Workspace meta-project) |

Cross-repo patterns are loop/infrastructure work — they belong in PM OS, not
duplicated across product backlogs. Grouped issues count toward PM OS's issue
cap only, not each affected product project's cap.

## Grouped issue format

Follow `agents/shared/conventions.md` and `agents/shared/issue-brief.md`, plus:

**Description** — standard Issue Brief with one extra line immediately after
**In short:**

```markdown
**Affects:** Resume Website, AI Landscape, Usercon
```

(List every affected project name from `projects.md`, comma-separated.)

**Title** — same as a single-project issue (emoji + gap). Do **not** put
"Affects N projects" in the title; the **Affects:** line carries the list.

**First comment** — merge execution detail from every project in the group.
Start with:

```
Grouped from N projects in one idea-sweep run (SHA-175 cross-project grouping).

**Projects:** Resume Website, AI Landscape, Usercon
**Match reason:** <identical In short / normalized title / judgment — pick one>
```

Then per-project sections:

```
### Resume Website
<that project's execution detail>

### AI Landscape
<that project's execution detail>
```

**Attachments** — attach screenshots from every affected project when
available (same mandatory self-QA screenshots as today, consolidated on one
issue).

## Orchestrator checklist (end of each role, multi-project only)

1. Collect all candidates for this role from the run ledger.
2. Cluster by match criteria above.
3. For each cluster:
   - If 1 project → file in that project's Linear project (normal Issue Brief).
   - If 2+ projects → file in PM OS with **Affects:** line and merged first comment.
4. Record filed issue URLs for the Slack summary.
5. Add to the PM OS channel summary when any grouped issues were filed:
   `Cross-project: [N] grouped issue(s) filed to PM OS` with links.

## Slack summary note

Per-project channel summaries stay the same shape. When grouping filed issues
to PM OS, the **#pm-ops** consolidated summary also lists those grouped issues
so Sharad sees them in one place.
