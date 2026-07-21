# SHA-25 Integration Guide

## Status: NOT merged to production (July 2026)

| Check | Result |
|---|---|
| [meet-sharad.vercel.app](https://meet-sharad.vercel.app/) | No "How this site was built" button |
| [AI-Workspace PR #16](https://github.com/rohrasharad-ship-it/AI-Workspace/pull/16) | **Closed without merge** |
| `rohrasharad-ship-it/resume-website` from cloud agent | **Inaccessible** — Cursor GitHub app only has `AI-Workspace` selected |

The implementation is complete in this folder (`AI-Workspace/resume-website/`). It was never applied to the private production repo.

## Placement (finalized spec)

- **Not** a fixed bottom-right chip/tab (voice agent owns bottom-right FAB)
- Inline at **document bottom**, after Contact
- Hidden until user scrolls to the end (`IntersectionObserver`)
- Tap **"How this site was built"** → dark sheet with auto-improve loop diagram

## Quick apply (local machine with resume-website clone)

```bash
git clone https://github.com/rohrasharad-ship-it/resume-website.git
cd resume-website
git checkout -b cursor/sha-25-build-transparency-9a2d

bash ../AI-Workspace/resume-website/scripts/integrate-build-transparency.sh \
  ../AI-Workspace/resume-website \
  .

# Edit src/app/page.tsx — add <BuildTransparency /> after Contact
# Update openspec/project.md capability index

npm run build
git add -A && git commit -m "feat(SHA-25): build transparency panel at page bottom"
git push -u origin cursor/sha-25-build-transparency-9a2d
```

## Files to copy

- `src/components/build-transparency/` (all files)
- `src/lib/build-stats.ts`
- `openspec/specs/build-transparency/spec.md`
- `openspec/changes/sha-25-build-transparency/`
- Update `openspec/project.md` capability index

## page.tsx integration

```tsx
import { BuildTransparency } from "@/components/build-transparency/BuildTransparency";

// After Contact section, before closing </main>:
<BuildTransparency />
```

## Unblock cloud agents

GitHub → Settings → Applications → Cursor → Repository access → add `resume-website`.
