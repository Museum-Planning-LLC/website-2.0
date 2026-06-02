# Business & SEO playbook — Museum Planning LLC

**Purpose:** Single handoff doc for future Cursor sessions (or any collaborator). Captures thread intent through June 2026: what the business is, which keywords matter, what’s already done, and how to evaluate new page requests.

**Open this repo** (`museum-planning-llc-website-2.0`) when working on museumplanning.com so `.cursor/rules/` applies.

---

## What the business is

Museum Planning LLC sells **high-trust consulting engagements** (often **$40K–$100K+**): feasibility studies, strategic planning, master planning, exhibition design, opening-day support.

**The website’s job:** rank for **five Tier 1 money keywords**, convert visitors to **Start a Conversation**, support outbound (LinkedIn, director email) with credible pillar URLs.

**This is not:** a content farm, a blog-first SEO play, or a separate “museum cost calculator” site. Every new URL must earn its place in the tier model.

**Voice on commercial pages:** **we / our practice** — not first-person **I**. OK to attribute pull quotes to **Mark Walhimer · Managing Partner**.

---

## Tier 1 — the business (do not dilute)

One **primary URL** per phrase. Hammer these in titles, H1s, internal links, LinkedIn posts, and email signatures.

| # | Money keyword | Primary URL | Status |
|---|---------------|-------------|--------|
| 1 | **Museum planning** | `index.html` (`/`) | Optimized — keyword in title, deck, schema; brand H1 |
| 2 | **Museum planning services** / **museum consultants** | `museum-planning-services.html` | Optimized — services in title/H1; consultants in body/FAQ |
| 3 | **Museum feasibility study** | `museum-feasibility-study.html` | Fully optimized |
| 4 | **Museum strategic planning** | `museum-strategic-planning.html` | Fully optimized |
| 5 | **Museum master planning** | `museum-master-planning.html` | Fully optimized |

**Rules**

- Do **not** create a second page targeting the same phrase.
- Do **not** let Museum School or Tier 2 pages **replace** these as canonical commercial owners.
- **Internal links** from everywhere else should point **up** to the matching Tier 1 URL.
- **Legacy WordPress URLs** must 301 to the correct Tier 1 page (Cloudflare + stubs).

Detail: [`docs/seo-keyword-strategy.md`](./seo-keyword-strategy.md) · Design patterns: [`STYLE-GUIDE.md`](../STYLE-GUIDE.md)

---

## Tier 2 — audience verticals (support Tier 1)

Sitemap priority **~0.45**. Link up to Tier 1; never duplicate Tier 1 copy or intent.

| URL | Role |
|-----|------|
| `for-cities.html` | Municipal / civic feasibility |
| `for-cities-science-center.html` | City science & tech centers |
| `for-universities.html` | University collections & campus museums |
| `local-history-museum.html` | Community / local history |
| `immersive-museum-planning.html` | Immersive & interactive exhibition design |

**New Tier 2 page?** Only if it serves a **distinct audience** (e.g. “for hospitals”) and links clearly to feasibility + services — not a new money-keyword hub.

---

## Tier 3 — Museum School (vocabulary only)

`museum-school/*.html` — “What is…?” education. Sitemap priority **~0.55** (below Tier 1).

Always link **up** to the commercial pillar:

| School page | Links up to |
|-------------|-------------|
| `what-is-a-museum-feasibility-study.html` | `museum-feasibility-study.html` |
| `what-is-a-museum-master-plan.html` | `museum-master-planning.html` |
| `how-to-start-a-museum.html` | `museum-planning-services.html` |

---

## New page requests — pushback protocol

When you (or an AI) ask for a new page — e.g. **“museum cost”**, **“museum budget”**, **“how much does a museum cost”** — **stop and classify** before writing HTML.

### Ask once

> **Which tier is this?** How does it support a Tier 1 money keyword without competing for the same query?

### Usually the right answer is NOT a new page

| Request | Better approach |
|---------|-----------------|
| Museum cost / museum budget | Add FAQ or section on **`museum-feasibility-study.html`** (operating cost modeling is core deliverable) |
| Museum strategic plan template | Section or FAQ on **`museum-strategic-planning.html`** |
| Master plan cost | FAQ on **`museum-master-planning.html`** or fee table on **`museum-planning-contact.html`** |
| Starting a museum (generic) | Existing **`museum-school/how-to-start-a-museum.html`** |
| Immersive / interactives | **`immersive-museum-planning.html`** (Tier 2) — don’t create a second immersive URL |

### When a new page IS allowed

1. **New Tier 2 audience** — e.g. a vertical you actively sell into, with unique copy and Tier 1 links (see `for-universities.html` as template).
2. **New project case study** — `projects/*.html` (proof, not keyword hubs).
3. **New Museum School explainer** — Tier 3 only, must link up to Tier 1.
4. **User explicitly overrides** — after one pushback, if they still want a standalone page, document which tier and keyword it owns in `seo-keyword-strategy.md`.

### Red flags — say no by default

- New URL targeting a Tier 1 phrase already owned
- Thin SEO page with no audience distinction (“museum cost calculator” as standalone)
- Keyword-stuffed duplicate of an existing pillar
- Blog/article that cannibalizes feasibility or master planning

---

## Technical SEO — completed (June 2026)

Do not re-litigate unless something breaks.

| Item | State |
|------|--------|
| GitHub Pages static site | Live |
| Cloudflare in front (301 redirects) | Live — verify with `curl -sI` on legacy paths |
| `redirects/legacy-redirects.json` + generator scripts | In repo |
| Rank-critical 301s (feasibility, strategic, master, immersive, consultants) | Verified |
| Tier 1 pillar pages + schema + FAQ | Done |
| Tier 2 immersive + universities SEO | Done |
| MAS portfolio (`projects/mas-*.html`) | Done |
| Sitemap + Museum School demoted to 0.55 | Done |
| `docs/seo-keyword-strategy.md` | Current |

**Regenerate redirects after map changes:**

```bash
python3 tools/gen_legacy_redirect_stubs.py
python3 tools/gen_cloudflare_bulk_redirects.py
```

Re-import CSV in Cloudflare → [`redirects/README.md`](../redirects/README.md)

---

## Growth sequence (post-site)

Order matters. Site structure first; outbound second.

| Phase | Actions |
|-------|---------|
| **Now** | GSC: monthly query + landing-page review; confirm Tier 1 URLs indexed |
| **Weeks 4–8** | MailChimp: replace mailto newsletter with embed + welcome sequence linking Tier 1 |
| **Ongoing** | LinkedIn (primary): 1–2 posts/week → pillar URL; personalized director email |
| **Parallel** | Museums 101 second edition (author authority, separate from site IA) |
| **Always** | GA4 + GSC; simple CRM for leads (e.g. Bob Moog Foundation) |

**Also useful:** outreach one-pager (capabilities), email signature with pillar links, GA4 events on contact/tel/mailto, referral relationships with architects.

---

## Doc index (read order for new sessions)

1. **This file** — business intent + pushback rules  
2. [`docs/seo-keyword-strategy.md`](./seo-keyword-strategy.md) — keyword ↔ URL map  
3. [`STYLE-GUIDE.md`](../STYLE-GUIDE.md) — design, voice, SEO head checklist  
4. [`redirects/README.md`](../redirects/README.md) — Cloudflare workflow  
5. [`SITE-STRATEGY.md`](../SITE-STRATEGY.md) — audience priority & funnel  
6. [`README.md`](../README.md) — repo overview & deploy  

---

## Revision log

| Date | Change |
|------|--------|
| 2026-06-02 | Initial playbook from Cursor thread: Tier 1 business model, pushback protocol, completed work, growth sequence |
