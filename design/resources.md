# UI Resource Catalog

Copy-paste sources for front-end UI and animation. **You own the code** after
copying — no black-box npm packages required unless the component's peer deps
demand it (e.g. `motion` for Framer-based snippets).

## Component libraries (copy-paste, React)

Best for: polished motion on React/Next.js sites without writing animation
logic from scratch. This is the Instagram-reel aesthetic in component form.

| Site | URL | Best for | Stack | Integration |
|---|---|---|---|---|
| **React Bits** | [reactbits.dev](https://reactbits.dev) | Text animations (BlurText, SplitText), backgrounds (Spotlight, Aurora), 3D cards, magnetic buttons | React + Tailwind | `npx shadcn add @react-bits/<Component>-TS-TW` or copy source |
| **Aceternity UI** | [ui.aceternity.com](https://ui.aceternity.com) | Landing-page wow effects — beams, particles, 3D cards, tracing borders | React + Tailwind + Motion | Copy component source from site |
| **Magic UI** | [magicui.design](https://magicui.design) | Marketing micro-interactions, neon gradients, marquee, bento grids | React + Tailwind + Motion | `npx shadcn add` or copy source |
| **shadcn/ui** | [ui.shadcn.com](https://ui.shadcn.com) | Accessible app primitives — not flashy, but solid foundation | React + Radix + Tailwind | `npx shadcn add <component>` |

### When to pick which

| You need… | Start here |
|---|---|
| Hero text reveal, decrypted/scramble text | React Bits |
| Cursor spotlight, aurora, particle background | React Bits or Aceternity UI |
| 3D tilt card, tracing beam, lamp effect | Aceternity UI |
| Marquee, animated beam, dock | Magic UI |
| Button, dialog, form, table, sidebar | shadcn/ui |

## Animation engines (write your own logic)

Best for: bespoke timelines, scroll choreography, SVG morphing, physics.
Higher effort — use only when no component library has what you need.

| Site | URL | Best for | Stack | Integration |
|---|---|---|---|---|
| **Anime.js** | [animejs.com](https://animejs.com) | Timelines, stagger, scroll observers, SVG, springs — any framework | Vanilla JS (works everywhere) | `npm i animejs` or CDN for previews |
| **Motion** | [motion.dev](https://motion.dev) | Declarative React animations, layout transitions, gestures | React | `npm i motion` |
| **GSAP** | [gsap.com](https://gsap.com) | Complex scroll (ScrollTrigger), SVG, commercial-grade timelines | Any | `npm i gsap` (free tier covers most) |

### When to pick which

| You need… | Start here |
|---|---|
| Scroll-linked stagger on vanilla HTML preview | Anime.js |
| React page transitions, layout animations | Motion |
| Complex scroll-pinned storytelling | GSAP ScrollTrigger |
| Something React Bits already ships | **Don't** reach for an engine — copy the component |

## CSS-only sources (no React, no JS)

Best for: simple hover effects, keyframe animations, loaders, toggles.

| Site | URL | Best for | Integration |
|---|---|---|---|
| **UI Verse** | [uiverse.io](https://uiverse.io) | Buttons, loaders, cards, toggles — pure CSS/HTML | Copy HTML + CSS |
| **Animista** | [animista.net](https://animista.net) | CSS keyframe generator | Export keyframes, paste into CSS |

## Comparison: Anime.js vs React Bits

These solve **different problems** — not interchangeable.

| | Anime.js | React Bits |
|---|---|---|
| **Category** | Animation engine | Component collection |
| **You get** | APIs to animate anything | 130+ finished animated UI pieces |
| **Framework** | Any (vanilla JS) | React / Next.js only |
| **Effort** | Higher — compose animations yourself | Lower — pick component, tweak props |
| **License** | MIT | MIT + Commons Clause (free for commercial) |

**Rule of thumb:** React Bits first for React projects. Anime.js only when
you need custom behavior no component library covers.

## Similar sites (bookmark list)

All follow copy-paste / you-own-the-code model:

- [Hover.dev](https://hover.dev) — React animation components
- [Cult UI](https://cult-ui.com) — shadcn-style animated components
- [Luxe UI](https://luxeui.com) — premium-feel React components
- [21st.dev](https://21st.dev) — community component registry (shadcn-compatible)
- [Tailwind UI](https://tailwindui.com) — paid, production-grade (use if project has license)

## Local snippets

See [`snippets/`](snippets/) for plain HTML/CSS/JS reference implementations
that mirror common patterns from the sites above. Use these when:

- Building a spec preview (`previews/*.html`) without React
- Adapting a pattern into a React component
- You need a working starting point faster than browsing external sites
