# Handover: Create Linear Issue — SHA-25 Resume Website Merge

**For:** Any agent with Linear MCP access  
**From:** Cursor cloud agent (SHA-25, July 2026)  
**Action:** Create new issue in **Resume Website** project, then **cancel SHA-25**

Sharad will add the correct `resume-website` repo URL and access details on the new issue. This handoff contains everything the builder agent needs.

---

## Step 1 — Cancel the old issue

| Field | Value |
|---|---|
| **Issue to cancel** | **SHA-25** (original "How This Site Was Built" transparency panel) |
| **Action** | Move to **Canceled** (or equivalent). Comment: *"Superseded by [NEW-ISSUE-ID] — implementation complete in AI-Workspace; merge handoff to production resume-website repo."* |

Do **not** delete SHA-25 history — link the new issue from SHA-25's final comment.

---

## Step 2 — Create the new Linear issue

Use **New Issue Conventions** from `AGENTS.md`:

| Field | Value |
|---|---|
| **Project** | Resume Website |
| **Status** | Backlog |
| **Label** | `spec-needed` initially — Sharad will add repo details, then swap to `agent-ready` when ready to build |
| **Assignee** | Sharad Rohra (never an agent at creation) |
| **Priority** | High |
| **Title** | `🛠️ [Feature] Merge build transparency panel to production resume-website` |

### Description (paste into Linear)

## Context

SHA-25 (build transparency / "How this site was built") was **fully implemented** but never merged to production. The original SHA-25 issue is being **canceled** — this issue tracks the production merge.

**Why it stalled:** Cloud agents could only access `rohrasharad-ship-it/AI-Workspace`, not the production `resume-website` repo. Implementation lives as a reference copy in AI-Workspace.

**Sharad:** Please add the correct GitHub repo URL (`owner/repo`) and confirm Cursor cloud agent access on this issue. When ready, swap label to `agent-ready` and assign a builder agent.

---

## What's already built (do not re-spec)

### Feature
Opt-in **"How this site was built"** panel at the **very bottom** of the page (after Contact):

- Hidden until user scrolls to document end (`IntersectionObserver` sentinel)
- **Not** a fixed bottom-right FAB (voice agent owns that)
- Tap **"How this site was built"** → dark sheet with:
  - Headline: **"This site auto-improves"**
  - Circular workflow diagram (Linear, Cursor, GitHub, Vercel, OpenSpec logos)
  - Stats row (24+ issues, ~1hr spec→preview, 8 capabilities)
  - OpenSpec capability list
  - Footer: `live site → new gaps found → loop repeats`
- z-index below voice-agent FAB (sheet at z-150)

### Finalized spec
`AI-Workspace/resume-website/openspec/specs/build-transparency/spec.md` on branch below.

---

## Source code location (AI-Workspace)

| Item | Location |
|---|---|
| **Primary branch** | `cursor/sha-25-build-transparency-9a2d` |
| **Repo** | https://github.com/rohrasharad-ship-it/AI-Workspace |
| **Reference implementation** | `resume-website/` subdirectory on that branch |
| **Integration guide** | `resume-website/SHA-25-INTEGRATION.md` |
| **Apply script** | `resume-website/scripts/integrate-build-transparency.sh` |
| **Closed PR (reference)** | https://github.com/rohrasharad-ship-it/AI-Workspace/pull/16 |

### Files to copy into production resume-website

```
src/components/build-transparency/BuildTransparency.tsx
src/components/build-transparency/WorkflowDiagram.tsx
src/components/build-transparency/SystemLogos.tsx
src/lib/build-stats.ts
openspec/specs/build-transparency/spec.md
openspec/changes/sha-25-build-transparency/
```

Update `openspec/project.md` capability index. Add to production `page.tsx` after Contact:

```tsx
import { BuildTransparency } from "@/components/build-transparency/BuildTransparency";
// ...
<BuildTransparency />
```

---

## Working preview (AI-Workspace sandbox)

**Tap this on your phone:**

https://ai-workspace-git-cursor-sha-2-180d7d-rohrasharad-5924s-projects.vercel.app/previews/SHA-25-build/index.html

Scroll to bottom → tap **"How this site was built"**.

(This is the closed PR branch deploy — not `meet-sharad.vercel.app`.)

---

## Builder agent instructions (when `agent-ready`)

1. Clone the **production** resume-website repo (URL Sharad adds to this issue)
2. Run `integrate-build-transparency.sh` or copy files from `AI-Workspace` branch `cursor/sha-25-build-transparency-9a2d`
3. Integrate `<BuildTransparency />` after Contact in real `page.tsx`
4. `npm run build` — must pass
5. Open PR on production repo with Vercel preview on `meet-sharad.vercel.app`
6. Visual Self-QA desktop + mobile on real preview
7. Slack + Linear per AGENTS.md Role 1
8. Wait for `@cursor approved` before merge

---

## Related / cleanup

| Item | Action |
|---|---|
| SHA-25 (original) | **Cancel** — superseded by this issue |
| AI-Workspace PR #16 | Closed unmerged — keep for reference |
| AI-Workspace PR #21 | Draft docs only — optional |
| AI-Workspace issue #20 | Close as superseded by this Linear issue |
| Branch `preview/SHA-25-build` | Delete per AGENTS.md once build starts |

---

## Instructions for receiving agent

1. Create the issue above in **Resume Website** project per New Issue Conventions.
2. **Cancel SHA-25** with link to new issue ID.
3. Comment on new issue: *"SHA-25 canceled — waiting on Sharad for repo URL + agent access confirmation."*
4. Close AI-Workspace GitHub issue #20 as superseded (optional).
5. Do **not** start building until Sharad adds repo details and sets `agent-ready`.
