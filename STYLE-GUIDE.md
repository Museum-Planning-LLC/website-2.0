# Museum Planning LLC Website Style Guide

This guide is the source of truth for visual and structural consistency in `website-2.0`.

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
  - Avoid playful/techy color palettes and novelty effects.

## 2) Global Navigation Standard

Use this exact nav pattern on all primary pages (including municipal funnels):

- Brand: `Museum <span>Planning</span> LLC`
- Links (in order):
  1. Services
  2. Projects
  3. Museum School
  4. **For Cities** → `for-cities.html`
  5. **Science Centers** → `for-cities-science-center.html`
  6. About
  7. Search icon button
  8. CTA: `Start a Conversation` → `museum-planning-contact.html`

On each page, set `class="active"` on the current section’s link only (typically the CTA uses `active` on the Contact page).

Rules:

- Do **not** add a separate `Contact` nav item.
- Keep nav height `60px`, dark background, gold CTA.
- Keep mobile behavior via:
  - `assets/nav-mobile.css`
  - `assets/nav-mobile.js`
- Keep search overlay behavior consistent (`searchToggle`, `searchOverlay`, `searchClose`, `searchResults` IDs).

## 3) Link and Path Conventions

- For root pages, prefer root-relative or site-relative consistency across the page.
- For nested pages (`projects/*`, `museum-school/*`, `documents/*`), adjust relative paths correctly (`../` or `../../` as needed).
- If you maintain a root file and a mirrored nested file, update both and fix asset paths in the nested copy.
- Canonical URLs should reflect the actual published GitHub Pages URL.

## 4) Page Structure Guidelines

Every new major page should follow the same top-level structure:

1. Fixed global nav
2. Hero section (dark field, serif headline, mono eyebrow, gold accents)
3. Content sections in readable blocks/cards
4. CTA section with gold primary action
5. Footer with standard links and contact details
6. Search overlay + scripts

## 5) Spacing and Rhythm

- Desktop horizontal padding baseline: `56px`
- Mobile horizontal padding baseline: `24px`
- Section spacing should feel generous and editorial, not cramped.
- Keep typography hierarchy clear:
  - H1: bold serif, high contrast
  - H2/H3: serif
  - Labels/meta/nav: mono uppercase tracking
  - Body copy: Lato with comfortable line-height

## 6) Buttons and CTA Rules

- Primary CTA style:
  - Gold background, dark text
  - Uppercase mono
  - Subtle hover to `--gold-lt`
- Avoid introducing new button styles unless there is a strong reason.
- Primary navigation CTA text remains: `Start a Conversation`.

## 7) Footer Standard

- Keep consistent footer composition:
  - Brand lockup
  - External links (Museum Planner, Museums 101, Museum Experiences)
  - Social links (if active; see Social Media Standard below)
  - Contact availability (contact page in footer is acceptable)
  - Copyright line

## 8) Social Media Standard

- **Official platforms (if active):** LinkedIn, Instagram, Facebook, X.
- **Default placement:** Site footer on all primary pages.
- **Optional additional placement:** Contact page only (expanded social row if desired).
- **Order:** LinkedIn, Instagram, Facebook, X.
- **Link labels:** `LinkedIn`, `Instagram`, `Facebook`, `X` (text labels, not icon-only).
- **Link behavior:** open in a new tab with `target="_blank"` and `rel="noopener noreferrer"`.
- **No placeholders:** If a platform is not active, omit it instead of linking to an empty/stub profile.
- **Consistency rule:** Use the same URLs and same order on every page where social links appear.
- **Personal profile exception:** Use Mark's personal LinkedIn only in the About Mark section; keep company LinkedIn in global/footer social links.

## 9) Content Consistency Rules

- Keep terms consistent:
  - `Museum School` (not variants)
  - `Start a Conversation` (exact capitalization)
  - `Museum Planning LLC` (exact branding)
- Avoid one-off visual systems on individual pages.
- New pages must inherit this design system unless explicitly approved otherwise.

## 10) Pre-Publish Checklist

Before committing any page changes:

1. Nav matches standard (order, labels, CTA, search, no separate Contact item).
2. Mobile nav works (hamburger toggles correctly).
3. Search overlay opens/closes and returns results.
4. Font stack and color tokens match system.
5. Links resolve correctly from that page depth.
6. Footer format matches site standard.
7. Social links (if present) follow the Social Media Standard.
8. No accidental alternate palette/theme introduced.

## 11) Change Control

If a change intentionally breaks this guide:

- Document why in the commit message.
- Apply the change consistently across all relevant pages in the same PR/commit set.
- Update this file so the new standard is explicit.
