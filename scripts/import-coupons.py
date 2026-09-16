#!/usr/bin/env python3
"""Bulk upload for the Shopping Gems coupon section.

Two files, two jobs (or two sheets with the same columns):
  brand-upload-template.csv   one row per brand: profile + FAQ (once per brand)
  coupon-upload-template.csv  one row per offer: coupons/deals (anytime)

Usage:
  python3 scripts/import-coupons.py file.csv [--dry-run] [--overwrite]
File type is auto-detected from the header row.
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANDS = ROOT / 'src/content/brands'
COUPONS = ROOT / 'src/content/coupons'

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


def check_url(raw: str, where: str, col: str) -> str:
    raw = raw.strip()
    if not raw.startswith(('http://', 'https://')):
        fail(f'{where}: {col} must start with http(s)://')
    return raw


def parse_date(raw: str, where: str, col: str) -> str | None:
    raw = raw.strip()
    if not raw:
        return None
    if not DATE_RE.match(raw):
        fail(f'{where}: {col} "{raw}" must be YYYY-MM-DD')
    try:
        date.fromisoformat(raw)
    except ValueError:
        fail(f'{where}: {col} "{raw}" is not a real calendar date')
    return raw


def read_rows(path: str) -> tuple[list[str], list[dict]]:
    try:
        rows = list(csv.DictReader(open(path, encoding='utf-8-sig')))
    except FileNotFoundError:
        fail(f'file not found: {path}')
    if not rows:
        fail('CSV has no data rows')
    header = rows[0].keys()
    return list(header), rows


def clean(rows: list[dict]) -> list[dict]:
    out = []
    for i, r in enumerate(rows, start=2):
        if None in r:
            fail(f'row {i}: has more cells than header columns — quote fields containing commas')
        out.append({k: (v or '').strip() for k, v in r.items()})
    return out


def split_list(raw: str) -> list[str]:
    return [t.strip() for t in raw.split('|') if t.strip()]


def import_brands(rows: list[dict], dry: bool, overwrite: bool) -> None:
    required = ['brand_slug', 'brand_name', 'brand_tagline', 'brand_description',
                'brand_website', 'brand_max_discount']
    seen = set()
    for i, r in enumerate(rows, start=2):
        where = f'row {i}'
        for col in required:
            if not r.get(col):
                fail(f'{where}: required field "{col}" is empty')
        slug = r['brand_slug']
        if not SLUG_RE.match(slug):
            fail(f'{where}: brand_slug "{slug}" must be lowercase letters/numbers/hyphens')
        if slug in seen:
            fail(f'{where}: duplicate brand_slug "{slug}" in this file')
        seen.add(slug)
        check_url(r['brand_website'], where, 'brand_website')
        if r.get('brand_affiliate_url'):
            check_url(r['brand_affiliate_url'], where, 'brand_affiliate_url')
        if r.get('brand_rating'):
            try:
                assert 0 <= float(r['brand_rating']) <= 5
            except (ValueError, AssertionError):
                fail(f'{where}: brand_rating must be 0–5 (real sources only — blank if unknown)')
        if r.get('brand_reviews') and not r['brand_reviews'].isdigit():
            fail(f'{where}: brand_reviews must be a whole number')
        dest = BRANDS / f'{slug}.md'
        if dest.exists() and not overwrite:
            fail(f'{where}: {dest.name} exists (use --overwrite to replace)')
        faqs = [(r.get(f'brand_faq_q{n}', ''), r.get(f'brand_faq_a{n}', ''))
                for n in range(1, 6)]
        faqs = [(q, a) for q, a in faqs if q and a]
        lines = ['---', f'name: {yq(r["brand_name"])}', f'tagline: {yq(r["brand_tagline"])}',
                 f'description: {yq(r["brand_description"])}', f'website: {yq(r["brand_website"])}']
        if r.get('brand_affiliate_url'):
            lines.append(f'affiliate_url: {yq(r["brand_affiliate_url"])}')
        if r.get('brand_logo'):
            lines.append(f'logo: {yq(r["brand_logo"])}')
        lines.append(f'category: {yq(r.get("brand_category") or "Shopping")}')
        if r.get('brand_rating'):
            lines.append(f'rating: {r["brand_rating"]}')
        if r.get('brand_reviews'):
            lines.append(f'reviews: {r["brand_reviews"]}')
        lines.append(f'maxDiscount: {yq(r["brand_max_discount"])}')
        if faqs:
            lines.append('faq:')
            for q, a in faqs:
                lines += [f'  - question: {yq(q)}', f'    answer: {yq(a)}']
        lines += ['---', '']
        if not dry:
            dest.write_text('\n'.join(lines))
        print(f'{"[dry] " if dry else ""}brand   {dest.name} ({len(faqs)} FAQs)')
    print(f'\nDone: {len(rows)} brand(s). Next: npm run build')


def import_coupons(rows: list[dict], dry: bool, overwrite: bool) -> None:
    required = ['brand_slug', 'brand_affiliate_url', 'coupon_title',
                'coupon_description', 'coupon_type', 'coupon_badge']
    aff_by_brand: dict[str, str] = {}
    coupons: list[dict] = []
    for i, r in enumerate(rows, start=2):
        where = f'row {i}'
        for col in required:
            if not r.get(col):
                fail(f'{where}: required field "{col}" is empty (brand_affiliate_url is locked: same value on every row)')
        slug = r['brand_slug']
        if not SLUG_RE.match(slug):
            fail(f'{where}: brand_slug "{slug}" must be lowercase letters/numbers/hyphens')
        if not (BRANDS / f'{slug}.md').exists():
            fail(f'{where}: brand "{slug}" does not exist yet — upload it via brand-upload-template.csv first')
        aff = check_url(r['brand_affiliate_url'], where, 'brand_affiliate_url')
        if slug in aff_by_brand and aff_by_brand[slug] != aff:
            fail(f'{where}: brand_affiliate_url differs from other rows for "{slug}" — one locked URL per brand')
        aff_by_brand[slug] = aff
        ctype = r['coupon_type'].lower()
        if ctype not in ('code', 'deal'):
            fail(f'{where}: coupon_type must be "code" or "deal"')
        if ctype == 'code' and not r.get('coupon_code', ''):
            fail(f'{where}: coupon_code is required when coupon_type is "code"')
        expiry = parse_date(r.get('coupon_expiry', ''), where, 'coupon_expiry')
        verified = parse_date(r.get('coupon_verified', ''), where, 'coupon_verified')
        if r.get('coupon_uses', '') and not r['coupon_uses'].isdigit():
            fail(f'{where}: coupon_uses must be a whole number')
        cslug = r.get('coupon_slug', '') or slug + '-' + re.sub(r'[^a-z0-9]+', '-', r['coupon_title'].lower()).strip('-')
        if not SLUG_RE.match(cslug):
            fail(f'{where}: coupon_slug "{cslug}" must be lowercase letters/numbers/hyphens')
        coupons.append({**r, '_slug': cslug, '_type': ctype,
                        '_expiry': expiry, '_verified': verified, '_where': where})

    seen = set()
    for c in coupons:
        if c['_slug'] in seen:
            fail(f'{c["_where"]}: duplicate coupon_slug "{c["_slug"]}" in this file')
        seen.add(c['_slug'])
        if (COUPONS / f'{c["_slug"]}.md').exists() and not overwrite:
            fail(f'{c["_where"]}: {c["_slug"]}.md exists (use --overwrite to replace)')

    # Sync the locked affiliate URL into each brand file
    for slug, aff in aff_by_brand.items():
        dest = BRANDS / f'{slug}.md'
        text = dest.read_text()
        m = re.search(r'^affiliate_url:.*$', text, re.M)
        if m:
            existing = m.group(0).split(':', 1)[1].strip().strip('"')
            if existing != aff:
                if not overwrite:
                    fail(f'brand "{slug}" already has a different affiliate_url — refusing to change it (use --overwrite to update)')
                text = text.replace(m.group(0), f'affiliate_url: {yq(aff)}')
        else:
            text = re.sub(r'^(website:.*)$', lambda mm: mm.group(1) + f'\naffiliate_url: {yq(aff)}', text, count=1, flags=re.M)
        if not dry:
            dest.write_text(text)
        print(f'{"[dry] " if dry else ""}brand   {slug}.md affiliate_url synced')

    for c in coupons:
        terms = split_list(c.get('coupon_terms', ''))
        labels = split_list(c.get('coupon_labels', ''))
        lines = ['---', f'brand: {yq(c["brand_slug"])}', f'title: {yq(c["coupon_title"])}',
                 f'description: {yq(c["coupon_description"])}', f'type: {c["_type"]}',
                 f'badge: {yq(c["coupon_badge"])}']
        if c['_type'] == 'code':
            lines.append(f'code: {yq(c["coupon_code"])}')
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
    print(f'\nDone: {len(aff_by_brand)} brand(s), {len(coupons)} coupon(s). Next: npm run build')


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1].startswith('-'):
        fail('usage: python3 scripts/import-coupons.py <brands|coupons csv> [--dry-run] [--overwrite]')
    header, rows = read_rows(sys.argv[1])
    dry, overwrite = '--dry-run' in sys.argv, '--overwrite' in sys.argv
    rows = clean(rows)
    if 'coupon_title' in header:
        import_coupons(rows, dry, overwrite)
    elif 'brand_name' in header:
        import_brands(rows, dry, overwrite)
    else:
        fail('cannot detect file type: header must contain coupon_title (offers) or brand_name (brands)')


if __name__ == '__main__':
    main()
