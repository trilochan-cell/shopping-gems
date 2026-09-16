# Coupon Upload Guide — send us brands in a spreadsheet

Fill **`coupon-upload-template.csv`** (one row = one offer, repeat the brand
columns on every row of that brand) and share the file back. We run it through
`scripts/import-coupons.py`, which validates every cell and generates the brand
page + offer cards. Open the CSV in Excel/Sheets; save as CSV UTF-8.

## Brand columns (repeat per row)

| Column | Required | Rules & tips |
|---|---|---|
| `brand_slug` | yes | Lowercase, letters/numbers/hyphens, e.g. `ionbottles`. One brand = one slug, used in the page URL `/coupons/<slug>/`. |
| `brand_name` | yes | Display name, e.g. `IonBottles`. |
| `brand_tagline` | yes | One line, e.g. `Molecular hydrogen water bottles`. |
| `brand_description` | yes | 2–3 sentences: what they sell, bestsellers, shipping/returns highlights. |
| `brand_website` | yes | Full URL with `https://`. The merchant homepage (fallback link). |
| `brand_affiliate_url` | no | Your tracked affiliate link for this brand (Impact, AvantLink, etc.). Used for **every** Go to Store / Get Deal / Show Code button when set; falls back to `brand_website`. |
| `brand_logo` | no | Path like `/images/brands/acme.svg` (send the file too) or an `https://` image URL. Leave blank for an automatic letter tile. |
| `brand_category` | no | Defaults to `Shopping`. |
| `brand_rating` / `brand_reviews` | no | **Only from a real source** (Trustpilot, Google). Leave blank if unknown — stars are hidden rather than invented. |
| `brand_max_discount` | yes | Headline stat, e.g. `30%`. Must match your best listed offer. |
| `brand_faq_q1`…`q5` + `brand_faq_a1`…`a5` | no | Up to 5 Q&As (how to use codes, stacking, expiry, returns). Plain text, no links, 40–60 words per answer. Fill as many pairs as you can; empty pairs are skipped. |

## Offer columns (one row each)

| Column | Required | Rules & tips |
|---|---|---|
| `coupon_slug` | no | Auto-made from the title if blank. Must be unique. |
| `coupon_title` | yes | e.g. `20% Off Sitewide`. |
| `coupon_description` | yes | 1–2 sentences: what it applies to, minimums, key limits. |
| `coupon_type` | yes | `code` (shopper types something) or `deal` (automatic price/drop). |
| `coupon_badge` | yes | Left box text: `20% OFF`, `Free Shipping`, `$10 OFF`, `Free Gift`. |
| `coupon_code` | if `code` | The exact code, e.g. `SAVE20`. **Only codes published by the merchant.** Never invent one. |
| `coupon_affiliate_url` | no | Per-offer tracked link (overrides the brand link for this card only). Falls back to `brand_affiliate_url`, then `brand_website`. |
| `coupon_expiry` | no | `YYYY-MM-DD`. Blank = ongoing offer (no fake deadline). Past dates auto-move to Expired on rebuild. |
| `coupon_verified` | no | `YYYY-MM-DD` you last confirmed it works. Shown on the card — keep honest. |
| `coupon_uses` | no | Shopper count from real data only; blank hides the counter. |
| `coupon_terms` | no | Separate items with ` \| `, e.g. `Excludes gift cards \| One per order`. |
| `coupon_labels` | no | Separate with ` \| `, e.g. `Sitewide \| Verified`. |
| `coupon_featured` | no | `yes` pins it to the top (max 1–2 per brand). |

## Example row (fictional)

```
brand_slug,brand_name,brand_tagline,brand_description,brand_website,brand_logo,brand_category,brand_rating,brand_reviews,brand_max_discount,brand_faq_q1,brand_faq_a1,coupon_slug,coupon_title,coupon_description,coupon_type,coupon_badge,coupon_code,coupon_expiry,coupon_verified,coupon_uses,coupon_terms,coupon_labels,coupon_featured
acme-tea,Acme Tea,Small-batch loose-leaf tea,Acme Tea sells single-origin loose-leaf teas and brewing kits with free shipping over $40.,https://example.com/acme,,Food & Drink,,,,25%,How do I use an Acme Tea code?,Add tea to your cart and paste the code in the discount box at checkout before paying.,,,,,,,,,acme-tea-25-off,25% Off Your First Order,New customers save 25% on their first tea order.,code,25% OFF,WELCOME25,,2026-12-31,2026-09-16,,First orders only | Excludes gift cards,First Order | Verified,yes
```

## Rules that keep pages trustworthy

1. Real merchant data only — no invented codes, discounts, ratings, or dates.
2. One promo code per `code` row; automatic prices are `deal` rows (no code).
3. `coupon_verified` = the day you actually checked it.
4. No expiry? Leave it blank — the page shows "Ongoing" instead of a fake deadline.
5. Send brand logos as separate files (square SVG/PNG preferred) and put the path in `brand_logo`.

## What happens after you share the file

We validate it (bad slugs, dates, missing codes, duplicates all get flagged by
row number), generate the pages, build the site, verify schema + links, and push
— then send you the live `/coupons/<brand>/` URLs to review.
