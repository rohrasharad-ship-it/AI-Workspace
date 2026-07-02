# Handover: Create Linear Issue — Vercel Preview Deployment Blocker

**For:** Any agent with Linear MCP access  
**From:** Cursor cloud agent (SHA-25 build session, July 2026)  
**Action:** Create this issue in the **PM OS** Linear project  
**Why this file exists:** Cloud agent sessions do not have Linear MCP connected. Sharad will forward this handover to an agent that does.

---

## Linear issue to create

Use **New Issue Conventions** from `AGENTS.md`:

| Field | Value |
|---|---|
| **Project** | PM OS |
| **Status** | Backlog |
| **Label** | `spec-needed` |
| **Assignee** | Sharad Rohra (never an agent) |
| **Priority** | High (suggested — blocks every PR review loop) |
| **Title** | `🚧 [Infra] Vercel preview URLs blocked by Deployment Protection — agents can't give Sharad a tappable preview` |

### Description (paste into Linear)

## Problem

During SHA-25 (Build Transparency panel), the builder agent could not provide a public Vercel preview URL Sharad could tap on his phone before merge. Every branch/PR preview URL redirected to Vercel login instead of serving the built site.

**Triggering incident:** [AI-Workspace PR #16](https://github.com/rohrasharad-ship-it/AI-Workspace/pull/16) (SHA-25). Sharad had to ask explicitly for a preview. Workaround was Netlify Drop (`remarkable-panda-60435c.netlify.app`, password `My-Drop-Site`).

---

## Root cause (confirmed)

**Vercel Deployment Protection (Vercel Authentication)** is enabled on preview deployments for the AI-Workspace Vercel project.

Evidence (reproducible with `curl -I`):

```bash
# Branch / PR preview URL → 302 redirect to Vercel SSO (NOT public)
curl -I "https://ai-workspace-git-cursor-sha-2-180d7d-rohrasharad-5924s-projects.vercel.app/"
# → location: https://vercel.com/sso-api?url=...

# Production custom domain → 200 (public)
curl -I "https://ai-workspace.vercel.app/"
# → HTTP/2 200
```

Anonymous users (including cloud agents, Playwright, and Sharad on his phone without a Vercel session) hit the SSO wall. Only users logged into Vercel with team access can view protected previews.

This is **not** a build failure, wrong URL format, or agent error polling too early. The deployment exists; access is gated.

Docs: [Vercel Deployment Protection](https://vercel.com/docs/deployment-protection) · [Vercel Authentication](https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication)

---

## What AGENTS.md assumes (and does not account for)

AGENTS.md treats Vercel preview URLs as **public, tappable, phone-reviewable** surfaces. It never mentions Deployment Protection or auth gates.

### Assumptions baked into the loop

| AGENTS.md rule | What it says | Reality when protection is on |
|---|---|---|
| Role 1 step 9 | Poll for "real public `*.vercel.app` URL" | URL exists but returns 302 → `/sso-api` for anonymous users |
| Role 1 step 9 | "not a Vercel dashboard/inspector link that requires login" | Branch preview URLs *do* require login — same failure mode |
| Role 1 step 10 | Visual Self-QA on "real deployed preview" | Playwright gets login page, not the app |
| Slack template | `Preview: [Vercel preview URL] ← tap this` | Sharad taps → Vercel login, not the feature |
| Rule 5 | "Vercel preview URL is the only review surface" | Review surface is inaccessible without Vercel account |
| Rule 14 | If no preview URL after ~2 min, post PR link — don't go silent | Correct fallback, but doesn't solve review |
| Visual Specs §5 | Spec previews on `preview/<issue-id>-vN` branches → `<deployment-url>/previews/...` | Same SSO block on branch deployment URLs |
| Project Index | AI-Workspace prod: `ai-workspace.vercel.app` (spec-preview sandbox) | Prod domain is public; **branch previews are not** |

### What AGENTS.md does get right

- Step 8: Move to In Review immediately — not gated on Vercel ✅
- Step 9 fallback: Don't go silent; post PR link if preview unavailable ✅
- Rule 14: Silence is the failure mode to avoid ✅

The process handles *missing* URLs gracefully but has **no playbook for URLs that exist but are auth-gated**.

---

## Compounding factors on SHA-25

These made the incident worse but are separate from the core Vercel auth issue:

1. **`resume-website` repo inaccessible** from cloud agent token (404). Implementation landed in `AI-Workspace/resume-website/` subdirectory instead — so even a working Vercel preview on `meet-sharad.vercel.app` wasn't in play.
2. **GitHub Pages fallback failed** — `gh-pages` branch pushed, but `gh api` returned 403 enabling Pages on the repo (integration lacks admin scope).
3. **Netlify Drop workaround** worked but requires password `My-Drop-Site` on first visit (anonymous deploy limitation).
4. **Surge.sh** blocked on interactive email/password login in non-interactive cloud agent.

---

## What was tried (SHA-25 session)

| Approach | Result |
|---|---|
| PR branch Vercel URL (`ai-workspace-git-cursor-sha-2-...vercel.app`) | 302 → Vercel SSO login |
| `preview/SHA-25-build` branch + static export at `/previews/SHA-25-build/` | Same SSO block |
| Static export committed to repo, linked from PR | Files in git; Vercel URL still gated |
| `gh-pages` branch push | Branch exists; Pages not enabled (403 on API) |
| Netlify anonymous deploy | ✅ Works — `https://remarkable-panda-60435c.netlify.app/` (password gate) |
| Surge.sh | ❌ Interactive login required |
| Cloudflare Pages / Wrangler | ❌ No `CLOUDFLARE_API_TOKEN` |

---

## Potential solutions (for brainstorm)

Sharad + agent should pick one or a tiered policy. Not prescriptive — these are options.

### A. Vercel config (simplest if acceptable security-wise)

**Disable or relax Deployment Protection** on preview deployments for projects agents use:

- Vercel dashboard → Project → Settings → Deployment Protection
- Set to allow public preview access, or use **Shareable Links** (query-string bypass for external reviewers)
- API: `PATCH /v10/projects/{id}` with `"ssoProtection": null` or scope to `preview` only

| Pros | Cons |
|---|---|
| Zero AGENTS.md change; matches current spec | Previews become public to anyone with URL |
| Sharad taps URL on phone — done | Security tradeoff for unreleased work |

**Best for:** AI-Workspace spec-preview sandbox, possibly Resume Website preview deploys.

### B. Update AGENTS.md with explicit preview-access policy

Document that Deployment Protection must be off (or Shareable Links enabled) for any project in the Project Index. Add a preflight check for agents:

```
curl -sI <preview-url> | grep -i location
# If location contains vercel.com/sso-api → preview is gated; escalate, don't claim success
```

| Pros | Cons |
|---|---|
| Prevents false "preview ready" claims | Doesn't fix infra by itself |
| Makes failure mode explicit | Requires Sharad to configure Vercel once |

### C. Fallback preview hosts (documented in AGENTS.md)

When Vercel preview is gated or unavailable, agents may deploy static export to an approved public host:

1. `STATIC_EXPORT=1 npm run build` (or `PREVIEW_BASE_PATH` for subpath hosts)
2. Deploy `out/` to Netlify Drop, GitHub Pages, or Cloudflare Pages
3. Post fallback URL in Slack + Linear with any access notes (e.g. Netlify Drop password)

| Pros | Cons |
|---|---|
| Works even with Vercel protection on | Extra step; ephemeral URLs (Netlify Drop expires in 60 min unless claimed) |
| Cloud agents can do it without Vercel dashboard access | Not the "one URL" simplicity AGENTS.md promises |

### D. GitHub Pages for AI-Workspace previews

Enable Pages on `gh-pages` branch (one-time Sharad action in repo Settings). Agents push static exports; public URL: `https://rohrasharad-ship-it.github.io/AI-Workspace/`.

| Pros | Cons |
|---|---|
| Stable, free, no auth | Requires Pages enable + `basePath: /AI-Workspace` in export |
| Good fit for spec-preview sandbox | Separate from Vercel prod domain |

### E. Fix cloud agent repo access

Ensure cloud agents can clone/push `rohrasharad-ship-it/resume-website` so Resume Website features get `meet-sharad.vercel.app` PR previews (if that project's protection is configured correctly).

| Pros | Cons |
|---|---|
| Features build in the right repo | Doesn't help if meet-sharad previews are also protected |
| Standard Vercel PR preview flow | Separate issue from AI-Workspace sandbox |

### F. Vercel Shareable Links

Keep protection on; generate shareable link per deployment for Sharad. Agent would need Vercel API token to automate.

| Pros | Cons |
|---|---|
| Security + external access | Requires API token as cloud agent secret |
| Official Vercel feature | Extra step per PR; not in AGENTS.md today |

---

## Recommended discussion questions for Sharad

1. Should **AI-Workspace** preview deployments be public (spec sandbox only), while **resume-website** stays protected?
2. Is a **Netlify Drop password** acceptable as fallback, or is that too much friction on mobile?
3. Should AGENTS.md **require a preflight `curl` check** before posting "Preview ready" to Slack?
4. Should we enable **GitHub Pages** on AI-Workspace as the canonical spec-preview host instead of Vercel branch deploys?
5. Should cloud agents get **`LINEAR_API_KEY`** + **`VERCEL_TOKEN`** secrets so they can create issues and manage preview access?

---

## Related artifacts

- SHA-25 PR: https://github.com/rohrasharad-ship-it/AI-Workspace/pull/16
- Working workaround preview: https://remarkable-panda-60435c.netlify.app/ (password: `My-Drop-Site`)
- `gh-pages` branch pushed (Pages not yet enabled): `rohrasharad-ship-it/AI-Workspace@gh-pages`
- AGENTS.md sections: Role 1 steps 9–10, Visual Specs §5, Rules 5 & 14, Project Index

---

## Instructions for receiving agent

1. Read `AGENTS.md` New Issue Conventions.
2. Create the issue above in **PM OS** with status Backlog, label `spec-needed`, assignee Sharad Rohra.
3. Paste the Description section (from "## Problem" through "## Recommended discussion questions").
4. Comment on SHA-25 (Resume Website project) linking this new PM OS issue: "Preview infra gap filed — [link]."
5. Optionally comment on AI-Workspace PR #16 with the new Linear issue link.
6. Do **not** implement any solution — this is `spec-needed` for brainstorm only.
