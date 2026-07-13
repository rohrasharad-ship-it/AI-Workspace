# UI Copy-Paste Workflow for Agents

Follow this whenever an issue touches visual UI or motion. Goal: ship polished
UI fast by adapting existing code, not inventing animations from scratch.

## 1. Classify the need

Before writing code, answer:

1. **What effect?** (text reveal, scroll stagger, hover spotlight, background, page transition…)
2. **What stack?** (React/Next.js project vs plain HTML spec preview)
3. **How custom?** (off-the-shelf component vs bespoke timeline)

Use the decision tree in [`README.md`](README.md) and the tables in
[`resources.md`](resources.md).

## 2. Find a source

Search in this order:

1. **Local snippets** — [`snippets/`](snippets/) for common patterns already in-repo
2. **Component library** — React Bits, Aceternity UI, Magic UI, shadcn/ui
3. **Animation engine** — Motion or Anime.js only if nothing above fits
4. **CSS-only** — UI Verse or Animista for simple effects

## 3. Copy, don't install wholesale

```
❌  npm install every animation library "just in case"
✅  Copy the one component's source file into the project
✅  Add only peer deps that component needs (usually motion, clsx, tailwind-merge)
✅  Adapt class names, colors, and props to match the project's design system
```

For shadcn/React Bits CLI installs (`npx shadcn add …`), that's fine — it
copies source into your repo, same outcome.

## 4. Adapt to the project

When pasting into a real project:

- Match existing **color tokens** and **spacing** (don't paste dark-theme defaults into a light site)
- Respect **reduced-motion** — wrap intense animations in `prefers-reduced-motion` checks
- Keep **bundle size** in mind — one hero animation is worth it; animating every paragraph is not
- Run the project **build** after adding deps — Motion/Anime.js must resolve

## 5. Spec previews (no React)

For `spec-needed` phase previews (`previews/<issue-id>-v<n>.html`):

- Use **plain HTML/CSS/JS** — no framework, no build step
- Anime.js via CDN is fine for engine demos
- Mimic React Bits patterns in vanilla JS when showing "what it would look like"
- See `agents/shared/visual-specs.md` for branch/deploy mechanics

## 6. Document what you used

In the PR or Linear comment, note:

- Which resource site (or local snippet) the effect came from
- What you changed during adaptation
- Any new peer dependency added

This helps Sharad trace effects back to source and future agents reuse the pattern.

## Anti-patterns

| Don't | Do instead |
|---|---|
| Write a custom scroll observer from scratch | Copy React Bits `FadeContent` or Anime.js `onScroll` |
| Install GSAP + Anime.js + Motion on one page | Pick one engine for the bespoke parts |
| Paste a full dark-theme hero into a light site | Swap CSS variables to project tokens |
| Skip mobile check | Test responsive + reduced-motion |
| Build UI without reading this folder first | Start at [`README.md`](README.md) |
