# Build Transparency Panel

## Purpose
Opt-in panel at the very bottom of the page revealing that this portfolio auto-improves through a spec-first AI-agent loop — unfakeable proof of the "living product demo" claim.

## Placement
- Inline at document end, after Contact section
- **Not** visible on landing — only appears when user scrolls to the very bottom (IntersectionObserver on sentinel)
- **Not** a fixed viewport chip or footer-row element
- z-index below voice-agent FAB (panel sheet at z-150 max; voice stays 150+)

## Interaction
- Bottom row fades in when sentinel enters viewport
- Tap "How this site was built" → dark sheet slides up (mobile) / centered card (desktop ≥640px)
- Dismiss: backdrop tap, × button, or Escape

## Content — auto-improve loop focus
1. **Headline:** "This site auto-improves"
2. **Subcopy:** One sentence on the closed loop (cron agents → spec → build → preview → approve → live → repeat)
3. **Circular workflow diagram** with tool logos at nodes:
   - Linear (idea feeders, spec)
   - Cursor (agent builds)
   - GitHub (PR)
   - Vercel (preview)
   - OpenSpec (live / archive)
   - Return arrow: "live site → new gaps found → loop repeats"
4. **Stats row:** issues shipped, spec→preview time, capability count (from `src/lib/build-stats.ts`)
5. **Capability list:** mirrors `openspec/specs/` names
6. **Footnote:** real stats, not marketing copy

## Visual tone
- Diagram-first, not emoji-driven
- Brand logos where systems are referenced
- Dark sheet (#111) on cream site palette

## Out of scope
- Linking to full AGENTS.md
- Auto-open on visit
- Animated loop steps
