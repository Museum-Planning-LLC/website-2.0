# Legacy URL redirects (no Cloudflare)

GitHub Pages **cannot send HTTP 301**. This repo uses two mechanisms instead:

## 1. Stub pages (primary — SEO recovery)

Each legacy WordPress path has a real file, e.g.:

- `museum-feasibility-studies/index.html` → canonical `museum-feasibility-study.html`
- `museum-consulting-and-cultural-planning-museum-planning-llc/index.html` → Services

Stubs return **HTTP 200** with `rel=canonical` and an instant refresh. Google treats that much better than **404 + JavaScript** in `404.html`.

**Regenerate after editing the map:**

```bash
python3 tools/gen_legacy_redirect_stubs.py
```

Source of truth: [`legacy-redirects.json`](legacy-redirects.json)

## 2. `wp-content/uploads` symlink

Old WordPress image URLs use `/wp-content/uploads/...`. The repo symlinks:

`wp-content/uploads` → `content/uploads`

Same files, old paths — no redirect needed for media.

## 3. `404.html` (fallback only)

Long-tail WordPress paths (portfolio pagination, tags, unknown slugs) still use JS redirect in `404.html`. Keep `legacy-redirects.json` and `404.html` in sync when adding ranked URLs.

---

## Rank-critical paths (former #1 queries)

| Legacy URL | Stub target |
|------------|-------------|
| `/museum-feasibility-studies` | `/museum-feasibility-study.html` |
| `/museum-consulting-and-cultural-planning-museum-planning-llc` | `/museum-planning-services.html` |
| `/museum-master-planning` | `/museum-school/what-is-a-museum-master-plan.html` |
| `/starting-a-museum` | `/museum-school/how-to-start-a-museum.html` |

After deploy, verify:

```bash
curl -sI "https://museumplanning.com/museum-feasibility-studies/" | head -3
# expect HTTP/2 200 (not 404)

curl -s "https://museumplanning.com/museum-feasibility-studies/" | grep canonical
# expect museum-feasibility-study.html
```

Then in **Google Search Console**: URL Inspection → Request indexing on the **target** pages.

---

## If you ever want true HTTP 301 (optional)

Without Cloudflare, the usual option is **Netlify** or **Vercel** with a `_redirects` / `vercel.json` file — same static site, GoDaddy DNS points to them instead of GitHub Pages. Not required if stubs are deployed.
