#!/usr/bin/env python3
"""Import one WordPress portfolio page from Simply Static export — HTML as-is.

Copies portfolio-item/<slug>/index.html, rewrites asset paths for GitHub Pages,
copies referenced wp-content / wp-includes files from the export, and optionally
replaces Google Drive PDF links with local copies when the file exists in uploads.

Usage (repo root):
  python3 tools/import_wp_portfolio.py --list
  python3 tools/import_wp_portfolio.py --slug c-o-polk-interactive-museum --dry-run
  python3 tools/import_wp_portfolio.py --slug c-o-polk-interactive-museum --write
  python3 tools/import_wp_portfolio.py --bootstrap-shared --write   # once: theme + jquery
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "projects-manifest.json"
SITE = "https://museumplanning.com"

# Google Drive PDF → local upload (when export has the file but WP linked externally)
DRIVE_PDF_LOCAL = {
    "11om_xgsLBoT-e-EF9F6mv6Z_w55-vb3F": "wp-content/uploads/2021/08/CO-Polk-Interactive-Museum-Project-PDF.pdf",
}

SHARED_BOOTSTRAP = [
    "wp-content/themes/x/framework/dist/css/site/stacks/integrity-light.css",
    "wp-content/plugins/revslider/sr6/assets/css/rs6.css",
    "wp-includes/js/jquery/jquery.min.js",
    "wp-includes/js/jquery/jquery-migrate.min.js",
]


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def expand_path(p: str) -> Path:
    return Path(p.replace("~", str(Path.home()))).expanduser().resolve()


def find_project(manifest: dict, slug: str) -> dict:
    slug = slug.strip().lower()
    for p in manifest["projects"]:
        if p.get("wp_slug") == slug or p["live_slug"] == slug:
            return p
    raise SystemExit(f"Unknown slug: {slug!r}. Use --list.")


def collect_asset_paths(html: str) -> set[str]:
    paths: set[str] = set()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html, re.I):
        u = m.group(1).split("?")[0]
        u = unquote(u)
        u = re.sub(r"^https?://museumplanning\.com", "", u, flags=re.I)
        if u.startswith("/"):
            u = u[1:]
        if u.startswith(("wp-content/", "wp-includes/")):
            paths.add(u)
    for m in re.finditer(r"srcset=\"([^\"]+)\"", html, re.I):
        for part in m.group(1).split(","):
            u = part.strip().split()[0].split("?")[0]
            u = unquote(u)
            u = re.sub(r"^https?://museumplanning\.com", "", u, flags=re.I)
            if u.startswith("/"):
                u = u[1:]
            if u.startswith(("wp-content/", "wp-includes/")):
                paths.add(u)
    for m in re.finditer(r"url\((['\"]?)(/wp-content/[^)'\"]+)\1?\)", html, re.I):
        paths.add(m.group(2).lstrip("/"))
    return paths


def rewrite_html(html: str, wp_slug: str) -> str:
    prefix = "../../"

    def fix_url(u: str) -> str:
        u = unquote(u)
        u = re.sub(r"^https?://museumplanning\.com", "", u, flags=re.I)
        # Google Drive → local PDF when known
        for drive_id, local in DRIVE_PDF_LOCAL.items():
            if drive_id in u:
                return prefix + local
        if u.startswith("/wp-content/") or u.startswith("/wp-includes/"):
            return prefix + u.lstrip("/")
        if u.startswith("wp-content/") or u.startswith("wp-includes/"):
            return prefix + u
        if u in ("/", ""):
            return prefix + "index.html"
        if u.startswith("/") and not u.startswith("//"):
            return prefix + u.lstrip("/")
        return u

    def attr_repl(match: re.Match[str]) -> str:
        attr, quote, url = match.group(1), match.group(2), match.group(3)
        return f'{attr}={quote}{fix_url(url)}{quote}'

    html = re.sub(
        r'(href|src)=(["\'])([^"\']+)\2',
        attr_repl,
        html,
        flags=re.I,
    )
    html = re.sub(
        r"url\((['\"]?)(/wp-content/[^)'\"]+)\1?\)",
        lambda m: f"url({prefix}{m.group(2).lstrip('/')})",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{SITE}/portfolio-item/{wp_slug}/">',
        html,
        count=1,
    )
    return html


def copy_assets(paths: set[str], export_dir: Path, dry_run: bool) -> tuple[int, list[str]]:
    copied = 0
    missing: list[str] = []
    for rel in sorted(paths):
        src = export_dir / rel
        dest = ROOT / rel
        if not src.is_file():
            missing.append(rel)
            continue
        if dry_run:
            copied += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
            shutil.copy2(src, dest)
        copied += 1
    return copied, missing


def bootstrap_shared(export_dir: Path, dry_run: bool) -> None:
    paths = set(SHARED_BOOTSTRAP)
    n, miss = copy_assets(paths, export_dir, dry_run)
    print(f"Bootstrap: {n} shared file(s)" + (f", {len(miss)} missing" if miss else ""))


def list_projects(manifest: dict) -> None:
    print(f"{'#':>3}  {'wp_slug':42}  title")
    print("-" * 90)
    n = 0
    for p in manifest["projects"]:
        if not p.get("wp_slug") or p["status"] == "done":
            continue
        n += 1
        print(f"{n:3}  {p['wp_slug']:42}  {p['title'][:40]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import WP portfolio HTML as-is.")
    parser.add_argument("--slug", help="wp_slug or live_slug")
    parser.add_argument("--export-dir", help="Simply Static export folder")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--bootstrap-shared",
        action="store_true",
        help="Copy theme CSS + jQuery once (run before first page import)",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    export_dir = expand_path(args.export_dir or manifest.get("export_dir_default", "~/Desktop/museum-export"))

    if args.list:
        list_projects(manifest)
        return

    if not export_dir.is_dir():
        raise SystemExit(f"Export not found: {export_dir}")

    if args.bootstrap_shared:
        bootstrap_shared(export_dir, dry_run=not args.write)
        if not args.slug:
            return

    if not args.slug:
        parser.error("Provide --slug or --list")

    project = find_project(manifest, args.slug)
    wp_slug = project.get("wp_slug")
    if not wp_slug:
        raise SystemExit(f"{project['live_slug']} has no WordPress export entry.")

    src_html = export_dir / "portfolio-item" / wp_slug / "index.html"
    if not src_html.is_file():
        raise SystemExit(f"Missing: {src_html}")

    raw = src_html.read_text(encoding="utf-8", errors="replace")
    assets = collect_asset_paths(raw)
    fixed = rewrite_html(raw, wp_slug)

    dest_html = ROOT / "portfolio-item" / wp_slug / "index.html"
    projects_redirect = ROOT / "projects" / f"{project['live_slug']}.html"

    print(f"Import: {project['title']}")
    print(f"  from: {src_html}")
    print(f"  to:   {dest_html.relative_to(ROOT)}")
    print(f"  assets to sync: {len(assets)}")

    if not args.write:
        copied, missing = copy_assets(assets, export_dir, dry_run=True)
        print(f"  dry-run: would copy {copied} asset file(s)")
        if missing:
            print(f"  missing in export ({len(missing)}):")
            for m in missing[:10]:
                print(f"    - {m}")
            if len(missing) > 10:
                print(f"    ... and {len(missing) - 10} more")
        print("\nUse --write to import.")
        return

    bootstrap_shared(export_dir, dry_run=False)
    for local in DRIVE_PDF_LOCAL.values():
        assets.add(local)
    copied, missing = copy_assets(assets, export_dir, dry_run=False)
    dest_html.parent.mkdir(parents=True, exist_ok=True)
    dest_html.write_text(fixed, encoding="utf-8")

    # Legacy projects/*.html URL → portfolio-item (WordPress path)
    canonical = f"{SITE}/portfolio-item/{wp_slug}/"
    projects_redirect.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={canonical}">
<title>Redirecting — Museum Planning LLC</title>
</head>
<body>
<p>Moved to <a href="{canonical}">portfolio-item/{wp_slug}/</a>.</p>
</body>
</html>
""",
        encoding="utf-8",
    )

    project["status"] = "wp-import"
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {dest_html.relative_to(ROOT)} ({len(fixed):,} bytes)")
    print(f"Copied {copied} asset file(s)")
    if missing:
        print(f"WARNING: {len(missing)} asset(s) missing from export")
    print(f"Redirect stub: {projects_redirect.relative_to(ROOT)} → portfolio-item/")
    print(f"\nPreview: cd repo && python3 -m http.server 8080")
    print(f"  http://localhost:8080/portfolio-item/{wp_slug}/")


if __name__ == "__main__":
    main()
