# Project page migration — WordPress HTML copy (current approach)

**Goal:** Reproduce WordPress portfolio pages faithfully on GitHub — same content, PDFs, videos, photos — not a redesign template.

## Prerequisites

- Simply Static export at `~/Desktop/museum-export`

## One-time: shared WordPress assets (theme CSS, jQuery)

```bash
cd /Users/markwalhimer/Documents/GitHub/museum-planning-llc-website-2.0
python3 tools/import_wp_portfolio.py --bootstrap-shared --write
```

## Import one project

```bash
python3 tools/import_wp_portfolio.py --list
python3 tools/import_wp_portfolio.py --slug c-o-polk-interactive-museum --dry-run
python3 tools/import_wp_portfolio.py --slug c-o-polk-interactive-museum --write
```

## What `--write` does

1. Copies WordPress `index.html` → `portfolio-item/<wp-slug>/index.html`
2. Rewrites `/wp-content/` and `/wp-includes/` to relative paths (`../../wp-content/…`)
3. Copies every referenced asset from the export into the repo
4. Replaces known Google Drive PDF links with local `wp-content/uploads/` files when available
5. Sets `projects/<live-slug>.html` to redirect → `portfolio-item/<wp-slug>/` (legacy URL)

## Preview

```bash
python3 -m http.server 8080
# http://localhost:8080/portfolio-item/c-o-polk-interactive-museum/
```

Use **8080** for the GitHub repo. Port **8000** may still be the old `museum-export` folder.

## After import

- Spot-check PDF downloads and Vimeo embeds
- Commit HTML + `wp-content/` assets together

## Skin into site design (no WordPress CSS)

Extract `.entry-content` and wrap in Museum Planning nav/footer:

```bash
python3 tools/skin_wp_portfolio.py --slug c-o-polk-interactive-museum --dry-run
python3 tools/skin_wp_portfolio.py --slug c-o-polk-interactive-museum --write
```

Output for Polk: `projects/city-of-mcdonough-georgia.html` (canonical hub URL).  
Legacy URLs redirect there: `projects/c-o-polk-interactive-museum.html`, `portfolio-item/c-o-polk-interactive-museum/`.

Assets use `content/uploads/` paths (same tree as existing project pages).

## Deprecated

`tools/build_project_page.py` (Alcatraz template builder) — kept for reference, not the primary path.
