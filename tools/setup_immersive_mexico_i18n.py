#!/usr/bin/env python3
"""Build immersive-mexico/en/ and immersive-mexico/es/ path-based locales."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "immersive-mexico"
BASE = "https://museumplanning.com/immersive-mexico"
SOURCE_INDEX = ROOT / "en" / "index.html"
SHARED_GROUND_SOURCE = ROOT / "_source" / "shared-ground.html"
POC_DISPLAY_URL = "https://interactive-sliders.netlify.app/poc"
POC_CONTROLLER_URL = "https://interactive-sliders.netlify.app/poc/controller"

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

SCROLL_REVEAL_SCRIPT = """<script>
(function () {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.fu').forEach(function (el) { el.classList.add('vis'); });
    return;
  }
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) e.target.classList.add('vis');
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.fu').forEach(function (el) { obs.observe(el); });
})();
</script>
"""


def ensure_scroll_reveal(html: str) -> str:
    if "IntersectionObserver" in html and "querySelectorAll('.fu')" in html:
        return html
    marker = '<script src="../../assets/search-pages.js">'
    alt = '<script src="../assets/search-pages.js">'
    if marker not in html and alt in html:
        marker = alt
    if marker not in html:
        raise ValueError("expected search-pages.js marker for scroll reveal injection")
    return html.replace(marker, SCROLL_REVEAL_SCRIPT + "\n" + marker, 1)

LANG_BUTTONS_EN = """<div class="lang-toggle">
    <a class="lang-btn active" href="./" hreflang="en" aria-current="page">EN</a>
    <a class="lang-btn" href="../es/" hreflang="es">ES</a>
  </div>"""

LANG_BUTTONS_ES = """<div class="lang-toggle">
    <a class="lang-btn" href="../en/" hreflang="en">EN</a>
    <a class="lang-btn active" href="./" hreflang="es" aria-current="page">ES</a>
  </div>"""


def fix_site_paths(html: str) -> str:
    placeholders: dict[str, str] = {}
    for i, match in enumerate(re.finditer(r'src="\.\./works/[^"]+"', html)):
        key = f"__IM_WORKS_{i}__"
        placeholders[key] = match.group(0)
        html = html.replace(match.group(0), key, 1)
    html = html.replace('href="../', 'href="../../').replace('src="../', 'src="../../')
    for key, val in placeholders.items():
        html = html.replace(key, val)
    return html


def build_index(lang: str) -> None:
    html = SOURCE_INDEX.read_text(encoding="utf-8")
    html = LANG_SCRIPT.sub("", html)
    html = ensure_scroll_reveal(html)

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


def build_scan_to_control(lang: str) -> None:
    page_file = "scan-to-control.html"
    switch = lang_switch_html(lang, page_file)
    if lang == "en":
        title = "Scan to Control · Lobby Sync POC | Museum Planning LLC"
        desc = (
            "Scan to Control — lobby sync proof of concept. QR + phone + projection wall "
            "with real-time Firebase sync. Technical brief for corporate lobby deployments."
        )
        h1 = "Scan to Control"
        subtitle = "Lobby sync POC · QR on wall · phone controller · real-time wall update"
        label = "Lobby Sync · Technical Brief"
        open_label = "Open phone controller ↗"
        brief_kicker = "Technical Brief"
        brief_h = "QR + phone + wall — the lobby <em>sensor layer.</em>"
        brief_lede = (
            "This proof-of-concept shows the interaction spine for a corporate lobby: a projection or "
            "mapped surface runs the artwork, a QR code invites visitors to their phone, and changes "
            "sync in real time to the wall. The same event stream feeds capture, dashboard metrics, "
            "and optional messaging — with an overhead camera adding anonymous traffic and engagement data."
        )
        stack_h = "Stack"
        stack_items = [
            ("01 · Wall display", "Full-screen browser on projector PC or media server. Runs the generative artwork or mapped surface."),
            ("02 · QR entry", "Unique URL per installation. Scan opens mobile controller — no app store, no login required."),
            ("03 · Phone controller", "Sliders, taps, or narrative choices. Each event is a identified or anonymous engagement signal."),
            ("04 · Real-time sync", "Firebase Realtime Database (or equivalent WebSocket layer) pushes parameters wall ↔ phone."),
            ("05 · Event log", "Scans, sessions, dwell, parameter changes → behavioral dashboard and CRM “captured” stage."),
            ("06 · Adaptation", "Rules engine aggregates reactions; generative parameters shift toward what visitors use most."),
            ("07 · Camera (optional)", "Overhead ML: foot traffic, phone-in-hand heuristic, zone dwell — no PII required."),
            ("08 · CRM + messaging (optional)", "Opt-in after scan for SMS/email; sales funnel stages beyond capture logged in CRM."),
        ]
        deploy_h = "Deployment notes"
        deploy_items = [
            "One controller URL per lobby (avoid session collision across sites).",
            "Privacy notice at QR landing; LFPDPPP consent for camera analytics and marketing messages in Mexico.",
            "Works with any generative piece — Surrender Machine, Living Commons, Shared Ground — same sync pattern.",
            "Production adds dashboard auth, per-client Firebase paths, and integration with Museum Planning Automation Dashboard.",
        ]
        try_h = "Try it now"
        try_p = "Open the display below on a large screen (or fullscreen this page). On your phone, open the controller link and move the sliders — the wall updates live when connected."
        footer = "Lobby sync proof of concept · Museum Planning LLC ·"
        back = "Back to overview"
        contact = "Start a conversation"
        back_nav = "← Immersive México"
    else:
        title = "Scan to Control · POC Sincronización Lobby | Museum Planning LLC"
        desc = (
            "Scan to Control — prueba de concepto de sincronización de lobby. QR + teléfono + muro "
            "con sincronización Firebase en tiempo real. Brief técnico para lobbies corporativos."
        )
        h1 = "Scan to Control"
        subtitle = "POC sincronización lobby · QR en muro · controlador móvil · actualización en vivo"
        label = "Sincronización Lobby · Brief Técnico"
        open_label = "Abrir controlador móvil ↗"
        brief_kicker = "Brief Técnico"
        brief_h = "QR + teléfono + muro — la <em>capa de sensores</em> del lobby."
        brief_lede = (
            "Esta prueba de concepto muestra la columna vertebral de interacción para un lobby corporativo: "
            "una proyección o superficie mapeada ejecuta la obra, un código QR invita al teléfono del visitante, "
            "y los cambios se sincronizan en tiempo real con el muro. El mismo flujo de eventos alimenta "
            "captura, métricas del panel y mensajería opcional — con cámara superior para tráfico anónimo."
        )
        stack_h = "Stack"
        stack_items = [
            ("01 · Pantalla de muro", "Navegador a pantalla completa en PC de proyección o servidor de medios."),
            ("02 · Entrada QR", "URL única por instalación. El escaneo abre el controlador móvil — sin app, sin login."),
            ("03 · Controlador móvil", "Sliders, toques o elecciones narrativas. Cada evento es una señal de interacción."),
            ("04 · Sincronización en vivo", "Firebase Realtime Database (u otra capa WebSocket) empuja parámetros muro ↔ teléfono."),
            ("05 · Registro de eventos", "Escaneos, sesiones, permanencia, cambios → panel de comportamiento y CRM “capturados”."),
            ("06 · Adaptación", "Motor de reglas agrega reacciones; parámetros generativos se inclinan hacia lo más usado."),
            ("07 · Cámara (opcional)", "ML superior: tráfico, teléfono en mano, permanencia por zona — sin PII."),
            ("08 · CRM + mensajes (opcional)", "Opt-in tras escaneo para SMS/email; etapas del embudo registradas en CRM."),
        ]
        deploy_h = "Notas de despliegue"
        deploy_items = [
            "Una URL de controlador por lobby (evitar colisión de sesiones entre sitios).",
            "Aviso de privacidad en landing QR; consentimiento LFPDPPP para cámara y mensajes en México.",
            "Funciona con cualquier pieza generativa — Surrender Machine, Living Commons, Shared Ground.",
            "Producción añade auth del panel, rutas Firebase por cliente e integración con el Panel de Automatización Museum Planning.",
        ]
        try_h = "Pruébalo ahora"
        try_p = "Abre la pantalla abajo en una pantalla grande (o pantalla completa). En tu teléfono, abre el controlador y mueve los sliders — el muro se actualiza en vivo cuando está conectado."
        footer = "Prueba de concepto sincronización lobby · Museum Planning LLC ·"
        back = "Volver al resumen"
        contact = "Iniciar una conversación"
        back_nav = "← Immersive México"

    stack_li = "\n".join(
        f'        <li><strong>{title}</strong> {body}</li>'
        for title, body in stack_items
    )
    deploy_li = "\n".join(f"        <li>{item}</li>" for item in deploy_items)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light" />
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{BASE}/{lang}/{page_file}" />
  <link rel="alternate" hreflang="en" href="{BASE}/en/{page_file}" />
  <link rel="alternate" hreflang="es" href="{BASE}/es/{page_file}" />
  <link rel="alternate" hreflang="x-default" href="{BASE}/en/{page_file}" />
  <link rel="icon" href="https://museumplanning.com/assets/favicon.png" type="image/png" sizes="48x48" />
  <link rel="stylesheet" href="../im-chrome.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Mono:wght@400;500&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
  <title>{title}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --ink: #111C27;
      --deep: #0D1520;
      --muted: #6b6760;
      --rule: rgba(201, 168, 76, 0.2);
      --gold: #C9A84C;
      --cream: #F8F4EC;
    }}
    html, body {{ min-height: 100%; }}
    body {{
      background: #fff;
      color: var(--ink);
      font-family: 'Lato', system-ui, sans-serif;
      display: flex;
      flex-direction: column;
    }}
    header.page-hd {{
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
    header.page-hd h1 {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 15px;
      font-weight: 700;
      color: var(--ink);
      letter-spacing: 0.02em;
      text-transform: none;
    }}
    .subtitle {{ font-size: 9px; color: rgba(107, 103, 96, 0.85); line-height: 1.5; }}
    header.page-hd a {{ color: var(--gold); text-decoration: none; white-space: nowrap; }}
    header.page-hd a:hover {{ text-decoration: underline; }}
    #stage {{
      flex: 0 0 auto;
      position: relative;
      width: 100%;
      aspect-ratio: 16/10;
      max-height: 62vh;
      background: #000;
    }}
    #stage iframe {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }}
    .brief {{
      flex: 1 1 auto;
      background: var(--cream);
      padding: 48px clamp(20px, 5vw, 56px) 64px;
    }}
    .brief-inner {{ max-width: 780px; margin: 0 auto; }}
    .brief-kicker {{
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brief-kicker::before {{ content: ''; width: 24px; height: 1px; background: var(--gold); }}
    .brief-h {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: clamp(26px, 3.5vw, 36px);
      font-weight: 700;
      line-height: 1.15;
      margin-bottom: 16px;
      color: var(--ink);
    }}
    .brief-h em {{ font-style: italic; color: var(--gold); }}
    .brief-lede {{
      font-size: 16px;
      line-height: 1.75;
      color: var(--muted);
      margin-bottom: 36px;
    }}
    .brief-h3 {{
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 20px;
      font-weight: 700;
      margin: 32px 0 14px;
      color: var(--ink);
    }}
    .stack, .deploy {{
      list-style: none;
      display: grid;
      gap: 12px;
    }}
    .stack li, .deploy li {{
      font-size: 14px;
      line-height: 1.65;
      color: var(--muted);
      padding: 14px 16px;
      background: #fff;
      border-left: 3px solid var(--gold);
    }}
    .stack li strong {{
      display: block;
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--ink);
      margin-bottom: 4px;
    }}
    .try-box {{
      margin-top: 36px;
      padding: 20px 22px;
      background: var(--deep);
      color: rgba(255,255,255,0.72);
      font-size: 14px;
      line-height: 1.7;
    }}
    .try-box strong {{
      display: block;
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--gold);
      margin-bottom: 8px;
    }}
    .try-box a {{ color: var(--gold); }}
    footer.page-ft {{
      padding: 12px 18px 16px;
      border-top: 1px solid var(--rule);
      font-family: 'DM Mono', monospace;
      font-size: 10px;
      letter-spacing: 0.08em;
      color: var(--muted);
      line-height: 1.7;
      background: #fff;
    }}
    footer.page-ft a {{ color: var(--gold); text-decoration: none; }}
    footer.page-ft a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="im-chrome">
    <a class="im-back" href="index.html">{back_nav}</a>
    {switch}
    <span class="im-label">{label}</span>
  </div>
  <header class="page-hd">
    <div class="header-main">
      <div class="kicker">Museum Planning LLC · Immersive Environments · México</div>
      <h1>{h1}</h1>
      <div class="subtitle">{subtitle}</div>
    </div>
    <a href="{POC_CONTROLLER_URL}" target="_blank" rel="noopener">{open_label}</a>
  </header>
  <div id="stage">
    <iframe
      src="{POC_DISPLAY_URL}"
      title="Scan to Control — lobby display"
      allow="fullscreen"
      loading="eager"
    ></iframe>
  </div>
  <section class="brief" id="brief">
    <div class="brief-inner">
      <div class="brief-kicker">{brief_kicker}</div>
      <h2 class="brief-h">{brief_h}</h2>
      <p class="brief-lede">{brief_lede}</p>

      <h3 class="brief-h3">{stack_h}</h3>
      <ol class="stack">
{stack_li}
      </ol>

      <h3 class="brief-h3">{deploy_h}</h3>
      <ul class="deploy">
{deploy_li}
      </ul>

      <div class="try-box">
        <strong>{try_h}</strong>
        {try_p}
        <br><br>
        <a href="{POC_CONTROLLER_URL}" target="_blank" rel="noopener">{POC_CONTROLLER_URL}</a>
      </div>
    </div>
  </section>
  <footer class="page-ft">
    {footer}
    <a href="index.html">{back}</a> ·
    <a href="../../museum-planning-contact.html">{contact}</a>
  </footer>
</body>
</html>
"""
    out = ROOT / lang / page_file
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT.parent)}")


def build_shared_ground(lang: str) -> None:
    src = SHARED_GROUND_SOURCE if SHARED_GROUND_SOURCE.exists() else ROOT / "en" / "shared-ground.html"
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
        build_scan_to_control(lang)

    write_locale_root_index()
    for meta in DEMO_PAGES:
        write_root_redirect(meta["file"], f"en/{meta['file']}")
    write_root_redirect("shared-ground.html", "en/shared-ground.html")
    write_root_redirect("scan-to-control.html", "en/scan-to-control.html")

    # Remove legacy flat demo pages (replaced by redirects)
    print("done")


if __name__ == "__main__":
    main()
