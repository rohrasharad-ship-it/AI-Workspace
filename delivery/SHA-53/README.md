# SHA-53 delivery — OG meta tags for AI-landscape

This branch contains the SHA-53 implementation ready to apply to `rohrasharad-ship-it/AI-landscape`.

**Blocked:** Cloud agent token cannot access the private AI-landscape repo.

## Apply to AI-landscape

1. In `index.html` `<head>`, after the viewport meta tag, add the OG/Twitter tags from `index.html.patch-source` lines 6-20.
2. Ensure `preview.png` (1200×630) is at the site root and deployed — the meta tags reference `https://ai-landscape-ten.vercel.app/preview.png`. See `social-sharing-spec.md` for image requirements.
3. Add `openspec/specs/social-sharing/spec.md` from `social-sharing-spec.md`.
4. Add `social-sharing` to `openspec/project.md` capabilities index.

Branch to push: `cursor/sha-53-og-meta-tags-e41b`
