#!/usr/bin/env python3
"""Build one Museum Planning project page from WordPress Simply Static export.

Extracts entry-content images, PDFs, and Vimeo IDs; copies full-resolution
assets into content/uploads/projects/<live_slug>/; writes projects/<live_slug>.html
from the Alcatraz landing / traveling templates; updates portfolio-item redirect.

Usage (repo root):
  python3 tools/build_project_page.py --list
  python3 tools/build_project_page.py --slug mide-museo-interactivo-de-economia --dry-run
  python3 tools/build_project_page.py --slug bolivian-museum --write

Requires export at ~/Desktop/museum-export (or --export-dir).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).resolve().parent / "projects-manifest.json"
SITE = "https://museumplanning.com"

THUMB_RE = re.compile(
    r"(-\d+x\d+|-scaled|-rotated)(?=\.[a-z0-9]+$)",
    re.IGNORECASE,
)
GENERIC_PDFS = {
    "museum_planning.pdf",
    "museum-planning-llc-process.pdf",
}
REDIRECT_STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={canonical}">
<title>Redirecting — Museum Planning LLC</title>
</head>
<body>
<p>Moved to <a href="{canonical}">projects/{live_slug}.html</a>.</p>
</body>
</html>
"""


@dataclass
class VideoAsset:
    vimeo_id: str
    title: str = "Project video"


@dataclass
class PdfAsset:
    label: str
    repo_path: str
    external: bool = False


@dataclass
class PhotoAsset:
    file_name: str
    alt: str
    aspect: str = "aspect-land"


@dataclass
class ProjectBuild:
    wp_slug: str
    live_slug: str
    title: str
    template: str
    paragraphs: list[str] = field(default_factory=list)
    photos: list[PhotoAsset] = field(default_factory=list)
    pdfs: list[PdfAsset] = field(default_factory=list)
    videos: list[VideoAsset] = field(default_factory=list)
    hero_file: str = ""
    missing_files: list[str] = field(default_factory=list)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_project(manifest: dict, slug: str) -> dict:
    slug = slug.strip().lower()
    for p in manifest["projects"]:
        if p.get("wp_slug") == slug or p["live_slug"] == slug:
            return p
    raise SystemExit(f"Unknown project slug: {slug!r}. Run with --list.")


def expand_path(p: str) -> Path:
    return Path(p.replace("~", str(Path.home()))).expanduser().resolve()


def normalize_upload_url(url: str) -> str | None:
    url = unquote(url.split("?")[0].strip())
    if not url:
        return None
    url = re.sub(r"^https?://museumplanning\.com", "", url, flags=re.I)
    url = re.sub(r"^https?://museum-planning-wordpress\.local", "", url, flags=re.I)
    if url.startswith("/"):
        url = url[1:]
    if "wp-content/uploads/" not in url.lower():
        return None
    idx = url.lower().index("wp-content/uploads/")
    return url[idx:]


def base_stem(filename: str) -> str:
    """Collapse WP size variants (photo-300x200.jpg, photo-1400x906.jpg) → photo."""
    stem = Path(filename).stem
    prev = None
    while stem != prev:
        prev = stem
        stem = re.sub(r"-\d+x\d+$", "", stem, flags=re.I)
        stem = re.sub(r"-(?:scaled|rotated)$", "", stem, flags=re.I)
    return stem.lower()


def is_image(path: str) -> bool:
    return Path(path).suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}


def extract_entry_content(page_html: str) -> str:
    m = re.search(
        r'<div class="entry-content content">\s*(.*?)\s*</div>\s*\n?\s*</div>\s*\n?\s*<footer',
        page_html,
        re.S | re.I,
    )
    return m.group(1) if m else ""


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text


def clean_title(raw: str) -> str:
    t = html.unescape(re.sub(r"\s+", " ", raw)).strip()
    t = re.sub(r"\s*\|\s*Museum Planning LLC\s*$", "", t, flags=re.I)
    if "book by mark walhimer" in t.lower():
        return "Designing Museum Experiences"
    if t.lower().startswith("full service traveling"):
        return "Alcatraz: Life on the Rock"
    return t


def parse_paragraphs(entry: str) -> list[str]:
    paras: list[str] = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", entry, re.S | re.I):
        inner = m.group(1)
        if re.search(r"amazon-adsystem|iframe|widget", inner, re.I):
            continue
        text = strip_tags(inner)
        if len(text) < 15:
            continue
        paras.append(text)
    return paras


def collect_upload_urls(entry: str) -> list[str]:
    urls: list[str] = []
    for m in re.finditer(r'(?:src|href)="([^"]+)"', entry, re.I):
        urls.append(m.group(1))
    for m in re.finditer(r"srcset=\"([^\"]+)\"", entry, re.I):
        for part in m.group(1).split(","):
            u = part.strip().split()[0]
            urls.append(u)
    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        n = normalize_upload_url(u)
        if n and n not in seen:
            seen.add(n)
            out.append(n)
    return out


def extract_videos(entry: str) -> list[VideoAsset]:
    videos: list[VideoAsset] = []
    seen: set[str] = set()
    for m in re.finditer(
        r'<iframe[^>]+src="https://player\.vimeo\.com/video/(\d+)[^"]*"[^>]*(?:title="([^"]*)")?',
        entry,
        re.I,
    ):
        vid = m.group(1)
        if vid in seen:
            continue
        seen.add(vid)
        title = html.unescape(m.group(2) or "Project video")
        videos.append(VideoAsset(vimeo_id=vid, title=title))
    for m in re.finditer(r"player\.vimeo\.com/video/(\d+)", entry):
        vid = m.group(1)
        if vid not in seen:
            seen.add(vid)
            videos.append(VideoAsset(vimeo_id=vid))
    return videos


def pick_best_upload(paths: list[str], export_dir: Path) -> str | None:
    """Choose largest full-resolution file from a group of WP size variants."""
    candidates: list[tuple[int, str]] = []
    for rel in paths:
        full = export_dir / rel
        if not full.is_file():
            continue
        size = full.stat().st_size
        candidates.append((size, rel))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def slugify_filename(stem: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return s or "image"


def copy_image(
    rel_upload: str,
    export_dir: Path,
    dest_dir: Path,
    dry_run: bool,
    dest_name: str | None = None,
) -> tuple[str | None, str | None]:
    """Copy full-res image; return (file_name, error)."""
    src = export_dir / rel_upload
    if not src.is_file():
        return None, rel_upload
    ext = src.suffix.lower()
    if ext == ".jpeg":
        ext = ".jpg"
    name = dest_name or (slugify_filename(base_stem(src.name)) + ext)
    dest = dest_dir / name
    web = dest_dir / f"{dest.stem}-1400{ext if ext != '.png' else '.jpg'}"
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        if ext in {".jpg", ".jpeg", ".png", ".webp"}:
            try:
                out_ext = ".jpg" if ext in {".jpg", ".jpeg", ".webp"} else ".jpg"
                web = dest_dir / f"{dest.stem}-1400{out_ext}"
                subprocess.run(
                    ["sips", "-Z", "1400", str(dest), "--out", str(web)],
                    check=True,
                    capture_output=True,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                shutil.copy2(dest, web)
        else:
            web = dest
    return name, None


def parse_project(
    project: dict,
    export_dir: Path,
    template_hint: str | None,
) -> ProjectBuild:
    wp_slug = project.get("wp_slug")
    if not wp_slug:
        raise SystemExit(
            f"{project['live_slug']} has no WordPress export entry (source: local-only). "
            "Use Local or add export first."
        )
    page_path = export_dir / "portfolio-item" / wp_slug / "index.html"
    if not page_path.is_file():
        raise SystemExit(f"Missing export page: {page_path}")

    page_html = page_path.read_text(encoding="utf-8", errors="replace")
    title_m = re.search(r"<title>([^<|]+)", page_html)
    title = clean_title(project.get("title") or (title_m.group(1) if title_m else wp_slug))
    entry = extract_entry_content(page_html)
    if not entry:
        raise SystemExit(f"No entry-content found in {page_path}")

    videos = extract_videos(entry)
    template = template_hint or project.get("template") or ("traveling" if videos else "landing")

    build = ProjectBuild(
        wp_slug=wp_slug,
        live_slug=project["live_slug"],
        title=title,
        template=template,
        paragraphs=parse_paragraphs(entry),
        videos=videos,
    )

    upload_urls = collect_upload_urls(entry)
    pdfs = [u for u in upload_urls if u.lower().endswith(".pdf")]
    images = [u for u in upload_urls if is_image(u)]

    # PDFs
    seen_pdf: set[str] = set()
    for rel in pdfs:
        base = Path(rel).name.lower()
        if base in GENERIC_PDFS:
            continue
        if rel in seen_pdf:
            continue
        seen_pdf.add(rel)
        label = Path(rel).stem.replace("-", " ").replace("_", " ")
        build.pdfs.append(
            PdfAsset(
                label=label,
                repo_path=f"../content/uploads/projects/{build.live_slug}/documents/{Path(rel).name}",
            )
        )

    # Images — group by base stem, pick largest file
    groups: dict[str, list[str]] = {}
    for rel in images:
        groups.setdefault(base_stem(Path(rel).name), []).append(rel)

    photos_dir = ROOT / "content/uploads/projects" / build.live_slug / "photos"
    for _stem, variants in sorted(groups.items()):
        best = pick_best_upload(variants, export_dir)
        if not best:
            build.missing_files.extend(variants[:1])
            continue
        alt_m = re.search(
            rf'src="[^"]*{re.escape(Path(best).name)}"[^>]*alt="([^"]*)"',
            entry,
            re.I,
        )
        alt = html.unescape(alt_m.group(1)) if alt_m else title
        canonical = slugify_filename(base_stem(Path(best).name)) + (
            ".jpg" if Path(best).suffix.lower() in {".jpg", ".jpeg", ".webp"} else Path(best).suffix.lower()
        )
        name, err = copy_image(best, export_dir, photos_dir, dry_run=True, dest_name=canonical)
        if err:
            build.missing_files.append(err)
            continue
        assert name
        aspect = "aspect-port" if "portrait" in alt.lower() or "poster" in best.lower() else "aspect-land"
        build.photos.append(PhotoAsset(file_name=name, alt=alt or title, aspect=aspect))

    if build.photos:
        # Prefer a wide exterior / hero-sized image over alphabetical thumb
        build.hero_file = max(
            build.photos,
            key=lambda p: (
                "exterior" in p.file_name.lower() or "hero" in p.alt.lower(),
                "1400" in p.file_name or "1030" in p.file_name,
                p.file_name,
            ),
        ).file_name
    return build


def materialize_assets(build: ProjectBuild, export_dir: Path) -> None:
    photos_dir = ROOT / "content/uploads/projects" / build.live_slug / "photos"
    docs_dir = ROOT / "content/uploads/projects" / build.live_slug / "documents"
    page_path = export_dir / "portfolio-item" / build.wp_slug / "index.html"
    entry = extract_entry_content(page_path.read_text(encoding="utf-8", errors="replace"))
    upload_urls = collect_upload_urls(entry)

    images = [u for u in upload_urls if is_image(u)]
    groups: dict[str, list[str]] = {}
    for rel in images:
        groups.setdefault(base_stem(Path(rel).name), []).append(rel)

    build.photos.clear()
    build.missing_files.clear()
    for _stem, variants in sorted(groups.items()):
        best = pick_best_upload(variants, export_dir)
        if not best:
            build.missing_files.extend(variants[:1])
            continue
        alt_m = re.search(
            rf'src="[^"]*{re.escape(Path(best).name)}"[^>]*alt="([^"]*)"',
            entry,
            re.I,
        )
        alt = html.unescape(alt_m.group(1)) if alt_m else build.title
        canonical = slugify_filename(base_stem(Path(best).name)) + (
            ".jpg" if Path(best).suffix.lower() in {".jpg", ".jpeg", ".webp"} else Path(best).suffix.lower()
        )
        name, err = copy_image(best, export_dir, photos_dir, dry_run=False, dest_name=canonical)
        if err:
            build.missing_files.append(err)
            continue
        assert name
        aspect = "aspect-port" if "portrait" in (alt or "").lower() else "aspect-land"
        build.photos.append(PhotoAsset(file_name=name, alt=alt or build.title, aspect=aspect))

    if build.photos:
        build.hero_file = max(
            build.photos,
            key=lambda p: (
                "exterior" in p.file_name.lower() or "hero" in p.alt.lower(),
                "1400" in p.file_name or "1030" in p.file_name,
                p.file_name,
            ),
        ).file_name

    docs_dir.mkdir(parents=True, exist_ok=True)
    for pdf in build.pdfs:
        fname = Path(pdf.repo_path).name
        rel = None
        for u in upload_urls:
            if u.lower().endswith(".pdf") and Path(u).name == fname:
                rel = u
                break
        if rel:
            src = export_dir / rel
            if src.is_file():
                shutil.copy2(src, docs_dir / fname)
            else:
                build.missing_files.append(rel)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def photo_ext(name: str) -> str:
    return Path(name).suffix.lower()


def render_gallery(build: ProjectBuild) -> str:
    if not build.photos:
        return ""
    items = []
    for i, ph in enumerate(build.photos):
        ext = photo_ext(ph.file_name)
        stem = Path(ph.file_name).stem
        web = f"{stem}-1400{ext if ext in {'.jpg', '.jpeg'} else '.jpg'}"
        wide = ' wide' if i == 1 else ""
        items.append(
            f"""    <button type="button" class="gallery-item {ph.aspect}{wide} gallery-expand" """
            f"""data-full="../content/uploads/projects/{build.live_slug}/photos/{ph.file_name}" """
            f"""aria-label="Expand photo: {esc(ph.alt)}">
      <img src="../content/uploads/projects/{build.live_slug}/photos/{web}" alt="{esc(ph.alt)}" loading="lazy">
    </button>"""
        )
    return f"""
<div class="gallery">
  <div class="gallery-label">Photography</div>
  <p class="gallery-intro">Project photography from the Museum Planning LLC archive — click any image to expand full resolution.</p>
  <div class="gallery-grid">
{chr(10).join(items)}
  </div>
  <p class="gallery-caption">Click any image to expand</p>
</div>"""


def render_documents(build: ProjectBuild) -> str:
    if not build.pdfs:
        return ""
    links = "\n".join(
        f'      <li><a href="{esc(p.repo_path)}">{esc(p.label)} (PDF)</a></li>'
        for p in build.pdfs
    )
    return f"""
      <h2>Project Documents</h2>
      <ul>
{links}
      </ul>"""


def render_videos(build: ProjectBuild) -> str:
    if not build.videos:
        return ""
    blocks = []
    for v in build.videos:
        blocks.append(
            f"""    <div class="video-block">
      <div class="video-wrap" data-vimeo-id="{esc(v.vimeo_id)}" data-vimeo-title="{esc(v.title)}">
        <button type="button" class="video-poster-btn" aria-label="Play {esc(v.title)}">
          <div class="video-play-btn" aria-hidden="true"></div>
        </button>
      </div>
      <p class="gallery-caption">{esc(v.title)}</p>
    </div>"""
        )
    return f"""
<div class="gallery">
  <div class="gallery-label">Film</div>
  <p class="gallery-intro">Video from the Museum Planning LLC project archive.</p>
  <div class="video-grid">
{chr(10).join(blocks)}
  </div>
</div>"""


def render_prose(build: ProjectBuild) -> str:
    if build.paragraphs:
        body = "\n".join(f"      <p>{esc(p)}</p>" for p in build.paragraphs)
    else:
        body = f"      <p>Museum Planning LLC project archive — {esc(build.title)}.</p>"
    docs = render_documents(build)
    return f"""
      <h2>Project Overview</h2>
{body}{docs}"""


def render_hero(build: ProjectBuild) -> str:
    hero_img = build.hero_file or "placeholder.jpg"
    stem = Path(hero_img).stem
    ext = photo_ext(hero_img)
    web = f"{stem}-1400{ext if ext in {'.jpg', '.jpeg'} else '.jpg'}"
    overview = build.paragraphs[0][:160] + ("…" if build.paragraphs and len(build.paragraphs[0]) > 160 else "")
    if not overview:
        overview = f"Museum Planning LLC — {build.title}"
    meta_desc = esc(overview)
    return f"""  <div class="hero-img" style="background-image: url('../content/uploads/projects/{build.live_slug}/photos/{web}');"></div>
  <div class="hero-content">
    <div class="breadcrumb">
      <a href="../museum-planning-projects.html">← All Projects</a>
      <span>/</span>
      <span>Project Archive</span>
    </div>
    <div class="hero-eyebrow">Museum Planning LLC · Project Archive</div>
    <h1>{esc(build.title)}</h1>
    <div class="hero-meta">
      <div class="meta-item">
        <div class="meta-label">Consultant</div>
        <div class="meta-value">Museum Planning, LLC</div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item">
        <div class="meta-label">Lead</div>
        <div class="meta-value">Mark Walhimer, Managing Partner</div>
      </div>
    </div>
  </div>"""


def render_sidebar(build: ProjectBuild) -> str:
    return f"""
    <div class="sidebar-card">
      <div class="sidebar-label">Project Details</div>
      <div class="detail-row"><span class="detail-key">Project</span><span class="detail-val">{esc(build.title)}</span></div>
      <div class="detail-row"><span class="detail-key">Consultant</span><span class="detail-val">Museum Planning, LLC</span></div>
      <div class="detail-row"><span class="detail-key">Lead</span><span class="detail-val">Mark Walhimer, Managing Partner</span></div>
      <div class="detail-row"><span class="detail-key">Archive</span><span class="detail-val">{len(build.photos)} photos · {len(build.pdfs)} PDFs · {len(build.videos)} videos</span></div>
    </div>
    <div class="sidebar-card">
      <div class="sidebar-label">Museum Planning LLC</div>
      <h3>Interested in a project like this?</h3>
      <p>Every engagement begins with a conversation. Mark Walhimer is personally involved in all projects — from the first feasibility study through opening day.</p>
    </div>
    <a href="mailto:mark@museumplanning.com" class="btn-cta">Start a Conversation →</a>"""


def render_page(build: ProjectBuild) -> str:
    tpl_name = (
        "alcatraz-traveling-exhibition.html"
        if build.template == "traveling"
        else "alcatraz-landing.html"
    )
    template = (ROOT / "projects" / tpl_name).read_text(encoding="utf-8")

    canonical = f"{SITE}/projects/{build.live_slug}.html"
    overview = build.paragraphs[0][:155] if build.paragraphs else build.title
    meta_desc = esc(f"Museum Planning LLC — {overview}")

    template = re.sub(
        r"<title>[^<]*</title>",
        f"<title>{esc(build.title)} — Museum Planning LLC</title>",
        template,
        count=1,
    )
    template = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{meta_desc}">',
        template,
        count=1,
    )
    template = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="{canonical}">',
        template,
        count=1,
    )

    middle = f"""<div class="hero">
{render_hero(build)}
</div>

<div class="body-wrap">
  <div class="prose">
{render_prose(build)}
  </div>
  <div class="sidebar">
{render_sidebar(build)}
  </div>
</div>
{render_gallery(build)}
{render_videos(build)}"""

    new_html, count = re.subn(
        r"<div class=\"hero\">.*?<div class=\"gallery-lightbox\"",
        middle + '\n\n<div class="gallery-lightbox"',
        template,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit("Template surgery failed — hero/gallery-lightbox block not found.")
    return new_html


def write_redirect(build: ProjectBuild) -> None:
    out = ROOT / "portfolio-item" / build.wp_slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    canonical = f"{SITE}/projects/{build.live_slug}.html"
    out.write_text(
        REDIRECT_STUB.format(canonical=canonical, live_slug=build.live_slug),
        encoding="utf-8",
    )


def write_assets_manifest(build: ProjectBuild) -> None:
    out = ROOT / "projects" / f"{build.live_slug}.assets.json"
    data = {
        "live_slug": build.live_slug,
        "wp_slug": build.wp_slug,
        "title": build.title,
        "photos": [p.file_name for p in build.photos],
        "pdfs": [Path(p.repo_path).name for p in build.pdfs],
        "videos": [{"vimeo_id": v.vimeo_id, "title": v.title} for v in build.videos],
        "missing_files": build.missing_files,
    }
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def print_report(build: ProjectBuild) -> None:
    print(f"\n{build.title}")
    print(f"  live: projects/{build.live_slug}.html")
    print(f"  wp:   portfolio-item/{build.wp_slug}/")
    print(f"  template: {build.template}")
    print(f"  photos: {len(build.photos)}  pdfs: {len(build.pdfs)}  videos: {len(build.videos)}")
    print(f"  paragraphs: {len(build.paragraphs)}")
    if build.missing_files:
        print("  MISSING:")
        for m in build.missing_files:
            print(f"    - {m}")


def list_projects(manifest: dict) -> None:
    print(f"{'#':>3}  {'status':8}  {'live_slug':42}  title")
    print("-" * 100)
    n = 0
    for p in manifest["projects"]:
        if p["status"] == "done":
            continue
        n += 1
        src = p.get("source", "export")
        status = p["status"] if p["status"] != "pending" else src
        print(f"{n:3}  {status:8}  {p['live_slug']:42}  {p['title'][:50]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build one project page from WP export.")
    parser.add_argument("--slug", help="live_slug or wp_slug from manifest")
    parser.add_argument("--export-dir", help="Simply Static export folder")
    parser.add_argument("--template", choices=["landing", "traveling", "auto"], default="auto")
    parser.add_argument("--list", action="store_true", help="List migratable projects")
    parser.add_argument("--dry-run", action="store_true", help="Report only; do not write files")
    parser.add_argument("--write", action="store_true", help="Copy assets and write HTML")
    args = parser.parse_args()

    manifest = load_manifest()
    if args.list:
        list_projects(manifest)
        return

    if not args.slug:
        parser.error("Provide --slug or use --list")

    project = find_project(manifest, args.slug)
    if project["status"] == "done":
        raise SystemExit(f"{project['live_slug']} is already marked done (Alcatraz). Pick another.")

    export_dir = expand_path(args.export_dir or manifest.get("export_dir_default", "~/Desktop/museum-export"))
    if not export_dir.is_dir():
        raise SystemExit(f"Export dir not found: {export_dir}")

    template_hint = None if args.template == "auto" else args.template
    build = parse_project(project, export_dir, template_hint)

    if args.write:
        materialize_assets(build, export_dir)
        page_html = render_page(build)
        out_html = ROOT / "projects" / f"{build.live_slug}.html"
        out_html.write_text(page_html, encoding="utf-8")
        write_redirect(build)
        write_assets_manifest(build)
        project["status"] = "migrated"
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out_html.relative_to(ROOT)}")
        print_report(build)
        print("\nNext: preview with python3 -m http.server, review prose/hero, then git commit.")
    else:
        print_report(build)
        if not args.dry_run:
            print("\nDry-run (no files written). Use --write to generate the page and copy assets.")


if __name__ == "__main__":
    main()
