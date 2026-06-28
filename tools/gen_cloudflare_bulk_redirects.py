#!/usr/bin/env python3
"""Build Cloudflare Bulk Redirects CSV from redirects/legacy-redirects.json.

Cloudflare CSV rules (dashboard import):
  - No header row
  - Column 0 source: host/path only — NO https://
  - Column 1 target: full URL WITH https://
  - Column 2 status: 301
  - Homepage target: https://museumplanning.com (no trailing slash)
  - Do NOT add parent portfolio-item/ when child portfolio-item/* rows exist (Cloudflare rejects overlap)

Run: python3 tools/gen_cloudflare_bulk_redirects.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_FILE = ROOT / "redirects" / "legacy-redirects.json"
OUT_FILE = ROOT / "redirects" / "cloudflare-bulk-redirects.csv"
OUT_PRIORITY = ROOT / "redirects" / "cloudflare-bulk-redirects-priority.csv"
HOST = "museumplanning.com"
SITE = f"https://{HOST}"

# Paths not in legacy-redirects.json exact map
EXTRA_EXACT = {
    "/museum-school": "/museum-school/index.html",
}

# Omit parent /portfolio-item — specific /portfolio-item/* rows cover WordPress projects.
SKIP_EXACT = {"/portfolio-item"}

PRIORITY_SOURCES = {
    "/museum-feasibility-studies",
    "/museum-feasibility-study",
    "/museum-master-planning",
    "/museum-consultants",
    "/museum-strategic-planning-consultants",
    "/museum-strategic-planning",
    "/museum-consulting-and-cultural-planning-museum-planning-llc",
    "/immersive-interactive-museum-transformation",
}


def target_url(path: str) -> str:
    if path == "/":
        return SITE
    return f"{SITE}{path}"


def source_url(path: str, *, trailing_slash: bool = False) -> str:
    path = path if path.startswith("/") else f"/{path}"
    if trailing_slash and not path.endswith("/"):
        path = f"{path}/"
    return f"{HOST}{path}"


def main() -> None:
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    exact: dict[str, str] = {**data["exact"], **EXTRA_EXACT}
    rows: list[list[str]] = []
    priority_rows: list[list[str]] = []
    seen: set[str] = set()

    def add(source_path: str, dest_path: str, *, trailing_slash: bool = False) -> None:
        src = source_url(source_path, trailing_slash=trailing_slash)
        if src in seen:
            return
        seen.add(src)
        row = [src, target_url(dest_path), "301"]
        rows.append(row)
        if source_path in PRIORITY_SOURCES:
            priority_rows.append(row)

    add("/wp-content/uploads", "/content/uploads/", trailing_slash=True)

    for source, dest in sorted(exact.items()):
        if source in SKIP_EXACT:
            continue
        add(source, dest, trailing_slash=False)
        # WordPress legacy URLs often used trailing slashes; Cloudflare must match both.
        add(source, dest, trailing_slash=True)

    skip_prefixes = {
        "/portfolio-item/",
        "/process/",
        "/museum-assessment/",
        "/mark-walhimer-resume/",
        "/portfolio/page",  # often conflicts with /page/ in Cloudflare UI
    }
    for entry in data.get("prefix", []):
        if entry["prefix"] in skip_prefixes:
            continue
        p = entry["prefix"].rstrip("/")
        # Exact prefix landing (e.g. /author/)
        add(p, entry["target"], trailing_slash=True)
        # Subpaths (e.g. /author/alvaro/) — Bulk Redirects need trailing /*
        src = f"{HOST}{p}/*"
        if src not in seen:
            seen.add(src)
            row = [src, target_url(entry["target"]), "301"]
            rows.append(row)

    for path in (OUT_FILE, OUT_PRIORITY):
        path.parent.mkdir(parents=True, exist_ok=True)

    with OUT_FILE.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL).writerows(rows)

    with OUT_PRIORITY.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL).writerows(priority_rows)

    print(f"Wrote {len(rows)} redirects to {OUT_FILE}")
    print(f"Wrote {len(priority_rows)} priority redirects to {OUT_PRIORITY}")


if __name__ == "__main__":
    main()
