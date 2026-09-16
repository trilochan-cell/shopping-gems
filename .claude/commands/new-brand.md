---
description: Scaffold a new brand coupon page (profile + starter offers) on Shopping Gems
argument-hint: <brand name + website>
---

Scaffold a coupon page for: **$ARGUMENTS**

1. Ask me for (or confirm from the argument): brand name, website URL, tagline,
   category, logo file (or generate a flat placeholder SVG in
   `public/images/brands/`), 2–4 REAL verified offers (title, code-or-deal,
   discount, expiry, terms). **Never invent codes, discounts, or "verified"
   claims** — if I can't provide real ones, create the page with the offers I
   give and mark the rest TODO explicitly. For REAL brands: fetch the actual
   logo (merchant `/cdn/shop/files/*logo*`, `og:image`, or press kit — save to
   `public/images/brands/`, never hotlink), use only on-site-verifiable offers
   (no `rating`/`reviews`/`uses` unless from a real source — omit them rather
   than invent), deals without end dates get no `expiry` (rendered "Ongoing").
2. Write `src/content/brands/<slug>.md` (schema in `src/content.config.ts`) and
   one file per offer in `src/content/coupons/<slug>-*.md`. Keep the fictional
   seed brands untouched.
3. Add 3–4 brand FAQs (how to use codes, stacking, expiry, returns).
4. `npm run build` — confirm `/coupons/<slug>/` renders; `curl` it (200) and
   check the `ItemList` schema block exists.
5. Report: URL, offers added, schema status, and what data is still TODO.
