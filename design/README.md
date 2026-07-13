# UI Design Reference System

Agents building anything with a visual or motion component should start here
**before writing UI from scratch**. This folder is the hub; external libraries
are copy-paste sources, not npm dependencies we pre-install everywhere.

## When to read this

| Role | Read when |
|---|---|
| **Builder** | The issue touches layout, styling, animation, or any user-facing surface |
| **Spec Conversation** | Proposing or previewing a visual/motion feature |
| **Idea-generation** (spec-drift, bug/error, market) | Filing an issue with a UI component |

Skip this for backend-only, config, or copy-only changes.

## What's in this folder

| File | Purpose |
|---|---|
| [`resources.md`](resources.md) | Catalog of external sites — what each offers and when to use it |
| [`workflow.md`](workflow.md) | Step-by-step copy-paste workflow for agents |
| [`snippets/`](snippets/) | Local reference implementations (plain HTML/CSS/JS) agents can adapt |

## Default stack (React / Next.js projects)

For Resume Website, Usercon, and similar sites:

1. **shadcn/ui** — foundation (buttons, cards, forms, layout)
2. **React Bits or Aceternity UI** — hero text, backgrounds, card flair
3. **Motion** — custom React animations not covered by a component library
4. **Anime.js** — only for vanilla JS or truly bespoke timeline/SVG work

Do **not** `npm install` every library up front. Copy the specific component
source you need, adapt it, and add only the peer deps that component requires
(usually `motion` or `tailwind` utilities you already have).

## Quick decision tree

```
Need animated UI on a React/Next.js site?
├─ Pre-built effect exists (text reveal, spotlight, 3D card)?
│  └─ Copy from React Bits or Aceternity UI → see resources.md
├─ Standard app component (dialog, dropdown, form)?
│  └─ shadcn/ui
├─ Custom scroll choreography or SVG morph?
│  └─ Motion (React) or Anime.js (vanilla)
└─ Pure CSS hover/transition, no JS?
   └─ UI Verse or Animista → see resources.md
```

## Spec previews

Live demos for spec discussion live in `previews/<issue-id>-v<n>.html` at the
repo root (see `agents/shared/visual-specs.md`). SHA-44's preview demonstrates
Anime.js vs React Bits patterns side by side:

`previews/SHA-44-v1.html` (deployed on the AI-Workspace Vercel project)
