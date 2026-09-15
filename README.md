# 💎 Shopping Gems

The best shopping blog for people who hate paying full price — sale calendars,
coupons, gift guides, and hand-picked deals. Built with **Astro 5** + **Tailwind CSS v4**,
fully static, SEO-first, and managed with **Claude Code**.

## Quickstart

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/ (+ sitemap)
npm run preview  # serve the production build
```

## What's inside

- **6 long-form guides** — AliExpress/Amazon sale calendars, coupon-stacking
  playbooks, gift picks, travel + marketing comparisons (400–700 words each,
  tables, FAQs, internal links)
- **Full blog system** — homepage hero, article pages with sticky sidebar
  (search, trending deals, latest posts, categories, tags, newsletter),
  category/tag archives, `/sales` + `/deals` hubs, about/contact/privacy,
  client-side `/search`, `/rss.xml`
- **SEO baked in** — unique titles + meta descriptions, canonicals, OG/Twitter
  cards, `BlogPosting` + `BreadcrumbList` + `AboutPage`/`ContactPage` JSON-LD,
  sitemap, RSS, AA-safe contrast, `scope="col"` on table headers
- **Editorial design** — serif headlines, flat brand red (`#d92632`), custom SVG
  icon set, zero emoji/gradient slop

## Content workflow

Posts live in `src/content/posts/<slug>.md`:

```yaml
title: "Primary Keyword … Compelling Tail"
description: "≤160 chars, keyword near front"
pubDate: 2026-07-20
category: "Online Shopping"   # new value = new archive page, auto-routed
tags: ["sale", "amazon"]       # new value = new tag page, auto-routed
image: "/images/<slug>/hero.jpg"
imageAlt: "Descriptive alt text"
views: 0
featured: false                # true = homepage hero (keep ≤3)
```

Images go in `public/images/<slug>/`. See `CLAUDE.md` for the full content
model, design rules, and SEO standards.

## Manage it with Claude Code

| Command | What it does |
|---|---|
| `/new-post <topic>` | Research → outline → images → publish a complete SEO post |
| `/content-plan [n]` | Dated idea calendar with keywords + search intent |
| `/topic-cluster <pillar>` | Pillar + spokes map with internal-link plan |
| `/seo-audit` | Content/health audit with file:line evidence |
| `/site-check` | Build + smoke-test every route |

Agents (`seo-blog-writer`, `content-planner`) and the `seo-blog-writing` skill
live in `.claude/`.

## Tech

Astro 5 (content collections) · Tailwind CSS v4 · MDX · `@astrojs/sitemap` ·
`@astrojs/rss` · rehype `scope` plugin · no database, no server — deploys
anywhere static.
