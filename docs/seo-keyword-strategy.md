# SEO keyword strategy — Museum Planning LLC

Single source of truth for **which phrases we target** and **which pages own them**. Update when positioning changes or after reviewing Search Console query data (quarterly is enough for most sites).

**Primary domain:** https://museumplanning.com  
**Implementation companion:** [`STYLE-GUIDE.md`](../STYLE-GUIDE.md) (page tiers, SEO head standard, voice) · [`redirects/README.md`](../redirects/README.md) (Cloudflare 301s + stubs)

---

## Tier 1 — money keywords (one URL per phrase)

These five phrases drive $100K-class engagements. Each has a **single primary URL**. Do not create competing pages or duplicate intent.

| # | Keyword / phrase | Primary URL | Sitemap priority |
|---|------------------|-------------|------------------|
| 1 | **Museum planning** | [`index.html`](../index.html) (`/`) | `1.0` |
| 2 | **Museum planning services** / **museum consultants** | [`museum-planning-services.html`](../museum-planning-services.html) | `0.9` |
| 3 | **Museum feasibility study** | [`museum-feasibility-study.html`](../museum-feasibility-study.html) | `0.85` |
| 4 | **Museum strategic planning** | [`museum-strategic-planning.html`](../museum-strategic-planning.html) | `0.85` |
| 5 | **Museum master planning** | [`museum-master-planning.html`](../museum-master-planning.html) | `0.85` |

**Notes**

- **Services hub** (`museum-planning-services.html`) owns *museum planning services* by URL and `ItemList` schema; title/H1 lead **museum consultants** (same hire-intent cluster). Both phrases are intentional.
- **Homepage** owns *museum planning* in title, OG, and `WebPage` schema; H1 is brand (“We Build Museums”) — acceptable for home.
- Treat **museum consultant** / **museum consultants** as the same cluster as the services page.
- Do **not** target **“museum”** alone — only inside longer queries.

### Tier 1 on-page checklist (each pillar page)

- [ ] Primary keyword in `<title>` (first), `| Museum Planning LLC` suffix
- [ ] Keyword in H1 (natural, not stuffed)
- [ ] ~155-char meta description, **we** voice, fee signal where appropriate
- [ ] Canonical with `.html`
- [ ] Open Graph + Twitter Card
- [ ] JSON-LD: `WebPage`, `Service`, `FAQPage` (visible FAQs must match), `BreadcrumbList`
- [ ] Intent strip linking sibling Tier 1 pages
- [ ] Legacy path in `redirects/legacy-redirects.json` + Cloudflare CSV if WordPress URL existed
- [ ] URL in `sitemap.xml`; request GSC indexing after deploy

**Status (2026-06-02):** Pillars 3–5 fully optimized. Homepage and services hub optimized with intentional brand/consultant emphasis (see notes above).

---

## Tier 2 — audience / vertical guides

Sitemap priority **`0.45`**. Link **up** to Tier 1; do not keyword-stuff or duplicate Tier 1 copy.

| Page | Audience / topic |
|------|------------------|
| [`for-cities.html`](../for-cities.html) | Municipal / civic museum feasibility |
| [`for-cities-science-center.html`](../for-cities-science-center.html) | City science & technology centers |
| [`for-universities.html`](../for-universities.html) | University museums & collections |
| [`local-history-museum.html`](../local-history-museum.html) | Local / community history museums |
| [`immersive-museum-planning.html`](../immersive-museum-planning.html) | Immersive & interactive exhibition design |

---

## Tier 3 — Museum School (vocabulary, not commercial owners)

Sitemap priority **lower than Tier 1** (informational). Answers “what is…?” before hire. Always link **up** to the matching Tier 1 commercial page.

| Museum School page | Links up to |
|--------------------|-------------|
| `museum-school/what-is-a-museum-feasibility-study.html` | `museum-feasibility-study.html` |
| `museum-school/what-is-a-museum-master-plan.html` | `museum-master-planning.html` |
| `museum-school/how-to-start-a-museum.html` | `museum-planning-services.html`, contact |

**Do not** treat Museum School URLs as primary owners for feasibility, strategic, or master planning commercial queries.

---

## Supporting pages (proof & brand)

| Role | URLs |
|------|------|
| Project proof | `museum-planning-projects.html`, `projects/*.html` |
| Brand / person | `museum-planning-about.html` (Mark Walhimer) |
| Conversion | `museum-planning-contact.html` |
| Thought leadership | `convergence-era.html`, `museum-vitality-index.html` |
| Capabilities PDF-style | `Museum_Planning_LLC_Capabilities.html` |

---

## Legacy URL routing (Cloudflare + stubs)

GitHub Pages cannot send HTTP 301. **Cloudflare Bulk Redirects** (preferred) plus GitHub stub pages (fallback).

**Regenerate after editing the map:**

```bash
python3 tools/gen_legacy_redirect_stubs.py
python3 tools/gen_cloudflare_bulk_redirects.py
```

Source of truth: [`redirects/legacy-redirects.json`](../redirects/legacy-redirects.json)

### Rank-critical legacy paths

| Legacy URL | 301 target |
|------------|------------|
| `/museum-feasibility-studies/` | `museum-feasibility-study.html` |
| `/museum-master-planning/` | `museum-master-planning.html` |
| `/museum-strategic-planning/` | `museum-strategic-planning.html` |
| `/museum-strategic-planning-consultants/` | `museum-strategic-planning.html` |
| `/museum-consultants/` | `museum-planning-services.html` |
| `/museum-consulting-and-cultural-planning-museum-planning-llc/` | `museum-planning-services.html` |
| `/immersive-interactive-museum-transformation/` | `immersive-museum-planning.html` |

Verify after Cloudflare import:

```bash
curl -sI "https://museumplanning.com/museum-master-planning/" | grep -iE "^HTTP|location"
```

---

## Secondary & extended keywords (phase 2)

One primary URL per row where possible. Use body copy and internal links — not duplicate hubs.

| Keyword / phrase | Intent | Primary URL | Supporting URLs |
|------------------|--------|-------------|-----------------|
| Museum exhibition design | Commercial | `museum-planning-services.html` | Project case studies, capabilities |
| Interactive museum exhibits | Commercial + informational | `museum-planning-projects.html`, `projects/*.html` | Services, immersive guide |
| Immersive museum planning | Commercial | `immersive-museum-planning.html` | Services, science-center vertical |
| Starting a museum | Informational | `museum-school/how-to-start-a-museum.html` | Services, contact |
| Mark Walhimer | Brand / navigational | `museum-planning-about.html` | Home, contact |

### Extended topical list (essays & future content)

| Theme | Typical phrases | Likely home |
|-------|-----------------|-------------|
| Future of museums | future of museums, museum relevance | `convergence-era.html` |
| Technology & museums | AI and museums, digital transformation | `convergence-era.html`, immersive guide |
| Experience | museum visitor engagement | Projects, immersive guide |
| Institutional health | museum benchmarking | `museum-vitality-index.html` |

---

## Measurement & maintenance

1. **Google Search Console** — monthly: impressions/clicks by query and landing page; confirm Tier 1 URLs receive impressions for target phrases.
2. **After any new commercial page** — add to `sitemap.xml`, legacy redirects if needed, request indexing, resubmit sitemap.
3. **Quarterly** — update this doc from GSC query data; refresh [`docs/seo-competitor-keyword-matrix.csv`](seo-competitor-keyword-matrix.csv) for top 5–10 queries.
4. **`meta name="keywords"`** — not used.
5. **Sitemap regen** — `python3 _gen_site_map.py` refreshes `site-map.html` / `sitemap.xml`; does not replace this strategy file.

---

## Remaining optimization (post-migration checklist)

Technical and on-page work completed as of **2026-06-02**. What remains is mostly **monitoring and optional polish**:

| Item | Priority | Status |
|------|----------|--------|
| Cloudflare 301s for rank-critical legacy paths | High | Done — verify periodically |
| Tier 1 pillar pages (feasibility, strategic, master) | High | Done |
| GSC sitemap resubmit | High | User done |
| GSC URL Inspection on all Tier 1 URLs | High | Confirm each requested once |
| Organic rank recovery | Medium | Wait 2–8 weeks post-301; track in GSC |
| Homepage H1 exact match for “museum planning” | Low | Done — keyword in hero deck; brand H1 retained |
| Services title/H1 “museum planning services” | Low | Done |
| Demote Museum School sitemap priority below 0.85 | Low | Done — now `0.55` |
| `for-universities.html` Tier 2 SEO pass | Medium | Done — OG, schema, Tier 1 links |
| Off-site backlinks & citations | Ongoing | Directories, speaking, museumplanner.org cross-links |
| GSC query-driven content (1 article/quarter) | Ongoing | Use Search Console “Queries” tab |

---

## Competitor SERP matrix

**File:** [`docs/seo-competitor-keyword-matrix.csv`](seo-competitor-keyword-matrix.csv)

Import into Sheets; replace competitor slots with URLs from GSC + manual SERP checks for your geo. Re-verify before tactical bets — exhibit-heavy SERPs shift quickly.

Peer cohorts in matrix: Lord Cultural Resources, AEA Consulting, JRA/RWS Global, Design and Production, Atelier Brückner, Kossmann.dejong, Gensler Culture, kubik maltbie, Gallagher, Local Projects, Ideum, Quatrefoil.

---

## Revision log

| Date | Change |
|------|--------|
| 2026-02-03 | Primary + extended keyword lists; website hierarchy; Services ↔ Museum School links. |
| 2026-05-05 | Competitor matrix CSV cohorts; Lord + AEA rows. |
| 2026-06-02 | **Tier 1 realignment:** commercial pillars own feasibility/strategic/master (not Museum School); five money keywords mapped; Cloudflare redirect table; Tier 2/3 split; remaining optimization checklist. |
