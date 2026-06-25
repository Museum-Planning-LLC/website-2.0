#!/usr/bin/env python3
"""Fill hero and sidebar Project Details from projects hub cards and WP snippets.

Usage (repo root):
  python3 tools/patch_project_details.py --dry-run
  python3 tools/patch_project_details.py --write
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "museum-planning-projects.html"
PROJECTS = ROOT / "projects"
MANIFEST = Path(__file__).resolve().parent / "projects-manifest.json"

# Archive-only pages (not on featured hub grid) — curated from WP export copy
ARCHIVE_DETAILS: dict[str, dict] = {
    "air-and-space-science-center-exhibition": {
        "client": "Discovery Science Center",
        "location": "Santa Ana, California",
        "period": "2001",
        "services": "Exhibition Design, Interactive Exhibits",
        "eyebrow": "Science Center Exhibition",
    },
    "amazing-sensations-science-center-exhibition": {
        "client": "Discovery Science Center",
        "location": "Santa Ana, California",
        "period": "2002",
        "services": "Traveling Exhibition, Exhibition Design",
        "eyebrow": "Traveling Exhibition",
    },
    "bolivian-museum": {
        "client": "Bolivian Museum of Modern Art (feasibility group)",
        "location": "Bolivia",
        "period": "Feasibility study",
        "services": "Feasibility Study",
        "eyebrow": "Museum Feasibility",
    },
    "habitot-childrens-museum": {
        "client": "Habitot Children's Museum",
        "location": "Berkeley, California",
        "period": "Exhibition project",
        "services": "Exhibition Design",
        "eyebrow": "Children's Museum",
    },
    "interactive-exhibit-consultant": {
        "client": "Louisiana State Museum",
        "location": "New Orleans, Louisiana",
        "period": "Design workshop",
        "services": "Exhibition Design, Workshop Facilitation",
        "eyebrow": "State Museum",
    },
    "mobius-science-center": {
        "client": "Mobius Science Center",
        "location": "Spokane, Washington",
        "period": "Science center project",
        "services": "Exhibition Design",
        "eyebrow": "Science Center",
    },
    "museum-customer-experience-design": {
        "client": "Museum Planning LLC",
        "location": "United States",
        "period": "Practice resource",
        "services": "Customer Experience Design",
        "eyebrow": "Museum Planning",
    },
    "museum-inclusion-simulator": {
        "client": "Designing Museum Experiences",
        "location": "Online",
        "period": "2021",
        "services": "Interactive Design, Inclusion",
        "eyebrow": "Book Project",
    },
    "museum-planning-workshop": {
        "client": "Museum clients",
        "location": "United States & international",
        "period": "Ongoing",
        "services": "Workshop Facilitation, Master Planning",
        "eyebrow": "Museum Planning Workshop",
    },
    "museum-project-management": {
        "client": "Museum clients",
        "location": "United States & international",
        "period": "Ongoing",
        "services": "Project Management, Owner's Representation",
        "eyebrow": "Project Management",
    },
    "museum-regular-man": {
        "client": "Alex Shear collection group",
        "location": "United States",
        "period": "Feasibility study",
        "services": "Feasibility Study",
        "eyebrow": "Museum Feasibility",
    },
    "nature-play-museum-strategic-planning": {
        "client": "Discovery Center at Murfree Spring",
        "location": "Murfreesboro, Tennessee",
        "period": "2020–2025",
        "services": "Strategic Planning, Nature Exhibition",
        "eyebrow": "Nature Center",
    },
    "poughkeepsie-center-for-arts-creativity-pcac-feasibility-study": {
        "client": "Poughkeepsie Center for Arts & Creativity (PCAC)",
        "location": "Poughkeepsie, New York",
        "period": "2012",
        "services": "Feasibility Study",
        "eyebrow": "Feasibility Study",
    },
    "science-of-surfing": {
        "client": "Discovery Science Center",
        "location": "Santa Ana, California",
        "period": "2001",
        "services": "Traveling Exhibition, Exhibition Design",
        "eyebrow": "Traveling Exhibition",
    },
    "steam-pop-up-museum": {
        "client": "STEAM Pop-up Museum",
        "location": "United States",
        "period": "Mobile exhibition",
        "services": "Exhibition Design, STEAM",
        "eyebrow": "Pop-up Museum",
    },
    "stem-steam-science-center": {
        "client": "Calgary Municipal Land Corporation (CMLC)",
        "location": "Calgary, Alberta, Canada",
        "period": "Public art proposal",
        "services": "Master Planning, STEAM, Public Art",
        "eyebrow": "STEM / STEAM Science Center",
    },
    "trans-studio-science-center": {
        "client": "Trans Studio",
        "location": "Indonesia",
        "period": "Science center project",
        "services": "Exhibition Design, Master Planning",
        "eyebrow": "Science Center",
    },
}

# Hand-built pages — always refresh metadata
FORCE_DETAILS: dict[str, dict] = {
    "city-of-mcdonough-georgia": {
        "client": "City of McDonough",
        "location": "McDonough, Georgia",
        "period": "July 20, 2019",
        "services": "Master Planning, Exhibition Design, Project Management, Website Design",
        "eyebrow": "History Museum",
        "hero_location": "McDonough, Georgia",
        "service_tags": ["Master Planning", "Exhibition Design", "Project Management", "Website Design"],
        "period_label": "Opened",
    },
    "nature-play-museum-strategic-planning": {
        "client": "Discovery Center at Murfree Spring",
        "location": "Murfreesboro, Tennessee",
        "period": "2020–2025",
        "services": "Strategic Planning, Nature Exhibition",
        "eyebrow": "Nature Center",
        "hero_location": "Murfreesboro, Tennessee",
        "service_tags": ["Strategic Planning", "Nature Exhibition"],
        "period_label": "Period",
    },
    "arizona-natural-resources-museum": {
        "client": "University of Arizona",
        "location": "Tucson, Arizona",
        "period": "2022–2023",
        "services": "Feasibility, Master Planning, Exhibition Design",
        "eyebrow": "University Museum",
        "hero_location": "University of Arizona · Tucson, Arizona",
        "service_tags": [
            "Feasibility Study",
            "Master Planning",
            "Exhibition Design",
            "Business Planning",
            "Strategic Planning",
        ],
        "period_label": "Year",
        "extra_rows": [("Opening", "Fall 2025"), ("Sq Footage", "30,000 sq ft total")],
    },
}

# Pages with hand-built sidebar — patch blank fields even when client is set
SKIP_IF_CLIENT_SET = False


def load_hub_cards() -> dict[str, dict]:
    text = HUB.read_text(encoding="utf-8")
    cards: dict[str, dict] = {}
    for m in re.finditer(
        r'<a href="projects/([^"]+)\.html" class="project-card"[^>]*>(.*?)</div>\s*\n\s*</div>\s*\n\s*</a>',
        text,
        re.DOTALL,
    ):
        slug, block = m.group(1), m.group(2)

        def grab(pat: str) -> str:
            x = re.search(pat, block)
            return x.group(1).strip() if x else ""

        cards[slug] = {
            "eyebrow": grab(r'card-meta">([^<]+)'),
            "title": grab(r'card-title">([^<]+)'),
            "location": grab(r'card-location">([^<]+)'),
            "period": grab(r'card-type-badge">([^<]+)'),
            "services": re.findall(r'service-tag">([^<]+)', block),
        }
    return cards


def split_client_location(location: str) -> tuple[str, str]:
    if " · " in location:
        a, b = location.split(" · ", 1)
        if any(w in a.lower() for w in ("university", "city of", "county", "museum", "llc", "inc")):
            return a.strip(), b.strip()
    return "", location.strip()


def hub_to_details(card: dict) -> dict:
    client, loc = split_client_location(card["location"])
    if not client:
        client = card["title"]
    if " · " in card["location"] and not loc:
        loc = card["location"].split(" · ", 1)[-1].strip()
    if card["slug"] == "alcatraz-traveling-exhibition" and " · " in card["location"]:
        parts = card["location"].split(" · ", 1)
        client = parts[1].strip()
        loc = parts[0].strip()
    services = ", ".join(card["services"])
    return {
        "client": client,
        "location": loc or card["location"],
        "period": card["period"] or "—",
        "services": services,
        "eyebrow": card["eyebrow"] or card["title"],
        "title": card["title"],
        "hero_location": card["location"],
        "service_tags": card["services"],
    }


def infer_from_page(text: str) -> dict:
    out: dict = {}
    for label, key in (
        ("Client", "client"),
        ("Location", "location"),
        ("Period", "period"),
        ("Date", "period"),
        ("Year", "period"),
        ("Opening Date", "period"),
        ("Services", "services"),
        ("Role", "services"),
    ):
        m = re.search(rf"<strong>{label}:?</strong>\s*([^<\n]+)", text, re.I)
        if m and key not in out:
            out[key] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    h1 = re.search(r"<h1[^>]*>([^<]+)</h1>", text)
    if h1 and "title" not in out:
        out["title"] = h1.group(1).strip()
    return out


def period_label(period: str) -> str:
    if re.search(r"opening|fall|spring|summer|winter", period, re.I):
        return "Opening"
    if re.search(r"\d{4}\s*[–-]\s*\d{4}", period):
        return "Period"
    if re.search(r"\b(19|20)\d{2}\b", period):
        return "Year"
    return "Period"


def is_blank_val(val: str) -> bool:
    return not val or val.strip() in ("—", "-", "?")


def service_tags_html(tags: list[str]) -> str:
    if not tags:
        return '<span class="service-tag">Museum Planning</span>'
    return "".join(f'<span class="service-tag">{html.escape(t)}</span>' for t in tags)


def patch_detail_row(page: str, key: str, value: str, force: bool = False) -> str:
    if is_blank_val(value):
        return page
    pat = rf'(<span class="detail-key">{re.escape(key)}</span><span class="detail-val">)([^<]*)(</span>)'

    def repl(m: re.Match[str]) -> str:
        if not force and not is_blank_val(m.group(2)):
            return m.group(0)
        return f"{m.group(1)}{html.escape(value)}{m.group(3)}"

    return re.sub(pat, repl, page, count=1)


def patch_hero_meta(page: str, details: dict, force: bool = False) -> str:
    loc = details.get("hero_location") or details.get("location", "")
    period = details.get("period", "")
    tags = details.get("service_tags") or [
        s.strip() for s in details.get("services", "").split(",") if s.strip()
    ]
    plabel = details.get("period_label") or period_label(period)

    if is_blank_val(loc) and is_blank_val(period):
        return page

    # Skip if hero already populated unless force
    if not force:
        meta = re.search(r'<div class="meta-value">([^<]*)</div>', page)
        if meta and not is_blank_val(meta.group(1)):
            loc_ok = re.search(
                r'<div class="meta-label">Location</div>\s*<div class="meta-value">([^<]+)</div>',
                page,
            )
            if loc_ok and not is_blank_val(loc_ok.group(1)):
                return page

    block = f"""    <div class="hero-meta">
      <div class="meta-item">
        <div class="meta-label">Location</div>
        <div class="meta-value">{html.escape(loc)}</div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item">
        <div class="meta-label">{plabel}</div>
        <div class="meta-value">{html.escape(period)}</div>
      </div>
      <div class="meta-divider"></div>
      <div class="meta-item">
        <div class="meta-label">Services</div>
        <div class="service-tags">{service_tags_html(tags)}</div>
      </div>
    </div>"""

    return re.sub(
        r"<div class=\"hero-meta\">.*?</div>\s*\n\s*</div>\s*\n</div>",
        block + "\n  </div>\n</div>",
        page,
        count=1,
        flags=re.DOTALL,
    )


def patch_eyebrow(page: str, eyebrow: str) -> str:
    if is_blank_val(eyebrow):
        return page
    return re.sub(
        r'(<div class="hero-eyebrow">)[^<]*(</div>)',
        lambda m: f"{m.group(1)}{html.escape(eyebrow)}{m.group(2)}",
        page,
        count=1,
    )


def build_details(slug: str, hub: dict[str, dict]) -> dict | None:
    if slug in FORCE_DETAILS:
        d = FORCE_DETAILS[slug].copy()
        d.setdefault("title", slug.replace("-", " ").title())
        d.setdefault("hero_location", d.get("location", ""))
        d.setdefault("service_tags", [s.strip() for s in d.get("services", "").split(",") if s.strip()])
        return d
    if slug in hub:
        card = hub[slug].copy()
        card["slug"] = slug
        return hub_to_details(card)
    if slug in ARCHIVE_DETAILS:
        d = ARCHIVE_DETAILS[slug].copy()
        d["title"] = d.get("title", slug.replace("-", " ").title())
        d["hero_location"] = d.get("location", "")
        d["service_tags"] = [s.strip() for s in d.get("services", "").split(",") if s.strip()]
        return d
    return None


def is_redirect(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    return 'http-equiv="refresh"' in text and len(text) < 2500


def patch_file(path: Path, details: dict, write: bool) -> bool:
    page = path.read_text(encoding="utf-8")
    original = page
    force = path.stem in FORCE_DETAILS

    page = patch_eyebrow(page, details.get("eyebrow", ""))
    page = patch_hero_meta(page, details, force=force)

    plabel = details.get("period_label") or period_label(details.get("period", ""))
    page = patch_detail_row(page, "Client", details.get("client", ""), force=force)
    page = patch_detail_row(page, "Location", details.get("location", ""), force=force)
    page = patch_detail_row(page, plabel, details.get("period", ""), force=force)
    if plabel != "Period":
        page = patch_detail_row(page, "Period", details.get("period", ""), force=False)
    if plabel != "Year":
        page = patch_detail_row(page, "Year", details.get("period", ""), force=False)
    if plabel != "Opening":
        page = patch_detail_row(page, "Opening", details.get("period", ""), force=False)
    page = patch_detail_row(page, "Services", details.get("services", ""), force=force)

    for key, val in details.get("extra_rows", []):
        page = patch_detail_row(page, key, val, force=force)

    if page != original:
        if write:
            path.write_text(page, encoding="utf-8")
        return True
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.write and not args.dry_run:
        ap.error("Pass --write or --dry-run")

    hub = load_hub_cards()
    patched = 0
    skipped = 0
    missing = []

    for path in sorted(PROJECTS.glob("*.html")):
        if path.stem in ("index",) or is_redirect(path):
            continue
        details = build_details(path.stem, hub)
        if not details:
            inferred = infer_from_page(path.read_text(encoding="utf-8", errors="replace"))
            if inferred.get("client") or inferred.get("location"):
                details = {
                    "client": inferred.get("client", ""),
                    "location": inferred.get("location", ""),
                    "period": inferred.get("period", ""),
                    "services": inferred.get("services", ""),
                    "eyebrow": inferred.get("title", ""),
                    "hero_location": inferred.get("location", ""),
                    "service_tags": [],
                }
        if not details:
            missing.append(path.stem)
            continue
        if patch_file(path, details, write=args.write):
            patched += 1
            print(f"{'[dry-run] ' if not args.write else ''}patched {path.name}")
        else:
            skipped += 1

    print(f"\nPatched: {patched}  Skipped (already set): {skipped}  No metadata: {len(missing)}")
    if missing:
        for s in missing:
            print(f"  missing: {s}")


if __name__ == "__main__":
    main()
