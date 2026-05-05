# SEO keyword strategy — Museum Planning LLC

Single source of truth for **which phrases we target** and **which pages own them**. Update when positioning changes or after reviewing Search Console query data (quarterly is enough for most sites).

**Primary domain:** https://museumplanning.com  

This document is the **strategy source of truth**. Page titles, meta descriptions, canonicals, and copy updates follow from the map below.

### Website hierarchy (how keywords route)

1. **`museum-planning-services.html`** — Primary commercial hub: *museum planning*, *museum consultant(s)*, *museum strategic planning*, *museum exhibition design*, *interactive museum exhibits* (in body copy), plus deep links to Museum School for *feasibility* and *master planning* explainers.
2. **`museum-planning-projects.html`** + **`projects/*.html`** — Proof and entity-rich pages; reinforce *interactive museum exhibits* and service filters (feasibility, master planning, etc.).
3. **`museum-school/*`** — Informational owners for *starting a museum*, *museum feasibility study*, *museum master planning*; linked from Services to clarify vocabulary before hiring.
4. **`museum-planning-about.html`** — Brand owner for *Mark Walhimer* and consultant credibility.
5. **`index.html`** — Site-wide positioning and navigational reinforcement for *museum planning* / *museum consultants*.

---

## Primary keyword list (commercial + brand core)

One **primary URL** per row avoids competing with yourself. Supporting pages reinforce the topic with internal links and proof (projects, Museum School, capabilities).

| Keyword / phrase | Intent | Primary URL | Supporting URLs |
|------------------|--------|-------------|-----------------|
| Museum planning | Commercial + informational | `museum-planning-services.html` | `index.html`, `museum-planning-projects.html`, `Museum_Planning_LLC_Capabilities.html` |
| Museum consultant(s) | Commercial | `museum-planning-services.html` | `museum-planning-about.html`, `museum-planning-contact.html`, `index.html` |
| Museum feasibility study | Informational + commercial | `museum-school/what-is-a-museum-feasibility-study.html` + `museum-planning-services.html` | `museum-planning-contact.html`, relevant `projects/*.html` |
| Museum master planning | Informational + commercial | `museum-school/what-is-a-museum-master-plan.html` + `museum-planning-services.html` | Capabilities, projects |
| Museum strategic planning | Commercial | `museum-planning-services.html` | About, capabilities |
| Museum exhibition design | Commercial | `museum-planning-services.html` | Project case studies, capabilities |
| Interactive museum exhibits | Commercial + informational | `museum-planning-projects.html` + relevant `projects/*.html` | Services (exhibitions / experience) |
| Starting a museum | Informational | `museum-school/how-to-start-a-museum.html` | `museum-school/index.html`, services, contact |
| Mark Walhimer | Brand / navigational | `museum-planning-about.html` | Home, contact, Museum School bylines |

**Notes**

- Treat **“museum consultants”** as the same cluster as **museum consultant**; use natural plural in body copy.
- Do **not** treat **“museum”** alone as a target phrase—use it only inside longer queries.

---

## Extended list (phase 2 — topical & niche)

Use these for **thought leadership**, **subsections on Services**, or **future articles**—not necessarily duplicate homepage/service hubs.

| Theme | Typical phrases | Likely home on site |
|-------|-----------------|---------------------|
| Future of museums | future of museums, museum relevance | Long-form (e.g. `convergence-era.html`) or a dedicated essay later |
| Technology & museums | AI and museums, digital transformation in museums | `convergence-era.html`, Services (light touch) |
| Experience | immersive museum experiences, museum visitor engagement | Projects + Services |
| Planning vocabulary | interpretive planning museum, museum capital campaign planning | Services + proof in projects (only if accurate to engagements) |
| Organizational change | museum change management, museum transformation | Services subsection + methodology if offered substantively |
| Institutional health | museum benchmarking, museum financial health | `museum-vitality-index.html`, capabilities |

---

## House rules

1. **`meta name="keywords"`** — Not used for ranking; optional at most. Prefer strong titles and descriptions per URL.
2. **Measurement** — Google Search Console: impressions and clicks by query and landing page; refine this doc from real data.
3. **Regeneration** — `_gen_site_map.py` refreshes `site-map.html` / `sitemap.xml`; it does **not** replace this strategy file.

---

## Competitor SERP matrix (working spreadsheet)

**File:** [`docs/seo-competitor-keyword-matrix.csv`](seo-competitor-keyword-matrix.csv)

Columns map **primary keyword → intent → your URL(s) → five illustrative competitor domains + page types → gap note**. Import into Google Sheets or Excel; replace competitor slots with **your geo’s top URLs** from Search Console (*Queries* + manual SERP check) or a rank-tracker. Rows labeled **US-default** used aggregated web-search snapshots **May 2026** — **re-verify before tactical bets.** Exhibit-heavy SERPs shift quickly; e.g. **Gallagher & Associates**, **Local Projects**, **Ideum**, **Quatrefoil** often rank depending on query wording but did not surface in the first automated pulls — see cohort rows in the CSV. User-added peers **JRA** ([RWS Global / JRA](https://www.rwsglobal.com/jra)) and **Design and Production** ([d-and-p.com](https://www.d-and-p.com/)) capture turnkey **museum experiences** / master-plan-to-operations positioning versus planner-led consulting firms. Additional cohort captured in CSV row **Atelier Brückner** ([atelier-brueckner.com/en](https://www.atelier-brueckner.com/en)), **Kossmann.dejong** ([kossmanndejong.nl](https://kossmanndejong.nl/)), **Gensler** ([gensler.com](https://www.gensler.com/) — Culture & Museums), **kubik maltbie** ([kubikmaltbie.com](https://kubikmaltbie.com/) fabrication/design-build): stratify **scenography / spatial narrative / AE breadth / fabrication** versus consulting planner positioning. **Mega institutional cultural consulting:** [Lord Cultural Resources](https://www.lord.ca/) (cultural planning breadth publications tools events) and [AEA Consulting projects hub](https://aeaconsulting.com/projects) (filterable international portfolio strategic/feasibility/capital) — compete on clarity of wedge not organizational scale.

---

## Revision log

| Date | Change |
|------|--------|
| 2026-02-03 | Primary + extended keyword lists; website hierarchy routing note; implementation across canonical tags, titles/meta, Services ↔ Museum School links, and site-relative nav/search URLs targeting museumplanning.com. |
| 2026-05-05 | Competitor matrix CSV cohorts through Kubik; Lord Cultural Resources + AEA mega cultural-strategy row added. |
