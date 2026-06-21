#!/usr/bin/env python3
"""Extract WordPress entry-content and wrap in Museum Planning project page shell.

No WordPress theme CSS — site nav, footer, Playfair/Lato styling only.

Usage (repo root):
  python3 tools/skin_wp_portfolio.py --slug c-o-polk-interactive-museum --dry-run
  python3 tools/skin_wp_portfolio.py --slug c-o-polk-interactive-museum --write
"""

from __future__ import annotations

import argparse
import json
import re
from html import escape
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "projects-manifest.json"
SITE = "https://museumplanning.com"
SHELL = ROOT / "projects" / "city-of-mcdonough-georgia.html"

# wp_slug → output page (when live_slug differs from hub URL)
OUTPUT_OVERRIDE = {
    "c-o-polk-interactive-museum": "city-of-mcdonough-georgia",
}

HERO = {
    "c-o-polk-interactive-museum": {
        "title": "C.O. Polk Interactive Museum",
        "subtitle": "Making Local History Relevant to Everyone",
        "eyebrow": "City of McDonough · Turn-key History Museum",
        "hero_image": "../content/uploads/2019/07/JT2A3857-1400x933.jpg",
        "location": "McDonough, Georgia",
        "year": "2019",
        "services": [
            "Master Planning",
            "Exhibition Design",
            "Project Management",
            "Website Design",
        ],
        "meta_description": (
            "C.O. Polk Interactive Museum — turn-key local history museum for the City of "
            "McDonough, Georgia. Master planning, exhibition design, and project management "
            "by Museum Planning LLC."
        ),
        "sidebar": {
            "client": "City of McDonough",
            "location": "McDonough, Georgia",
            "opening": "July 20, 2019",
            "services": "Master Planning, Exhibition Design, Project Management",
            "live_url": "https://copolkmuseum.org/",
        },
    },
}


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_project(manifest: dict, slug: str) -> dict:
    slug = slug.strip().lower()
    for p in manifest["projects"]:
        if p.get("wp_slug") == slug or p["live_slug"] == slug:
            return p
    raise SystemExit(f"Unknown slug: {slug!r}. Use --list.")


def extract_entry_content(html: str) -> str:
    m = re.search(
        r'<div class="entry-content content">(.*?)</div>\s*\n\s*</div>\s*\n\s*<div class="entry-extra">',
        html,
        re.DOTALL | re.I,
    )
    if not m:
        raise SystemExit("Could not find .entry-content in portfolio HTML")
    return m.group(1).strip()


def best_image_src(src: str, srcset: str | None) -> str:
    """Prefer largest -1400 variant from srcset when present."""
    candidates = [src]
    if srcset:
        for part in srcset.split(","):
            u = part.strip().split()[0]
            candidates.append(u)
    best = src
    best_w = 0
    for u in candidates:
        u = u.lstrip("/")
        m = re.search(r"-(\d+)x(\d+)\.", u)
        w = int(m.group(1)) if m else 0
        if w >= best_w:
            best_w = w
            best = u
    return best


def rewrite_upload_path(path: str) -> str:
    path = unquote(path)
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


def clean_content(html: str) -> str:
    # Drop fixed-width caption wrappers
    html = re.sub(r'\s*style="width:\s*\d+px"', "", html, flags=re.I)
    html = re.sub(r'\s*style="text-align:\s*center;"', "", html, flags=re.I)
    html = re.sub(r'<span style="color:\s*#993300;">\s*', "", html, flags=re.I)
    html = re.sub(r"\s*</span>", "", html, count=1)

    html = re.sub(r'\s*allowfullscreen="allowfullscreen"', "", html, flags=re.I)
    html = re.sub(r'\s*frameborder="0"', "", html, flags=re.I)
    html = re.sub(r'\s*width="\d+"\s*height="\d+"', "", html, flags=re.I)

    # Images: upgrade src, drop srcset/sizes/wp classes
    def fix_img(m: re.Match[str]) -> str:
        tag = m.group(0)
        src_m = re.search(r'src="([^"]+)"', tag, re.I)
        srcset_m = re.search(r'srcset="([^"]+)"', tag, re.I)
        if not src_m:
            return tag
        src = src_m.group(1)
        srcset = srcset_m.group(1) if srcset_m else None
        new_src = rewrite_upload_path(best_image_src(src, srcset))
        alt_m = re.search(r'alt="([^"]*)"', tag, re.I)
        alt = alt_m.group(1) if alt_m else ""
        return f'<img src="{new_src}" alt="{escape(alt, quote=True)}" loading="lazy">'

    html = re.sub(r"<img[^>]+>", fix_img, html, flags=re.I)

    # PDF download links (before general href rewrites)
    pdf_block = re.search(
        r"((?:<p>(?:<strong>)?<a href=\"[^\"]+\.pdf\"[^>]*>.*?</a>(?:</strong>)?</p>\s*)+)",
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

    # PDF and internal links
    def fix_href(m: re.Match[str]) -> str:
        href = m.group(1)
        if "contact-museum-planning" in href:
            return 'href="../museum-planning-contact.html"'
        if "wp-content/uploads" in href or href.startswith("../../wp-content"):
            return f'href="{rewrite_upload_path(href)}"'
        return m.group(0)

    html = re.sub(r'href="([^"]+)"', fix_href, html)

    # wp-caption blocks → semantic figure
    html = re.sub(
        r'<div id="attachment_\d+"[^>]*class="wp-caption[^"]*">(.*?)</div>',
        fix_caption_block,
        html,
        flags=re.DOTALL | re.I,
    )

    # Responsive Vimeo embeds
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
    html = re.sub(
        r"(<p>[^<]*?)<br>\s*(<div class=\"video-wrap\">)",
        r"\1</p>\n\2",
        html,
        flags=re.I,
    )
    html = re.sub(r"</div></p>", "</div>", html)
    html = re.sub(r"<p>\s*</p>", "", html)

    # Lead paragraph after title block
    html = re.sub(
        r"<h3[^>]*><strong>C\.O\. Polk Interactive Museum</strong></h3>\s*"
        r"<p[^>]*>(Reimagining the local history museum[^<]+)</p>",
        r'<p class="lead">\1</p>',
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<h3[^>]*><strong>C\.O\. Polk Interactive Museum</strong></h3>\s*",
        "",
        html,
        count=1,
        flags=re.I,
    )

    # Strip remaining inline styles and wp image classes on containers
    html = re.sub(r'\s*class="[^"]*wp-image-\d+[^"]*"', "", html)
    html = re.sub(r'\s*class="[^"]*size-large[^"]*"', "", html)
    html = re.sub(r'\s*class="aligncenter"', "", html)
    html = re.sub(r'\s*decoding="async"', "", html)
    html = re.sub(r'\s*aria-describedby="[^"]*"', "", html)

    return html.strip()


def read_shell_parts() -> tuple[str, str]:
    """Return (head_through_hero_end, footer_from_next_projects)."""
    text = SHELL.read_text(encoding="utf-8")
    # Head ends before body-wrap prose; we rebuild hero + body-wrap
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


def build_page(wp_slug: str, content_html: str) -> str:
    hero = HERO.get(wp_slug)
    if not hero:
        raise SystemExit(f"No HERO config for {wp_slug!r}. Add to skin_wp_portfolio.py.")

    out_slug = OUTPUT_OVERRIDE.get(wp_slug, wp_slug)
    head, footer = read_shell_parts()

    # Patch title/meta in head
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
        f'<link rel="canonical" href="{SITE}/projects/{out_slug}.html">',
        head,
    )

    service_tags = "".join(f'<span class="service-tag">{s}</span>' for s in hero["services"])
    sb = hero["sidebar"]

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
        <div class="meta-label">Opened</div>
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
      <div class="detail-row"><span class="detail-key">Opening</span><span class="detail-val">{escape(sb["opening"])}</span></div>
      <div class="detail-row"><span class="detail-key">Services</span><span class="detail-val">{escape(sb["services"])}</span></div>
    </div>
    <div class="sidebar-card">
      <div class="sidebar-label">See It Live</div>
      <p><a href="{sb["live_url"]}" target="_blank" rel="noopener noreferrer" style="color:var(--navy);font-weight:700;">copolkmuseum.org →</a></p>
    </div>
    <div class="sidebar-card">
      <div class="sidebar-label">Museum Planning LLC</div>
      <h3>Interested in a turn-key museum?</h3>
      <p>Every engagement begins with a conversation. Mark Walhimer is personally involved in all projects — from feasibility through opening day.</p>
    </div>
    <a href="../museum-planning-contact.html" class="btn-cta">Start a Conversation →</a>
  </div>
</div>

"""

    return f"<!DOCTYPE html>\n<html lang=\"en\">\n{head}\n{body}\n{footer}"


def redirect_html(target: str) -> str:
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
<p>Moved to <a href="{url}">{target}.html</a>.</p>
</body>
</html>
"""


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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", required=True, help="wp_slug from manifest")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    manifest = load_manifest()
    project = find_project(manifest, args.slug)
    wp_slug = project.get("wp_slug") or args.slug

    src = ROOT / "portfolio-item" / wp_slug / "index.html"
    if not src.is_file():
        raise SystemExit(f"Missing {src}. Run import_wp_portfolio.py --write first.")

    raw = src.read_text(encoding="utf-8")
    entry = extract_entry_content(raw)
    cleaned = clean_content(entry)
    page = build_page(wp_slug, cleaned)

    out_slug = OUTPUT_OVERRIDE.get(wp_slug, project["live_slug"])
    out_path = ROOT / "projects" / f"{out_slug}.html"

    print(f"Source: {src}")
    print(f"Output: {out_path}")
    print(f"Content: {len(cleaned):,} chars, {cleaned.count('<img')} images, {cleaned.count('video-wrap')} videos")

    if args.dry_run and not args.write:
        preview = ROOT / "tools" / f".skin-preview-{out_slug}.html"
        preview.write_text(page, encoding="utf-8")
        print(f"Dry-run preview: {preview}")
        return

    if not args.write:
        print("Pass --write to save, or --dry-run for preview file.")
        return

    out_path.write_text(page, encoding="utf-8")
    print(f"Wrote {out_path}")

    live_slug = project["live_slug"]
    redirect_slugs = sorted({s for s in (live_slug, wp_slug) if s != out_slug})
    for slug in redirect_slugs:
        live_path = ROOT / "projects" / f"{slug}.html"
        live_path.write_text(redirect_html(out_slug), encoding="utf-8")
        print(f"Wrote redirect {live_path} → {out_slug}.html")

    port_path = ROOT / "portfolio-item" / wp_slug / "index.html"
    port_path.write_text(portfolio_redirect_html(out_slug), encoding="utf-8")
    print(f"Wrote portfolio redirect {port_path}")

    # Update manifest status
    for p in manifest["projects"]:
        if p.get("wp_slug") == wp_slug:
            p["status"] = "skinned"
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Updated manifest status → skinned")


if __name__ == "__main__":
    main()
