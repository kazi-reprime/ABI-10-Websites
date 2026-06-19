"""ABI builder v5 — per-site design inheritance + mobile-first responsive + centered EN/ES + partners with images + transitions."""
from __future__ import annotations
import json, os, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ASSETS = ROOT / "assets"
CONTENT = json.loads((ROOT / "_content" / "content.json").read_text())
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]

def load_tokens(slug):
    return json.loads((ROOT / "_content" / "tokens" / f"{slug}.json").read_text())

B, UI, NAV = CONTENT["brand"], CONTENT["ui"], CONTENT["nav"]
def tel(p): return p.replace("(","").replace(")","").replace(" ","").replace("-","")
def bi(d):
    if isinstance(d, str): return d
    return f'<span class="lang-en">{d.get("en","")}</span><span class="lang-es">{d.get("es","")}</span>'

# Nav minus haircuts (removed per user request)
NAV_ITEMS = [
    ("home","/"), ("about","/about"), ("programs","/programs"), ("instructors","/instructors"),
    ("gallery","/gallery"), ("partners","/partners"),
    ("jobplacement","/job-placement"), ("resources","/resources"), ("faq","/faq"), ("contact","/contact")
]

BRAND_TITLE = "American Barber Institute · New York's Dedicated Barber School"
BRAND_DESC_EN = "American Barber Institute (ABI) — New York's only dedicated barber school. NY State licensed. 30+ years, 10,000+ graduates. GI Bill® accepted. Manhattan & Bronx campuses."

PAGE_TITLES = {
    "/":"American Barber Institute · New York's Dedicated Barber School",
    "/about":"About · American Barber Institute · NYC",
    "/programs":"Programs & Tuition · American Barber Institute",
    "/instructors":"Instructors · American Barber Institute",
    "/gallery":"Gallery · American Barber Institute",
    "/partners":"Partner Shops · American Barber Institute",
    "/job-placement":"Job Placement · American Barber Institute",
    "/resources":"Resources · Veterans · ACCES-VR · ABI",
    "/faq":"Frequently Asked Questions · American Barber Institute",
    "/contact":"Contact · American Barber Institute · NYC",
}

# Per-site partner image assignments (deterministic) — gallery imgs ordered consistently
GALLERY_FILES = sorted([f for f in os.listdir(SRC_ASSETS/"img") if f.lower().endswith(('.jpeg','.jpg','.png'))])
PARTNER_IMGS = GALLERY_FILES[:6] if len(GALLERY_FILES) >= 6 else GALLERY_FILES * 2

def head_meta(page_path):
    title = PAGE_TITLES.get(page_path, BRAND_TITLE)
    return f'''<meta name="description" content="{BRAND_DESC_EN}">
<meta name="keywords" content="barber school nyc, american barber institute, abi, master barber program, gi bill barber school, escuela de barberia nueva york">
<meta name="author" content="American Barber Institute">
<meta name="robots" content="index, follow">
<link rel="canonical" href="/">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="icon" type="image/jpeg" href="/assets/logo.jpeg">
<link rel="apple-touch-icon" href="/assets/logo.jpeg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{BRAND_DESC_EN}">
<meta property="og:image" content="/assets/logo.jpeg">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{BRAND_DESC_EN}">
<meta name="twitter:image" content="/assets/logo.jpeg">
<meta name="format-detection" content="telephone=yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">'''

def jsonld(include_faq=False):
    school = {"@context":"https://schema.org","@type":"EducationalOrganization","name":"American Barber Institute","alternateName":"ABI","description":BRAND_DESC_EN,"telephone":B["phone_manhattan"],"email":B["email"],"foundingDate":"1995","address":[{"@type":"PostalAddress","streetAddress":"48 West 39th Street","addressLocality":"New York","addressRegion":"NY","postalCode":"10018","addressCountry":"US"},{"@type":"PostalAddress","streetAddress":"121 Westchester Square","addressLocality":"Bronx","addressRegion":"NY","postalCode":"10461","addressCountry":"US"}],"aggregateRating":{"@type":"AggregateRating","ratingValue":"4.3","ratingCount":"100"}}
    out = f'<script type="application/ld+json">{json.dumps(school)}</script>'
    if include_faq:
        faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q["q"]["en"],"acceptedAnswer":{"@type":"Answer","text":q["a"]["en"]}} for q in CONTENT["faqs"]]}
        out += f'<script type="application/ld+json">{json.dumps(faq)}</script>'
    return out

# Top banner — centered dual call buttons + lang toggle. ALWAYS at top of every page.
def top_banner():
    return f'''<div class="top-banner">
  <a class="cta-call cta-en" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call English admissions">
    <span class="cta-flag">EN</span>
    <span class="cta-label"><span class="lang-en">Call Admissions</span><span class="lang-es">Llama a Admisiones</span></span>
    <span class="cta-num">{B["phone_manhattan"]}</span>
  </a>
  <a class="cta-call cta-es" href="tel:{tel(B["phone_manhattan_es"])}" aria-label="Call Spanish admissions">
    <span class="cta-flag">ES</span>
    <span class="cta-label"><span class="lang-en">Llama en Español</span><span class="lang-es">Llama en Español</span></span>
    <span class="cta-num">{B["phone_manhattan_es"]}</span>
  </a>
  <div class="lang-toggle" role="group" aria-label="Language toggle">
    <button type="button" data-lang="en">EN</button>
    <button type="button" data-lang="es">ES</button>
  </div>
</div>'''

# Main header — logo left, nav center single line, hamburger right
def header_html(active_key=""):
    links = "".join(
        f'<a href="{p}" class="{"active" if k==active_key else ""}">{bi(NAV[k])}</a>'
        for k,p in NAV_ITEMS
    )
    return f'''<header class="site-header">
  <div class="header-inner">
    <a class="brand-logo" href="/" aria-label="American Barber Institute home">
      <img src="/assets/logo.jpeg" alt="ABI">
      <span class="brand-name"><span class="brand-line1">American Barber</span><span class="brand-line2">Institute</span></span>
    </a>
    <nav class="primary-nav" id="primary-nav">{links}</nav>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''

# Sticky mobile bottom bar (EN + ES side-by-side)
def sticky_call():
    return f'''<div class="sticky-call" role="region" aria-label="Quick call">
  <a class="en" href="tel:{tel(B["phone_manhattan"])}"><span class="flag">EN</span> {B["phone_manhattan"]}</a>
  <a class="es" href="tel:{tel(B["phone_manhattan_es"])}"><span class="flag">ES</span> {B["phone_manhattan_es"]}</a>
</div>'''

def footer_html():
    nav_items_visible = NAV_ITEMS  # no haircuts
    nav_html = "".join(f'<a href="{p}">{bi(NAV[k])}</a>' for k,p in nav_items_visible if k != "home")
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>American Barber Institute</h4>
        <p>{bi({"en":"New York's only dedicated barber school. 30+ years. 10,000+ graduates.","es":"La única escuela de barbería dedicada en NY. 30+ años. 10,000+ graduados."})}</p>
        <p style="margin-top:10px;font-size:.85rem">{bi({"en":"Licensed by NY State Dept. of Education (BPSS). GI Bill® · ACCES-VR.","es":"Licenciada por el Depto. de Educación de NY (BPSS). GI Bill® · ACCES-VR."})}</p>
      </div>
      <div>
        <h4>{bi({"en":"Pages","es":"Páginas"})}</h4>
        {nav_html}
      </div>
      <div>
        <h4>{bi({"en":"Contact","es":"Contacto"})}</h4>
        <a href="tel:{tel(B["phone_manhattan"])}">Manhattan EN · {B["phone_manhattan"]}</a>
        <a href="tel:{tel(B["phone_manhattan_es"])}">Manhattan ES · {B["phone_manhattan_es"]}</a>
        <a href="tel:{tel(B["phone_bronx"])}">Bronx · {B["phone_bronx"]}</a>
        <a href="mailto:{B["email"]}">{B["email"]}</a>
      </div>
      <div>
        <h4>{bi({"en":"Campuses","es":"Campus"})}</h4>
        <p>48 W 39th St, NY 10018</p>
        <p>121 Westchester Sq, Bronx 10461</p>
        <p style="margin-top:8px;font-size:.85rem">Mon–Fri 8AM–8PM · Sat–Sun 9AM–7PM</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 American Barber Institute. <span class="lang-en">All rights reserved.</span><span class="lang-es">Todos los derechos reservados.</span></span>
    </div>
  </div>
</footer>'''

# Decoration layer — site-specific extra visual element
def decoration_layer(tokens):
    deco = tokens.get("decoration","")
    if deco == "neon-glow":
        return '<div class="deco-neon" aria-hidden="true"></div>'
    if deco == "chrome-brutalism":
        return '<div class="deco-chrome" aria-hidden="true"></div>'
    if deco == "holographic":
        return '<div class="deco-holo" aria-hidden="true"></div>'
    if deco == "hud-scanlines":
        return '<div class="deco-hud" aria-hidden="true"></div>'
    if deco == "luxe-gold":
        return '<div class="deco-gold" aria-hidden="true"></div>'
    if deco == "particle-network":
        return '<div class="deco-grid" aria-hidden="true"></div>'
    if deco == "flat-brutalist":
        return '<div class="deco-flat" aria-hidden="true"></div>'
    if deco == "aurora-orbs":
        return '<div class="deco-orbs" aria-hidden="true"><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span></div>'
    if deco == "noir-spotlight":
        return '<div class="deco-spotlight" aria-hidden="true"></div>'
    if deco == "vapor-grid":
        return '<div class="deco-vapor" aria-hidden="true"><span class="vsun"></span></div>'
    return ''

# ============== UNIVERSAL CSS — mobile-first ==============
def css_for_site(t):
    button_radius = t["button_radius"]
    card_radius = t["card_radius"]
    button_shape = t.get("button_shape","pill")
    button_clip = ""
    if button_shape == "clip-blade":
        button_clip = "clip-path: polygon(6% 0,100% 0,94% 100%,0 100%);"
    
    # H1 effects per site
    h1_effect_css = ""
    h1_class_target = "h1, .subpage-hero h1"
    if t.get("h1_effect") == "glow":
        h1_effect_css = f"{h1_class_target} {{ text-shadow: 0 0 24px {t['accent']}66, 0 0 48px {t['accent']}33; }}"
    elif t.get("h1_effect") == "holo-gradient":
        h1_effect_css = f"{h1_class_target} {{ background: linear-gradient(90deg, {t['accent']}, {t.get('accent2',t['accent'])}, {t.get('accent3',t['accent'])}, {t['accent']}); background-size: 300% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: holoflow 8s linear infinite; }} @keyframes holoflow {{ from{{background-position:0% 50%}} to {{background-position:300% 50%}} }}"
    elif t.get("h1_effect") == "gold-sheen":
        h1_effect_css = f"{h1_class_target} {{ background: linear-gradient(90deg, {t['accent']}, {t.get('accent2',t['accent'])}, {t['accent']}); background-size: 200% 100%; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: sheen 6s ease infinite; }} @keyframes sheen {{ 0%,100%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} }}"
    elif t.get("h1_effect") == "chrome":
        h1_effect_css = f"{h1_class_target} {{ background: linear-gradient(180deg,#fff 0%,{t['mut']} 50%,#fff 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }}"
    elif t.get("h1_effect") == "hud":
        h1_effect_css = f"{h1_class_target} {{ color: {t['ink']}; }} {h1_class_target} .accent {{ color: {t['accent']}; }}"
    elif t.get("h1_effect") == "neon-shadow":
        h1_effect_css = f"{h1_class_target} {{ text-shadow: 0 0 20px {t['accent']}66; }}"
    elif t.get("h1_effect") == "vapor-shadow":
        h1_effect_css = f"{h1_class_target} {{ text-shadow: 3px 3px 0 {t.get('accent2',t['accent'])}, -2px -2px 0 {t['accent']}; }}"

    # Decoration-specific CSS
    decoration_css = ""
    if t.get("decoration") == "neon-glow":
        decoration_css = f".deco-neon {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(ellipse 80% 60% at 20% 0%, {t['accent']}22 0, transparent 50%), radial-gradient(ellipse 60% 50% at 90% 100%, {t['accent2']}22 0, transparent 50%); }}"
    elif t.get("decoration") == "chrome-brutalism":
        decoration_css = f".deco-chrome {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: linear-gradient(135deg, transparent 0, transparent 49%, {t['line']} 49%, {t['line']} 51%, transparent 51%, transparent 100%); background-size: 80px 80px; opacity: .4; }}"
    elif t.get("decoration") == "holographic":
        decoration_css = f".deco-holo {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(circle at 25% 25%, {t['accent']}33 0, transparent 40%), radial-gradient(circle at 75% 75%, {t['accent2']}33 0, transparent 40%); }}"
    elif t.get("decoration") == "hud-scanlines":
        decoration_css = f".deco-hud {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: repeating-linear-gradient(0deg, transparent 0 3px, {t['accent2']}0a 3px 4px); mix-blend-mode: screen; }}"
    elif t.get("decoration") == "luxe-gold":
        decoration_css = f".deco-gold {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(ellipse 50% 40% at 50% 0%, {t['accent']}22 0, transparent 60%); }}"
    elif t.get("decoration") == "particle-network":
        decoration_css = f".deco-grid {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background-image: linear-gradient({t['accent']}11 1px, transparent 1px), linear-gradient(90deg, {t['accent']}11 1px, transparent 1px); background-size: 64px 64px; mask-image: radial-gradient(circle at center, black 0, transparent 70%); }}"
    elif t.get("decoration") == "flat-brutalist":
        decoration_css = f".deco-flat {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: linear-gradient(180deg, transparent 0, transparent 70%, {t['accent']}0a 100%); }}"
    elif t.get("decoration") == "aurora-orbs":
        decoration_css = f""".deco-orbs {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; overflow: hidden; }}
.deco-orbs .orb {{ position: absolute; width: 480px; height: 480px; border-radius: 50%; filter: blur(120px); opacity: .35; animation: orbDrift 20s ease-in-out infinite; }}
.deco-orbs .o1 {{ background: {t['accent']}; top: -20%; left: -10%; }}
.deco-orbs .o2 {{ background: {t['accent2']}; top: 40%; right: -10%; animation-delay: -7s; }}
.deco-orbs .o3 {{ background: {t.get('accent3', t['accent'])}; bottom: -10%; left: 30%; animation-delay: -14s; }}
@keyframes orbDrift {{ 0%,100%{{transform:translate(0,0)}} 33%{{transform:translate(40px,-40px)}} 66%{{transform:translate(-30px,30px)}} }}"""
    elif t.get("decoration") == "noir-spotlight":
        decoration_css = f".deco-spotlight {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; background: radial-gradient(circle 560px at var(--spot-x, 50%) var(--spot-y, 30%), {t['accent']}22 0, transparent 100%); transition: background .3s; }}"
    elif t.get("decoration") == "vapor-grid":
        decoration_css = f""".deco-vapor {{ position: fixed; inset: 0; pointer-events: none; z-index: 1; perspective: 800px; overflow: hidden; }}
.deco-vapor::before {{ content: ""; position: absolute; bottom: 0; left: -50%; right: -50%; height: 50%; background-image: linear-gradient({t['accent']}66 1px, transparent 1px), linear-gradient(90deg, {t['accent']}66 1px, transparent 1px); background-size: 50px 50px; transform: rotateX(60deg); mask-image: linear-gradient(180deg, transparent 0, black 50%, black 100%); }}
.vsun {{ position: absolute; left: 50%; top: 50%; width: 280px; height: 280px; border-radius: 50%; background: radial-gradient(circle, {t['accent2']} 0, {t['accent']} 70%, transparent 100%); transform: translate(-50%, -75%); filter: blur(2px); opacity: .25; }}"""

    return f'''<style>
:root {{
  --bg: {t['bg']};
  --bg2: {t['bg2']};
  --ink: {t['ink']};
  --mut: {t['mut']};
  --accent: {t['accent']};
  --accent2: {t.get('accent2', t['accent'])};
  --accent3: {t.get('accent3', t['accent'])};
  --line: {t['line']};
  --glass: {t['glass']};
  --card-r: {card_radius};
  --btn-r: {button_radius};
  --touch: 48px;
  --safe-top: env(safe-area-inset-top);
  --safe-bottom: env(safe-area-inset-bottom);
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; text-size-adjust: 100%; -webkit-tap-highlight-color: transparent; }}
body {{
  background: var(--bg);
  color: var(--ink);
  font-family: {t['body_font']};
  line-height: 1.65;
  font-size: 16px;
  overflow-x: hidden;
  min-height: 100vh;
  min-height: 100svh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding-bottom: calc(82px + var(--safe-bottom));
}}
@media (min-width: 981px) {{ body {{ padding-bottom: 0; }} }}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; height: auto; display: block; }}
video {{ max-width: 100%; height: auto; }}
button {{ font-family: inherit; cursor: pointer; }}

h1, h2, h3, h4 {{ font-family: {t['heading_font']}; letter-spacing: {t['heading_ls']}; line-height: {t['heading_lh']}; color: var(--ink); }}
h1 {{ font-size: clamp(2rem, 7vw, 4.6rem); }}
h2 {{ font-size: clamp(1.5rem, 4.4vw, 2.6rem); }}
h3 {{ font-size: clamp(1.15rem, 2.8vw, 1.4rem); }}

/* Language switcher */
body.lang-en .lang-es, body.lang-es .lang-en {{ display: none !important; }}

/* Page transitions */
@media (prefers-reduced-motion: no-preference) {{
  @view-transition {{ navigation: auto; }}
  body {{ animation: pageIn .42s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes pageIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .reveal {{ animation: revealUp .6s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes revealUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
}}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation-duration: .001s !important; transition-duration: .001s !important; }} }}

/* Background video + overlay */
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100vh; height: 100svh; object-fit: cover; z-index: 0; opacity: .14; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .07; }} }}
.bg-overlay {{ position: fixed; inset: 0; background: radial-gradient(ellipse at center, transparent 0, rgba(0,0,0,.4) 70%, var(--bg) 100%); z-index: 1; pointer-events: none; }}

{decoration_css}

/* Top banner — centered call buttons + lang toggle */
.top-banner {{
  position: relative; z-index: 40;
  background: {t['ribbon_bg']};
  color: {t['ribbon_color']};
  padding: 10px 14px calc(10px + var(--safe-top));
  display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap;
}}
.cta-call {{
  display: inline-flex; align-items: center; gap: 8px;
  padding: 9px 18px; min-height: 44px;
  background: rgba(0,0,0,.18);
  color: inherit;
  border-radius: 999px;
  font-weight: 800; font-size: .82rem;
  border: 2px solid currentColor;
  white-space: nowrap;
  transition: transform .2s, background .2s;
}}
.cta-call:hover {{ background: rgba(0,0,0,.35); transform: translateY(-1px); }}
.cta-call .cta-flag {{ font-size: .68rem; padding: 2px 7px; border: 1.5px solid currentColor; border-radius: 999px; font-weight: 900; letter-spacing: .08em; }}
.cta-call .cta-label {{ font-size: .8rem; font-weight: 700; letter-spacing: .04em; }}
.cta-call .cta-num {{ font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-size: .88rem; font-weight: 800; }}

.lang-toggle {{ display: inline-flex; align-items: stretch; height: 38px; border-radius: 999px; border: 2px solid currentColor; overflow: hidden; }}
.lang-toggle button {{ background: transparent; border: 0; color: inherit; padding: 0 14px; min-width: 44px; cursor: pointer; font-weight: 900; letter-spacing: .12em; font-family: inherit; font-size: .78rem; }}
.lang-toggle button.active {{ background: rgba(0,0,0,.35); }}

/* Header */
.site-header {{
  position: sticky; top: 0; z-index: 30;
  background: var(--glass);
  backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--line);
}}
.header-inner {{
  display: flex; align-items: center; gap: 16px;
  height: 68px; padding: 0 18px;
  max-width: 1280px; margin: 0 auto;
}}
.brand-logo {{ display: flex; align-items: center; gap: 12px; flex-shrink: 0; min-width: 0; }}
.brand-logo img {{ width: 40px; height: 40px; border-radius: 10px; object-fit: cover; flex-shrink: 0; }}
.brand-name {{ font-family: {t['heading_font']}; font-weight: 800; letter-spacing: .02em; line-height: 1.1; display: flex; flex-direction: column; font-size: .92rem; }}
.brand-name .brand-line1 {{ color: var(--ink); }}
.brand-name .brand-line2 {{ color: var(--accent); }}

.primary-nav {{
  display: flex; align-items: center; gap: 4px;
  flex: 1; justify-content: center; flex-wrap: nowrap;
  overflow: hidden;
}}
.primary-nav a {{
  color: var(--mut); padding: 8px 10px; min-height: 44px;
  display: inline-flex; align-items: center;
  font-size: .82rem; font-weight: 600; letter-spacing: .02em;
  white-space: nowrap;
  border-radius: 8px;
  transition: color .2s, background .2s;
}}
.primary-nav a:hover, .primary-nav a.active {{ color: var(--accent); background: rgba(255,255,255,.04); }}

.burger {{ width: 48px; height: 48px; display: none; flex-direction: column; gap: 5px; align-items: center; justify-content: center; background: transparent; border: 0; }}
.burger span {{ width: 26px; height: 2px; background: var(--accent); transition: .2s; border-radius: 2px; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

/* Responsive nav — hamburger on tablet/mobile */
@media (max-width: 1100px) {{
  .primary-nav {{
    position: fixed; inset: 134px 0 auto 0;
    flex-direction: column; align-items: stretch; gap: 0;
    background: var(--bg);
    backdrop-filter: blur(20px);
    padding: 12px 18px 28px;
    transform: translateY(-130%); transition: transform .3s ease;
    box-shadow: 0 24px 48px rgba(0,0,0,.5);
    max-height: calc(100vh - 134px); overflow-y: auto;
    border-bottom: 1px solid var(--line);
  }}
  .primary-nav.open {{ transform: translateY(0); }}
  .primary-nav a {{ padding: 16px 8px; border-bottom: 1px solid var(--line); font-size: 1.05rem; min-height: 56px; }}
  .primary-nav a:last-child {{ border-bottom: 0; }}
  .burger {{ display: inline-flex; margin-left: auto; }}
}}
@media (max-width: 760px) {{
  .header-inner {{ height: 64px; padding: 0 14px; }}
  .brand-name {{ font-size: .85rem; }}
  .top-banner {{ padding: 8px 10px calc(8px + var(--safe-top)); gap: 6px; }}
  .cta-call {{ padding: 7px 12px; min-height: 40px; font-size: .76rem; gap: 6px; }}
  .cta-call .cta-num {{ font-size: .82rem; }}
  .lang-toggle {{ height: 36px; }}
  .primary-nav {{ inset: 124px 0 auto 0; max-height: calc(100vh - 124px); }}
}}
@media (max-width: 480px) {{
  .header-inner {{ height: 60px; padding: 0 12px; }}
  .brand-name .brand-line2 {{ display: none; }}
  .brand-name {{ font-size: .8rem; }}
  .brand-logo img {{ width: 36px; height: 36px; }}
  .top-banner {{ padding: 7px 8px calc(7px + var(--safe-top)); gap: 5px; }}
  .cta-call {{ padding: 6px 10px; min-height: 38px; font-size: .7rem; }}
  .cta-call .cta-label {{ display: none; }}
  .cta-call .cta-num {{ font-size: .78rem; }}
  .cta-call .cta-flag {{ font-size: .62rem; padding: 1px 5px; }}
  .primary-nav {{ inset: 116px 0 auto 0; max-height: calc(100vh - 116px); }}
}}

/* Subpage hero */
.subpage-hero {{ position: relative; z-index: 2; padding: clamp(48px, 8vw, 100px) 0 clamp(36px, 6vw, 60px); text-align: center; }}
.subpage-hero .container {{ max-width: 940px; }}
.eyebrow {{ display: inline-block; padding: 7px 16px; border: 1px solid var(--line); border-radius: 999px; font-size: .7rem; letter-spacing: .3em; text-transform: uppercase; color: var(--accent); font-weight: 800; }}
.subpage-hero h1 {{ margin: 22px 0 14px; }}
{h1_effect_css}
.subpage-hero p.sub {{ max-width: 720px; margin: 0 auto; color: var(--mut); font-size: clamp(1rem, 2.2vw, 1.12rem); }}

section {{ padding: clamp(36px, 6vw, 64px) 0; position: relative; z-index: 2; }}
section h2 {{ margin-bottom: 14px; }}
section p.lead {{ color: var(--mut); max-width: 780px; margin-bottom: 24px; font-size: clamp(1rem, 2.2vw, 1.08rem); }}

.container {{ max-width: 1200px; margin: 0 auto; padding: 0 clamp(14px, 4vw, 28px); position: relative; z-index: 2; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: clamp(12px, 2.4vw, 20px); }}
.grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: clamp(14px, 2.6vw, 22px); }}
.gallery-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: clamp(8px, 1.6vw, 14px); }}

.card {{ background: var(--glass); border: 1px solid var(--line); border-radius: var(--card-r); padding: clamp(20px, 3vw, 28px); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); transition: transform .3s, border-color .3s, box-shadow .3s; }}
.card:hover {{ transform: translateY(-4px); border-color: var(--accent); box-shadow: 0 16px 40px rgba(0,0,0,.35); }}

.partner-card {{ overflow: hidden; padding: 0; display: flex; flex-direction: column; }}
.partner-card .img-wrap {{ position: relative; aspect-ratio: 16/10; overflow: hidden; background: var(--bg2); }}
.partner-card .img-wrap img {{ width: 100%; height: 100%; object-fit: cover; transition: transform .5s; }}
.partner-card:hover .img-wrap img {{ transform: scale(1.06); }}
.partner-card .img-wrap::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 50%, rgba(0,0,0,.55) 100%); }}
.partner-card .img-wrap .partner-name {{ position: absolute; left: 18px; bottom: 14px; z-index: 2; font-family: {t['heading_font']}; font-size: 1.3rem; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.6); }}
.partner-card .body {{ padding: 22px; }}
.partner-card .locations {{ font-size: .72rem; letter-spacing: .2em; text-transform: uppercase; color: var(--accent); font-weight: 700; margin-bottom: 10px; }}
.partner-card .desc {{ color: var(--mut); font-size: .94rem; margin-bottom: 12px; }}
.partner-card .why {{ font-size: .88rem; color: var(--accent); font-weight: 700; }}

.gallery-tile {{ position: relative; aspect-ratio: 4/3; overflow: hidden; border-radius: var(--card-r); background: var(--bg2); border: 1px solid var(--line); cursor: zoom-in; }}
.gallery-tile img {{ width: 100%; height: 100%; object-fit: cover; transition: transform .6s cubic-bezier(.2,.8,.2,1); }}
.gallery-tile:hover img {{ transform: scale(1.08); }}
.gallery-tile::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, transparent 60%, rgba(0,0,0,.4) 100%); opacity: 0; transition: opacity .3s; }}
.gallery-tile:hover::after {{ opacity: 1; }}

.btn {{
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px 28px; min-height: 48px;
  border-radius: var(--btn-r);
  font-weight: 800; font-size: .94rem;
  text-decoration: none; border: 0;
  cursor: pointer;
  transition: transform .2s, filter .2s, background .2s, box-shadow .2s;
  {button_clip}
}}
.btn-primary {{ background: var(--accent); color: var(--bg); }}
.btn-primary:hover {{ filter: brightness(1.08); transform: translateY(-2px); box-shadow: 0 14px 28px rgba(0,0,0,.32); }}
.btn-ghost {{ border: 2px solid var(--accent); color: var(--accent); background: transparent; }}
.btn-ghost:hover {{ background: var(--accent); color: var(--bg); }}

.input {{ background: var(--bg2); border: 1px solid var(--line); border-radius: var(--card-r); padding: 14px; color: var(--ink); font-size: 1rem; font-family: inherit; min-height: 48px; -webkit-appearance: none; appearance: none; }}
.input:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent); }}

.eyebrow-acc {{ color: var(--accent); font-size: .72rem; letter-spacing: .28em; text-transform: uppercase; font-weight: 800; }}
.row-stat {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin: 22px 0; }}
.row-stat .s {{ padding: 18px 14px; border: 1px solid var(--line); border-radius: var(--card-r); background: var(--glass); }}
.row-stat .s b {{ display: block; font-size: clamp(1.4rem, 4vw, 2rem); color: var(--accent); font-weight: 800; line-height: 1.1; font-family: {t['heading_font']}; }}
.row-stat .s small {{ color: var(--mut); font-size: .82rem; }}
.list-clean {{ list-style: none; padding: 0; }}
.list-clean li {{ padding: 12px 0; border-bottom: 1px solid var(--line); color: var(--mut); }}
.list-clean li:last-child {{ border-bottom: 0; }}
.list-clean li::before {{ content: "▸ "; color: var(--accent); font-weight: 800; }}
.contact-strip {{ display: flex; gap: 14px; flex-wrap: wrap; padding: 16px 18px; border: 1px solid var(--accent); border-radius: var(--card-r); background: var(--glass); margin: 20px 0; }}
.contact-strip a {{ color: var(--accent); font-weight: 800; }}

details.card summary {{ cursor: pointer; font-weight: 800; font-size: 1.05rem; min-height: 32px; list-style: none; padding-right: 20px; position: relative; }}
details.card summary::-webkit-details-marker {{ display: none; }}
details.card summary::after {{ content: "+"; position: absolute; right: 4px; top: 0; color: var(--accent); font-size: 1.4rem; transition: transform .2s; }}
details.card[open] summary::after {{ transform: rotate(45deg); }}

/* Footer */
.site-footer {{ padding: clamp(40px, 6vw, 60px) 0 clamp(80px, 9vw, 100px); border-top: 1px solid var(--line); margin-top: 60px; background: rgba(0,0,0,.4); color: var(--mut); position: relative; z-index: 2; font-size: .9rem; }}
.footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1.2fr 1fr; gap: clamp(20px, 3vw, 32px); margin-bottom: 26px; }}
.footer-grid h4 {{ font-size: .82rem; text-transform: uppercase; letter-spacing: .18em; color: var(--ink); margin-bottom: 12px; font-family: {t['heading_font']}; }}
.footer-grid a {{ display: block; padding: 4px 0; color: var(--mut); }}
.footer-grid a:hover {{ color: var(--accent); }}
.footer-bottom {{ padding-top: 24px; border-top: 1px solid var(--line); font-size: .78rem; text-align: center; }}
@media (max-width: 860px) {{ .footer-grid {{ grid-template-columns: 1fr 1fr; }} }}
@media (max-width: 480px) {{ .footer-grid {{ grid-template-columns: 1fr; }} }}

/* Sticky mobile bottom bar */
.sticky-call {{ display: none; position: fixed; left: max(12px, var(--safe-bottom)); right: 12px; bottom: calc(12px + var(--safe-bottom)); z-index: 50; gap: 8px; }}
.sticky-call a {{ flex: 1; padding: 14px 10px; min-height: 52px; border-radius: 999px; font-weight: 800; font-size: .88rem; text-align: center; text-decoration: none; box-shadow: 0 16px 40px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06); display: inline-flex; align-items: center; justify-content: center; gap: 6px; }}
.sticky-call a.en {{ background: var(--accent); color: var(--bg); }}
.sticky-call a.es {{ background: var(--bg2); color: var(--ink); border: 2px solid var(--accent); }}
.sticky-call .flag {{ font-size: .68rem; padding: 1px 6px; border: 1px solid currentColor; border-radius: 999px; font-weight: 900; }}
@media (max-width: 980px) {{ .sticky-call {{ display: flex; }} }}

@media (max-width: 480px) {{
  section {{ padding: clamp(28px, 5vw, 48px) 0; }}
  .subpage-hero {{ padding: clamp(36px, 6vw, 70px) 0 clamp(24px, 4vw, 40px); }}
  .row-stat {{ grid-template-columns: 1fr 1fr; gap: 8px; }}
  .row-stat .s {{ padding: 14px 10px; }}
  .row-stat .s b {{ font-size: 1.3rem; }}
}}

/* ============ ANIMATED STAT COUNTERS ============ */
.stats-band {{ padding: clamp(28px, 5vw, 56px) 0; }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: clamp(10px, 2vw, 18px); }}
.stat-card {{ padding: clamp(22px, 3vw, 32px) clamp(16px, 2.4vw, 22px); border: 1px solid var(--line); border-radius: var(--card-r); background: var(--glass); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); position: relative; overflow: hidden; transition: transform .3s, border-color .3s; text-align: center; }}
.stat-card:hover {{ transform: translateY(-4px); border-color: var(--accent); }}
.stat-card::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--accent); transform: scaleY(0); transform-origin: top; transition: transform .4s cubic-bezier(.2,.8,.2,1); }}
.stat-card.in::before, .stat-card:hover::before {{ transform: scaleY(1); }}
.stat-card .count {{ display: block; font-size: clamp(2.2rem, 7vw, 4rem); font-weight: 900; color: var(--accent); line-height: 1; font-family: {t['heading_font']}; letter-spacing: -.02em; margin-bottom: 6px; font-variant-numeric: tabular-nums; }}
.stat-card .label {{ display: block; font-size: clamp(.78rem, 1.6vw, .92rem); color: var(--mut); font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }}
.stat-card .sublabel {{ display: block; font-size: .7rem; color: var(--mut); opacity: .65; margin-top: 4px; }}

/* ============ RESPONSIVE LOGO (mobile-first) ============ */
.brand-logo img {{ width: clamp(34px, 4.6vw, 44px); height: clamp(34px, 4.6vw, 44px); border-radius: clamp(8px, 1vw, 11px); object-fit: cover; flex-shrink: 0; box-shadow: 0 6px 18px rgba(0,0,0,.25); border: 1px solid var(--line); }}
.brand-name {{ font-size: clamp(.78rem, 1.7vw, .98rem); }}
@media (max-width: 1180px) {{ .brand-name .brand-line2 {{ font-size: .82em; }} }}
@media (max-width: 760px) {{ .brand-logo img {{ width: 38px; height: 38px; }} .brand-name {{ font-size: .85rem; }} }}
@media (max-width: 480px) {{ .brand-logo img {{ width: 34px; height: 34px; border-radius: 8px; }} .brand-name .brand-line1 {{ font-size: .82rem; }} .brand-name .brand-line2 {{ display: none; }} }}
@media (max-width: 360px) {{ .brand-logo img {{ width: 32px; height: 32px; }} .brand-name {{ display: none; }} }}

/* ============ PHONES NEVER HIDDEN ============ */
.cta-call .cta-num {{ font-family: ui-monospace, 'SF Mono', Menlo, monospace; font-weight: 900; }}
@media (max-width: 480px) {{ .cta-call .cta-num {{ font-size: .82rem; }} }}
@media (max-width: 360px) {{ .cta-call {{ padding: 6px 8px; }} .cta-call .cta-num {{ font-size: .78rem; }} }}

/* ============ UPGRADED CONTACT FORM ============ */
.form-grid {{ display: grid; gap: 14px; }}
.form-grid .row-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
@media (max-width: 540px) {{ .form-grid .row-2 {{ grid-template-columns: 1fr; }} }}
.field-group {{ display: flex; flex-direction: column; gap: 6px; }}
.field-group label {{ font-size: .76rem; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); font-weight: 800; }}
.field-group small.hint {{ font-size: .76rem; color: var(--mut); }}
.radio-row {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.radio-pill {{ position: relative; cursor: pointer; }}
.radio-pill input {{ position: absolute; opacity: 0; pointer-events: none; }}
.radio-pill span {{ display: inline-block; padding: 10px 18px; min-height: 44px; line-height: 24px; border: 1.5px solid var(--line); border-radius: 999px; font-size: .88rem; font-weight: 700; color: var(--mut); transition: all .2s; user-select: none; }}
.radio-pill input:checked + span {{ background: var(--accent); color: var(--bg); border-color: var(--accent); }}
.radio-pill:hover span {{ border-color: var(--accent); color: var(--accent); }}
.form-cta {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-top: 8px; }}
.form-cta .privacy {{ font-size: .78rem; color: var(--mut); flex: 1; min-width: 200px; }}
</style>'''

# ============== JS — hamburger + lang + page transition ==============
JS = '''<script>
(function() {
  // Language switcher
  var saved = localStorage.getItem('abi_lang') || 'en';
  document.body.classList.remove('lang-en','lang-es');
  document.body.classList.add('lang-' + saved);
  document.documentElement.lang = saved;
  function setLang(lang) {
    document.body.classList.remove('lang-en','lang-es');
    document.body.classList.add('lang-' + lang);
    document.documentElement.lang = lang;
    localStorage.setItem('abi_lang', lang);
    document.querySelectorAll('.lang-toggle button').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('data-lang') === lang);
    });
  }
  document.querySelectorAll('.lang-toggle button').forEach(function(b) {
    b.addEventListener('click', function() { setLang(this.getAttribute('data-lang')); });
    if (b.getAttribute('data-lang') === saved) b.classList.add('active');
  });

  // Hamburger
  var nav = document.querySelector('.primary-nav');
  var burger = document.querySelector('.burger');
  if (nav && burger) {
    function close() { nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); document.body.style.overflow = ''; }
    burger.addEventListener('click', function() {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true':'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach(function(a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function(e) { if (e.key==='Escape') close(); });
  }

  // Spotlight follow (only used by noir-spotlight decoration)
  if (document.querySelector('.deco-spotlight')) {
    var el = document.querySelector('.deco-spotlight');
    document.addEventListener('mousemove', function(e) {
      el.style.setProperty('--spot-x', e.clientX + 'px');
      el.style.setProperty('--spot-y', e.clientY + 'px');
    });
  }

  // Reveal on scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('reveal'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('section, .card, .row-stat .s').forEach(function(el) { io.observe(el); });
  }

  // Animated counters
  if ('IntersectionObserver' in window) {
    var counters = document.querySelectorAll('.stat-card .count[data-target]');
    var countObs = new IntersectionObserver(function(entries) {
      entries.forEach(function(en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var target = parseInt(el.getAttribute('data-target'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var prefix = el.getAttribute('data-prefix') || '';
        var dur = 1400;
        var start = performance.now();
        el.parentElement.classList.add('in');
        function step(t) {
          var p = Math.min(1, (t - start) / dur);
          var eased = 1 - Math.pow(1 - p, 3);
          var n = Math.floor(target * eased);
          el.textContent = prefix + n.toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = prefix + target.toLocaleString() + suffix;
        }
        requestAnimationFrame(step);
        countObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function(c) { countObs.observe(c); });
  }
})();
</script>'''

# ============== SUBPAGE TEMPLATE ==============
SUBPAGE_TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=5">
<title>{title}</title>
{head_meta}
{jsonld}
{css}
</head>
<body class="lang-en">
<video class="bg-video" autoplay muted loop playsinline poster="/assets/logo.jpeg" aria-hidden="true"><source src="/assets/bg.mp4" type="video/mp4"></video>
<div class="bg-overlay"></div>
{decoration}
{top_banner}
{header}
<main>
  <section class="subpage-hero">
    <div class="container">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
    </div>
  </section>
  {body}
</main>
{footer}
{sticky_call}
{js}
</body>
</html>'''

def render_subpage(tokens, page_key, pdata):
    return SUBPAGE_TPL.format(
        title=PAGE_TITLES[pdata["path"]],
        head_meta=head_meta(pdata["path"]),
        jsonld=jsonld(include_faq=(page_key=="faq")),
        css=css_for_site(tokens),
        decoration=decoration_layer(tokens),
        top_banner=top_banner(),
        header=header_html(page_key),
        eyebrow=pdata["eyebrow"], h1=pdata["h1"], sub=pdata["sub"], body=pdata["body"],
        footer=footer_html(),
        sticky_call=sticky_call(),
        js=JS,
    )

# ============== PAGE CONTENT BUILDERS ==============

def p_about():
    instr_cards = "".join(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{bi(i["role"])}</div><h3 style="margin-bottom:10px">{i["name"]}</h3><p style="color:var(--mut);margin-bottom:10px">{bi(i["bio"])}</p><p style="font-size:.8rem;color:var(--accent);font-weight:700">{" · ".join(bi(t) for t in i["tags"])}</p></div>' for i in CONTENT["instructors"][:3])
    why = "".join(f"<li>{bi(w)}</li>" for w in CONTENT["why_choose"])
    return {"path":"/about",
        "eyebrow": bi({"en":"About ABI","es":"Acerca de ABI"}),
        "h1": bi({"en":"30+ years. 10,000+ graduates. One craft.","es":"30+ años. 10,000+ graduados. Un oficio."}),
        "sub": bi({"en":"American Barber Institute is New York's only dedicated barber school — changing lives in Manhattan and the Bronx for over three decades.","es":"American Barber Institute es la única escuela de barbería dedicada de Nueva York — cambiando vidas en Manhattan y el Bronx por más de tres décadas."}),
        "body": f'''<section><div class="container"><div class="grid-2">
<div><h2>{bi({"en":"Our story","es":"Nuestra historia"})}</h2><p class="lead">{bi({"en":"ABI was built on a simple idea: barbering deserves a school that does <em>only</em> barbering. No nails. No esthetics. No detours. Just the craft, taught by master barbers, on a working clinic floor.","es":"ABI fue construida con una idea simple: la barbería merece una escuela que se dedique <em>solo</em> a la barbería. Sin uñas. Sin estética. Sin desvíos. Solo el oficio, enseñado por maestros barberos."})}</p><p class="lead">{bi({"en":"Three decades and ten thousand graduates later, that idea has produced the people behind some of New York's most respected shops.","es":"Tres décadas y diez mil graduados después, esa idea ha producido a las personas detrás de algunas de las barberías más respetadas de Nueva York."})}</p></div>
<div class="card"><h3 style="margin-bottom:10px">{bi({"en":"The facility","es":"Las instalaciones"})}</h3><p style="color:var(--mut)">{bi(B["facility"])}.</p>
<div class="row-stat"><div class="s"><b>{B["years_in_business"]}</b><small>{bi({"en":"Years","es":"Años"})}</small></div><div class="s"><b>{B["graduates"]}</b><small>{bi({"en":"Graduates","es":"Graduados"})}</small></div><div class="s"><b>{B["rating"]}</b><small>Google</small></div></div></div>
</div></div></section>
<section class="stats-band"><div class="container"><div class="eyebrow-acc" style="margin-bottom:14px;text-align:center;display:block">{bi({"en":"By the numbers","es":"En cifras"})}</div><h2 style="margin-bottom:24px;text-align:center">{bi({"en":"Built on three decades.","es":"Construido sobre tres décadas."})}</h2><div class="stats-grid">
<div class="stat-card"><b class="count" data-target="30" data-suffix="+">0</b><span class="label">{bi({"en":"Years in business","es":"Años en activo"})}</span><span class="sublabel">{bi({"en":"NY State licensed","es":"Licenciado por NY"})}</span></div>
<div class="stat-card"><b class="count" data-target="10000" data-suffix="+">0</b><span class="label">{bi({"en":"Graduates trained","es":"Graduados entrenados"})}</span><span class="sublabel">{bi({"en":"& counting","es":"y subiendo"})}</span></div>
<div class="stat-card"><b class="count" data-target="2" data-suffix="">0</b><span class="label">{bi({"en":"NYC campuses","es":"Campus en NYC"})}</span><span class="sublabel">{bi({"en":"Manhattan + Bronx","es":"Manhattan + Bronx"})}</span></div>
<div class="stat-card"><b class="count" data-target="17" data-suffix="">0</b><span class="label">{bi({"en":"Weeks to license","es":"Semanas a la licencia"})}</span><span class="sublabel">{bi({"en":"Full-time track","es":"Tiempo completo"})}</span></div>
<div class="stat-card"><b class="count" data-target="3000" data-suffix=" sq ft">0</b><span class="label">{bi({"en":"Facility size","es":"Tamaño del campus"})}</span><span class="sublabel">{bi({"en":"Two floors · Midtown","es":"Dos pisos · Midtown"})}</span></div>
<div class="stat-card"><b class="count" data-target="100" data-suffix="+">0</b><span class="label">{bi({"en":"Google reviews","es":"Reseñas Google"})}</span><span class="sublabel">{bi({"en":"4.3★ average","es":"4.3★ promedio"})}</span></div>
</div></div>
</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Leadership","es":"Liderazgo"})}</div><h2 style="margin-bottom:24px">{bi({"en":"The faculty","es":"La facultad"})}</h2><div class="grid">{instr_cards}</div><p style="margin-top:20px"><a class="btn btn-ghost" href="/instructors">{bi({"en":"Meet all instructors →","es":"Conoce a todos →"})}</a></p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Why ABI","es":"Por qué ABI"})}</div><h2 style="margin-bottom:18px">{bi({"en":"What makes us different","es":"Lo que nos hace diferentes"})}</h2><ul class="list-clean" style="max-width:820px">{why}</ul></div></section>
<section><div class="container" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_programs():
    rows = []
    for p in CONTENT["programs"]:
        flag = f'<span style="position:absolute;top:14px;right:14px;font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;background:var(--accent);color:var(--bg);padding:5px 10px;border-radius:999px;font-weight:800">{bi({"en":"Flagship","es":"Insignia"})}</span>' if p.get("flagship") else ""
        det = f'<p style="color:var(--mut);font-size:.88rem;margin-top:10px">{bi(p["details"])}</p>' if p.get("details") else ""
        price = bi(p["price"]) if isinstance(p["price"], dict) else p["price"]
        rows.append(f'<div class="card" style="position:relative">{flag}<div class="eyebrow-acc">{bi(p["campus"])} · {bi(p["duration"])}</div><h3 style="margin:8px 0">{bi(p["name"])}</h3><div style="font-size:1.4rem;font-weight:800;color:var(--accent);margin-bottom:10px;">{price}</div><p style="color:var(--mut)">{bi(p["summary"])}</p>{det}</div>')
    rows = "".join(rows)
    sched = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(s["label"])}</div><h3 style="margin:8px 0">{bi(s["days"])} · {s["time"]}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:10px 0 6px">{s["tuition"]}</div><p style="color:var(--mut);font-size:.92rem">{bi(s["plan"])}</p></div>' for s in CONTENT["schedules"])
    steps = "".join(f'<div class="card"><div style="font-size:2.4rem;color:var(--accent);font-weight:800;line-height:1;font-family:inherit">0{s["step"]}</div><h3 style="margin:8px 0">{bi(s["title"])}</h3><p style="color:var(--mut);font-size:.94rem">{bi(s["desc"])}</p></div>' for s in CONTENT["enrollment_steps"])
    req = "".join(f"<li>{bi(r)}</li>" for r in CONTENT["requirements"])
    earnings = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(e["window"])}</div><h3 style="margin:8px 0">{bi(e["stage"])}</h3><div style="font-size:1.4rem;font-weight:800;color:var(--accent);margin:6px 0 8px">{e["range"]}</div><p style="color:var(--mut);font-size:.92rem">{bi(e["desc"])}</p></div>' for e in CONTENT["career_earnings"])
    return {"path":"/programs",
        "eyebrow": bi({"en":"Programs & Tuition","es":"Programas y Matrícula"}),
        "h1": bi({"en":"Programs, tuition, what you'll learn.","es":"Programas, matrícula, qué aprenderás."}),
        "sub": bi({"en":"Five programs across two campuses. Three flexible tracks. NY State Master Barber License at the end.","es":"Cinco programas en dos campus. Tres opciones flexibles. Licencia de Maestro Barbero al final."}),
        "body": f'''<section><div class="container"><h2>{bi({"en":"Choose your program","es":"Elige tu programa"})}</h2><p class="lead">{bi({"en":"Every program is state-licensed and exam-prep ready. Flexible weekly payment plans on every track.","es":"Cada programa está licenciado por el estado y listo para el examen. Planes de pago semanales flexibles."})}</p><div class="grid">{rows}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Schedule & Tuition","es":"Horario y Matrícula"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three flexible schedules","es":"Tres horarios flexibles"})}</h2><div class="grid">{sched}</div><p style="margin-top:18px;color:var(--mut);font-size:.92rem">{bi({"en":"Veterans &amp; GI Bill® accepted. ACCES-VR accepted.","es":"Beneficios para Veteranos y GI Bill® aceptados. ACCES-VR aceptado."})} <a href="/resources" style="color:var(--accent);text-decoration:underline">{bi({"en":"See full benefits guide →","es":"Ver guía completa →"})}</a></p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Enrollment","es":"Inscripción"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three steps to your first chair","es":"Tres pasos a tu primer sillón"})}</h2><div class="grid">{steps}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Requirements","es":"Requisitos"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Documents to enroll","es":"Documentos para inscribirte"})}</h2><ul class="list-clean" style="max-width:680px">{req}</ul></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Career earnings","es":"Ingresos de carrera"})}</div><h2 style="margin-bottom:14px">{bi({"en":"What barbers earn","es":"Lo que ganan los barberos"})}</h2><div class="grid">{earnings}</div><p style="margin-top:18px;color:var(--mut);font-size:.85rem">{bi(CONTENT["earnings_note"])}</p></div></section>
<section><div class="container" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">{bi(UI["read_faq"])}</a></div></section>'''}

def p_instructors():
    cards = "".join(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{bi(i["role"])}</div><h3 style="margin-bottom:10px">{i["name"]}</h3><p style="color:var(--mut);line-height:1.7;margin-bottom:14px">{bi(i["bio"])}</p><p style="font-size:.84rem;color:var(--accent);font-weight:700">{" · ".join(bi(t) for t in i["tags"])}</p></div>' for i in CONTENT["instructors"])
    return {"path":"/instructors",
        "eyebrow": bi({"en":"Faculty","es":"Profesorado"}),
        "h1": bi({"en":"Master barbers. Master teachers.","es":"Maestros barberos. Maestros instructores."}),
        "sub": bi({"en":"Decades of working-floor experience and a clinic-first teaching style. You learn by chair time, with an instructor inches away.","es":"Décadas de experiencia en el piso y un estilo de enseñanza centrado en la clínica. Aprendes con tiempo en la silla."}),
        "body": f'''<section><div class="container"><div class="grid-2">{cards}</div></div></section>
<section><div class="container" style="text-align:center"><h2 style="margin-bottom:14px">{bi({"en":"Train with us","es":"Entrena con nosotros"})}</h2><p class="lead" style="margin:0 auto 20px">{bi({"en":"New cohorts begin the first Monday of every month.","es":"Las nuevas generaciones comienzan el primer lunes de cada mes."})}</p><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_gallery(site_dir):
    imgs = sorted([f for f in os.listdir(site_dir/"assets"/"img") if f.lower().endswith(('.jpeg','.jpg','.png'))])[:30]
    tiles = "".join(f'<a class="gallery-tile" href="/assets/img/{f}" target="_blank" rel="noopener"><img src="/assets/img/{f}" loading="lazy" alt="ABI student work"></a>' for f in imgs)
    return {"path":"/gallery",
        "eyebrow": bi({"en":"On the floor","es":"En el piso"}),
        "h1": bi({"en":"Student work. Clinic life. Graduation day.","es":"Trabajo de estudiantes. Vida en la clínica. Día de graduación."}),
        "sub": bi({"en":"A glimpse inside the American Barber Institute. Real students. Real chairs. Real fades.","es":"Un vistazo al interior de American Barber Institute. Estudiantes reales. Sillas reales. Degradados reales."}),
        "body": f'<section><div class="container"><div class="gallery-grid">{tiles}</div></div></section><section><div class="container" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["visit_campus"])}</a></div></section>'}

def p_partners():
    cards = []
    for i, p in enumerate(CONTENT["partners"]):
        img = PARTNER_IMGS[i % len(PARTNER_IMGS)]
        cards.append(f'<div class="card partner-card"><div class="img-wrap"><img src="/assets/img/{img}" loading="lazy" alt="{p["name"]}"><div class="partner-name">{p["name"]}</div></div><div class="body"><div class="locations">{p["locations"]}</div><p class="desc">{bi(p["desc"])}</p><p class="why">→ {bi(p["why"])}</p></div></div>')
    return {"path":"/partners",
        "eyebrow": bi({"en":"Partner Shops","es":"Barberías Aliadas"}),
        "h1": bi({"en":"Where ABI graduates work.","es":"Dónde trabajan los graduados de ABI."}),
        "sub": bi({"en":"Real shops. Real owners. Many of them started right here on the ABI clinic floor.","es":"Barberías reales. Dueños reales. Muchos comenzaron aquí mismo en el piso clínico de ABI."}),
        "body": f'''<section><div class="container"><div class="grid-2">{"".join(cards)}</div></div></section>
<section><div class="container" style="text-align:center"><h2 style="margin-bottom:10px">{bi({"en":"Your path to one of these chairs","es":"Tu camino a una de estas sillas"})}</h2><p class="lead" style="margin:0 auto 20px">{bi({"en":"Our Job Placement Office connects every graduate with our partner network.","es":"Nuestra Oficina de Colocación Laboral conecta a cada graduado con nuestra red."})}</p><a class="btn btn-primary" href="/job-placement">{bi({"en":"See job placement","es":"Ver colocación laboral"})}</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">{bi(UI["talk_admissions"])}</a></div></section>'''}

def p_jobplacement():
    j = CONTENT["job_placement"]
    services = "".join(f"<li>{bi(s)}</li>" for s in j["services"])
    return {"path":"/job-placement",
        "eyebrow": bi({"en":"Job Placement","es":"Colocación Laboral"}),
        "h1": bi({"en":"From license to first chair.","es":"De la licencia a la primera silla."}),
        "sub": bi(j["intro"]),
        "body": f'''<section><div class="container"><div class="grid-2"><div><h2>{bi({"en":"What our Job Placement Office does","es":"Qué hace nuestra Oficina de Colocación Laboral"})}</h2><ul class="list-clean">{services}</ul></div><div class="card"><h3 style="margin-bottom:10px">{bi({"en":"The outcome","es":"El resultado"})}</h3><p style="color:var(--mut);line-height:1.7">{bi(j["outcomes"])}</p><a class="btn btn-primary" style="margin-top:18px" href="/partners">{bi({"en":"See partner shops →","es":"Ver barberías aliadas →"})}</a></div></div></div></section>
<section><div class="container" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_resources():
    r = CONTENT["resources"]
    def block(b):
        items = "".join(f"<li>{bi(i)}</li>" for i in b.get("items", []))
        intro = f'<p style="color:var(--mut);margin-bottom:14px">{bi(b["intro"])}</p>' if b.get("intro") else ""
        outro = f'<p style="color:var(--mut);font-size:.92rem;margin-top:14px">{bi(b["outro"])}</p>' if b.get("outro") else ""
        title = bi(b["title"]) if isinstance(b["title"], dict) else b["title"]
        return f'<div class="card"><h3 style="margin-bottom:10px">{title}</h3>{intro}<ul class="list-clean">{items}</ul>{outro}</div>'
    cards = block(r["veterans"]) + block(r["accesvr"]) + block(r["licensing"]) + block(r["tools"])
    return {"path":"/resources",
        "eyebrow": bi({"en":"Resources","es":"Recursos"}),
        "h1": bi({"en":"Everything you need to start.","es":"Todo lo que necesitas para empezar."}),
        "sub": bi({"en":"Veterans benefits. ACCES-VR. NY State licensing. Tools.","es":"Beneficios para Veteranos. ACCES-VR. Licencias. Herramientas."}),
        "body": f'''<section><div class="container"><div class="grid-2">{cards}</div></div></section>
<section><div class="container" style="text-align:center"><h2 style="margin-bottom:14px">{bi({"en":"Still have questions?","es":"¿Aún tienes preguntas?"})}</h2><a class="btn btn-primary" href="/contact">{bi(UI["talk_admissions"])}</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">{bi(UI["read_faq"])}</a></div></section>'''}

def p_faq():
    items = "".join(f'<details class="card" style="margin-bottom:11px"><summary>{bi(q["q"])}</summary><p style="margin-top:12px;color:var(--mut);line-height:1.7">{bi(q["a"])}</p></details>' for q in CONTENT["faqs"])
    return {"path":"/faq",
        "eyebrow": bi({"en":"FAQ","es":"Preguntas Frecuentes"}),
        "h1": bi({"en":"Frequently asked questions.","es":"Preguntas frecuentes."}),
        "sub": bi({"en":"Tuition, schedule, licensing, GI Bill®, ACCES-VR, job placement.","es":"Matrícula, horario, licencias, GI Bill®, ACCES-VR, colocación laboral."}),
        "body": f'<section><div class="container" style="max-width:820px">{items}</div></section><section><div class="container" style="text-align:center"><p class="lead" style="margin:0 auto 18px">{bi({"en":"Still have questions? We answer the phone.","es":"¿Aún tienes preguntas? Respondemos el teléfono."})}</p><a class="btn btn-primary" href="tel:{tel(B["phone_manhattan"])}">{bi(UI["call_admissions"])} · {B["phone_manhattan"]}</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">{bi(UI["send_message"])}</a></div></section>'}

def p_contact():
    c1, c2 = CONTENT["campuses"]
    return {"path":"/contact",
        "eyebrow": bi({"en":"Contact","es":"Contacto"}),
        "h1": bi({"en":"Visit ABI.","es":"Visita ABI."}),
        "sub": bi({"en":"Two campuses across NYC. Call, walk in, or send a message — admissions responds same-day.","es":"Dos campus en NYC. Llama, ven sin cita, o envía un mensaje — admisiones responde el mismo día."}),
        "body": f'''<section><div class="container"><div class="grid-2">
<div class="card"><div class="eyebrow-acc">{bi({"en":"Manhattan Campus","es":"Campus de Manhattan"})}</div><h3 style="margin:8px 0">{bi(c1["name"])} — 48 W 39th St</h3><p style="color:var(--mut);margin-bottom:8px">{c1["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c1["phone"])}" style="color:var(--accent);font-weight:800;font-size:1.05rem">{c1["phone"]} <span class="lang-en">(English)</span><span class="lang-es">(Inglés)</span></a></p>
<p style="margin-bottom:6px"><a href="tel:{tel(B["phone_manhattan_es"])}" style="color:var(--accent);font-weight:800;font-size:1.05rem">{B["phone_manhattan_es"]} <span class="lang-en">(Spanish)</span><span class="lang-es">(Español)</span></a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{bi(c1["hours"])}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=48+West+39th+Street+New+York+NY" target="_blank" rel="noopener">{bi(UI["get_directions"])}</a></div>
<div class="card"><div class="eyebrow-acc">{bi({"en":"Bronx Campus","es":"Campus del Bronx"})}</div><h3 style="margin:8px 0">{bi(c2["name"])} — 121 Westchester Sq</h3><p style="color:var(--mut);margin-bottom:8px">{c2["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c2["phone"])}" style="color:var(--accent);font-weight:800;font-size:1.05rem">{c2["phone"]}</a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{bi(c2["hours"])}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=121+Westchester+Square+Bronx+NY" target="_blank" rel="noopener">{bi(UI["get_directions"])}</a></div>
</div></div></section>
<section><div class="container"><div class="card" style="max-width:680px;margin:0 auto"><h2 style="margin-bottom:8px">{bi({"en":"Request information","es":"Solicita información"})}</h2><p style="color:var(--mut);margin-bottom:22px">{bi({"en":"Tell us a little about you and an admissions advisor will be in touch within one business day.","es":"Cuéntanos un poco sobre ti y un asesor de admisiones se comunicará contigo en un día hábil."})}</p><form action="mailto:{B["email"]}" method="post" enctype="text/plain" class="form-grid" novalidate>
<div class="row-2"><div class="field-group"><label for="f-first">{bi({"en":"First name","es":"Nombre"})} *</label><input required id="f-first" name="firstName" autocomplete="given-name" placeholder="John / Juan" class="input"></div><div class="field-group"><label for="f-last">{bi({"en":"Last name","es":"Apellido"})} *</label><input required id="f-last" name="lastName" autocomplete="family-name" placeholder="Smith / Garcia" class="input"></div></div>
<div class="row-2"><div class="field-group"><label for="f-email">Email *</label><input required id="f-email" name="email" type="email" autocomplete="email" inputmode="email" placeholder="you@example.com" class="input"></div><div class="field-group"><label for="f-phone">{bi({"en":"Phone","es":"Teléfono"})} *</label><input required id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(212) 555-0123" class="input"></div></div>
<div class="field-group"><label>{bi({"en":"Preferred language","es":"Idioma preferido"})}</label><div class="radio-row"><label class="radio-pill"><input type="radio" name="lang" value="EN" checked><span>English</span></label><label class="radio-pill"><input type="radio" name="lang" value="ES"><span>Español</span></label></div></div>
<div class="field-group"><label>{bi({"en":"Best way to reach you","es":"Cómo prefieres que te contactemos"})}</label><div class="radio-row"><label class="radio-pill"><input type="radio" name="contactBy" value="call" checked><span>{bi({"en":"Call","es":"Llamada"})}</span></label><label class="radio-pill"><input type="radio" name="contactBy" value="text"><span>{bi({"en":"Text","es":"Texto"})}</span></label><label class="radio-pill"><input type="radio" name="contactBy" value="email"><span>Email</span></label></div></div>
<div class="row-2"><div class="field-group"><label for="f-program">{bi({"en":"Program of interest","es":"Programa de interés"})}</label><select id="f-program" name="program" class="input"><option>500-Hour Master Barber (Manhattan)</option><option>540-Hour Master Barber (Bronx)</option><option>50-Hour Refresher</option><option>3-Hour Contagious Diseases</option><option>{bi({"en":"Not sure yet","es":"Aún no estoy seguro"})}</option></select></div><div class="field-group"><label for="f-schedule">{bi({"en":"Preferred schedule","es":"Horario preferido"})}</label><select id="f-schedule" name="schedule" class="input"><option>{bi({"en":"Morning (Mon–Fri 8AM–2PM)","es":"Mañana (Lun–Vie 8AM–2PM)"})}</option><option>{bi({"en":"Afternoon (Mon–Fri 2PM–8PM)","es":"Tarde (Lun–Vie 2PM–8PM)"})}</option><option>{bi({"en":"Weekend (Sat–Sun 9AM–7PM)","es":"Fin de Semana (Sáb–Dom 9AM–7PM)"})}</option><option>{bi({"en":"Flexible","es":"Flexible"})}</option></select></div></div>
<div class="field-group"><label for="f-funding">{bi({"en":"Funding (optional)","es":"Financiamiento (opcional)"})}</label><select id="f-funding" name="funding" class="input"><option>{bi({"en":"Self-pay / weekly plan","es":"Pago propio / plan semanal"})}</option><option>GI Bill® (Post-9/11 / VR&E / Montgomery / DEA)</option><option>ACCES-VR</option><option>{bi({"en":"Not sure yet","es":"Aún no estoy seguro"})}</option></select></div>
<div class="field-group"><label for="f-msg">{bi({"en":"What would you like to know?","es":"¿Qué te gustaría saber?"})}</label><textarea id="f-msg" name="message" placeholder="{bi({"en":"Optional — any questions for admissions","es":"Opcional — preguntas para admisiones"})}" rows="4" class="input" style="resize:vertical"></textarea></div>
<div class="form-cta"><button type="submit" class="btn btn-primary">{bi({"en":"Send to admissions","es":"Enviar a admisiones"})}</button><p class="privacy">{bi({"en":"We respond same-day during business hours. Never spam.","es":"Respondemos el mismo día en horario laboral. Nunca spam."})}</p></div>
</form></div></div></section>'''}

# ============== ASSET BUNDLER ==============
def bundle_assets(site, site_dir):
    a = site_dir / "assets"; (a/"img").mkdir(parents=True, exist_ok=True)
    sl = SRC_ASSETS / "logos" / site["logo"]
    if sl.exists(): shutil.copy2(sl, a / "logo.jpeg")
    sv = SRC_ASSETS / "videos" / site["video"]
    if sv.exists(): shutil.copy2(sv, a / "bg.mp4")
    for f in os.listdir(SRC_ASSETS / "img"):
        if f.lower().endswith(('.jpeg','.jpg','.png')):
            dst = a / "img" / f
            if not dst.exists(): shutil.copy2(SRC_ASSETS / "img" / f, dst)

# ============== INDEX HTML SURGERY ==============
def strip_old_injection(html):
    html = re.sub(r'<!-- ABI v[2-9]+ (SEO )?INJECTED -->\n?', '', html)
    for pat in ['<meta name="description"','<meta name="keywords"','<meta name="author"','<meta name="robots"','<meta name="theme-color"','<link rel="canonical"','<link rel="sitemap"','<link rel="icon"','<link rel="apple-touch-icon"','<link rel="preconnect"','<link rel="dns-prefetch"','<meta name="format-detection"','<meta name="apple-mobile-web-app','<meta name="mobile-web-app']:
        html = re.sub(re.escape(pat) + r'[^>]*>\n?', '', html, count=1)
    html = re.sub(r'<meta property="og:[^"]*"[^>]*>\n?', '', html, count=0)
    html = re.sub(r'<meta name="twitter:[^"]*"[^>]*>\n?', '', html, count=0)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<style>\n?/\* (mobile-first|=====|per-site)[^<]*</style>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r"<script>\s*\(function\(\)\s*\{[^<]*?(burger|abi_lang)[^<]*?\}\)\(\);\s*</script>\n?", '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<a class="sticky-call"[^<]*?</a>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<div class="sticky-call"[^>]*>.*?</div>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<div class="top-banner"[^>]*>.*?</div>\n?(\s*</?nav>)?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<div class="call-row"[^>]*>.*?</div>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<a class="call-btn"[^<]*?</a>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<div class="lang-toggle"[^>]*>.*?</div>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<video class="bg-video"[^<]*<source[^>]*></video>\n?', '', html, count=0)
    return html

def fix_paths(html):
    html = html.replace("https://abi-assets.vercel.app/", "/")
    html = html.replace("../assets/", "/assets/")
    return html

def replace_title(html):
    return re.sub(r'<title>[^<]*</title>', f'<title>{BRAND_TITLE}</title>', html, count=1)

def inject_into_head(html, extras):
    return re.sub(r'</title>', lambda m: m.group(0) + "\n" + extras, html, count=1)

# Inject top-banner + new header BEFORE the existing header. Strip nav from existing header.
def add_v5_chrome(html, tokens):
    # Insert before </head>: add view-transition meta + extra meta tags
    head_extras = head_meta("/") + "\n" + jsonld() + "\n" + css_for_site(tokens)
    html = inject_into_head(html, head_extras)
    # Inject decoration layer + top banner + new header right after <body>
    new_chrome = decoration_layer(tokens) + "\n" + top_banner() + "\n" + header_html("home")
    # Match <body...> and insert
    html = re.sub(r'<body[^>]*>', lambda m: m.group(0).replace('<body', '<body class="lang-en"', 1) if 'class=' not in m.group(0) else m.group(0).replace('class="', 'class="lang-en ', 1), html, count=1)
    html = re.sub(r'(<body[^>]*>)', lambda m: m.group(0) + "\n" + new_chrome, html, count=1)
    # Remove the existing site's <header>...</header> (since we have our own now)
    html = re.sub(r'<header(?![^>]*site-header)[^>]*>.*?</header>', '', html, count=1, flags=re.DOTALL)
    # Inject bg video after our header
    vid = '<video class="bg-video" autoplay muted loop playsinline aria-hidden="true" poster="/assets/logo.jpeg"><source src="/assets/bg.mp4" type="video/mp4"></video>'
    html = re.sub(r'(</header>)', lambda m: m.group(0) + "\n" + vid, html, count=1)
    # Inject sticky call + JS before </body>
    html = html.replace('</body>', f'{footer_html()}\n{sticky_call()}\n{JS}\n</body>', 1)
    html = html.replace('</head>', '<!-- ABI v5 INJECTED -->\n</head>', 1)
    # Update viewport meta to include maximum-scale=5
    html = re.sub(r'<meta name="viewport"[^>]*>', '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=5">', html, count=1)
    return html

def build_site(site):
    slug = site["slug"]
    site_dir = ROOT / slug
    if not site_dir.exists(): return
    tokens = load_tokens(slug)

    # Bundle assets
    bundle_assets(site, site_dir)

    # Enhance index.html
    idx = site_dir / "index.html"
    html = idx.read_text(encoding="utf-8", errors="replace")
    html = strip_old_injection(html)
    html = replace_title(html)
    html = fix_paths(html)
    html = add_v5_chrome(html, tokens)
    idx.write_text(html, encoding="utf-8")

    # Sub-pages (no haircuts)
    pages_def = [
        ("about.html", "about", p_about),
        ("programs.html", "programs", p_programs),
        ("instructors.html", "instructors", p_instructors),
        ("gallery.html", "gallery", lambda: p_gallery(site_dir)),
        ("partners.html", "partners", p_partners),
        ("job-placement.html", "jobplacement", p_jobplacement),
        ("resources.html", "resources", p_resources),
        ("faq.html", "faq", p_faq),
        ("contact.html", "contact", p_contact),
    ]
    for fname, key, fn in pages_def:
        pdata = fn()
        (site_dir / fname).write_text(render_subpage(tokens, key, pdata), encoding="utf-8")

    # Remove haircuts if present
    hc = site_dir / "haircuts.html"
    if hc.exists(): hc.unlink()

    # Sitemap (no haircuts)
    base = f"https://{site['vercel_name']}.vercel.app"
    paths = ["/", "/about", "/programs", "/instructors", "/gallery", "/partners", "/job-placement", "/resources", "/faq", "/contact"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in paths:
        sm += f'  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq><priority>{"1.0" if p=="/" else "0.7"}</priority></url>\n'
    sm += '</urlset>\n'
    (site_dir / "sitemap.xml").write_text(sm)
    (site_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    (site_dir / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": False, "headers": [
        {"source": "/assets/(.*)", "headers": [{"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},
        {"source": "/(.*).html", "headers": [{"key":"Cache-Control","value":"public, max-age=300, must-revalidate"}]},
    ]}, indent=2))
    print(f"  OK {slug}: v5 — design-inherited sub-pages, mobile-first, centered calls")

if __name__ == "__main__":
    print("Building v5 — per-site design inheritance + mobile-first + centered calls + partner imgs + transitions")
    for s in SITES:
        build_site(s)
    print("Done.")
