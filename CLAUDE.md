# Shopping Gems — Claude Code Guide

Shopping blog (Astro 5, static) modeled on classic coupon blogs: sale calendars,
coupons, gift guides, deal picks. Runs on `http://localhost:4321`.

## Commands

| Task | Command |
|---|---|
| Dev server | `npm run dev` (port 4321, `--host`) |
| Production build | `npm run build` → `dist/` (28–30 pages + sitemap) |
| Serve production | `npm run preview` (port 4321) |
| Install deps | `npm install` |

Restart the dev server after changing `astro.config.mjs` or `src/content.config.ts`.

## Stack

Astro 5 (content collections + MDX) · Tailwind CSS v4 (`@tailwindcss/vite`, theme in
`src/styles/global.css`) · `@astrojs/sitemap` · `@astrojs/rss` (`/rss.xml`) ·
rehype plugin `src/plugins/rehype-table-scope.mjs` (adds `scope="col"` to `<th>`).

## Repo map

- `src/content/posts/*.md` — all blog posts (Markdown + frontmatter below)
- `src/content.config.ts` — `posts` collection schema
- `src/pages/` — `index.astro` (home) · `posts/[slug].astro` (article + sidebar) ·
  `category/[category].astro` · `tag/[tag].astro` · `sales.astro` · `deals.astro` ·
  `about/contact/privacy.astro` · `search.astro` · `rss.xml.js`
- `src/layouts/BaseLayout.astro` — head SEO, header/footer. Import global CSS in
  frontmatter (`import '../styles/global.css'`), never `@import` inside `<style>`.
- `src/components/` — `PostCard.astro` (listing card) · `Sidebar.astro` (search,
  promo, latest, categories, tags, newsletter) · `Icon.astro` (SVG icon set)
- `src/plugins/` — markdown rehype plugins
- `public/images/<post-slug>/` — local post images (hero + in-body)
- `public/robots.txt`, `public/favicon.svg`

## Content model (frontmatter)

```yaml
title: "Exact headline (becomes URL via slug = filename)"
description: "≤160 chars, keyword near front, no clickbait"   # meta + OG + cards
pubDate: 2026-07-20
updatedDate: 2026-09-15              # bump on every substantial rewrite (feeds dateModified)
category: "Online Shopping | Gift Guides | Travel | Marketing"  # new value = new archive page, auto-routed
tags: ["sale", "amazon"]          # new value = new tag page, auto-routed
image: "/images/<slug>/hero.jpg"  # hero + OG image + card thumbnail
imageAlt: "Descriptive alt text"
views: 0                          # seed plausible number for new posts
featured: false                   # true = homepage hero (keep ≤3 featured)
faq:                              # 5 Q&As → rendered FAQ block + FAQPage JSON-LD (plain text, no links)
  - question: "…?"
    answer: "40–60 words."
```

Body conventions: **≥2500 words** (body + FAQ answers) · lead paragraph first · `##` sections with keyword headings ·
one comparison/table section where it fits (gets card styling + `scope` free) ·
numbered how-to · "Mistakes to avoid" where useful · FAQ lives in frontmatter
(`faq:` — auto-rendered + schema), never duplicated in the body · **≥3 internal links** to real posts/pages
(slugs live in `src/content/posts/`, hubs at `/sales`, `/deals`, categories).

## Design system (non-negotiable)

- **No emojis in UI.** Use `<Icon name="..." />` (names: diamond, flame, gift,
  bolt, chart, calendar, chat, eye, mail, lock, tag, check, briefcase, search,
  store, pen). Star-ratings inside article *content* are the only exception.
- **Flat colors only.** Brand red `#d92632` (AA-safe), hover `#a50e1a`, neutrals +
  `bg-stone-50` sections. No decorative gradients — the black fade over hero
  images stays (text legibility).
- **Serif headlines.** `main h1/h2` and `.prose-sg h3` are Georgia via CSS; cards,
  meta, buttons stay sans (Inter).
- Reuse `PostCard` and `Sidebar` on every listing surface; keep the article
  template structure (breadcrumb → card → author box → prev/next → related).

## SEO standards (every page/post)

Unique `<title>` + meta description · canonical · robots `index,follow` · OG +
Twitter cards · JSON-LD (perfected `BlogPosting` — author, publisher+logo,
`dateModified`, section, keywords, wordCount — plus `BreadcrumbList` and
frontmatter-driven `FAQPage` on posts; `AboutPage`/`ContactPage` on those pages,
`WebSite` globally — use BaseLayout's `slot="head"`)
· single `h1`, no skipped heading levels · descriptive alts · sitemap + RSS ·
internal links on every post · FAQ block on guides.

## Gotchas

- `/search` is **fully static**: filtering is client-side JS over an embedded post
  index (`search.astro`). No server code will ever run there.
- `/sitemap-index.xml` exists only after `npm run build` (local file or preview).
- Dev server serves the latest file saves automatically (HMR); hard-refresh the
  browser (Cmd+Shift+R) when styles look stale.
- Never invent slugs/URLs — verify against `src/content/posts/` and `src/pages/`.

## Coupon section (brands + offers)

- `src/content/brands/<slug>.md` — brand profile: `name, tagline, description,
  website, category, rating (0–5), reviews, maxDiscount ("30%"), faq[]`.
  One file = one page at `/coupons/<slug>/` (auto-routed). Optional
  `logo: "/images/brands/<slug>.svg"` (square SVG/PNG) shown in the hero,
  directory, and similar-brand cards — otherwise a letter tile renders.
- Outbound links resolve per offer: coupon `affiliate_url` → brand
  `affiliate_url` → plain `website` (helpers in `[brand].astro`).
- `src/content/coupons/<brand>-<offer>.md` — one offer per file:
  `brand` (brand slug) · `title` · `description` · `type: code|deal` ·
  `badge: "20% OFF"` (left box) · `code` (required for `type: code`) ·
  `expiry: YYYY-MM-DD` (past dates auto-move to the Expired section at build) ·
  `verified, uses, terms[], labels[], featured`.
- Templates: `src/pages/coupons/index.astro` (brand directory) ·
  `src/pages/coupons/[brand].astro` (Valuecom-style: header, All/Codes/Deals
  tabs, reveal-code `<details>` + copy button, expired list, stats, how-to,
  FAQ + `ItemList/Offer` schema). Outbound store links use
  `rel="nofollow sponsored noopener"`.
- Clicking Show Code / Get Deal opens the store in a background tab and pops a
  modal with the code (copy button) or deal summary — see the `#coupon-modal`
  block in `src/pages/coupons/[brand].astro`. No-JS fallback: Get Deal links
  navigate directly; codes render via `<noscript>`.
- Seed brands/coupons are **fictional placeholders** — replace with real,
  verified merchant data (never invent "verified" codes for real businesses).
- **Bulk uploads:** share a filled `coupon-upload-template.csv` (rules in
  `coupon-upload-guide.md`); import with
  `python3 scripts/import-coupons.py file.csv --dry-run` then without the flag.
  The script validates every cell (row-numbered errors) and writes brand +
  coupon files — then build + verify as usual.
- Rebuild regularly: expiry filtering, "verified" dates, and sitemaps are
  build-time. Use `/new-brand` to scaffold a brand.

## Verify (after any change)

```
npm run build                                        # must be 0 errors
grep -ri "uncategorized\|xocoupon" dist/ | head      # must be empty
for p in / /sales /deals /about /contact /privacy /search /rss.xml; do
  curl -s -o /dev/null -w "$p %{http_code}\n" "http://localhost:4321$p"; done
```

## Claude Code extensions (this repo)

- Skill: `.claude/skills/seo-blog-writing/SKILL.md` — full research → outline →
  images → write → verify workflow. Use it for every new post.
- Commands: `/new-post` `/content-plan` `/topic-cluster` `/seo-audit` `/site-check`
  `/new-brand`
- Agents: `seo-blog-writer` (writes a post end-to-end) · `content-planner`
  (calendars and clusters, then proposes work)
