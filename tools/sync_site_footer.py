#!/usr/bin/env python3
"""Sync canonical site footer links across museumplanning.com HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {"docs", "portfolio-item", "node_modules", ".git"}
SKIP_FILES = {
    "museum-ai/index.html",
    "documents/vitality/museum-vitality-index.html",
    "documents/convergence/convergence-era-v3.html",
}

FOOTER_ITEMS = [
    ("About", "museum-planning-about.html", False),
    ("For Cities", "for-cities.html", False),
    ("Museum School", "museum-school/index.html", False),
    ("Field Notes", "thought-leadership.html", False),
    ("Museums 101", "https://museums101.com", True),
    ("Museum Experiences", "https://museum-experiences.com", True),
    (
        "LinkedIn",
        "https://www.linkedin.com/company/museum-planning-llc/",
        True,
    ),
    ("Instagram", "https://www.instagram.com/museumplanning/", True),
    ("Facebook", "https://www.facebook.com/MuseumPlanningLLC/", True),
    ("X", "https://x.com/MuseumPlanning", True),
    ("Site map", "site-map.html", False),
    ("Contact", "museum-planning-contact.html", False),
]


def depth_prefix(rel: str) -> str:
    parts = Path(rel).parts
    n = len(parts) - 1
    return "../" * n if n else ""


def build_footer_links(prefix: str) -> str:
    lines = ['  <ul class="footer-links">']
    for label, href, external in FOOTER_ITEMS:
        url = href if external else prefix + href
        if external:
            lines.append(
                f'    <li><a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a></li>'
            )
        else:
            lines.append(f'    <li><a href="{url}">{label}</a></li>')
    lines.append("  </ul>")
    return "\n".join(lines)


def replace_footer_links(html: str, new_links: str) -> str | None:
    m = re.search(r"<ul class=\"footer-links\">.*?</ul>", html, re.S)
    if not m:
        return None
    return html[: m.start()] + new_links + html[m.end() :]


def main() -> None:
    updated: list[str] = []
    skipped: list[str] = []

    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if rel in SKIP_FILES:
            skipped.append(rel)
            continue

        html = path.read_text(encoding="utf-8", errors="ignore")
        if "footer-links" not in html:
            skipped.append(rel + " (no footer-links)")
            continue

        prefix = depth_prefix(rel)
        new_links = build_footer_links(prefix)
        new_html = replace_footer_links(html, new_links)
        if not new_html or new_html == html:
            continue

        path.write_text(new_html, encoding="utf-8")
        updated.append(rel)

    print(f"Updated {len(updated)} files")
    for r in updated:
        print(f"  {r}")
    if skipped:
        print(f"\nSkipped {len(skipped)}")


if __name__ == "__main__":
    main()
