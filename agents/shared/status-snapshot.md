# Shared Module: The Issue Description — Spec Text vs. Status Snapshot

Referenced by: `agents/builder.md`, `agents/spec-conversation.md`

Every issue description has two parts, updated under different rules — this
is what lets Sharad get a full picture from the description alone, without
digging through comment history, while still keeping the spec itself from
being rewritten mid-conversation on a whim:

1. **Spec text** — the finalized feature description. Only changes on
   approval (see `agents/spec-conversation.md`). This is what the builder
   reads as "the spec."
2. **Status Snapshot** — a short block pinned at the very top of the
   description, refreshed by whichever agent/role last touched the issue, on
   *every* meaningful turn (spec reply, PR opened, self-QA fix found,
   approval, merge) — not gated on the spec being locked.

```
--- STATUS ---
Phase: <Spec discussion | Building | In Review | Done>
Last update: <date> — <one sentence of what just happened>
PR: <link, or "none yet">
Preview: <link, or "none yet">
--- END STATUS ---
```

Keep it to those four lines — this is a dashboard, not a log. Comments remain
the full history; this block is only ever overwritten with the current
snapshot, never appended to.

## Preview field — what Sharad's Preview button actually shows

Linear's **Preview** button (next to Review / Squash / Merge on a linked PR)
opens the **Vercel deployment for that PR's branch** — the bare `*.vercel.app`
root URL. It does **not** read the `Preview:` line in this snapshot; that line
is for humans scanning the issue description and for Slack.

**Why Preview sometimes looks wrong:**

| Situation | What Preview shows | What to do |
|---|---|---|
| **Product repo build** (resume-website, ai-landscape, etc.) | The real app on the PR branch — this is correct | Use Preview button normally |
| **AI-Workspace infra/docs** (no UI) | The sandbox placeholder homepage ("PM OS — Spec Preview Sandbox") — **not** the change | Ignore Preview; use `Preview: N/A` in snapshot; verify on GitHub |
| **Spec phase** (wireframe mockup) | Bare deployment root = placeholder homepage, **not** the mockup | Agent must link the **full file path**: `<deployment-url>/previews/<issue-id>-v<n>.html` in the snapshot; open that URL directly, not Preview button |
| **Stale spec preview** after build starts | Old wireframe from before `agent-ready` | Builder deletes `preview/*` branch and overwrites snapshot with the PR's real preview URL (or N/A) |

**Agent rules for the `Preview:` line:**

1. **Product repo with UI change:** branch Vercel URL from the Vercel bot's PR
   comment (e.g. `resume-website-git-feature-xxx.vercel.app`). Never the
   production domain (`meet-sharad.vercel.app`, etc.).
2. **AI-Workspace infra/docs-only:** `N/A (infra-only — verify on GitHub)`.
3. **Spec discussion with a visual mockup:** full path to the HTML file, not
   the bare deployment URL (see `agents/shared/visual-specs.md`).
4. **Clear on phase change:** when spec locks (`agent-ready`) or build starts,
   replace any spec-phase preview URL — do not leave a wireframe link on an
   issue that is now In Review.

**Production domains are not PR previews.** `ai-workspace.vercel.app` in
particular is misconfigured (stale unrelated app). Always use the branch URL
from the Vercel bot comment on the PR.
