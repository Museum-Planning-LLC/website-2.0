#!/usr/bin/env python3
"""Build immersive-mexico/en/ and immersive-mexico/es/ path-based locales."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "immersive-mexico"
BASE = "https://museumplanning.com/immersive-mexico"
SOURCE_INDEX = ROOT / "index.html"

DEMO_PAGES = [
    {
        "file": "living-commons.html",
        "canonical_slug": "living-commons.html",
        "title_en": "Living Commons · Lobby Demo | Museum Planning LLC",
        "title_es": "Living Commons · Demo Lobby | Museum Planning LLC",
        "desc_en": "Living Commons — commercial lobby demo. Co-presence generative environment for corporate shared spaces. Museum Planning LLC.",
        "desc_es": "Living Commons — demo de lobby comercial. Entorno generativo de co-presencia para espacios corporativos compartidos. Museum Planning LLC.",
        "label_en": "Corporate Lobby · Commercial Demo",
        "label_es": "Lobby Corporativo · Demo Comercial",
        "h1": "Living Commons",
        "subtitle_en": "Co-presence generative work · two inputs · one emergent result · kiosk-ready",
        "subtitle_es": "Obra generativa de co-presencia · dos entradas · un resultado emergente · listo para kiosco",
        "work": "living-commons-work.html",
        "iframe_title_en": "Living Commons — commercial lobby demo",
        "iframe_title_es": "Living Commons — demo de lobby comercial",
        "open_en": "Open full screen ↗",
        "open_es": "Abrir pantalla completa ↗",
        "footer_en": "Commercial deployment demo · Mark Walhimer · Museum Planning LLC ·",
        "footer_es": "Demo de despliegue comercial · Mark Walhimer · Museum Planning LLC ·",
        "back_en": "Back to overview",
        "back_es": "Volver al resumen",
        "contact_en": "Start a conversation",
        "contact_es": "Iniciar una conversación",
        "back_nav_en": "← Immersive México",
        "back_nav_es": "← Immersive México",
    },
    {
        "file": "surrender-machine-77823.html",
        "canonical_slug": "surrender-machine-77823.html",
        "title_en": "Surrender Machine 77823 · Preview Center Demo | Museum Planning LLC",
        "title_es": "Surrender Machine 77823 · Demo Centro de Previsualización | Museum Planning LLC",
        "desc_en": "Surrender Machine 77823 — commercial preview center demo. Three-zone generative environment for immersive sales spaces. Museum Planning LLC.",
        "desc_es": "Surrender Machine 77823 — demo de centro de previsualización comercial. Entorno generativo de tres zonas para espacios de venta inmersivos. Museum Planning LLC.",
        "label_en": "Preview Center · Commercial Demo",
        "label_es": "Centro de Previsualización · Demo Comercial",
        "h1": "Surrender Machine 77823",
        "subtitle_en": "Three zones · narrative cylinder · dense field · sensor-ready spatial logic",
        "subtitle_es": "Tres zonas · cilindro narrativo · campo denso · lógica espacial lista para sensores",
        "work": "surrender-machine-work.html",
        "iframe_title_en": "Surrender Machine 77823 — commercial preview center demo",
        "iframe_title_es": "Surrender Machine 77823 — demo de centro de previsualización comercial",
        "open_en": "Open full screen ↗",
        "open_es": "Abrir pantalla completa ↗",
        "footer_en": "Commercial deployment demo · Mark Walhimer · Museum Planning LLC ·",
        "footer_es": "Demo de despliegue comercial · Mark Walhimer · Museum Planning LLC ·",
        "back_en": "Back to overview",
        "back_es": "Volver al resumen",
        "contact_en": "Start a conversation",
        "contact_es": "Iniciar una conversación",
        "back_nav_en": "← Immersive México",
        "back_nav_es": "← Immersive México",
    },
]

LANG_SCRIPT = re.compile(
    r"<script>\s*function setLang\(lang, updateUrl\).*?</script>\s*",
    re.DOTALL,
)

LANG_BUTTONS_EN = """<div class="lang-toggle">
    <a class="lang-btn active" href="./" hreflang="en" aria-current="page">EN</a>
    <a class="lang-btn" href="../es/" hreflang="es">ES</a>
  </div>"""

LANG_BUTTONS_ES = """<div class="lang-toggle">
    <a class="lang-btn" href="../en/" hreflang="en">EN</a>
    <a class="lang-btn active" href="./" hreflang="es" aria-current="page">ES</a>
  </div>"""


def fix_site_paths(html: str) -> str:
    return html.replace('href="../', 'href="../../').replace('src="../', 'src="../../')


def build_index(lang: str) -> None:
    html = SOURCE_INDEX.read_text(encoding="utf-8")
    html = fix_site_paths(html)
    html = LANG_SCRIPT.sub("", html)

    other = "es" if lang == "en" else "en"
    buttons = LANG_BUTTONS_EN if lang == "en" else LANG_BUTTONS_ES
    html = re.sub(
        r"<div class=\"lang-toggle\">.*?</div>",
        buttons,
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace("<html lang=\"en\">", f"<html lang=\"{lang}\">", 1)
    html = html.replace('body class="lang-en"', f'body class="lang-{lang}"', 1)

    html = re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="{BASE}/{lang}/">',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="en" href="[^"]+">',
        f'<link rel="alternate" hreflang="en" href="{BASE}/en/">',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="es" href="[^"]+">',
        f'<link rel="alternate" hreflang="es" href="{BASE}/es/">',
        html,
        count=1,
    )
    html = re.sub(
        r'<link rel="alternate" hreflang="x-default" href="[^"]+">',
        f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/">',
        html,
        count=1,
    )

    out = ROOT / lang / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT.parent)}")


def lang_switch_html(lang: str, page_file: str) -> str:
    other = "es" if lang == "en" else "en"
    cur = "active" if lang == "en" else ""
    cur_es = "active" if lang == "es" else ""
    return f"""<span class="im-lang">
    <a class="lang-btn {cur}" href="../en/{page_file}" hreflang="en"{" aria-current=\"page\"" if lang == "en" else ""}>EN</a>
    <a class="lang-btn {cur_es}" href="../es/{page_file}" hreflang="es"{" aria-current=\"page\"" if lang == "es" else ""}>ES</a>
  </span>"""


def build_demo_page(meta: dict, lang: str) -> None:
    page_file = meta["file"]
    suffix = "_en" if lang == "en" else "_es"
    switch = lang_switch_html(lang, page_file)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light" />
  <meta name="description" content="{meta['desc' + suffix]}" />
  <link rel="canonical" href="{BASE}/{lang}/{page_file}" />
  <link rel="alternate" hreflang="en" href="{BASE}/en/{page_file}" />
  <link rel="alternate" hreflang="es" href="{BASE}/es/{page_file}" />
  <link rel="alternate" hreflang="x-default" href="{BASE}/en/{page_file}" />
  <link rel="icon" href="https://museumplanning.com/assets/favicon.png" type="image/png" sizes="48x48" />
  <link rel="stylesheet" href="../im-chrome.css" />
  <title>{meta['title' + suffix]}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --ink: #111C27;
      --muted: #6b6760;
      --rule: rgba(201, 168, 76, 0.2);
      --gold: #C9A84C;
    }}
    html, body {{ height: 100%; }}
    body {{
      background: #fff;
      color: var(--ink);
      font-family: 'Lato', system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}
    header {{
      flex: 0 0 auto;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px 16px;
      align-items: center;
      padding: 14px 18px;
      border-bottom: 1px solid var(--rule);
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
    }}
    .header-main {{ display: grid; gap: 4px; min-width: 0; }}
    .kicker {{ letter-spacing: 0.14em; color: var(--gold); }}
    header h1 {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--ink);
      letter-spacing: 0.02em;
      text-transform: none;
    }}
    .subtitle {{ font-size: 9px; color: rgba(107, 103, 96, 0.85); line-height: 1.5; }}
    header a {{ color: var(--gold); text-decoration: none; white-space: nowrap; }}
    header a:hover {{ text-decoration: underline; }}
    #stage {{
      flex: 1 1 auto;
      min-height: 0;
      position: relative;
      background: #fff;
    }}
    #stage iframe {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }}
    footer {{
      flex: 0 0 auto;
      padding: 10px 18px 14px;
      border-top: 1px solid var(--rule);
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.08em;
      color: var(--muted);
      line-height: 1.7;
    }}
    footer a {{ color: var(--gold); text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="im-chrome">
    <a class="im-back" href="index.html">{meta['back_nav' + suffix]}</a>
    {switch}
    <span class="im-label">{meta['label' + suffix]}</span>
  </div>
  <header>
    <div class="header-main">
      <div class="kicker">Museum Planning LLC · Immersive Environments · México</div>
      <h1>{meta['h1']}</h1>
      <div class="subtitle">{meta['subtitle' + suffix]}</div>
    </div>
    <a href="../works/{meta['work']}" target="_blank" rel="noopener">{meta['open' + suffix]}</a>
  </header>
  <div id="stage">
    <iframe
      src="../works/{meta['work']}"
      title="{meta['iframe_title' + suffix]}"
      allow="fullscreen"
      loading="eager"
    ></iframe>
  </div>
  <footer>
    {meta['footer' + suffix]}
    <a href="index.html">{meta['back' + suffix]}</a> ·
    <a href="../../museum-planning-contact.html">{meta['contact' + suffix]}</a>
  </footer>
</body>
</html>
"""
    out = ROOT / lang / page_file
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT.parent)}")


def build_shared_ground(lang: str) -> None:
    src = ROOT / "shared-ground.html"
    html = src.read_text(encoding="utf-8")
    html = html.replace("<html lang=\"en\">", f"<html lang=\"{lang}\">", 1)
    html = html.replace(
        'href="index.html" style="color:var(--accent)">Immersive México overview',
        f'href="index.html" style="color:var(--accent)">'
        + ("Immersive México overview" if lang == "en" else "Resumen Immersive México"),
    )
    switch = lang_switch_html(lang, "shared-ground.html")
    chrome = f"""<div class="im-chrome" style="position:relative;z-index:9999">
  <a class="im-back" href="index.html">{"← Immersive México" if lang == "en" else "← Immersive México"}</a>
  {switch}
  <span class="im-label">{"Visitor Center · Commercial Demo" if lang == "en" else "Centro de Visitantes · Demo Comercial"}</span>
</div>
<link rel="stylesheet" href="../im-chrome.css" />
"""
    if "<body>" in html and "im-chrome" not in html:
        html = html.replace("<body>", "<body>\n" + chrome, 1)

    head_extra = f"""
  <link rel="canonical" href="{BASE}/{lang}/shared-ground.html" />
  <link rel="alternate" hreflang="en" href="{BASE}/en/shared-ground.html" />
  <link rel="alternate" hreflang="es" href="{BASE}/es/shared-ground.html" />
  <link rel="alternate" hreflang="x-default" href="{BASE}/en/shared-ground.html" />
"""
    html = html.replace("</head>", head_extra + "</head>", 1)

    out = ROOT / lang / "shared-ground.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT.parent)}")


def write_root_redirect(name: str, target: str) -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="{BASE}/en/{name}">
  <meta http-equiv="refresh" content="0; url=en/{name}">
  <script>
  (function() {{
    var q = location.search || '';
    var dest = (q.indexOf('lang=es') !== -1 ? 'es/' : 'en/') + '{name}' + location.hash;
    location.replace(dest);
  }})();
  </script>
</head>
<body>
  <p><a href="en/{name}">English</a> · <a href="es/{name}">Español</a></p>
</body>
</html>
"""
    (ROOT / name).write_text(html, encoding="utf-8")
    print(f"wrote redirect {name} → {target}")


def write_locale_root_index() -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Immersive Environments · Mexico | Museum Planning LLC</title>
  <link rel="canonical" href="{BASE}/en/">
  <meta http-equiv="refresh" content="0; url=en/">
  <script>
  (function() {{
    var q = location.search || '';
    var dest = q.indexOf('lang=es') !== -1 ? 'es/' : 'en/';
    location.replace(dest + location.hash);
  }})();
  </script>
</head>
<body>
  <p><a href="en/">English</a> · <a href="es/">Español</a></p>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("wrote immersive-mexico/index.html redirect")


def main() -> None:
    if not SOURCE_INDEX.exists():
        raise SystemExit(f"missing {SOURCE_INDEX}")

    for lang in ("en", "es"):
        build_index(lang)
        for meta in DEMO_PAGES:
            build_demo_page(meta, lang)
        build_shared_ground(lang)

    write_locale_root_index()
    for meta in DEMO_PAGES:
        write_root_redirect(meta["file"], f"en/{meta['file']}")
    write_root_redirect("shared-ground.html", "en/shared-ground.html")

    # Remove legacy flat demo pages (replaced by redirects)
    print("done")


if __name__ == "__main__":
    main()
