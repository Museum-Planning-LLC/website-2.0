#!/usr/bin/env python3
"""Batch-restore project pages from Local WordPress Simply Static export.

For each manifest entry with a wp_slug, imports full WordPress entry-content,
copies referenced uploads from the export and Local WordPress (fallback), and
writes skinned projects/<live_slug>.html pages.

Arizona (university-of-arizona) is restored from a saved WP HTML snapshot when
the export predates that portfolio post.

Usage (repo root):
  python3 tools/batch_restore_projects.py --dry-run
  python3 tools/batch_restore_projects.py --write
  python3 tools/batch_restore_projects.py --write --slug mide-museo-interactivo-de-economia
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from html import escape, unescape
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "projects-manifest.json"
SITE = "https://museumplanning.com"
SHELL = ROOT / "projects" / "howard-natural-history-museum.html"

SIMPLY_STATIC = Path(
    "/Users/markwalhimer/Local Sites/museum-planning-wordpress/app/public"
    "/wp-content/uploads/simply-static/temp-files/simply-static-1-1782065628"
)
LOCAL_UPLOADS = Path(
    "/Users/markwalhimer/Local Sites/museum-planning-wordpress/app/public/wp-content/uploads"
)
ARIZONA_SOURCE = Path(__file__).resolve().parent / "sources" / "university-of-arizona-wp.html"

OUTPUT_OVERRIDE = {
    "c-o-polk-interactive-museum": "city-of-mcdonough-georgia",
}

SKIP_STATUS = {"done", "live"}

DRIVE_PDF_LOCAL = {
    "11om_xgsLBoT-e-EF9F6mv6Z_w55-vb3F": "wp-content/uploads/2021/08/CO-Polk-Interactive-Museum-Project-PDF.pdf",
}


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_project(manifest: dict, slug: str) -> dict:
    slug = slug.strip().lower()
    for p in manifest["projects"]:
        if p.get("wp_slug") == slug or p["live_slug"] == slug:
            return p
    raise SystemExit(f"Unknown slug: {slug!r}")


def normalize_wayback_html(html: str) -> str:
    html = re.sub(
        r"https://web\.archive\.org/web/\d+(?:im_|if_)?/https?://(?:i\d+\.wp\.com/)?(?:www\.)?museumplanning\.com/wp-content/",
        "/wp-content/",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"https://web\.archive\.org/web/\d+(?:im_|if_)?/https?://(?:www\.)?museumplanning\.com/",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r"\?resize=[^\"'\s>&]+", "", html)
    html = re.sub(r"&amp;ssl=1", "", html)
    return html


def extract_entry_content(html: str) -> str:
    for pat in (
        r'<div class="entry-content content">(.*?)</div>\s*\n\s*</div>\s*\n\s*<div class="entry-extra">',
        r'<div class="entry-content[^"]*">(.*?)</div>\s*</div>\s*<div class="entry-extra">',
    ):
        m = re.search(pat, html, re.DOTALL | re.I)
        if m:
            return m.group(1).strip()
    raise ValueError("Could not find .entry-content in portfolio HTML")


def best_image_src(src: str, srcset: str | None) -> str:
    candidates = [src]
    if srcset:
        for part in srcset.split(","):
            candidates.append(part.strip().split()[0])
    best, best_w = src, 0
    for u in candidates:
        u = u.lstrip("/")
        m = re.search(r"-(\d+)x(\d+)\.", u)
        w = int(m.group(1)) if m else 0
        if w >= best_w:
            best_w, best = w, u
    return best


def rewrite_upload_path(path: str) -> str:
    path = unquote(path.split("?")[0])
    if path.startswith("../content/uploads/"):
        return path
    path = re.sub(r"^https?://museumplanning\.com", "", path, flags=re.I)
    path = path.lstrip("/")
    for prefix in (
        "../../wp-content/uploads/",
        "/wp-content/uploads/",
        "wp-content/uploads/",
        "../content/uploads/",
    ):
        if path.startswith(prefix):
            path = path[len(prefix) :]
            break
    return f"../content/uploads/{path}"


def fix_caption_block(m: re.Match[str]) -> str:
    inner = m.group(1).strip()
    inner = re.sub(
        r'<p id="caption-attachment-\d+" class="wp-caption-text">',
        "<figcaption>",
        inner,
        flags=re.I,
    )
    inner = re.sub(r"</p>\s*$", "</figcaption>", inner, flags=re.I)
    return f'<figure class="wp-caption aligncenter">{inner}</figure>'


def clean_content(html: str, title: str = "") -> str:
    html = re.sub(r"<noscript>.*?</noscript>", "", html, flags=re.DOTALL | re.I)
    html = re.sub(r'\s*data-wp-editing="[^"]*"', "", html, flags=re.I)
    html = re.sub(r"\?w=\d+", "", html)
    html = re.sub(r'\s*style="width:\s*\d+px"', "", html, flags=re.I)
    html = re.sub(r'\s*style="text-align:\s*center;"', "", html, flags=re.I)
    html = re.sub(r'<span style="color:\s*#993300;">\s*', "", html, flags=re.I)
    html = re.sub(r"\s*</span>", "", html, count=1)

    html = re.sub(r'\s*allowfullscreen="allowfullscreen"', "", html, flags=re.I)
    html = re.sub(r'\s*frameborder="0"', "", html, flags=re.I)
    html = re.sub(r'\s*width="\d+"\s*height="\d+"', "", html, flags=re.I)

    def fix_img(m: re.Match[str]) -> str:
        tag = m.group(0)
        src_m = re.search(r'src="([^"]+)"', tag, re.I)
        srcset_m = re.search(r'srcset="([^"]+)"', tag, re.I)
        if not src_m:
            return tag
        new_src = rewrite_upload_path(best_image_src(src_m.group(1), srcset_m.group(1) if srcset_m else None))
        alt_m = re.search(r'alt="([^"]*)"', tag, re.I)
        alt = alt_m.group(1) if alt_m else ""
        return f'<img src="{new_src}" alt="{escape(alt, quote=True)}" loading="lazy">'

    html = re.sub(r"<img[^>]+>", fix_img, html, flags=re.I)

    pdf_block = re.search(
        r"((?:<p>(?:<strong>)?<a href=\"[^\"]+\.pdf\"[^>]*>.*?</a>((?:</strong>)?</p>\s*)+))",
        html,
        flags=re.DOTALL | re.I,
    )
    if pdf_block:
        links = re.findall(
            r'<p>(?:<strong>)?<a href="([^"]+\.pdf)"[^>]*>(.*?)</a>(?:</strong>)?</p>',
            pdf_block.group(1),
            flags=re.DOTALL | re.I,
        )
        if links:
            inner = "".join(
                f'<a href="{rewrite_upload_path(h)}" target="_blank" rel="noopener">{t.strip()}</a>'
                for h, t in links
            )
            html = (
                html[: pdf_block.start()]
                + f'<div class="pdf-links">{inner}</div>'
                + html[pdf_block.end() :]
            )

    def fix_href(m: re.Match[str]) -> str:
        href = m.group(1)
        if "contact-museum-planning" in href or "museum-planning-contact" in href:
            return 'href="../museum-planning-contact.html"'
        if "wp-content/uploads" in href or href.startswith("../../wp-content"):
            return f'href="{rewrite_upload_path(href)}"'
        if href.startswith("/portfolio-item/") or href.startswith("portfolio-item/"):
            return m.group(0)
        return m.group(0)

    html = re.sub(r'href="([^"]+)"', fix_href, html)

    html = re.sub(
        r'<div id="attachment_\d+"[^>]*class="wp-caption[^"]*">(.*?)</div>',
        fix_caption_block,
        html,
        flags=re.DOTALL | re.I,
    )

    html = re.sub(
        r"<iframe([^>]*src=\"https://player\.vimeo\.com[^\"]+\"[^>]*)></iframe>",
        r'<div class="video-wrap"><iframe\1></iframe></div>',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<p>\s*(<div class=\"video-wrap\">.*?</div>)\s*</p>",
        r"\1",
        html,
        flags=re.DOTALL | re.I,
    )
    html = re.sub(r"</div></p>", "</div>", html)
    html = re.sub(r"<p>\s*</p>", "", html)

    if title:
        esc = re.escape(title)
        html = re.sub(
            rf"<h3[^>]*><strong>{esc}</strong></h3>\s*<p[^>]*>([^<]+)</p>",
            r'<p class="lead">\1</p>',
            html,
            count=1,
            flags=re.I,
        )
        html = re.sub(rf"<h3[^>]*><strong>{esc}</strong></h3>\s*", "", html, count=1, flags=re.I)

    html = re.sub(r'\s*class="[^"]*wp-image-\d+[^"]*"', "", html)
    html = re.sub(r'\s*class="[^"]*size-large[^"]*"', "", html)
    html = re.sub(r'\s*class="aligncenter"', "", html)
    html = re.sub(r'\s*decoding="async"', "", html)
    html = re.sub(r'\s*aria-describedby="[^"]*"', "", html)
    html = re.sub(r"<p>\s*&nbsp;\s*</p>", "", html, flags=re.I)
    html = re.sub(r"<p>\s*<strong>\s*((?:<img[^>]+>\s*)+)</strong>\s*</p>", r"\1", html, flags=re.I)
    html = re.sub(r"<p>\s*((?:<img[^>]+>\s*)+)</p>", r"\1", html, flags=re.I)

    return html.strip()


def collect_upload_paths(html: str) -> set[str]:
    paths: set[str] = set()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html, re.I):
        u = unquote(m.group(1).split("?")[0])
        u = re.sub(r"^https?://museumplanning\.com", "", u, flags=re.I)
        if u.startswith("/"):
            u = u[1:]
        if u.startswith("wp-content/uploads/"):
            paths.add(u)
    for m in re.finditer(r"srcset=\"([^\"]+)\"", html, re.I):
        for part in m.group(1).split(","):
            u = unquote(part.strip().split()[0].split("?")[0])
            u = re.sub(r"^https?://museumplanning\.com", "", u, flags=re.I)
            if u.startswith("/"):
                u = u[1:]
            if u.startswith("wp-content/uploads/"):
                paths.add(u)
    for drive_id, local in DRIVE_PDF_LOCAL.items():
        if drive_id in html:
            paths.add(local)
    return paths


def upload_rel_to_content_dest(rel: str) -> Path:
    sub = rel.removeprefix("wp-content/uploads/")
    return ROOT / "content/uploads" / sub


def copy_uploads(paths: set[str], dry_run: bool) -> tuple[int, list[str]]:
    copied = 0
    missing: list[str] = []
    export_uploads = SIMPLY_STATIC / "wp-content/uploads"
    for rel in sorted(paths):
        sub = rel.removeprefix("wp-content/uploads/")
        dest = ROOT / "content/uploads" / sub
        src = None
        for base in (export_uploads, LOCAL_UPLOADS):
            candidate = base / sub
            if candidate.is_file():
                src = candidate
                break
        if not src:
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


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def parse_field(html: str, *labels: str) -> str:
    for label in labels:
        m = re.search(
            rf"<strong>{re.escape(label)}:?</strong>\s*([^<\n]+)",
            html,
            flags=re.I,
        )
        if m:
            return strip_tags(m.group(1))
        m = re.search(rf"{re.escape(label)}:\s*([^<\n]+)", html, flags=re.I)
        if m:
            return strip_tags(m.group(1))
    return ""


def infer_hero(project: dict, raw_html: str, cleaned: str) -> dict:
    title = project["title"]
    client = parse_field(raw_html, "Client")
    location = parse_field(raw_html, "Location")
    opening = parse_field(raw_html, "Opening Date", "Opening", "Period", "Date", "Year")
    services_text = parse_field(raw_html, "Services")

    hero_img = ""
    for m in re.finditer(r'src="([^"]+)"', cleaned):
        src = m.group(1)
        if "/uploads/" in src and "Logo" not in src:
            hero_img = src
            break

    lead_m = re.search(r'<p class="lead">([^<]+)</p>', cleaned)
    if not lead_m:
        lead_m = re.search(r"<p>([^<]{40,200})</p>", cleaned)
    subtitle = strip_tags(lead_m.group(1)) if lead_m else ""

    eyebrow_bits = [b for b in (client, location.split(",")[0] if location else "") if b]
    eyebrow = " · ".join(eyebrow_bits[:2]) if eyebrow_bits else "Museum Planning LLC Project"

    services = []
    if services_text:
        services = [s.strip() for s in re.split(r"[,·/]", services_text) if s.strip()][:5]

    meta_desc = f"{title} — Museum Planning LLC project case study."
    if location:
        meta_desc = f"{title} · {location} · Museum Planning LLC"

    return {
        "title": title,
        "subtitle": subtitle or title,
        "eyebrow": eyebrow,
        "hero_image": hero_img or "../content/uploads/2020/09/cropped-favico-192x192.png",
        "location": location or "—",
        "year": opening or "—",
        "services": services or ["Museum Planning"],
        "meta_description": meta_desc,
        "sidebar": {
            "client": client or "—",
            "location": location or "—",
            "opening": opening or "—",
            "services": services_text or ", ".join(services),
        },
    }


def read_shell_parts() -> tuple[str, str]:
    text = SHELL.read_text(encoding="utf-8")
    head_end = text.index("</head>")
    head = text[: head_end + len("</head>")]
    if "wp-archive-prose.css" not in head:
        head = head.replace(
            '<link rel="stylesheet" href="../assets/site-nav.css">',
            '<link rel="stylesheet" href="../assets/site-nav.css">\n'
            '  <link rel="stylesheet" href="../assets/wp-archive-prose.css">',
        )
    footer_start = text.index('<div class="next-projects">')
    footer = text[footer_start:]
    return head, footer


def preserve_tail(live_slug: str, default_footer: str) -> str:
    live_path = ROOT / "projects" / f"{live_slug}.html"
    if not live_path.is_file():
        return default_footer
    text = live_path.read_text(encoding="utf-8")
    if '<div class="next-projects">' not in text:
        return default_footer
    return text[text.index('<div class="next-projects">'):]


def build_page(hero: dict, content_html: str, live_slug: str, footer: str) -> str:
    head, _ = read_shell_parts()
    head = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{escape(hero['title'])} — Museum Planning LLC</title>",
        head,
    )
    head = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{escape(hero["meta_description"], quote=True)}">',
        head,
    )
    head = re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="{SITE}/projects/{live_slug}.html">',
        head,
    )

    service_tags = "".join(f'<span class="service-tag">{escape(s)}</span>' for s in hero["services"])
    sb = hero["sidebar"]
    year_label = "Opened" if re.search(r"\b(19|20)\d{2}\b", hero["year"]) else "Period"

    body = f"""
<body class="project-wp-archive">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PGG4KV35"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<nav class="site-nav" id="site-nav">
  <a href="../index.html" class="nav-logo">Museum <span>Planning</span> LLC</a>
  <button type="button" class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav-menu">
    <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
  </button>
  <ul class="nav-links" id="site-nav-menu">
    <li><a href="../museum-planning-services.html">Services</a></li>
    <li><a href="../for-cities.html">For Cities</a></li>
    <li><a href="../museum-planning-projects.html" class="active">Projects</a></li>
    <li><a href="../museum-school/index.html">Museum School</a></li>
    <li><a href="../thought-leadership.html">Field Notes</a></li>
    <li><a href="../museum-planning-about.html">About</a></li>
    <li class="nav-search"><button type="button" class="search-toggle" id="searchToggle" aria-label="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button></li>
    <li><a href="../museum-planning-contact.html" class="nav-cta">Start a Conversation</a></li>
  </ul>
</nav>

<div class="hero">
  <div class="hero-img" style="background-image: url('{hero["hero_image"]}');"></div>
  <div class="hero-content">
    <div class="breadcrumb">
      <a href="../museum-planning-projects.html">← All Projects</a>
      <span>/</span>
      <span>{escape(hero["title"])}</span>
    </div>
    <div class="hero-eyebrow">{escape(hero["eyebrow"])}</div>
    <h1>{escape(hero["title"])}</h1>
    <p style="font-family:var(--serif);font-size:clamp(18px,2.5vw,24px);color:rgba(255,255,255,.75);max-width:720px;margin-bottom:28px;font-style:italic;">{escape(hero["subtitle"])}</p>
    <div class="hero-meta">
      <div class="meta-item">
        <div class="meta-label">Location</div>
        <div class="meta-value">{escape(hero["location"])}</div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item">
        <div class="meta-label">{year_label}</div>
        <div class="meta-value">{escape(hero["year"])}</div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item">
        <div class="meta-label">Services</div>
        <div class="service-tags">{service_tags}</div>
      </div>
    </div>
  </div>
</div>

<div class="body-wrap">
  <div class="prose wp-archive">
{content_html}
  </div>
  <div class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Project Details</div>
      <div class="detail-row"><span class="detail-key">Client</span><span class="detail-val">{escape(sb["client"])}</span></div>
      <div class="detail-row"><span class="detail-key">Location</span><span class="detail-val">{escape(sb["location"])}</span></div>
      <div class="detail-row"><span class="detail-key">{year_label}</span><span class="detail-val">{escape(sb["opening"])}</span></div>
      <div class="detail-row"><span class="detail-key">Services</span><span class="detail-val">{escape(sb["services"])}</span></div>
    </div>
    <div class="sidebar-card">
      <div class="sidebar-label">Museum Planning LLC</div>
      <h3>Interested in a project like this?</h3>
      <p>Every engagement begins with a conversation. Mark Walhimer is personally involved in all projects — from feasibility through opening day.</p>
    </div>
    <a href="../museum-planning-contact.html" class="btn-cta">Start a Conversation →</a>
  </div>
</div>

"""
    return f'<!DOCTYPE html>\n<html lang="en">\n{head}\n{body}\n{footer}'


def portfolio_redirect_html(target: str) -> str:
    url = f"{SITE}/projects/{target}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0;url={url}">
<title>Redirecting — Museum Planning LLC</title>
</head>
<body>
<p>Moved to <a href="{url}">projects/{target}.html</a>.</p>
</body>
</html>
"""


def source_html_for(project: dict) -> tuple[Path, str]:
    wp_slug = project.get("wp_slug")
    if wp_slug:
        src = SIMPLY_STATIC / "portfolio-item" / wp_slug / "index.html"
        if src.is_file():
            return src, "export"
    if project["live_slug"] == "arizona-natural-resources-museum":
        if not ARIZONA_SOURCE.is_file():
            raise FileNotFoundError(
                f"Missing {ARIZONA_SOURCE}. Save WP HTML snapshot first."
            )
        return ARIZONA_SOURCE, "arizona-snapshot"
    raise FileNotFoundError(f"No HTML source for {project['live_slug']}")


def restore_one(project: dict, dry_run: bool) -> dict:
    wp_slug = project.get("wp_slug") or "university-of-arizona"
    live_slug = OUTPUT_OVERRIDE.get(wp_slug, project["live_slug"])
    src_path, source_kind = source_html_for(project)

    raw = src_path.read_text(encoding="utf-8", errors="replace")
    if source_kind == "arizona-snapshot":
        raw = normalize_wayback_html(raw)

    entry = extract_entry_content(raw)
    cleaned = clean_content(entry, title=project["title"])
    assets = collect_upload_paths(raw)
    assets |= collect_upload_paths(cleaned)

    hero = infer_hero(project, entry, cleaned)
    _, default_footer = read_shell_parts()
    footer = preserve_tail(live_slug, default_footer)
    page = build_page(hero, cleaned, live_slug, footer)

    copied, missing = copy_uploads(assets, dry_run=dry_run)
    out_path = ROOT / "projects" / f"{live_slug}.html"

    result = {
        "live_slug": live_slug,
        "wp_slug": wp_slug,
        "source": str(src_path),
        "content_chars": len(cleaned),
        "images": cleaned.count("<img"),
        "assets": len(assets),
        "copied": copied,
        "missing": missing,
        "out_path": str(out_path.relative_to(ROOT)),
    }

    if dry_run:
        return result

    out_path.write_text(page, encoding="utf-8")
    port_path = ROOT / "portfolio-item" / wp_slug / "index.html"
    port_path.parent.mkdir(parents=True, exist_ok=True)
    port_path.write_text(portfolio_redirect_html(live_slug), encoding="utf-8")
    project["status"] = "skinned"
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", help="Restore one wp_slug or live_slug")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    if not args.write and not args.dry_run:
        ap.error("Pass --write or --dry-run")

    if not SIMPLY_STATIC.is_dir():
        raise SystemExit(f"Simply Static export not found: {SIMPLY_STATIC}")

    manifest = load_manifest()
    projects = manifest["projects"]

    if args.slug:
        targets = [find_project(manifest, args.slug)]
    else:
        targets = []
        for p in projects:
            if p["status"] in SKIP_STATUS:
                continue
            if p.get("wp_slug"):
                targets.append(p)
            elif p["live_slug"] == "arizona-natural-resources-museum":
                targets.append(p)

    default_footer = read_shell_parts()[1]
    results = []
    errors = []

    for project in targets:
        label = project.get("wp_slug") or project["live_slug"]
        try:
            r = restore_one(project, dry_run=not args.write)
            results.append(r)
            miss = f", {len(r['missing'])} missing assets" if r["missing"] else ""
            print(
                f"{'[dry-run] ' if not args.write else ''}{label} → {r['out_path']}: "
                f"{r['content_chars']:,} chars, {r['images']} imgs, {r['copied']} assets{miss}"
            )
            if r["missing"][:5]:
                for m in r["missing"][:5]:
                    print(f"    missing: {m}")
        except Exception as exc:
            errors.append((label, str(exc)))
            print(f"ERROR {label}: {exc}", file=sys.stderr)

    if args.write:
        manifest["export_dir_default"] = str(SIMPLY_STATIC)
        for p in projects:
            if p.get("live_slug") == "arizona-natural-resources-museum":
                p["wp_slug"] = "university-of-arizona"
                p["source"] = "wordpress"
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"\nUpdated {MANIFEST.name}")

    print(f"\nRestored: {len(results)}  Errors: {len(errors)}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
