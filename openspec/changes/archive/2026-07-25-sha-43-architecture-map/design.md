## Context

The AI-Workspace Vercel project deploys the repo root as static files. `index.html` is the bare `*.vercel.app` URL Sharad sees from Linear's Preview button on PM OS PRs. Today it is a one-paragraph placeholder.

## Goals

- Miro-style board layout with positioned cards, zone labels, dot-grid background, and shaded zone regions
- Icons, short descriptions on every card, and a rich side panel with step-by-step "What happens"
- Animated walkthroughs: **Build loop** and **Idea sweep** with step captions, flowing arrows, and traveling dots (Anime.js)
- Edge routing from card ports (not centers) to reduce visual clutter; clickable chips in side panel
- Single render path per viewport (no duplicate DOM nodes); mobile uses grouped card grids

## Non-Goals

- Auto-generating the graph from markdown at build time (static data embedded in JS is enough for now)
- Editing or syncing back to source files from the UI

## Decisions

1. **Data in JS** — `ARCHITECTURE` constant mirrors `agents/` and `routines/` as of this change; manual update when structure changes (acceptable for a sanity-check tool).
2. **SVG edges** — Bezier paths between column node centers; `path` stroke opacity tied to highlight state.
3. **Visual style** — Dark theme consistent with `previews/SHA-44-v1.html` (grain, radial glow, system font).
4. **AGENTS.md router** — Shown as a header badge above the three columns, not a fourth column.

## Risks / Trade-offs

- Graph data can drift from git → mitigated by linking file paths in the detail panel so mismatches are obvious when clicking through.
