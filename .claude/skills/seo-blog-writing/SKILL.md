---
name: seo-blog-writing
description: Research, outline, illustrate, and publish an SEO-friendly Shopping Gems blog post — keyword targeting, internal links, local images, FAQ, build verification. Use for any new post.
---

# SEO Blog Writing (Shopping Gems)

End-to-end workflow for one post. Follow every step; never skip verification.

## 0. Input

Topic or keyword from the user. If vague, propose 3 concrete angles (keyword +
intent + why it fits the site's categories) and ask which to write.

## 1. Research (brief, evidence-based)

- `Glob src/content/posts/*.md` + `Read` the 2–3 closest posts: avoid keyword
  cannibalization; note exact slugs for internal links.
- If the topic needs fresh facts (sale dates, prices, specs), `WebSearch` once or
  twice. Record only verifiable facts — never invent dates, prices, or URLs.
- Pick ONE primary keyword + 2–3 secondaries. Keyword goes in title (front or
  near-front), first paragraph, one `##`, slug-adjacent filename, image alts.

## 2. Outline (get the shape right before writing)

- `##` sections that mirror search intent (dates → what to expect → how-to →
  mistakes → FAQ). One comparison/table section wherever two+ options exist.
- 5 FAQ questions in frontmatter `faq:` (40–60 word plain-text answers, no
  links — they render the FAQ block AND the `FAQPage` schema automatically).
- ≥3 internal links mapped to REAL targets: `Glob`/`Grep` slugs first. Prefer
  hub pages (`/sales`, `/deals`), same-category posts, and one category archive.

## 3. Images (local-first)

- Directory: `public/images/<slug>/` (`hero.jpg` + optional `picks-1.jpg`…).
- Hero: landscape ~1600×900, <300 KB (resize/compress; `.jpg` photos, `.png`
  only for graphics). It becomes the OG image, article hero, and card thumbnail.
- Every image needs a descriptive `imageAlt` (keyword naturally, never stuffed).
- Source: original screenshots, retailer press kits, or royalty-free
  (Unsplash/Pexels) with genuine topical relevance. Remote hotlinking is a
  fallback, not the default.
- Reference as `/images/<slug>/hero.jpg` in frontmatter; in-body images as
  `![alt](/images/<slug>/picks-1.jpg)`.

## 4. Frontmatter (exact schema)

```yaml
title: "Primary Keyword … Compelling Tail (≤70 chars)"
description: "Primary keyword in first 120 chars. ≤160 chars total."
pubDate: YYYY-MM-DD              # today unless scheduled
category: "Online Shopping | Gift Guides | Travel | Marketing"  # existing preferred; new value auto-creates an archive
tags: ["keyword", "store-or-topic", "sale|deals"]                # lowercase, 2–4
image: "/images/<slug>/hero.jpg"
imageAlt: "Descriptive alt text with keyword"
views: 0
featured: false                  # true only for hero-worthy sale guides (≤3 site-wide)
updatedDate: YYYY-MM-DD          # = pubDate for new posts; bump on rewrites
faq:                             # 5 Q&As, plain text, no links (block + schema auto)
  - question: "…?"
    answer: "40–60 words."
```

## 5. Body template (**≥2500 words** body + FAQ answers)

1. Lead paragraph: hook + primary keyword in first 100 words.
2. `##` keyword sections; exactly one `table` where comparison fits.
3. Numbered how-to or tips (`1.`); short "Mistakes to avoid" list where useful.
4. NO faq in the body — it lives in frontmatter (auto-rendered + schema).
5. Closing line linking to `/deals`, `/sales`, or the category archive.
6. No emojis (content exception: ★ ratings only). No invented facts.

## 6. Write + build + verify

- `Write src/content/posts/<slug>.md` (kebab-case slug matching the keyword).
- `npm run build` — 0 errors; page count should grow by ~1 per new tag.
- Verify: `curl -s http://localhost:4321/posts/<slug>/ | grep -o "<title>[^<]*</title>"`;
  confirm hero `<img … alt="…">` non-empty; confirm internal links resolve
  (`curl -s -o /dev/null -w "%{http_code}"` each).
- `grep -ri "lorem\|TODO\|FIXME" src/content/posts/<slug>.md` must be empty.

## 7. Report

Reply with: title + URL, primary keyword, word count, internal links added,
images added, build result. One line on what to write next (cluster gap).
