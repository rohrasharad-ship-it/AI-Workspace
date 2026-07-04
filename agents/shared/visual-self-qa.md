# Shared Module: Visual Self-QA (looking at the real, live result)

Referenced by: `agents/builder.md`, `agents/spec-drift.md`, `agents/bug-error.md`,
`agents/market-feature.md`

This is different from Visual Specs (`agents/shared/visual-specs.md`). Visual
Specs is a **mockup of a proposed idea** before anything is built. Visual
Self-QA is **looking at the real, live-deployed result** — either something
just built (builder) or the actual current state of the site (idea-generation
agents) — the way a human QA tester would: open the browser, look at it, judge
whether it's actually right.

**Why this exists:** DOM-level test assertions (`element exists`,
`toBeVisible()`, `href contains X`) do not catch actual visual defects.
Something can be technically "visible" per Playwright's definition while
overlapping another element, cut off, squished on mobile, or just ugly. An
agent must not rely on code-level checks alone to claim something looks
right — it has to actually look.

**Mandatory, not optional, for all of the following:**

| Role | What to screenshot | Viewport(s) |
|---|---|---|
| **Builder**, after build/tests pass, before opening PR | The specific area you changed on the real deployed preview | Desktop and mobile — both, always |
| **Spec-Drift** | The live area related to the gap you're filing — shows the actual current (missing/incomplete) state as evidence | Whichever shows the gap clearly, usually desktop |
| **Bug/Error** | The live area showing the actual bug | Whichever reproduces it; both if the bug is viewport-specific |
| **Market/Feature** | The homepage or one to two relevant existing areas, for context on where the proposed idea would fit | Desktop |

**Mechanism:**
1. Use Playwright (already available in resume-website) to navigate to the
   real URL — the PR's Vercel preview for the builder, production for the
   idea-generation agents — and capture a screenshot to a local file.
   - **If the page you land on is a Vercel/SSO login screen, not the actual
     site, stop and flag it** (see the preflight check in `agents/builder.md`)
     rather than screenshotting and attaching a login page as if it were real
     evidence.
2. **Actually view the screenshot** using your own vision, the same way you'd
   look at any image. Reason about it like a QA tester: does anything overlap,
   get cut off, look misaligned, break on this viewport? If something looks
   wrong, fix it (builder) or note it precisely in the issue (idea-generation)
   — don't just note that a screenshot was taken.
3. **Attach the screenshot to the Linear issue** so Sharad sees the same
   visual evidence you used, not just your verbal claim:
   - Call `prepare_attachment_upload` with the issue ID, filename, content
     type, and file size — this returns a signed `uploadRequest` and an `assetUrl`
   - PUT the raw file bytes to `uploadRequest.url` with the exact headers
     given, unmodified — this happens outside your context window, the image
     bytes never pass through your token stream
   - Call `create_attachment_from_upload` with the issue ID and `assetUrl` to
     link it to the issue
   - Reference the same `assetUrl` inline in your comment (e.g.
     `![screenshot](assetUrl)`) so it's visible directly in the conversation,
     not just buried in the issue's attachment list
4. **Never use a base64/inline-content upload path for this.** That routes
   the image through your own context and is genuinely expensive in tokens —
   the signed-upload flow above is not. If your tooling only offers a
   base64 fallback, flag it to Sharad rather than defaulting to it silently.

This is worth the token cost — Sharad has explicitly said so. Don't skip it
to save tokens; that defeats the purpose.
