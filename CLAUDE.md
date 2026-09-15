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
category: "Online Shopping | Gift Guides | Travel | Marketing"  # new value = new archive page, auto-routed
tags: ["sale", "amazon"]          # new value = new tag page, auto-routed
image: "/images/<slug>/hero.jpg"  # hero + OG image + card thumbnail
imageAlt: "Descriptive alt text"
views: 0                          # seed plausible number for new posts
featured: false                   # true = homepage hero (keep ≤3 featured)
```

Body conventions: lead paragraph first · `##` sections with keyword headings ·
one comparison/table section where it fits (gets card styling + `scope` free) ·
numbered how-to · "Mistakes to avoid" where useful · `###`-style FAQ with 3–4
short Q&As (featured-snippet bait) · **≥3 internal links** to real posts/pages
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
Twitter cards · JSON-LD (`BlogPosting`+`BreadcrumbList` on posts, `AboutPage`/
`ContactPage` on those pages, `WebSite` globally — use BaseLayout's `slot="head"`)
· single `h1`, no skipped heading levels · descriptive alts · sitemap + RSS ·
internal links on every post · FAQ block on guides.

## Gotchas

- `/search` is **fully static**: filtering is client-side JS over an embedded post
  index (`search.astro`). No server code will ever run there.
- `/sitemap-index.xml` exists only after `npm run build` (local file or preview).
- Dev server serves the latest file saves automatically (HMR); hard-refresh the
  browser (Cmd+Shift+R) when styles look stale.
- Never invent slugs/URLs — verify against `src/content/posts/` and `src/pages/`.

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
- Agents: `seo-blog-writer` (writes a post end-to-end) · `content-planner`
  (calendars and clusters, then proposes work)
