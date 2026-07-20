# Capability: Social Sharing

## Purpose
Ensure shared links to the map show a rich preview (title, description, and map
image) on LinkedIn, Slack, X, and other platforms that read Open Graph or
Twitter Card metadata.

## What Exists Today
- `index.html` includes `meta name="description"`, Open Graph tags, and Twitter
  Card tags in the document `<head>`.
- `preview.png` (1200×630) is the social preview image: dark background with the
  radial map graphic (colored node clusters and connection lines), title text,
  and catalog stats so recipients can see what the link leads to before clicking.
- Tags point at the live production URL and absolute image path on Vercel.

## Metadata
| Tag | Value |
|---|---|
| Title | AI Landscape 2026 — Interactive AI Ecosystem Map |
| Description | 156 tools, 310 connections, 6 layers from chip foundries to end-user apps. Explore how the AI stack connects. |
| Image | `/preview.png` (served as absolute URL in meta tags) |

## Constraints
- Use absolute URLs for `og:image` and `og:url` so crawlers resolve them correctly.
- Keep `preview.png` at 1200×630 (standard OG aspect ratio) and visually
  representative of the radial map — not a blank or text-only card.
- Do not add a build step or server-side rendering; metadata lives in static HTML.
