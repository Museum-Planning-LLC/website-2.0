#!/usr/bin/env python3
"""Migrate exhibition design series from museum-planner-2.0 into Museum School."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/markwalhimer/Documents/GitHub/museum-planner-2.0/exhibition-design")
OUT = REPO / "museum-school" / "museum-exhibition-design"

FILES = {
    "museum-exhibition-design-hub.html": "index.html",
    "exhibition-design-part-i.html": "exhibition-design-part-i.html",
    "exhibition-design-part-ii.html": "exhibition-design-part-ii.html",
    "exhibition-design-part-iii.html": "exhibition-design-part-iii.html",
    "exhibition-design-part-iv.html": "exhibition-design-part-iv.html",
    "exhibition-design-part-v.html": "exhibition-design-part-v.html",
    "exhibition-design-part-vi.html": "exhibition-design-part-vi.html",
}

BASE = "https://museumplanning.com/museum-school/museum-exhibition-design"

META = {
    "index.html": (
        "Museum Exhibition Design Guide — Museum Planning LLC",
        "Museum exhibition design from planning through maintenance — a six-part reference series by Mark Walhimer, Museum Planning LLC.",
    ),
    "exhibition-design-part-i.html": (
        "Museum Exhibition Design Part I: Planning — Museum Planning LLC",
        "Exhibition design planning — visitor objectives, project charter, budget, and schedule before anyone draws anything.",
    ),
    "exhibition-design-part-ii.html": (
        "Museum Exhibition Design Part II: Design — Museum Planning LLC",
        "Exhibition script, schematic design, design development, and final design documents for museum galleries.",
    ),
    "exhibition-design-part-iii.html": (
        "Museum Exhibition Design Part III: Fabrication — Museum Planning LLC",
        "Translating exhibition drawings into built exhibits — fabricator selection, working drawings, and quality control.",
    ),
    "exhibition-design-part-iv.html": (
        "Museum Exhibition Design Part IV: Installation — Museum Planning LLC",
        "Museum exhibition installation — load-in, staging, punch list, soft opening, and the 26-step installation checklist.",
    ),
    "exhibition-design-part-v.html": (
        "Museum Exhibition Design Part V: Maintenance — Museum Planning LLC",
        "Keeping museum exhibits operational — maintenance manuals, staff training, content updates, and evaluation.",
    ),
    "exhibition-design-part-vi.html": (
        "Museum Exhibition Design: Full Process — Museum Planning LLC",
        "The complete museum exhibition design process from first meeting through long-term operation — executive summary and checklist.",
    ),
}

NAV = """<nav class="site-nav" id="site-nav">
  <a href="../../index.html" class="nav-logo">Museum <span>Planning</span> LLC</a>
  <button type="button" class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav-menu">
    <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
  </button>
  <ul class="nav-links" id="site-nav-menu">
    <li><a href="../../museum-planning-services.html">Services</a></li>
    <li><a href="../../for-cities.html">For Cities</a></li>
    <li><a href="../../for-universities.html">For Universities</a></li>
    <li><a href="../../museum-planning-projects.html">Projects</a></li>
    <li><a href="../index.html" class="active">Museum School</a></li>
    <li><a href="../../for-cities-science-center.html">Science Centers</a></li>
    <li><a href="../../museum-planning-about.html">About</a></li>
    <li><a href="../../museum-planning-contact.html">Contact</a></li>
    <li class="nav-search"><button class="search-toggle" id="searchToggle" aria-label="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button></li>
    <li><a href="../../museum-planning-contact.html" class="nav-cta">Start a Conversation</a></li>
  </ul>
</nav>"""

TIER3_BAND = """
<div class="tier3-band">
  <div class="tier3-inner">
    <div class="tier3-label">Commercial guide</div>
    <p class="tier3-body">This series is educational reference. For exhibition design engagements — process, deliverables, and typical fees — see <a href="../../museum-planning-services.html">museum planning services</a> and <a href="../../immersive-museum-planning.html">immersive museum planning</a>.</p>
  </div>
</div>"""

FOOTER = """
<p class="privacy-strip"><a href="../../museum-planning-privacy.html">Privacy &amp; analytics</a> — how this site uses cookies and Google Analytics.</p>
<footer>
  <div class="footer-logo">Museum <span>Planning</span> LLC</div>
  <ul class="footer-links">
    <li><a href="../index.html">Museum School</a></li>
    <li><a href="https://museums101.com">Museums 101</a></li>
    <li><a href="https://museum-experiences.com">Museum Experiences</a></li>
    <li><a href="../../museum-planning-contact.html">Contact</a></li>
    <li><a href="../../museum-planning-privacy.html">Privacy</a></li>
  </ul>
  <div class="footer-copy">© 2026 Museum Planning LLC</div>
</footer>

<div class="search-overlay" id="searchOverlay">
  <button class="search-close" id="searchClose">×</button>
  <div class="search-input-wrap">
    <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    <input type="text" id="search-input" placeholder="Search the site..." autocomplete="off">
  </div>
  <div class="search-results" id="searchResults"></div>
</div>

<script>
const PAGES = [
  { type: "Museum School", title: "Museum Exhibition Design — Overview", desc: "Six-part series from planning through maintenance.", url: "index.html" },
  { type: "Museum School", title: "Exhibition Design Part I — Planning", desc: "Visitor objectives, charter, budget, schedule.", url: "exhibition-design-part-i.html" },
  { type: "Museum School", title: "Exhibition Design Part II — Design", desc: "Script, schematic, design development, final design.", url: "exhibition-design-part-ii.html" },
  { type: "Museum School", title: "Exhibition Design Part III — Fabrication", desc: "Working drawings, fabricator, quality control.", url: "exhibition-design-part-iii.html" },
  { type: "Museum School", title: "Exhibition Design Part IV — Installation", desc: "Load-in, staging, punch list, opening.", url: "exhibition-design-part-iv.html" },
  { type: "Museum School", title: "Exhibition Design Part V — Maintenance", desc: "Operational exhibits, staff training, evaluation.", url: "exhibition-design-part-v.html" },
  { type: "Museum School", title: "Exhibition Design Part VI — Full Process", desc: "Complete process summary and checklist.", url: "exhibition-design-part-vi.html" },
  { type: "Services", title: "Museum Planning Services", desc: "Feasibility, strategic planning, master planning, exhibition design.", url: "../../museum-planning-services.html" },
  { type: "Guide", title: "Immersive Museum Planning", desc: "Interactive and immersive exhibition design.", url: "../../immersive-museum-planning.html" },
  { type: "Museum School", title: "How to Start a Museum", desc: "Ten steps to starting a museum.", url: "../how-to-start-a-museum.html" },
];
const input = document.getElementById('search-input');
const results = document.getElementById('searchResults');
const overlay = document.getElementById('searchOverlay');
document.getElementById('searchToggle').addEventListener('click', () => {
  overlay.classList.add('open');
  setTimeout(() => input.focus(), 100);
});
document.getElementById('searchClose').addEventListener('click', () => {
  overlay.classList.remove('open');
  input.value = '';
  results.innerHTML = '';
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') { overlay.classList.remove('open'); input.value = ''; results.innerHTML = ''; }
});
input.addEventListener('input', () => {
  const q = input.value.toLowerCase().trim();
  if (!q) { results.innerHTML = ''; return; }
  const matches = PAGES.filter(p => p.title.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q));
  results.innerHTML = matches.length ? matches.map(p => `<a href="${p.url}" class="search-result"><div class="sr-type">${p.type}</div><div class="sr-title">${p.title}</div><div class="sr-desc">${p.desc}</div></a>`).join('') : '<div class="search-empty">No results found.</div>';
});
</script>
<script src="../../assets/nav-mobile.js" defer></script>"""


def extract_style(html: str) -> str:
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    return m.group(1) if m else ""


def extract_body_content(html: str) -> str:
    """Series bar through end of body-wrap (exclude old header/footer)."""
    start = html.find('<nav class="series-bar">')
    if start == -1:
        raise ValueError("series-bar not found")
    footer = html.find("<footer", start)
    if footer == -1:
        raise ValueError("footer not found")
    chunk = html[start:footer]
    # Trim back to closing of outer body-wrap (last </div> before footer).
    last = chunk.rfind("</div>")
    if last == -1:
        raise ValueError("body-wrap end not found")
    return chunk[: last + len("</div>")].strip()


def rewrite_links(content: str) -> str:
    content = content.replace("museum-exhibition-design-hub.html", "index.html")
    content = re.sub(
        r'href="https://museumplanner\.org[^"]*"',
        'href="../../museum-planning-services.html"',
        content,
    )
    return content


def build_page(src_name: str, out_name: str) -> str:
    html = (SOURCE / src_name).read_text(encoding="utf-8")
    title, desc = META[out_name]
    canonical = f"{BASE}/{out_name}" if out_name != "index.html" else f"{BASE}/"
    style = extract_style(html)
    body = rewrite_links(extract_body_content(html))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="https://museumplanning.com/assets/favicon.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="https://museumplanning.com/assets/apple-touch-icon.png" sizes="180x180">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{style}
/* museumplanning.com shell */
:root{{--gold:#C9A84C;--deep:#111C27;}}
nav.site-nav{{position:fixed;top:0;left:0;right:0;background:var(--deep);height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;z-index:200;border-bottom:1px solid rgba(201,168,76,.15);}}
nav.site-nav .nav-logo{{font-family:'Playfair Display',serif;font-size:15px;color:#fff;text-decoration:none;}}
nav.site-nav .nav-logo span{{color:var(--gold);}}
nav.site-nav .nav-links{{display:flex;gap:24px;list-style:none;align-items:center;margin:0;padding:0;}}
nav.site-nav .nav-links a{{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.45);text-decoration:none;}}
nav.site-nav .nav-links a:hover,nav.site-nav .nav-links a.active{{color:rgba(255,255,255,.9);}}
nav.site-nav .nav-cta{{background:var(--gold)!important;color:var(--deep)!important;padding:8px 16px;}}
nav.site-nav .search-toggle{{background:none;border:none;cursor:pointer;padding:4px;}}
nav.site-nav .search-toggle svg{{width:18px;height:18px;stroke:rgba(255,255,255,.5);fill:none;stroke-width:2;}}
.hero{{padding-top:124px!important;}}
.series-bar{{position:sticky;top:60px;z-index:150;}}
.tier3-band{{background:#1B2A3B;padding:28px 40px;border-top:3px solid var(--gold);}}
.tier3-inner{{max-width:960px;margin:0 auto;}}
.tier3-label{{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:8px;}}
.tier3-body{{font-size:15px;color:rgba(255,255,255,.65);line-height:1.7;margin:0;}}
.tier3-body a{{color:var(--gold);}}
footer .footer-logo{{font-family:'Playfair Display',serif;font-size:16px;color:#fff;}}
footer .footer-logo span{{color:var(--gold);}}
footer{{background:var(--deep);padding:32px 40px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px;}}
footer .footer-links{{display:flex;gap:24px;list-style:none;margin:0;padding:0;}}
footer .footer-links a{{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.4);text-decoration:none;}}
footer .footer-copy{{font-size:12px;color:rgba(255,255,255,.25);}}
.privacy-strip{{text-align:center;padding:12px;font-size:12px;color:#888;background:#f0ebe0;}}
.privacy-strip a{{color:#666;}}
.search-overlay{{display:none;position:fixed;inset:0;background:rgba(17,28,39,.97);z-index:300;flex-direction:column;align-items:center;padding-top:120px;}}
.search-overlay.open{{display:flex;}}
.search-close{{position:absolute;top:24px;right:32px;background:none;border:none;color:#fff;font-size:32px;cursor:pointer;}}
.search-input-wrap{{display:flex;align-items:center;gap:16px;width:90%;max-width:680px;border-bottom:1px solid rgba(255,255,255,.15);padding-bottom:12px;}}
.search-input-wrap svg{{width:22px;height:22px;stroke:var(--gold);fill:none;stroke-width:2;}}
#search-input{{flex:1;background:none;border:none;outline:none;font-family:'Playfair Display',serif;font-size:clamp(24px,4vw,36px);color:#fff;}}
.search-results{{width:90%;max-width:680px;margin-top:24px;}}
.search-result{{display:block;padding:16px 20px;text-decoration:none;border-left:3px solid transparent;margin-bottom:4px;background:rgba(255,255,255,.04);}}
.search-result:hover{{border-color:var(--gold);}}
.sr-type{{font-family:'DM Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);}}
.sr-title{{font-family:'Playfair Display',serif;font-size:18px;color:#fff;margin:4px 0;}}
.sr-desc{{font-size:13px;color:rgba(255,255,255,.4);}}
.search-empty{{color:rgba(255,255,255,.3);font-style:italic;text-align:center;padding:40px;}}
@media(max-width:900px){{nav.site-nav .nav-links:not(.open){{display:none;}}}}
</style>
<link rel="stylesheet" href="../../assets/nav-mobile.css">
<link rel="stylesheet" href="../../assets/site-footer.css">
<script src="../../assets/ga-measurement-id.js"></script>
<script src="../../assets/analytics.js" defer></script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PGG4KV35" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{NAV}
{body}
{TIER3_BAND}
{FOOTER}
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src, dst in FILES.items():
        out_path = OUT / dst
        out_path.write_text(build_page(src, dst), encoding="utf-8")
        print(f"wrote {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
