---
description: Build the site and smoke-test every route on localhost
---

Verify the site end-to-end:

```
npm run build
grep -ri "uncategorized\|xocoupon" dist/ | head
for p in / /deals /coupons /about /contact /privacy /search /rss.xml /sitemap-index.xml; do
  curl -s -o /dev/null -w "$p %{http_code}\n" "http://localhost:4321$p"
done
ls dist/category/ && ls dist/posts/ | head
```

All routes must return 200 (sitemap needs `npm run preview` if the dev server is
running, since dev doesn't serve it). Report pass/fail per line; stop and show
the error if the build fails.
