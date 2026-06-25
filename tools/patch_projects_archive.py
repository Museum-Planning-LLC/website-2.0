#!/usr/bin/env python3
"""Inject / refresh the Full Project Archive block on museum-planning-projects.html.

Scans projects/*.html (skips redirects), builds an alphabetical link list, and
replaces the marked archive region in the projects hub page.

Usage (repo root):
  python3 tools/patch_projects_archive.py
  python3 tools/patch_projects_archive.py --write
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_HUB = ROOT / "museum-planning-projects.html"
PROJECTS_DIR = ROOT / "projects"

START = "<!-- PROJECTS_ARCHIVE_START -->"
END = "<!-- PROJECTS_ARCHIVE_END -->"

TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.I)


def is_redirect(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return 'http-equiv="refresh"' in text and len(text) < 2500


def title_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = TITLE_RE.search(text)
    if m:
        return re.sub(r"\s*[—–-]\s*Museum Planning LLC\s*$", "", m.group(1).strip(), flags=re.I)
    return path.stem.replace("-", " ").title()


def archive_block() -> str:
    rows: list[tuple[str, str]] = []
    for path in sorted(PROJECTS_DIR.glob("*.html")):
        if path.stem == "index" or is_redirect(path):
            continue
        rows.append((f"projects/{path.name}", title_for(path)))

    items = "\n".join(
        f'        <li><a href="{href}">{title}</a></li>' for href, title in rows
    )
    n = len(rows)
    return f"""{START}
<div class="projects-archive">
  <div class="archive-inner">
    <div class="archive-label">Full project archive</div>
    <h2 class="archive-title">All case studies</h2>
    <p class="archive-deck">Complete index of {n} museum planning projects — including earlier engagements not shown in the featured grid above. Every page is a full case study with images and project documentation.</p>
    <ul class="archive-list">
{items}
    </ul>
  </div>
</div>
{END}
"""


def patch_hub(write: bool) -> None:
    text = PROJECTS_HUB.read_text(encoding="utf-8")
    block = archive_block()

    if START in text and END in text:
        text = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            block,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        anchor = '<div class="projects-cta">'
        if anchor not in text:
            raise SystemExit("Could not find projects-cta anchor in museum-planning-projects.html")
        text = text.replace(anchor, block + "\n\n" + anchor, 1)

    css = """
/* ── FULL ARCHIVE ── */
.projects-archive {
  background: var(--navy);
  padding: 72px 56px 88px;
  border-top: 3px solid var(--gold);
}
.archive-inner { max-width: 1100px; margin: 0 auto; }
.archive-label {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(255,255,255,.35);
  margin-bottom: 14px;
}
.archive-title {
  font-family: var(--serif);
  font-size: clamp(28px, 3.5vw, 40px);
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
}
.archive-deck {
  font-size: 15px;
  line-height: 1.75;
  color: rgba(255,255,255,.55);
  max-width: 720px;
  margin-bottom: 36px;
}
.archive-list {
  list-style: none;
  margin: 0;
  padding: 0;
  columns: 2;
  column-gap: 3rem;
}
.archive-list li {
  break-inside: avoid;
  margin: 0 0 10px;
}
.archive-list a {
  font-family: var(--sans);
  font-size: 15px;
  color: rgba(255,255,255,.82);
  text-decoration: none;
  border-bottom: 1px solid rgba(201,168,76,.25);
  line-height: 1.5;
}
.archive-list a:hover { color: var(--gold); border-color: var(--gold); }
@media (max-width: 768px) {
  .projects-archive { padding: 56px 24px 72px; }
  .archive-list { columns: 1; }
}
"""

    if "/* ── FULL ARCHIVE ── */" not in text:
        text = text.replace("</style>", css + "\n</style>", 1)

    if not write:
        print(block[:500] + "...")
        print(f"\nWould patch {PROJECTS_HUB.name} ({len(rows if False else re.findall(r'<li><a', block))} archive links)")
        return

    PROJECTS_HUB.write_text(text, encoding="utf-8")
    count = block.count("<li><a")
    print(f"Patched {PROJECTS_HUB.name} — {count} archive links")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    patch_hub(write=args.write)


if __name__ == "__main__":
    main()
