#!/usr/bin/env python3
"""Generate legacy-path index.html stubs from redirects/legacy-redirects.json.

GitHub Pages cannot emit HTTP 301. Each stub returns 200 with canonical + refresh
so crawlers consolidate on the new URL (better than 404 + JS in 404.html).

Run from repo root: python3 tools/gen_legacy_redirect_stubs.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_FILE = ROOT / "redirects" / "legacy-redirects.json"
SITE = "https://museumplanning.com"

# Never stub these — real index.html already lives here or stub would clobber content.
SKIP_SOURCES = {"/museum-school"}

STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={canonical}">
<title>Redirecting — Museum Planning LLC</title>
</head>
<body>
<p>Moved to <a href="{canonical}">{label}</a>.</p>
</body>
</html>
"""


def target_url(path: str) -> str:
    if path == "/":
        return f"{SITE}/"
    return f"{SITE}{path}"


def stub_path(source: str) -> Path:
    """/museum-feasibility-studies -> museum-feasibility-studies/index.html"""
    rel = source.strip("/")
    if not rel:
        raise ValueError("root / is not stubbed; use homepage")
    parts = rel.split("/")
    return ROOT.joinpath(*parts, "index.html")


def main() -> None:
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    exact: dict[str, str] = data["exact"]
    count = 0
    for source, dest in sorted(exact.items()):
        if source in SKIP_SOURCES:
            continue
        out = stub_path(source)
        canonical = target_url(dest)
        label = canonical.replace(SITE, "").lstrip("/") or "home"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            STUB.format(canonical=canonical, label=label),
            encoding="utf-8",
        )
        count += 1
    print(f"Wrote {count} redirect stubs under {ROOT}")


if __name__ == "__main__":
    main()
