# Museum Planning LLC Website Style Guide

This guide is the source of truth for visual, structural, and SEO consistency in `website-2.0`.

**Browser version:** [style-guide.html](./style-guide.html)

## 1) Design System (Do Not Drift)

- **Primary palette**
  - `--deep: #111C27` (dark nav / hero background)
  - `--gold: #C9A84C` (accent / CTA)
  - `--gold-lt: #E8D099` (CTA hover)
  - `--cream: #F8F4EC` (page background)
  - `--ink: #1A1A1A` (body text)
  - `--mid: #5A5A5A` (secondary text)
  - `--rule: #D4C8B0` (borders/rules)
- **Typography**
  - Serif display/headlines: `Playfair Display`
  - Utility labels/nav/meta: `DM Mono`
  - Body copy: `Lato`
- **Voice and tone**
  - Premium, practical, direct.
  - Use **we** / **our practice** on commercial and vertical pages — not first-person **I**.
  - Pull-quote attribution may use **Mark Walhimer · Managing Partner**.
  - Avoid playful/techy color palettes and novelty effects.

## 2) Global Navigation Standard

Use this nav pattern on all primary pages (commercial pillars, vertical guides, municipal funnels):

- Brand: `Museum <span>Planning</span> LLC`
- Links (in order):
  1. Services → `museum-planning-services.html`
  2. For Cities → `for-cities.html`
  3. For Universities → `for-universities.html`
  4. Projects → `museum-planning-projects.html`
  5. Museum School → `museum-school/index.html`
  6. Science Centers → `for-cities-science-center.html`
  7. About → `museum-planning-about.html`
  8. Contact → `museum-planning-contact.html`
  9. Search icon button
  10. CTA: `Start a Conversation` → `museum-planning-contact.html`

On each page, set `class="active"` on the current section’s link only (typically `active` on Contact when on the contact page).

Rules:

- Keep nav height `60px`, dark background, gold CTA.
- Keep mobile behavior via `assets/nav-mobile.css` and `assets/nav-mobile.js`.
- Keep search overlay IDs consistent: `searchToggle`, `searchOverlay`, `searchClose`, `searchResults`, `search-input`.

## 3) Link and Path Conventions

- Root pages use site-relative paths (`museum-feasibility-study.html`).
- Nested pages (`projects/*`, `museum-school/*`) use correct `../` depth.
- **Canonical URLs:** `https://museumplanning.com/<filename>.html` (always include `.html`).
- **Do not** use extensionless canonicals unless a matching redirect stub exists.

## 4) Page Structure Guidelines

Every new major page should follow:

1. Fixed global nav (+ mobile hamburger)
2. Hero (dark field, keyword in H1, mono eyebrow, gold accents)
3. Content sections (readable blocks/cards)
4. FAQ section (commercial and vertical pages) — visible copy must match JSON-LD
5. Related / intent strip linking Tier 1 and sibling Tier 2 pages
6. CTA section with contact form → `museum-planning-contact.html` or inline mailto form
7. Privacy strip + standard footer
8. Search overlay + `PAGES` array for site search
9. GTM: `assets/ga-measurement-id.js`, `assets/analytics.js`

**Reference templates**

| Tier | Copy from |
|------|-----------|
| Tier 1 commercial pillar | `museum-feasibility-study.html` |
| Tier 2 vertical guide | `local-history-museum.html` or `immersive-museum-planning.html` |

## 5) Page Tiers (SEO / IA)

Do not create competing URLs for the same intent.

| Tier | Sitemap priority | Examples |
|------|------------------|----------|
| **Tier 1** — money keywords | `0.85` | `museum-feasibility-study.html`, `museum-strategic-planning.html`, `museum-master-planning.html`, `museum-planning-services.html` |
| **Tier 2** — audience / vertical | `0.45` | `for-cities.html`, `for-cities-science-center.html`, `local-history-museum.html`, `immersive-museum-planning.html` |
| **Tier 3** — Museum School | lower | `museum-school/*.html` |

Tier 2 pages link **up** to Tier 1 and **across** to related Tier 2 pages. They do not keyword-stuff or duplicate Tier 1 copy.

## 6) SEO Standard (Commercial & Vertical Pages)

Required in `<head>`:

- Unique `<title>` — primary keyword first, `| Museum Planning LLC` suffix
- `<meta name="description">` — ~155 characters, **we** voice, fee signal where appropriate
- `<link rel="canonical">` — full HTTPS URL with `.html`
- Open Graph + Twitter Card (`og:image` = Mark Walhimer headshot URL used on homepage)
- `application/ld+json` `@graph` with:
  - `ProfessionalService` (reference `#organization`)
  - `WebPage` (`dateModified`, `primaryImageOfPage`)
  - `Service` (Tier 1) where applicable
  - `FAQPage` — every visible FAQ question, text must match
  - `BreadcrumbList` — Home → Services → Page (or Home → Page for services hub)

**Avoid:** `meta keywords`, keyword-stuffed H2s, extensionless canonicals without stubs, FAQ schema that does not match visible copy.

After publish: add URL to `sitemap.xml`; add legacy redirect if replacing a WordPress path; request GSC indexing.

## 7) Spacing and Rhythm

- Desktop horizontal padding: `56px` (sections), nav matches
- Mobile horizontal padding: `24px`
- Section spacing: generous and editorial
- H1: bold serif, primary keyword where natural
- Labels/meta/nav: mono uppercase tracking
- Body: Lato, comfortable line-height (~1.65–1.78)

## 8) Buttons and CTA Rules

- Primary CTA: gold background, dark text, uppercase mono
- Hover: `--gold-lt` or opacity reduction
- Primary nav CTA text: `Start a Conversation`
- Page CTAs should route to `#contact` on-page or `museum-planning-contact.html`

## 9) Footer Standard

- Brand lockup
- External links: Museum Planner, Museums 101, Museum Experiences
- Social links when active (LinkedIn, Instagram, Facebook, X) — see §10
- Contact / Privacy links
- Copyright line
- Use `assets/site-footer.css` where shared footer classes apply

## 10) Social Media Standard

- **Platforms (if active):** LinkedIn, Instagram, Facebook, X
- **Placement:** footer on primary pages; optional expanded row on contact page
- **Order:** LinkedIn, Instagram, Facebook, X
- **Behavior:** `target="_blank"` + `rel="noopener noreferrer"`
- **No placeholders** for inactive profiles
- **Personal LinkedIn** only in About Mark section; company LinkedIn in footer

## 11) Content Consistency Rules

- Exact terms: `Museum School`, `Start a Conversation`, `Museum Planning LLC`
- One visual system — no one-off palettes (e.g. copper/red draft themes)
- New commercial pages inherit navy/gold/Lato unless a deliberate rebrand is approved site-wide

## 12) Pre-Publish Checklist

1. Nav matches §2 (order, mobile, search).
2. Voice is **we**, not **I**.
3. H1 includes primary keyword naturally; body is not keyword-stuffed.
4. SEO head complete (§6); FAQ schema matches visible FAQ.
5. Internal links to Tier 1 + related Tier 2 pages.
6. `sitemap.xml` updated.
7. Legacy redirect added if needed (`redirects/legacy-redirects.json` + stub generator).
8. `PAGES` search array updated on new page and key hub pages.
9. Links and asset paths resolve at page depth.
10. Footer and privacy strip present.

## 13) Change Control

If a change intentionally breaks this guide:

- Document why in the commit message.
- Apply consistently across all relevant pages in the same commit set.
- Update this file and `style-guide.html`.
