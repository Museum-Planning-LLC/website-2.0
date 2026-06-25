#!/usr/bin/env python3
"""Migrate local project pages from old prose+gallery layout to wp-archive template."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"


def extract_gallery_images(html: str) -> list[tuple[str, str]]:
    images: list[tuple[str, str]] = []
    for block in re.finditer(r'<div class="gallery">.*?</div>\s*(?=<div class="(?:gallery|next-projects|cta-band)">|\Z)', html, re.DOTALL):
        for img in re.finditer(r"<img\s([^>]+)>", block.group(0)):
            attrs = img.group(1)
            src_m = re.search(r'src="([^"]+)"', attrs)
            if not src_m:
                continue
            alt_m = re.search(r'alt="([^"]*)"', attrs)
            images.append((src_m.group(1), alt_m.group(1) if alt_m else ""))
    return images


def h2_to_section_p(prose: str) -> str:
    return re.sub(
        r"\s*<h2>(.*?)</h2>\s*",
        lambda m: f"\n<p>{m.group(1).strip()}</p>\n",
        prose,
        flags=re.DOTALL,
    )


def migrate_html(text: str) -> tuple[str, bool]:
    if "prose wp-archive" in text:
        return text, False

    if '<div class="prose">' not in text:
        return text, False

    if "wp-archive-prose.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="../assets/site-nav.css">',
            '<link rel="stylesheet" href="../assets/site-nav.css">\n'
            '  <link rel="stylesheet" href="../assets/wp-archive-prose.css">',
        )

    text = re.sub(r"<body>", '<body class="project-wp-archive">', text, count=1)

    gallery_images = extract_gallery_images(text)

    prose_match = re.search(
        r'(<div class="body-wrap">\s*)<div class="prose">(.*?)(</div>\s*<div class="sidebar">)',
        text,
        re.DOTALL,
    )
    if not prose_match:
        raise ValueError("Could not locate prose block")

    prose_inner = h2_to_section_p(prose_match.group(2).strip())
    if gallery_images:
        img_lines = []
        for src, alt in gallery_images:
            alt_attr = alt or "Project photo"
            img_lines.append(
                f'<img class="aligncenter size-large" src="{src}" alt="{alt_attr}" loading="lazy">'
            )
        prose_inner = prose_inner.rstrip() + "\n" + "\n".join(img_lines) + "\n"

    replacement = (
        f'{prose_match.group(1)}<div class="prose wp-archive">\n{prose_inner}  '
        f"{prose_match.group(3)}"
    )
    text = text[: prose_match.start()] + replacement + text[prose_match.end() :]

    text = re.sub(
        r'\n\n<div class="gallery">.*?</div>\n(?=\n<div class="(?:gallery|next-projects|cta-band)">)',
        "\n",
        text,
        flags=re.DOTALL,
    )

    return text, True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    changed: list[str] = []
    skipped: list[str] = []

    for path in sorted(PROJECTS.glob("*.html")):
        original = path.read_text(encoding="utf-8")
        updated, did_change = migrate_html(original)
        if not did_change:
            skipped.append(path.name)
            continue
        changed.append(path.name)
        if args.write:
            path.write_text(updated, encoding="utf-8")

    print(f"Changed: {len(changed)}")
    for name in changed:
        print(f"  {name}")
    print(f"Skipped: {len(skipped)}")


if __name__ == "__main__":
    main()
