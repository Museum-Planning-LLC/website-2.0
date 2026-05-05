#!/usr/bin/env python3
"""Inject GA4 loader + site-footer.css + privacy strip/footer links across static HTML."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEAD_SNIPPET = """  <link rel="stylesheet" href="{prefix}assets/site-footer.css">
  <script src="{prefix}assets/ga-measurement-id.js"></script>
  <script src="{prefix}assets/analytics.js" defer></script>
"""

CONTACT_LI_RE = re.compile(
    r'(<li><a href="(?:\.\./)*museum-planning-contact\.html">Contact</a></li>)'
)

SPAN_FOOTER_RE = re.compile(
    r'(<footer>\s*\n\s*<span>)(Museum Planning LLC ·)',
    re.MULTILINE,
)


def asset_prefix(html_path: Path) -> str:
    depth = len(html_path.relative_to(ROOT).parts) - 1
    return "../" * depth


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "assets/analytics.js" in text:
        return False

    prefix = asset_prefix(path)
    privacy_href = prefix + "museum-planning-privacy.html"

    if "</head>" not in text:
        print(f"skip (no </head>): {path.relative_to(ROOT)}", file=sys.stderr)
        return False

    snippet = HEAD_SNIPPET.format(prefix=prefix)
    text = text.replace("</head>", snippet + "\n</head>", 1)

    if "privacy-strip" not in text and "<footer>" in text:
        strip = (
            f'<p class="privacy-strip"><a href="{privacy_href}">'
            f'Privacy &amp; analytics</a> — how this site uses cookies and Google Analytics.</p>\n\n'
        )
        text = text.replace("<footer>", strip + "<footer>", 1)

    if path.name != "museum-planning-privacy.html" and (
        'museum-planning-privacy.html">Privacy</a>' not in text
    ):
        if "<ul class=\"footer-links\">" in text:
            m = CONTACT_LI_RE.search(text)
            if m:
                insert = (
                    f'{m.group(1)}\n    <li><a href="{privacy_href}">Privacy</a></li>'
                )
                text = CONTACT_LI_RE.sub(insert, text, count=1)
        elif SPAN_FOOTER_RE.search(text):
            text = SPAN_FOOTER_RE.sub(
                rf'\1<a href="{privacy_href}">Privacy</a></span>\n  <span>\2',
                text,
                count=1,
            )

    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for p in sorted(ROOT.rglob("*.html")):
        if patch_file(p):
            changed += 1
            print(p.relative_to(ROOT))
    print(f"Patched {changed} files.", file=sys.stderr)


if __name__ == "__main__":
    main()
