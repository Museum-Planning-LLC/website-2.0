#!/usr/bin/env python3
"""Build for-universities.html from for-cities.html shell + museumplanner.org source."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DESKTOP = Path("/Users/markwalhimer/Desktop/museumplanner.org/for-universities.html")
template = (ROOT / "for-cities.html").read_text(encoding="utf-8")
src = DESKTOP.read_text(encoding="utf-8")

template = template.replace(
    "<title>Museum Feasibility Study for Cities & Municipalities | Museum Planning LLC</title>",
    "<title>University Museum Planning & Feasibility | Museum Planning LLC</title>",
)
template = template.replace(
    "content=\"Museum Planning LLC helps city managers, mayors' offices, and economic development directors evaluate museum feasibility, plan cultural destinations, and understand real operating costs — before capital is committed.\"",
    "content=\"Museum Planning LLC helps university presidents, provosts, and boards turn collections in storage and underused buildings into public-facing museums that serve both the campus and the surrounding community.\"",
)
template = template.replace(
    '<link rel="canonical" href="https://museumplanning.com/for-cities.html">',
    '<link rel="canonical" href="https://museumplanning.com/for-universities.html">',
)

extra_css = """
/* ─── TENSION CALLOUT ─── */
.tension-callout {
  background: var(--deep);
  padding: 40px 44px;
  margin-bottom: 40px;
  border-left: 4px solid var(--gold);
}
.tension-callout .tension-label {
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 16px;
}
.tension-callout h3 {
  font-family: var(--serif);
  font-size: clamp(22px, 2.5vw, 28px);
  font-weight: 700;
  color: var(--white);
  line-height: 1.2;
  margin-bottom: 18px;
}
.tension-callout h3 em { font-style: italic; color: rgba(255,255,255,0.55); }
.tension-callout p {
  font-size: 15px;
  color: rgba(255,255,255,0.55);
  line-height: 1.75;
  margin-bottom: 14px;
}
.tension-callout p:last-child { margin-bottom: 0; }

/* ─── MODEL GRID ─── */
.model-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.model-card {
  border: 1px solid var(--rule);
  padding: 28px 24px;
  background: var(--white);
  transition: border-color 0.2s;
}
.model-card:hover { border-color: var(--gold); }
.model-num {
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 10px;
}
.model-card h3 {
  font-family: var(--serif);
  font-size: 17px;
  font-weight: 600;
  color: var(--deep);
  margin-bottom: 10px;
  line-height: 1.25;
}
.model-card h3 em { font-style: italic; color: var(--gold); }
.model-card p {
  font-size: 14px;
  color: var(--mid);
  line-height: 1.65;
}
"""
template = template.replace("/* ─── RESPONSIVE ─── */", extra_css + "\n/* ─── RESPONSIVE ─── */")
template = template.replace(
    "  .audience-grid { grid-template-columns: 1fr 1fr; }",
    "  .audience-grid,\n  .model-grid { grid-template-columns: 1fr 1fr; }",
)
template = template.replace(
    "  .audience-grid { grid-template-columns: 1fr; }",
    "  .audience-grid,\n  .model-grid { grid-template-columns: 1fr; }",
)
template = template.replace(
    '<li><a href="for-cities.html" class="active">For Cities</a></li>',
    '<li><a href="for-cities.html">For Cities</a></li>\n    <li><a href="for-universities.html" class="active">For Universities</a></li>',
)

# Extract desktop prose blocks (strip HTML) for reuse — use structured body below
body = r'''<!-- HERO -->
<section class="hero">
  <motion.div class="hero-inner">
'''
