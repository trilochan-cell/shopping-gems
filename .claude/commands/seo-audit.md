---
description: Audit Shopping Gems SEO + content health and report issues with file locations
---

Audit this site's SEO and content health. Check and report each with evidence
(`file:line` or command output):

1. `npm run build` — 0 errors; note page count.
2. Every post: description ≤160 chars with keyword near front; exactly one `h1`
   (template) and no skipped levels in body; ≥3 internal links, all resolving
   (`curl` each target, expect 200); every image has non-empty alt; 5-item
   `faq:` frontmatter present; `updatedDate` set; body + FAQ answers ≥2500 words
   (count: strip frontmatter, split on whitespace).
3. Templates: canonical + OG + Twitter + JSON-LD present in rendered HTML of
   `/`, one post, one category page (`BlogPosting` must include author,
   publisher+logo, dateModified, section, keywords, wordCount; `FAQPage` with
   ≥5 questions on posts); `/rss.xml` lists all posts; sitemap exists
   in `dist/`.
4. Design-system violations: emojis in `src/**/*.astro`, decorative gradients
   outside hero legibility fades, off-palette colors (only `stormy-teal`,
   `pearl-aqua`, `alice-blue`, `almond-silk`, `tangerine-dream`, slate/neutral
   scales plus legacy `brand`/`ink` aliases may appear).
5. Dead ends: `grep -ri "lorem\|TODO\|FIXME\|\[FILL" src/` (the About-page
   `[FILL: target audience]` is a known placeholder — flag if still there).
6. Thin content: any post under 2500 words (body + FAQ answers).

Output a table: severity (high/med/low) · issue · location · fix. Fix highs only
after I confirm.
