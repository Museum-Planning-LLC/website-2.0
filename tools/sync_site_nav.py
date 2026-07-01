#!/usr/bin/env python3
"""Sync canonical site nav across museumplanning.com HTML pages.

Spec: docs/NAVIGATION.md · STYLE-GUIDE.md §2
"""
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {"docs", "portfolio-item", "node_modules", ".git"}
SKIP_FILES = {
    "museum-ai/index.html",
    "documents/vitality/museum-vitality-index.html",
    "documents/convergence/convergence-era-v3.html",
}
# Exhibition series index uses series-bar layout only (no site-nav block).
SKIP_PREFIX = "museum-school/museum-exhibition-design/index.html"

NAV_ITEMS = [
    ("Projects", "museum-planning-projects.html"),
    ("Services", "museum-planning-services.html"),
]

SEARCH_SVG = (
    '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/>'
    '<line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
)


def depth_prefix(rel: str) -> str:
    parts = Path(rel).parts
    n = len(parts) - 1
    return "../" * n if n else ""


def active_href(rel: str) -> str | None:
    name = Path(rel).name
    if name == "museum-planning-services.html":
        return "museum-planning-services.html"
    if name in ("for-cities.html", "for-cities-science-center.html"):
        return "for-cities.html"
    if name == "museum-planning-projects.html" or rel.startswith("projects/"):
        return "museum-planning-projects.html"
    if rel.startswith("museum-school/"):
        return "museum-school/index.html"
    if name in (
        "thought-leadership.html",
        "convergence-era.html",
        "immersive-museum-planning.html",
        "museum-staff-portal.html",
        "museum-projects-to-watch-2026.html",
        "landmark-supreme-court-decisions-museums-2026.html",
        "museum-vitality-index.html",
        "museum-ai/index.html",
    ) or rel.startswith("museum-ai/"):
        return "thought-leadership.html"
    if name == "museum-planning-about.html":
        return "museum-planning-about.html"
    if name == "museum-planning-contact.html":
        return None
    return None


def build_nav(prefix: str, active: str | None) -> str:
    lines = [
        '<nav class="site-nav" id="site-nav">',
        f'  <a href="{prefix}index.html" class="nav-logo">Museum <span>Planning</span> LLC</a>',
        '  <button type="button" class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav-menu">',
        '    <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>',
        "  </button>",
        '  <ul class="nav-links" id="site-nav-menu">',
    ]
    for label, href in NAV_ITEMS:
        full = prefix + href
        cls = ' class="active"' if active and href == active else ""
        lines.append(f'    <li><a href="{full}"{cls}>{label}</a></li>')
    lines.extend(
        [
            '    <li class="nav-search"><button type="button" class="search-toggle" id="searchToggle" aria-label="Search">'
            f"{SEARCH_SVG}</button></li>",
            f'    <li><a href="{prefix}museum-planning-contact.html" class="nav-cta">Start a Conversation</a></li>',
            "  </ul>",
            "</nav>",
        ]
    )
    return "\n".join(lines)


def build_projects_nav() -> str:
    """Minimal article nav → full site nav for 2026 projects page."""
    return build_nav("", "thought-leadership.html")


def replace_site_nav(html: str, new_nav: str) -> str | None:
    m = re.search(r'<nav class="site-nav"[^>]*>.*?</nav>', html, re.S)
    if not m:
        return None
    return html[: m.start()] + new_nav + html[m.end() :]


def ensure_nav_assets(html: str, prefix: str) -> str:
    css = f'{prefix}assets/site-nav.css'
    js = f'{prefix}assets/nav-mobile.js'
    mobile_css = f'{prefix}assets/nav-mobile.css'
    if css not in html and "</head>" in html:
        inject = f'  <link rel="stylesheet" href="{css}">\n'
        if mobile_css not in html:
            inject = f'  <link rel="stylesheet" href="{mobile_css}">\n' + inject
        html = html.replace("</head>", inject + "</head>", 1)
    if js not in html and "</body>" in html:
        html = html.replace("</body>", f'  <script src="{js}" defer></script>\n</body>', 1)
    return html


def replace_projects_minimal_nav(html: str) -> str | None:
    m = re.search(r"<nav>\s*<a[^>]*nav-logo.*?</nav>", html, re.S)
    if not m:
        return None
    new = build_projects_nav()
    html = html[: m.start()] + new + html[m.end() :]
    return ensure_nav_assets(html, "")


def main() -> None:
    updated: list[str] = []
    skipped: list[str] = []

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if rel in SKIP_FILES or rel.startswith(SKIP_PREFIX):
            skipped.append(rel)
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")
        prefix = depth_prefix(rel)
        active = active_href(rel)

        if rel == "museum-projects-to-watch-2026.html":
            new_html = replace_projects_minimal_nav(html)
        else:
            new_nav = build_nav(prefix, active)
            new_html = replace_site_nav(html, new_nav)
            if new_html:
                new_html = ensure_nav_assets(new_html, prefix)

        if not new_html or new_html == html:
            if "<nav" in html and "site-nav" not in html and rel not in SKIP_FILES:
                skipped.append(rel + " (non-site-nav)")
            continue

        path.write_text(new_html, encoding="utf-8")
        updated.append(rel)

    print(f"Updated {len(updated)} files")
    for r in updated:
        print(f"  {r}")
    if skipped:
        print(f"\nSkipped {len(skipped)} (custom or series nav)")
        for r in skipped[:20]:
            print(f"  {r}")
        if len(skipped) > 20:
            print(f"  ... +{len(skipped) - 20} more")


if __name__ == "__main__":
    main()
