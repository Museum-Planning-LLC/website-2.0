# Museum Planning LLC — Website (`website-2.0`)

Public marketing site for **[museumplanning.com](https://museumplanning.com/)**, hosted on **GitHub Pages** from this repository (`main` branch). **Cloudflare** sits in front of the domain for true HTTP **301** redirects from legacy WordPress URLs.

## What this repo is

- Static **HTML** site (no build step required for publish).
- Primary goals: **credibility**, **lead generation** (conversation → feasibility → broader engagements), and **SEO** for museum planning–related intent.
- **`STYLE-GUIDE.md`** is the source of truth for layout, nav, typography, voice, and SEO patterns on new pages.

## Documentation

| File | Purpose |
|------|---------|
| [STYLE-GUIDE.md](./STYLE-GUIDE.md) | Design system, global nav, footer, voice, SEO checklist |
| [style-guide.html](./style-guide.html) | Browser-readable version of the style guide |
| [SITE-STRATEGY.md](./SITE-STRATEGY.md) | Audience, funnel, keyword clusters (internal reference) |
| [docs/seo-keyword-strategy.md](./docs/seo-keyword-strategy.md) | Keyword tiers and landing-page backlog |
| [redirects/README.md](./redirects/README.md) | Legacy URL mapping, Cloudflare bulk redirect import |

## Page tiers (information architecture)

Each tier maps to **one primary URL** per keyword cluster. Cross-link between tiers; do not duplicate intent across thin pages.

### Tier 1 — Commercial pillars (priority 0.85 in sitemap)

| URL | Primary intent |
|-----|----------------|
| `index.html` | Museum consultants, firm credibility |
| `museum-planning-services.html` | Museum consultant / full methodology |
| `museum-feasibility-study.html` | Museum feasibility study |
| `museum-strategic-planning.html` | Museum strategic planning consultants |
| `museum-master-planning.html` | Museum master planning |

**Template reference:** copy structure from `museum-feasibility-study.html` (nav, hero, sections, FAQ, intent strip, contact form, JSON-LD).

### Tier 2 — Vertical / audience guides (priority 0.45)

| URL | Primary intent |
|-----|----------------|
| `for-cities.html` | Municipal / civic museum feasibility |
| `for-cities-science-center.html` | Science & technology centers for cities |
| `for-universities.html` | University museum planning |
| `local-history-museum.html` | Local history & community museums |
| `immersive-museum-planning.html` | Immersive / interactive exhibition design (science center, local history, natural history) |

Tier 2 pages **support** Tier 1 — they link up to feasibility, master planning, and services; they do not replace them.

### Tier 3 — Museum School (education, not primary conversion)

`museum-school/*.html` — vocabulary and process guides. Each School article should link up to the matching commercial page where one exists.

## SEO and redirects workflow

1. **New page** — follow [STYLE-GUIDE.md § SEO](./STYLE-GUIDE.md); add URL to `sitemap.xml`; add to site search `PAGES` on related pages.
2. **Legacy WordPress path** — add mapping in `redirects/legacy-redirects.json`, then run:
   ```bash
   python3 tools/gen_legacy_redirect_stubs.py
   python3 tools/gen_cloudflare_bulk_redirects.py
   ```
3. **Deploy** — push to `main`; GitHub Pages updates within minutes.
4. **Cloudflare** — re-import or edit bulk redirect rules if legacy paths changed ([redirects/README.md](./redirects/README.md)).
5. **Google Search Console** — request indexing on new/changed URLs; resubmit `sitemap.xml`.

## Local preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

## Deploy

Changes pushed to `main` update **GitHub Pages** for **museumplanning.com**.

## Related repos

This repository is **Museum Planning LLC** web presence — not personal/artwork sites. Commercial positioning and production copy for the firm belong here.
