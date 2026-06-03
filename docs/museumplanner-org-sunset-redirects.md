# museumplanner.org → museumplanning.com (sunset redirects)

**Context:** [`DOMAINS-AND-OBJECTIVES-STRATEGY.md`](./DOMAINS-AND-OBJECTIVES-STRATEGY.md) — Museum Planner brand, Museum School targets, vs `/museum-planner/` landing.

**Status (live check 2026-06-03):** **Done** — apex + **www** return **301** to Museum School (`server: cloudflare`). Verified with `bash tools/verify-museumplanner-redirects.sh` after GitHub unpublish + Cloudflare Bulk Redirects (20 rows). If apex `curl` fails locally while `dig` works, flush macOS DNS: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`. Optional: test catch-all URLs (`/old-blog-slug/`); if **530**, revisit `museumplanner.org/*` rows in Cloudflare.

**Policy:** museumplanning.com is the single consulting domain. museumplanner.org educational content moves to **Museum School** (Tier 3). Do not create competing Tier 1 URLs for exhibition design.

---

## Root forward vs path-by-path (recommendation)

| Approach | Pros | Cons |
|----------|------|------|
| **Root only** (`/` → one URL) | Fast to ship | Deep links (exhibition parts, starting-a-museum) stay **404** unless catch-all exists |
| **Path-by-path only** | Best SEO for known URLs | Unknown blog slugs still **404** |
| **Hybrid (recommended)** | Known paths → exact Museum School targets; catch-all for everything else | Slightly more Cloudflare rows |

**Use hybrid:**

1. Import path rules from [`../redirects/museumplanner-org-cloudflare-redirects.csv`](../redirects/museumplanner-org-cloudflare-redirects.csv).
2. Keep the final row `museumplanner.org/*` → Museum School index (catch-all for old blog posts).
3. Point **museumplanner.org** DNS to **Cloudflare** (proxied orange cloud) on the account that hosts museumplanning.com **or** add museumplanner.org as its own zone.
4. **Unpublish** the old GitHub Pages site for museumplanner.org **before** redirects will work reliably (see below).

**Default targets (aligned to strategy doc):**

| Traffic type | Redirect to |
|--------------|-------------|
| Homepage `/` | `https://museumplanning.com/museum-school/index.html` |
| Exhibition design series | Matching `museum-school/museum-exhibition-design/*` |
| Starting a museum | `museum-school/how-to-start-a-museum.html` |
| Everything else (`/*`) | `museum-school/index.html` |

**Optional revenue-focused variant:** Change only the **root** rows to `https://museumplanning.com/museum-strategic-planning.html` if GSC shows .org homepage traffic is hire-intent, not education. Keep path-by-path exhibition rules on Museum School.

---

## Cloudflare setup (museumplanner.org zone)

### DNS records — fix these (common blocker)

Orange cloud alone is not enough if **content still points at GitHub**:

| Record | Wrong (sends traffic to GitHub) | Right (redirect-only sunset) |
|--------|----------------------------------|------------------------------|
| **www** CNAME | `museum-planning-llc.github.io` | **CNAME** `museumplanner.org` (same zone), **Proxied** — Bulk Redirect list also has explicit `www.museumplanner.org/...` rows |
| **@** A | `3.33.251.168`, `15.197.225.128` (GitHub Pages apex IPs) | **One** A → `192.0.2.1`, **Proxied** (placeholder; origin never used once Bulk Redirects run) |
| **@** AAAA | `2606:50c0:8000::…` (GitHub IPv6) | **Delete** the four AAAA rows unless you need IPv6; use apex A `192.0.2.1` only |
| **_dmarc** TXT | DNS only (grey) | Leave as-is |

### GitHub Pages — unpublish (easy to miss)

Cloudflare Bulk Redirects only help if the domain is not still **owned by a live GitHub Pages site**. While Pages is published with `museumplanner.org` / `www` on the custom domain, browsers and curl often still see **`server: GitHub.com`** and **404** — not your **301** list.

In the repo that hosted the old site (e.g. **museum-planning-llc**):

1. **Settings → Pages**
2. **Remove** custom domains `museumplanner.org` and `www.museumplanner.org` (if still listed).
3. **Unpublish** the site: set **Source** to **None** / disable Pages, or delete the `gh-pages` branch / workflow that deploys it — until the site is no longer “Your site is live at …”.

You do **not** need to delete the repo; only stop serving HTTPS for that hostname from GitHub.

Do this **in addition to** Cloudflare DNS (no CNAME to `*.github.io`) and the 20-row Bulk Redirect import.

**Bulk Redirect list** includes both `museumplanner.org/...` and `www.museumplanner.org/...` (20 rows in CSV). Do not add bare hosts without trailing slash (Cloudflare `duplicate_item_value`).

1. Add **museumplanner.org** (and **www**) to Cloudflare if not already a zone.
2. Update DNS at registrar to Cloudflare nameservers; apply the table above. Remove GitHub Pages custom domain for museumplanner.org.
3. **Bulk Redirects** → create list `museumplanner-org-sunset` → **Import** [`museumplanner-org-cloudflare-redirects.csv`](../redirects/museumplanner-org-cloudflare-redirects.csv) (no header row; same format as [`cloudflare-bulk-redirects.csv`](../redirects/cloudflare-bulk-redirects.csv)).
   - **One source URL per row** — do not import both `museumplanner.org/foo` and `museumplanner.org/foo/` (Cloudflare error: `duplicate_item_value` at position 1).
   - CSV uses **trailing-slash** paths only; each host’s catch-all (`museumplanner.org/*`, then `www.museumplanner.org/*`) is **last** for that host — **20 rows** total after import.
4. **Bulk Redirect Rule** → attach list → deploy on **museumplanner.org** hostname (not museumplanning.com).
5. Verify:

```bash
curl -sI "https://museumplanner.org/" | grep -iE "^HTTP|location"
curl -sI "https://museumplanner.org/museum-exhibition-design-part-i/" | grep -iE "^HTTP|location"
curl -sI "https://museumplanner.org/some-old-blog-slug/" | grep -iE "^HTTP|location"
curl -sI "https://www.museumplanner.org/museum-exhibition-design-part-i/" | grep -iE "^HTTP|location"
```

Expect **301** and `location: https://museumplanning.com/...`.

**If you still see GitHub 404 after import:** responses should show `server: cloudflare` and a `cf-ray` header when the zone is proxied and the Bulk Redirect Rule is deployed. No `cf-ray` + `server: GitHub.com` means traffic is reaching GitHub as origin without edge redirects — fix in order:

1. **DNS (museumplanner.org zone)** — `@` and `www` records must be **Proxied** (orange cloud), not DNS-only (grey).
2. **Bulk Redirect Rule** — list **museumplanner** attached → **Save and Deploy** (not draft).
3. **GitHub Pages** — remove custom domains **and unpublish** (Source → None); see **GitHub Pages — unpublish** above.
4. Re-run the `curl` checks below.

**Free plan:** If import hits the item cap, import exhibition + starting-a-museum rows first, then root, then add catch-all `/*` last.

## Exhibition Design series (live on museumplanning.com)

| Legacy URL (museumplanner.org) | New URL (museumplanning.com) |
|--------------------------------|------------------------------|
| `/museum-exhibition-design-2/` | `/museum-school/museum-exhibition-design/` |
| `/museum-exhibition-design-part-i/` | `/museum-school/museum-exhibition-design/exhibition-design-part-i.html` |
| `/museum-exhibition-design-part-ii/` | `/museum-school/museum-exhibition-design/exhibition-design-part-ii.html` |
| `/museum-exhibition-design-part-iii/` | `/museum-school/museum-exhibition-design/exhibition-design-part-iii.html` |
| `/museum-exhibition-design-part-4/` | `/museum-school/museum-exhibition-design/exhibition-design-part-iv.html` |
| `/museum-exhibition-design-v/` | `/museum-school/museum-exhibition-design/exhibition-design-part-v.html` |
| `/frequently-asked-museum-questions/` (FAQ hub) | `/museum-school/museum-exhibition-design/` (interim; migrate FAQ content separately if needed) |

## Still to migrate (backlog)

| Content | Suggested destination |
|---------|----------------------|
| Starting a museum (10 steps) | Already covered by `museum-school/how-to-start-a-museum.html` — redirect legacy `/starting-a-museum/` there |
| Starting a science center | New Tier 3 page or section on `how-to-start-a-museum.html`; fix museumplanning.com `/starting-a-science-center` → that page (not Museum School index) |
| Remaining blog posts / FAQ | Museum School or retire with 301 to closest guide |

## Rebuild exhibition series pages

Source of truth for HTML body: `museum-planner-2.0/exhibition-design/`. Regenerate on museumplanning.com:

```bash
python3 tools/build_exhibition_design_series.py
```

## Close checklist

1. All high-traffic museumplanner.org URLs have 301 targets on museumplanning.com.
2. Google Search Console: change-of-address or URL removal for museumplanner.org after 301s live.
3. Bing Webmaster Tools: same.
4. Remove `museumplanner.org` links from museumplanning.com footers once sunset is complete (optional — or point to Museum School index).
5. Confirm museumplanner.org GitHub Pages / WordPress is decommissioned so nothing serves duplicate content.
