#!/usr/bin/env python3
"""Replace per-page inline search scripts with shared search assets."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SEARCH_BLOCK_RE = re.compile(
    r"const PAGES\s*=\s*\[[\s\S]*?"
    r"input\.addEventListener\(\s*['\"]input['\"][\s\S]*?\}\s*\)\s*;?",
    re.MULTILINE,
)

NAV_MOBILE_RE = re.compile(
    r'(<script\s+src="([^"]*?)assets/nav-mobile\.js"[^>]*></script>)'
)


def asset_prefix(rel: str) -> str:
    depth = rel.count("/")
    return "../" * depth if depth else ""


def patch_file(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    if "id=\"searchOverlay\"" not in text:
        return False

    prefix = asset_prefix(rel)
    inject = (
        f'<script src="{prefix}assets/search-pages.js"></script>\n'
        f'<script src="{prefix}assets/site-search.js"></script>\n'
    )

    if "assets/site-search.js" in text and not SEARCH_BLOCK_RE.search(text):
        return False

    new_text, n = SEARCH_BLOCK_RE.subn("", text)
    if n == 0 and "assets/site-search.js" in text:
        return False
    if n == 0:
        print(f"  skip (no PAGES block): {rel}")
        return False

    if f"{prefix}assets/site-search.js" not in new_text:
        nav_match = NAV_MOBILE_RE.search(new_text)
        if nav_match:
            new_text = new_text.replace(
                nav_match.group(1), inject + nav_match.group(1), 1
            )
        else:
            new_text = new_text.replace("</body>", inject + "</body>", 1)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"  patched: {rel}")
        return True
    return False


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if patch_file(path):
            count += 1
    print(f"Patched {count} file(s).")


if __name__ == "__main__":
    main()
