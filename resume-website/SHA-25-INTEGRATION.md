# SHA-25 Integration Guide

## Status
The `rohrasharad-ship-it/resume-website` GitHub repo was not accessible from this cloud agent token. Implementation lives in this `resume-website/` folder as a buildable reference.

## Merge into production resume-website

1. Copy these files into the real repo:
   - `src/components/build-transparency/` (all files)
   - `src/lib/build-stats.ts`
   - `openspec/specs/build-transparency/spec.md`
   - `openspec/changes/sha-25-build-transparency/`
   - Update `openspec/project.md` capability index (add `build-transparency` row)

2. In `app/page.tsx` (or layout), after Contact section:
   ```tsx
   import { BuildTransparency } from "@/components/build-transparency/BuildTransparency";
   // ...
   <BuildTransparency />
   ```

3. Ensure voice-agent FAB z-index stays above the sheet (150+).

## Spec summary (finalized)
- **Placement:** inline at document bottom; hidden until user scrolls to end
- **Focus:** circular auto-improve loop diagram with Linear, Cursor, GitHub, Vercel, OpenSpec logos
- **Interaction:** tap trigger → dark sheet with diagram, stats, capability list
