---
description: Audit Shopping Gems SEO + content health and report issues with file locations
---

Audit this site's SEO and content health. Check and report each with evidence
(`file:line` or command output):

1. `npm run build` — 0 errors; note page count.
2. Every post: description ≤160 chars with keyword near front; exactly one `h1`
   (template) and no skipped levels in body; ≥3 internal links, all resolving
   (`curl` each target, expect 200); every image has non-empty alt; FAQ present
   on guides.
3. Templates: canonical + OG + Twitter + JSON-LD present in rendered HTML of
   `/`, one post, one category page; `/rss.xml` lists all posts; sitemap exists
   in `dist/`.
4. Design-system violations: emojis in `src/**/*.astro`, decorative gradients
   outside hero legibility fades, `#e63946` remnants (must be `#d92632`).
5. Dead ends: `grep -ri "lorem\|TODO\|FIXME\|\[FILL" src/` (the About-page
   `[FILL: target audience]` is a known placeholder — flag if still there).
6. Thin content: any post under ~300 words.

Output a table: severity (high/med/low) · issue · location · fix. Fix highs only
after I confirm.
