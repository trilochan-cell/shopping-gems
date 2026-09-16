#!/usr/bin/env python3
"""Import brand coupon pages from a filled copy of coupon-upload-template.csv.

Usage:
  python3 scripts/import-coupons.py data.csv              # validate + write files
  python3 scripts/import-coupons.py data.csv --dry-run    # validate only
  python3 scripts/import-coupons.py data.csv --overwrite  # replace existing slugs

One CSV row = one offer. Repeat the brand_* columns on every row of that brand.
See coupon-upload-guide.md for the column rules.
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANDS = ROOT / 'src/content/brands'
COUPONS = ROOT / 'src/content/coupons'

REQUIRED_BRAND = ['brand_slug', 'brand_name', 'brand_tagline', 'brand_description',
                  'brand_website', 'brand_max_discount']
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
TRUTHY = {'yes', 'true', '1', 'y'}


def yq(value: str) -> str:
    """YAML-quote a single-line scalar when needed."""
    value = re.sub(r'\s+', ' ', value).strip()
    if value == '' or re.search(r'[:#\[\]{},&*!|>\'"%@`]|^-|^\?|:$', value) or value != value.strip():
        return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return value


def fail(msg: str) -> None:
    print(f'ERROR: {msg}')
    sys.exit(1)


def parse_date(raw: str, where: str) -> str | None:
    raw = raw.strip()
    if not raw:
        return None
    if not DATE_RE.match(raw):
        fail(f'{where}: date "{raw}" must be YYYY-MM-DD')
    try:
        date.fromisoformat(raw)
    except ValueError:
        fail(f'{where}: date "{raw}" is not a real calendar date')
    return raw


def main() -> None:
    if len(sys.argv) < 2:
        fail('usage: python3 scripts/import-coupons.py <file.csv> [--dry-run] [--overwrite]')
    path, dry, overwrite = sys.argv[1], '--dry-run' in sys.argv, '--overwrite' in sys.argv
    rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    if not rows:
        fail('CSV has no data rows (fill the template, one row per offer)')
    missing = [c for c in REQUIRED_BRAND + ['coupon_title', 'coupon_description',
               'coupon_type', 'coupon_badge'] if c not in (rows[0] or {})]
    if missing:
        fail(f'missing columns: {", ".join(missing)}')

    brands: dict[str, dict] = {}
    coupons: list[dict] = []
    for i, r in enumerate(rows, start=2):
        if None in r:
            fail(f'row {i}: has more cells than header columns — quote any field containing commas')
        r = {k: (v or '').strip() for k, v in r.items()}
        where = f'row {i}'
        for col in REQUIRED_BRAND + ['coupon_title', 'coupon_description', 'coupon_type', 'coupon_badge']:
            if not r.get(col):
                fail(f'{where}: required field "{col}" is empty')
        slug = r['brand_slug']
        if not SLUG_RE.match(slug):
            fail(f'{where}: brand_slug "{slug}" must be lowercase letters/numbers/hyphens')
        if not r['brand_website'].startswith(('http://', 'https://')):
            fail(f'{where}: brand_website must start with http(s)://')
        for urlcol in ('brand_affiliate_url', 'coupon_affiliate_url'):
            if r.get(urlcol, '') and not r[urlcol].startswith(('http://', 'https://')):
                fail(f'{where}: {urlcol} must start with http(s)://')
        ctype = r['coupon_type'].lower()
        if ctype not in ('code', 'deal'):
            fail(f'{where}: coupon_type must be "code" or "deal"')
        code = r.get('coupon_code', '')
        if ctype == 'code' and not code:
            fail(f'{where}: coupon_code is required when coupon_type is "code"')
        expiry = parse_date(r.get('coupon_expiry', ''), where)
        verified = parse_date(r.get('coupon_verified', ''), where)
        uses = r.get('coupon_uses', '')
        if uses and not uses.isdigit():
            fail(f'{where}: coupon_uses must be a whole number')
        rating = r.get('brand_rating', '')
        if rating:
            try:
                assert 0 <= float(rating) <= 5
            except (ValueError, AssertionError):
                fail(f'{where}: brand_rating must be 0–5')
        if r.get('brand_reviews', '') and not r['brand_reviews'].isdigit():
            fail(f'{where}: brand_reviews must be a whole number')

        if slug in brands and brands[slug]['name'] != r['brand_name']:
            fail(f'{where}: brand_slug "{slug}" already used for "{brands[slug]["name"]}"')
        faqs = [(r.get(f'brand_faq_q{n}', ''), r.get(f'brand_faq_a{n}', ''))
                for n in range(1, 6)]
        faqs = [(q, a) for q, a in faqs if q and a]
        brands.setdefault(slug, {
            'name': r['brand_name'], 'tagline': r['brand_tagline'],
            'description': r['brand_description'], 'website': r['brand_website'],
            'affiliate': r.get('brand_affiliate_url', ''),
            'logo': r.get('brand_logo', ''), 'category': r.get('brand_category', 'Shopping') or 'Shopping',
            'rating': rating, 'reviews': r.get('brand_reviews', ''), 'max': r['brand_max_discount'],
            'faqs': faqs,
        })
        cslug = r.get('coupon_slug', '') or slug + '-' + re.sub(r'[^a-z0-9]+', '-', r['coupon_title'].lower()).strip('-')
        if not SLUG_RE.match(cslug):
            fail(f'{where}: coupon_slug "{cslug}" must be lowercase letters/numbers/hyphens')
        coupons.append({**r, '_slug': cslug, '_type': ctype, '_expiry': expiry,
                        '_verified': verified, '_where': where})

    # Collision check against existing files
    for slug in brands:
        if (BRANDS / f'{slug}.md').exists() and not overwrite:
            print(f'NOTE: brand "{slug}" exists — profile kept, only new coupons added')
    seen = set()
    for c in coupons:
        if c['_slug'] in seen:
            fail(f'{c["_where"]}: duplicate coupon_slug "{c["_slug"]}" in this CSV')
        seen.add(c['_slug'])
        if (COUPONS / f'{c["_slug"]}.md').exists() and not overwrite:
            fail(f'{c["_where"]}: {c["_slug"]}.md exists (use --overwrite to replace)')

    # Write
    for slug, b in brands.items():
        lines = ['---', f'name: {yq(b["name"])}', f'tagline: {yq(b["tagline"])}',
                 f'description: {yq(b["description"])}', f'website: {yq(b["website"])}']
        if b['affiliate']:
            lines.append(f'affiliate_url: {yq(b["affiliate"])}')
        if b['logo']:
            lines.append(f'logo: {yq(b["logo"])}')
        lines += [f'category: {yq(b["category"])}']
        if b['rating']:
            lines.append(f'rating: {b["rating"]}')
        if b['reviews']:
            lines.append(f'reviews: {b["reviews"]}')
        lines.append(f'maxDiscount: {yq(b["max"])}')
        if b['faqs']:
            lines.append('faq:')
            for q, a in b['faqs']:
                lines += [f'  - question: {yq(q)}', f'    answer: {yq(a)}']
        lines += ['---', '']
        dest = BRANDS / f'{slug}.md'
        if not dry and (overwrite or not dest.exists()):
            dest.write_text('\n'.join(lines))
        print(f'{"[dry] " if dry else ""}brand   {dest.name} ({len(b["faqs"])} FAQs)')

    for c in coupons:
        terms = [t.strip() for t in c.get('coupon_terms', '').split('|') if t.strip()]
        labels = [t.strip() for t in c.get('coupon_labels', '').split('|') if t.strip()]
        lines = ['---', f'brand: {yq(c["brand_slug"])}', f'title: {yq(c["coupon_title"])}',
                 f'description: {yq(c["coupon_description"])}', f'type: {c["_type"]}',
                 f'badge: {yq(c["coupon_badge"])}']
        if c['_type'] == 'code':
            lines.append(f'code: {yq(c["coupon_code"])}')
        if c.get('coupon_affiliate_url', ''):
            lines.append(f'affiliate_url: {yq(c["coupon_affiliate_url"])}')
        if c['_expiry']:
            lines.append(f'expiry: {c["_expiry"]}')
        if c['_verified']:
            lines.append(f'verified: {c["_verified"]}')
        if c.get('coupon_uses', ''):
            lines.append(f'uses: {c["coupon_uses"]}')
        if terms:
            lines.append('terms:')
            lines += [f'  - {yq(t)}' for t in terms]
        if labels:
            lines.append('labels:')
            lines += [f'  - {yq(t)}' for t in labels]
        if c.get('coupon_featured', '').lower() in TRUTHY:
            lines.append('featured: true')
        lines += ['---', '']
        dest = COUPONS / f'{c["_slug"]}.md'
        if not dry:
            dest.write_text('\n'.join(lines))
        print(f'{"[dry] " if dry else ""}coupon  {dest.name} [{c["_type"]}]')

    print(f'\nDone: {len(brands)} brand(s), {len(coupons)} coupon(s). Next: npm run build')


if __name__ == '__main__':
    main()
