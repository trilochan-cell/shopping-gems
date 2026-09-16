# Coupon Upload Guide — send us brands in spreadsheets

Two files, two jobs (or two sheets with the same columns — open in
Excel/Sheets, save as CSV UTF-8):

| File | Purpose | When |
|---|---|---|
| `brand-upload-template.csv` | One row per **brand**: profile + FAQ | Once per brand, before its coupons |
| `coupon-upload-template.csv` | One row per **offer**: coupons/deals | Anytime (brand must already exist) |

Share the filled file(s) back. We run `scripts/import-coupons.py`, which
validates every cell with row-numbered errors, generates the pages, builds,
verifies, and pushes — then sends you the live `/coupons/<brand>/` URLs.

## File 1 — brands: `brand-upload-template.csv`

| Column | Required | Rules |
|---|---|---|
| `brand_slug` | yes | Lowercase letters/numbers/hyphens, e.g. `ionbottles`. Becomes the URL `/coupons/<slug>/`. |
| `brand_name` | yes | Display name. |
| `brand_tagline` | yes | One line, e.g. `Molecular hydrogen water bottles`. |
| `brand_description` | yes | 2–3 sentences: what they sell, bestsellers, shipping/returns highlights. |
| `brand_website` | yes | Full `https://` merchant homepage (fallback link). |
| `brand_affiliate_url` | no | Tracked affiliate link, if you have one at brand time (coupons file can set it later). |
| `brand_logo` | no | Path like `/images/brands/acme.svg` (send the file too). Blank = letter tile. |
| `brand_category` | no | Defaults to `Shopping`. |
| `brand_rating` / `brand_reviews` | no | Real sources only (Trustpilot, Google). Blank hides stars — never invented. |
| `brand_max_discount` | yes | Headline stat, e.g. `30%`. Must match your best offer. |
| `brand_faq_q1`…`q5` / `brand_faq_a1`…`a5` | no | Up to 5 Q&As, plain text, 40–60 words per answer. Empty pairs skipped. |

## File 2 — coupons: `coupon-upload-template.csv` (offers only)

| Column | Required | Rules |
|---|---|---|
| `brand_slug` | yes | Must already exist (upload the brand first). |
| `brand_affiliate_url` | yes | The **one locked affiliate URL for the brand** — identical on every row. The importer rejects the file if rows disagree, and refuses to overwrite a different URL already on file. No per-offer links: this value cannot be changed per coupon. |
| `coupon_slug` | no | Auto-made from the title if blank. Must be unique. |
| `coupon_title` | yes | e.g. `20% Off Sitewide`. |
| `coupon_description` | yes | 1–2 sentences: scope, minimums, key limits. |
| `coupon_type` | yes | `code` (shopper types something) or `deal` (automatic). |
| `coupon_badge` | yes | Left box: `20% OFF`, `Free Shipping`, `$10 OFF`, `Free Gift`. |
| `coupon_code` | if `code` | Exact merchant-published code. **Never invented.** |
| `coupon_expiry` | no | `YYYY-MM-DD`. Blank = ongoing (no fake deadline); past dates auto-move to Expired. |
| `coupon_verified` | no | `YYYY-MM-DD` you confirmed it. Shown on the card — keep honest. |
| `coupon_uses` | no | Real counts only; blank hides the counter. |
| `coupon_terms` | no | Items separated with ` \| `, e.g. `Excludes gift cards \| One per order`. |
| `coupon_labels` | no | Separated with ` \| `, e.g. `Sitewide \| Verified`. |
| `coupon_featured` | no | `yes` pins to top (max 1–2 per brand). |

## Example coupon rows (fictional)

```
brand_slug,brand_affiliate_url,coupon_title,coupon_description,coupon_type,coupon_badge,coupon_code,coupon_expiry,coupon_verified,coupon_terms,coupon_labels,coupon_featured
acme-tea,https://aff.example.net/acme,25% Off Your First Order,New customers save 25% on their first tea order.,code,25% OFF,WELCOME25,2026-12-31,2026-09-16,First orders only | Excludes gift cards,First Order | Verified,yes
acme-tea,https://aff.example.net/acme,Free Shipping Over $40,Every $40+ tea order ships free.,deal,Free Shipping,,,2026-09-16,,Orders $40+ | Test store only,Free Shipping,
```

Note the same affiliate URL on both rows — that is enforced, not coincidence.

## Trust rules (non-negotiable)

1. Real merchant data only — no invented codes, discounts, ratings, or dates.
2. One locked affiliate URL per brand; per-offer overrides do not exist.
3. `coupon_verified` = the day you actually checked it.
4. No expiry? Leave it blank — the page shows "Ongoing".
5. Send logos as separate files (square SVG/PNG); put the path in `brand_logo`.
