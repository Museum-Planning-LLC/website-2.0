# Legacy URL redirects

GitHub Pages **cannot send HTTP 301**. This repo uses **Cloudflare Bulk Redirects** (preferred) plus GitHub stubs as fallback:

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
| `/museum-master-planning` | `/museum-master-planning.html` |
| `/museum-strategic-planning` | `/museum-strategic-planning.html` |
| `/museum-strategic-planning-consultants` | `/museum-strategic-planning.html` |
| `/immersive-interactive-museum-transformation` | `/immersive-museum-planning.html` |
| `/starting-a-museum` | `/museum-school/how-to-start-a-museum.html` |

After Cloudflare import, verify **301** (trailing slash — WordPress default):

```bash
curl -sI "https://museumplanning.com/museum-feasibility-studies/" | grep -iE "^HTTP|location"
curl -sI "https://museumplanning.com/museum-master-planning/" | grep -iE "^HTTP|location"
curl -sI "https://museumplanning.com/museum-strategic-planning-consultants/" | grep -iE "^HTTP|location"
curl -sI "https://museumplanning.com/immersive-interactive-museum-transformation/" | grep -iE "^HTTP|location"
```

Without Cloudflare, stubs return **200** + canonical (still OK for SEO, weaker than 301).

Then in **Google Search Console**: URL Inspection → Request indexing on the **target** pages.

---

## If you ever want true HTTP 301 (optional)

Without Cloudflare, the usual option is **Netlify** or **Vercel** with a `_redirects` / `vercel.json` file — same static site, GoDaddy DNS points to them instead of GitHub Pages. Not required if stubs are deployed.

### Cloudflare Bulk Redirects (CSV import)

Generate or refresh the import file:

```bash
python3 tools/gen_cloudflare_bulk_redirects.py
```

Files:

- `redirects/cloudflare-bulk-redirects.csv` — full list, **no header row**
- `redirects/cloudflare-bulk-redirects-priority.csv` — rank-critical rows only (Free plan cap fallback)
- Source map: `redirects/legacy-redirects.json` (do not override in `EXTRA_EXACT` except `/museum-school`)

**CSV column format:** source = `museumplanning.com/path` (no `https://`); target = full `https://museumplanning.com/...` URL.

**Prefix paths** (e.g. `/author/`, `/category/`) emit exact `…/author/` plus wildcard `…/author/*` rows. **Wildcards often do not match on Bulk Redirect Lists** — use **Rules → Redirect Rules** (static 301 + `starts_with(http.request.uri.path, "/author/")`) for all author subpaths, or add **exact** sources (e.g. `museumplanning.com/author/alvaro/`) the same way as `about.html`.

**Import in Cloudflare:**

1. **Bulk Redirects** → **Create Bulk Redirect List** → name it e.g. `wordpress-legacy`
2. **Import** → upload `cloudflare-bulk-redirects.csv`
3. Review imported rows → **Continue to Redirect Rules**
4. **Create Bulk Redirect Rule** → attach the list → **Deploy**

**Important:** `@` and `www` DNS records must be **Proxied** (orange cloud) or redirect rules never run.

Verify:

```bash
curl -sI "https://museumplanning.com/museum-feasibility-studies/" | grep -iE "^HTTP|location|cf-ray"
```

Expect `301` and `location: …museum-feasibility-study.html`.

**Free plan note:** Cloudflare Free may cap how many bulk redirect items you can import. If import fails, import only the rank-critical rows (feasibility, consultants, master planning, strategic planning, wp-content) from the top of the CSV.
