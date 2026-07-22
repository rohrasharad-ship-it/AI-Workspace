## Context

Idea-sweep already fans out (role × project) and each role files issues directly in the target project's Linear project. SHA-175 adds a grouping pass when the trigger names more than one project (or "all projects").

## Goals / Non-Goals

**Goals:**

- One Linear issue per shared gap per run, listing every affected project.
- Single-project sweeps unchanged — immediate filing as today.
- Grouping keyed by role + normalized gap signature (same underlying problem).

**Non-Goals:**

- Cross-run deduplication (searching Linear for prior grouped issues) — existing per-project dedupe still applies; grouping is within-run only.
- Automatic fix rollout across repos — grouping is triage efficiency only.
- Code/scripts — this remains instruction-driven orchestration in markdown.

## Decisions

### 1. When grouping applies

Only when the trigger names **two or more projects** in the same run. One project → roles file immediately (no change).

### 2. Deferred filing flow

During multi-project sweeps:

1. Each (role × project) pair still scans and dedupes against that project's Linear backlog.
2. Instead of `save_issue`, the role appends a **candidate** to the run's in-memory list (or orchestrator ledger): role, project name, Issue Brief fields, execution-detail payload, screenshots/previews collected.
3. After all pairs for a given **role** finish (or after all roles — see below), the orchestrator runs grouping for that role's candidates.

**Order:** Group per role after that role completes all projects (spec-drift across all projects → group spec-drift candidates → file; then bug-error; then market-feature). This keeps bug patterns separate from spec gaps and from feature ideas.

### 3. Match criteria

Two candidates from the same role in the same run **match** when a human would call them the same underlying gap:

- Normalize: lowercase, strip emoji from title, collapse whitespace.
- **Strong match:** identical normalized title OR identical **In short** field (3–4 words).
- **Judgment match:** same problem + same solution outcome even if wording differs slightly — orchestrator/agent must document why grouped in the first comment.
- **Never group across roles** (spec-drift ≠ bug-error ≠ market-feature).

When in doubt, do **not** group — filing two issues is safer than hiding distinct gaps.

### 4. Where grouped issues are filed

**PM OS** Linear project (AI-Workspace meta-project) — cross-repo patterns are loop/infrastructure concerns. The Issue Brief **Problem** line names affected projects; description includes an **Affects:** line.

Single-project candidates still file in that project's own Linear project.

### 5. Grouped issue shape

- **Title:** Same as today (one emoji + gap title) — no "Affects N" in title; the description carries the list.
- **Description:** Standard Issue Brief plus an extra line after **In short:**
  ```
  **Affects:** Resume Website, AI Landscape, Usercon
  ```
- **First comment:** Execution detail from every affected project (spec refs, log excerpts, dedupe terms per repo), plus explicit note: "Grouped from N projects in one idea-sweep run — see agents/shared/cross-project-grouping.md."
- **Screenshots:** Attach one per affected project when available (same as today, just consolidated on one issue).

### 6. Slack summary

Unchanged shape per project channel for counts, but grouped issues link once from PM OS channel summary. Add a line to the **PM OS** sweep summary when grouping filed there: `Cross-project: [N] grouped issues filed to PM OS`.

## Risks / Trade-offs

- **PM OS backlog noise** → Acceptable; cross-repo items are meta-work. Cap still applies per project — grouped issues count toward PM OS cap only, not each affected product project.
- **Orchestrator complexity** → Mitigated by shared module; single-project path untouched.

## Migration

Docs-only. Takes effect on next multi-project idea-sweep run.
