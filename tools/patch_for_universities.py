#!/usr/bin/env python3
"""Patch for-universities.html with site chrome (nav, footer, analytics)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "for-universities.html"
cities_nav = (ROOT / "for-cities.html").read_text(encoding="utf-8")
text = path.read_text(encoding="utf-8")

SITE_HEAD = """<link rel="canonical" href="https://museumplanning.com/for-universities.html">
<script>document.documentElement.classList.add('js-ready');</script>
<link rel="icon" href="https://museumplanning.com/assets/favicon.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="https://museumplanning.com/assets/apple-touch-icon.png" sizes="180x180">

"""

SITE_NAV = """<nav class="site-nav" id="site-nav">
  <a href="index.html" class="nav-logo">Museum <span>Planning</span> LLC</a>
  <button type="button" class="nav-hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav-menu">
    <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
  </button>
  <ul class="nav-links" id="site-nav-menu">
    <li><a href="museum-planning-services.html">Services</a></li>
    <li><a href="for-cities.html">For Cities</a></li>
    <li><a href="for-universities.html" class="active">For Universities</a></li>
    <li><a href="museum-planning-projects.html">Projects</a></li>
    <li><a href="museum-school/index.html">Museum School</a></li>
    <li><a href="for-cities-science-center.html">Science Centers</a></li>
    <li><a href="museum-planning-about.html">About</a></li>
    <li><a href="museum-planning-contact.html">Contact</a></li>
    <li class="nav-search"><button type="button" class="search-toggle" id="searchToggle" aria-label="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button></li>
    <li><a href="#contact" class="nav-cta">Start a Conversation</a></li>
  </ul>
</nav>"""

# Extract search overlay + footer tail from for-cities
cities = (ROOT / "for-cities.html").read_text(encoding="utf-8")
tail_start = cities.index('<p class="privacy-strip">')
SITE_TAIL = cities[tail_start:]

SITE_NAV_CSS = """
/* Site nav (museumplanning.com) */
body { padding-top: 60px; }
nav.site-nav#site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  padding: 0 56px;
  background: #111C27;
  border-bottom: 1px solid rgba(201, 168, 76, 0.15);
  z-index: 100;
}
nav.site-nav#site-nav .nav-logo {
  font-family: 'Playfair Display', serif;
  font-size: 15px;
  color: #fff;
  text-decoration: none;
}
nav.site-nav#site-nav .nav-logo span { color: #C9A84C; }
nav.site-nav#site-nav .nav-links a {
  font-family: 'DM Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.5);
}
nav.site-nav#site-nav .nav-links a:hover,
nav.site-nav#site-nav .nav-links a.active { color: #C9A84C; }
nav.site-nav#site-nav .nav-cta {
  background: #C9A84C;
  color: #111C27 !important;
  padding: 8px 20px;
}
"""

if "<link rel=\"canonical\"" not in text:
    text = text.replace(
        '<meta name="description" content="Museum Planning LLC helps university presidents',
        '<meta name="description" content="Museum Planning LLC helps university presidents',
    )
    text = text.replace(
        "content=\"Museum Planning LLC helps university presidents, provosts, and boards turn collections in storage and underused buildings into public-facing museums that serve both the campus and the surrounding community.\">",
        "content=\"Museum Planning LLC helps university presidents, provosts, and boards turn collections in storage and underused buildings into public-facing museums that serve both the campus and the surrounding community.\">\n" + SITE_HEAD,
    )

if "nav-hamburger" not in text:
    text = text.replace("/* ── NAV ── */", "/* ── NAV (page legacy — overridden by site nav) ── */")
    text = text.replace("</style>", SITE_NAV_CSS + "\n</style>\n  <link rel=\"stylesheet\" href=\"assets/nav-mobile.css\">\n  <link rel=\"stylesheet\" href=\"assets/site-footer.css\">")

# Replace nav block
import re
text = re.sub(r"<!-- NAV -->.*?</nav>", "<!-- NAV -->\n" + SITE_NAV, text, count=1, flags=re.S)

# Fix broken question item + duplicate enrollment
text = re.sub(
    r'\s*<motion.div class="question-item">\s*<div class="question-answer">This is one of the most powerful arguments.*?</div>\s*</div>\s*</div>',
    "",
    text,
    flags=re.S,
)
# Add museum studies question after third enrollment answer
studies_q = """
    <div class="question-item">
      <div class="question-q">"</div>
      <div class="question-body">
        <div class="question-text">We have a museum studies program. Can the museum be a teaching lab for our students?</div>
        <div class="question-answer">This is one of the most powerful arguments for a university museum. We design the museum from the start as a working institution — with governance, staffing structures, and physical space that allow museum studies students to do real curatorial, interpretive, development, and administrative work.</div>
      </div>
    </div>
"""
if "museum studies program" not in text:
    text = text.replace(
        "We build the enrollment and recruitment case into the feasibility study alongside the community relations case — because in most university museum conversations, both are true simultaneously.</motion.div>\n      </div>\n    </div>",
        "We build the enrollment and recruitment case into the feasibility study alongside the community relations case — because in most university museum conversations, both are true simultaneously.</div>\n      </div>\n    </div>" + studies_q,
    )

# Remove duplicate enrollment block (second one with WICHE stats)
text = re.sub(
    r'\s*<div class="question-item">\s*<div class="question-q">"</motion.div>.*?Our admissions numbers are declining\. Can a museum actually help with enrollment\?.*?</div>\s*</div>\s*</div>\s*(?=\s*<div class="question-item">\s*<div class="question-q">"\s*<div class="question-body">\s*<div class="question-text">We have an early childhood)',
    "\n    ",
    text,
    count=1,
    flags=re.S,
)

# Portfolio links
text = text.replace(
    'href="mailto:mark@museumplanning.com?subject=Reference%20Request%20—%20Frehner%20Museum" class="port-link">Request reference →</a>',
    'href="projects/frehner-museum-southern-utah-university.html" class="port-link">View project →</a>',
)
text = text.replace(
    'href="mailto:mark@museumplanning.com?subject=Reference%20Request%20—%20Arizona%20NRM" class="port-link">Request reference →</a>',
    'href="projects/arizona-natural-resources-museum.html" class="port-link">View project →</a>',
)
text = text.replace(
    'href="mailto:mark@museumplanning.com?subject=Reference%20Request%20—%20Howard%20NHM" class="port-link">Request reference →</a>',
    'href="projects/howard-natural-history-museum.html" class="port-link">View project →</a>',
)

# Relative internal links in nav (already relative in new nav)
text = text.replace("https://museumplanning.com/index.html", "index.html")
text = text.replace("https://museumplanning.com/museum-planning-services.html", "museum-planning-services.html")
text = text.replace("https://museumplanning.com/for-cities.html", "for-cities.html")
text = text.replace("https://museumplanning.com/for-universities.html", "for-universities.html")
text = text.replace("https://museumplanning.com/for-cities-science-center.html", "for-cities-science-center.html")
text = text.replace("https://museumplanning.com/museum-planning-projects.html", "museum-planning-projects.html")
text = text.replace("https://museumplanning.com/museum-planning-about.html", "museum-planning-about.html")
text = text.replace("https://museumplanning.com/museum-planning-contact.html", "museum-planning-contact.html")
text = text.replace("https://museumplanning.com/museum-planning-privacy.html", "museum-planning-privacy.html")

# Replace footer through end with site tail (includes search + nav-mobile.js)
if "search-overlay" not in text:
    text = re.sub(
        r"<!-- FOOTER -->.*</html>",
        "<!-- FOOTER (site) -->\n" + SITE_TAIL,
        text,
        flags=re.S,
    )

# Add universities to PAGES in search script
if "For Universities" not in text or 'url: "for-universities.html"' not in text:
    text = text.replace(
        'const PAGES = [\n  { type: "Municipal", title: "For Cities',
        'const PAGES = [\n  { type: "University", title: "For Universities — Museum Planning", desc: "Presidents, provosts, deans, and feasibility before capital.", url: "for-universities.html" },\n  { type: "Municipal", title: "For Cities',
    )

path.write_text(text, encoding="utf-8")
print("Patched", path)
