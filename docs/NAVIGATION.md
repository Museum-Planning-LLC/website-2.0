# Global navigation — Museum Planning LLC

**Canonical spec:** [STYLE-GUIDE.md §2](../STYLE-GUIDE.md#2-global-navigation-standard) · **Browser:** [style-guide.html](../style-guide.html) · **Sync tool:** `tools/sync_site_nav.py`

Last updated: **2026-06**

---

## Design goal

One **slim** top bar across the marketing site: enough discovery for Tier 1–3 and thought leadership, without crowding desktop nav or duplicating the contact CTA.

**Do not** add new top-level nav items without updating this doc, `STYLE-GUIDE.md`, `style-guide.html`, and running the sync script.

---

## Standard `site-nav` (root-relative)

Use on all primary pages: Tier 1 pillars, Tier 2 audience guides, Tier 3 Museum School (except exhibition-series hub), projects, thought-leadership hub, `site-map.html`, etc.

| # | Label | Href (from site root) | `active` when |
|---|--------|------------------------|---------------|
| — | Museum **Planning** LLC (logo) | `index.html` | — |
| 1 | Services | `museum-planning-services.html` | On services page |
| 2 | For Cities | `for-cities.html` | On `for-cities.html` or `for-cities-science-center.html` |
| 3 | Projects | `museum-planning-projects.html` | On projects index or `projects/*` |
| 4 | Museum School | `museum-school/index.html` | On `museum-school/*` (not exhibition-series index) |
| 5 | **Field Notes** | `thought-leadership.html` | On TL hub or TL article URLs (see below) |
| 6 | About | `museum-planning-about.html` | On about page |
| 7 | Search | (button, no link) | — |
| 8 | **Start a Conversation** (CTA) | `museum-planning-contact.html` | — |

**Removed from top bar (2026-06):** For Universities, Science Centers, separate Contact link.

Those pages remain live — discover via **Services**, **For Cities** body copy, site search `PAGES`, footer, and intent strips.

---

## Field Notes hub

**URL:** `thought-leadership.html`  
**Nav label:** `Field Notes` (short; not “Thought Leadership” in the bar)

Articles linked from the hub (not separate nav items):

- `museum-ai/`
- `convergence-era.html`
- `museum-projects-to-watch-2026.html`
- `immersive-museum-planning.html`
- `museum-staff-portal.html`
- `museum-vitality-index.html`

Set `class="active"` on **Field Notes** when the current file is any of the above or `thought-leadership.html`.

---

## Assets

| File | Role |
|------|------|
| `assets/nav-mobile.css` | Hamburger + full-screen menu ≤900px |
| `assets/nav-mobile.js` | Toggle `nav-open` on `site-nav` |
| `assets/site-nav.css` | Tighter gap/padding after page inline nav styles |

Load order: page inline nav styles → `nav-mobile.css` → `site-nav.css`.

Search overlay IDs (unchanged): `searchToggle`, `searchOverlay`, `searchClose`, `searchResults`, `search-input`.

---

## Path depth

| Location | Prefix for root links |
|----------|---------------------|
| Site root (`*.html`) | *(none)* |
| `projects/`, `museum-school/` | `../` |
| `museum-school/museum-exhibition-design/` (parts I–VI) | `../../` |

---

## Sync all pages

After any nav change, run from repo root:

```bash
python3 tools/sync_site_nav.py
```

The script:

- Replaces `<nav class="site-nav" id="site-nav">…</nav>` on ~58 pages
- Sets `active` from file path heuristics
- Skips exceptions below
- Adds `site-nav.css` / `nav-mobile.js` when missing

Commit **HTML + `tools/sync_site_nav.py` + this doc + STYLE-GUIDE** in one change set.

---

## Exceptions (do not run sync blindly)

| Path | Nav pattern |
|------|-------------|
| `museum-ai/index.html` | In-page anchors (Approach, Capabilities, Process, FAQ) + logo to home |
| `museum-school/museum-exhibition-design/index.html` | Compact header + **series bar** only (no global `site-nav-menu`) |
| `documents/vitality/*`, `documents/convergence/*` | Archive mirrors; legacy nav until retired |
| `museum-planner/`, WordPress stub folders | Legacy; not primary IA |
| `projects/mas-*.html` | Minimal template |

---

## Adding a new marketing page

1. Copy nav from `museum-feasibility-study.html` or run `sync_site_nav.py` after adding `site-nav` skeleton.
2. Add entry to site search `PAGES` on the page and on `index.html` / `site-map.html` JSON as needed.
3. Add URL to `sitemap.xml`.
4. If thought leadership → link from `thought-leadership.html`; do **not** add a ninth nav item.
5. If Tier 2 audience (e.g. new vertical) → link from Services / For Cities; only add to top bar if strategy approves removing or merging another item.

---

## Pre-publish nav check

- [ ] `python3 tools/sync_site_nav.py` run (or nav matches § Standard)
- [ ] Mobile menu opens/closes; CTA visible
- [ ] Nested page links resolve (`../` depth)
- [ ] No duplicate Contact + CTA
- [ ] Field Notes → `thought-leadership.html` on root nav
