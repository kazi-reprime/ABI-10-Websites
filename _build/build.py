"""ABI 10-Websites builder v4 — bilingual EN/ES, per-site bundled assets, dual call buttons, no shared CDN."""
from __future__ import annotations
import json, os, re, shutil, sys, random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ASSETS = ROOT / "assets"
CONTENT = json.loads((ROOT / "_content" / "content.json").read_text())
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]

B = CONTENT["brand"]
UI = CONTENT["ui"]
NAV = CONTENT["nav"]

def tel(p): return p.replace("(","").replace(")","").replace(" ","").replace("-","")
def L(d, lang): return d[lang] if isinstance(d, dict) and lang in d else (d if isinstance(d, str) else "")
def bi(d):
    """Emit dual-language <span> from a {en, es} dict."""
    if isinstance(d, str): return d
    en = d.get("en","") if isinstance(d, dict) else ""
    es = d.get("es","") if isinstance(d, dict) else ""
    return f'<span class="lang-en">{en}</span><span class="lang-es">{es}</span>'

# Neutral title (no theme name)
BRAND_TITLE = "American Barber Institute · New York's Dedicated Barber School"
BRAND_DESC_EN = "American Barber Institute (ABI) — New York's only dedicated barber school. NY State licensed. 30+ years, 10,000+ graduates. GI Bill® accepted. Manhattan & Bronx campuses."
BRAND_DESC_ES = "American Barber Institute (ABI) — la única escuela de barbería dedicada de Nueva York. Licenciada por el Estado de NY. 30+ años, 10,000+ graduados. GI Bill® aceptado. Campus en Manhattan y el Bronx."

PAGE_META = {
    "/":           {"key":"home"},
    "/about":      {"key":"about"},
    "/programs":   {"key":"programs"},
    "/instructors":{"key":"instructors"},
    "/gallery":    {"key":"gallery"},
    "/partners":   {"key":"partners"},
    "/haircuts":   {"key":"haircuts"},
    "/job-placement":{"key":"jobplacement"},
    "/resources":  {"key":"resources"},
    "/faq":        {"key":"faq"},
    "/contact":    {"key":"contact"},
}
PAGE_TITLES = {
    "/":            "American Barber Institute · New York's Dedicated Barber School",
    "/about":       "About · American Barber Institute · NYC",
    "/programs":    "Programs & Tuition · American Barber Institute",
    "/instructors": "Instructors · American Barber Institute",
    "/gallery":     "Gallery · American Barber Institute",
    "/partners":    "Partner Shops · American Barber Institute",
    "/haircuts":    "Public Student Clinic Haircuts · ABI · $3",
    "/job-placement": "Job Placement · American Barber Institute",
    "/resources":   "Resources · Veterans · ACCES-VR · ABI",
    "/faq":         "Frequently Asked Questions · American Barber Institute",
    "/contact":     "Contact · American Barber Institute · NYC",
}

# Per-site assets are LOCAL (no CDN). Paths are relative: assets/logo.jpeg, assets/bg.mp4, assets/img/...
LOGO_PATH = "assets/logo.jpeg"
VIDEO_PATH = "assets/bg.mp4"

def head_meta(page_path="/", site=None):
    title = PAGE_TITLES.get(page_path, BRAND_TITLE)
    return f'''<meta name="description" content="{BRAND_DESC_EN}">
<meta name="keywords" content="barber school nyc, american barber institute, abi, barber school new york, master barber program, master barber license ny, barber academy nyc, gi bill barber school, escuela de barberia nueva york, escuela barberia manhattan">
<meta name="author" content="American Barber Institute">
<meta name="robots" content="index, follow">
<link rel="canonical" href="/">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="icon" type="image/jpeg" href="/{LOGO_PATH}">
<link rel="apple-touch-icon" href="/{LOGO_PATH}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{BRAND_DESC_EN}">
<meta property="og:image" content="/{LOGO_PATH}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{BRAND_DESC_EN}">
<meta name="twitter:image" content="/{LOGO_PATH}">
<meta name="format-detection" content="telephone=yes">'''

def jsonld(include_faq=True):
    school = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "American Barber Institute",
        "alternateName": "ABI",
        "url": "/",
        "description": BRAND_DESC_EN,
        "telephone": B["phone_manhattan"],
        "email": B["email"],
        "foundingDate": "1995",
        "address": [
            {"@type":"PostalAddress","streetAddress":"48 West 39th Street","addressLocality":"New York","addressRegion":"NY","postalCode":"10018","addressCountry":"US"},
            {"@type":"PostalAddress","streetAddress":"121 Westchester Square","addressLocality":"Bronx","addressRegion":"NY","postalCode":"10461","addressCountry":"US"},
        ],
        "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.3","ratingCount":"100"},
    }
    out = f'<script type="application/ld+json">{json.dumps(school)}</script>'
    if include_faq:
        faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q["q"]["en"],"acceptedAnswer":{"@type":"Answer","text":q["a"]["en"]}} for q in CONTENT["faqs"]]}
        out += f'\n<script type="application/ld+json">{json.dumps(faq)}</script>'
    return out

# Universal CSS + JS for language switcher + dual call buttons + responsive
def universal_overlay(site):
    return f'''<style>
/* mobile-first responsive + bilingual switcher + dual call buttons */
:root {{ --abi-touch: 44px; --abi-accent: {site["primary_color"]}; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ overflow-x: hidden; }}
img {{ max-width: 100%; height: auto; display: block; }}
video {{ max-width: 100%; height: auto; }}
button, .btn, a.btn, .nav-cta, a.nav-cta {{ min-height: var(--abi-touch); display: inline-flex; align-items: center; justify-content: center; }}
/* Bilingual: hide opposite language. Default = lang-en. */
body.lang-en .lang-es, body.lang-es .lang-en {{ display: none !important; }}
.lang-en, .lang-es {{ /* keep default display */ }}

/* Language toggle button — top right */
.lang-toggle {{ display: inline-flex; align-items: center; height: 36px; border-radius: 30px; border: 1px solid var(--abi-accent); overflow: hidden; font-size: .78rem; font-weight: 800; letter-spacing: .12em; }}
.lang-toggle button {{ background: transparent; border: 0; color: var(--abi-accent); padding: 0 12px; height: 34px; cursor: pointer; font-weight: 800; letter-spacing: .12em; font-family: inherit; }}
.lang-toggle button.active {{ background: var(--abi-accent); color: #04060c; }}
.lang-toggle button:focus-visible {{ outline: 2px solid #fff; outline-offset: 2px; }}

/* Dual call buttons in header */
.call-row {{ display: flex; gap: 8px; align-items: center; flex-wrap: nowrap; }}
.call-btn {{ display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 30px; border: 1px solid var(--abi-accent); color: var(--abi-accent); font-weight: 700; font-size: .78rem; text-decoration: none; min-height: 38px; transition: .2s; white-space: nowrap; }}
.call-btn:hover {{ background: var(--abi-accent); color: #04060c; }}
.call-btn .flag {{ font-size: .7rem; opacity: .85; padding: 2px 6px; border: 1px solid currentColor; border-radius: 10px; }}
.call-btn .num {{ font-family: ui-monospace, monospace; font-size: .82rem; }}

.burger {{ width: var(--abi-touch); height: var(--abi-touch); display: none; flex-direction: column; gap: 5px; cursor: pointer; align-items: center; justify-content: center; background: transparent; border: 0; padding: 0; }}
.burger span {{ width: 26px; height: 2px; background: currentColor; transition: .2s; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

@media (max-width: 1100px) {{
  .call-btn .num {{ display: none; }}
  .call-btn .flag {{ font-size: .68rem; }}
}}
@media (max-width: 980px) {{
  .nav-links {{ position: fixed !important; inset: 70px 0 auto 0 !important; flex-direction: column !important; align-items: stretch !important; gap: 0 !important; background: rgba(8,8,14,.97) !important; backdrop-filter: blur(20px); padding: 12px 18px 22px !important; transform: translateY(-110%); transition: transform .28s ease; box-shadow: 0 18px 36px rgba(0,0,0,.45); z-index: 24; display: flex !important; max-height: calc(100vh - 70px); overflow-y: auto; }}
  .nav-links a {{ padding: 14px 6px !important; border-bottom: 1px solid rgba(255,255,255,.07); font-size: 1rem !important; min-height: var(--abi-touch); display: flex !important; align-items: center; }}
  .nav-links a:last-child {{ border-bottom: 0; }}
  .nav-links.open {{ transform: translateY(0); }}
  .burger {{ display: inline-flex; color: var(--abi-accent); }}
  .call-row {{ gap: 4px; }}
  .call-btn {{ padding: 6px 10px; min-height: 36px; font-size: .72rem; }}
  .call-btn .num {{ display: none; }}
  h1 {{ font-size: clamp(2.1rem, 9vw, 3.4rem) !important; }}
  h2 {{ font-size: clamp(1.55rem, 6.4vw, 2.2rem) !important; }}
  .wrap, .container {{ padding-left: 18px !important; padding-right: 18px !important; }}
  section {{ padding-top: 48px !important; padding-bottom: 48px !important; }}
  .hero {{ min-height: 86vh !important; padding-top: 80px !important; padding-bottom: 40px !important; }}
  .btn-row, .actions, .hero-actions {{ flex-direction: column !important; align-items: stretch !important; gap: 12px !important; }}
  .btn-row > *, .actions > *, .hero-actions > * {{ width: 100%; text-align: center; }}
  .grid, [class*="grid"] {{ grid-template-columns: 1fr !important; }}
  .ticker {{ font-size: .65rem !important; }}
  body {{ padding-bottom: 72px; }}
  .sticky-call {{ display: flex !important; }}
}}
@media (max-width: 480px) {{
  .wrap, .container {{ padding-left: 14px !important; padding-right: 14px !important; }}
  .call-btn span:not(.flag) {{ display: none; }}
  .call-btn .flag {{ margin: 0; }}
}}
@media (min-width: 981px) {{ .burger {{ display: none !important; }} }}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation-duration: .001s !important; transition-duration: .001s !important; }} }}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .14; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .08; }} }}
.hero-logo-mark {{ max-width: 84px; max-height: 84px; border-radius: 20px; }}

/* Sticky call bar at bottom on mobile */
.sticky-call {{ display: none; position: fixed; left: 14px; right: 14px; bottom: 14px; z-index: 50; gap: 8px; align-items: stretch; }}
.sticky-call a {{ flex: 1; padding: 14px 12px; border-radius: 999px; font-weight: 800; font-size: .9rem; text-align: center; text-decoration: none; box-shadow: 0 16px 40px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06); display: inline-flex; align-items: center; justify-content: center; gap: 6px; }}
.sticky-call a.en {{ background: var(--abi-accent); color: #06070c; }}
.sticky-call a.es {{ background: #1a1d24; color: #fff; border: 1px solid var(--abi-accent); }}
</style>'''

def hamburger_js_and_lang_js():
    return f'''<script>
(function() {{
  // ── Language switcher ─────────────────────────────────
  var saved = localStorage.getItem('abi_lang') || 'en';
  document.body.classList.remove('lang-en','lang-es');
  document.body.classList.add('lang-' + saved);
  document.documentElement.lang = saved;
  // wire up toggle buttons (any with .lang-toggle button)
  function setLang(lang) {{
    document.body.classList.remove('lang-en','lang-es');
    document.body.classList.add('lang-' + lang);
    document.documentElement.lang = lang;
    localStorage.setItem('abi_lang', lang);
    document.querySelectorAll('.lang-toggle button').forEach(function(b) {{
      b.classList.toggle('active', b.getAttribute('data-lang') === lang);
    }});
  }}
  document.querySelectorAll('.lang-toggle button').forEach(function(b) {{
    b.addEventListener('click', function() {{ setLang(this.getAttribute('data-lang')); }});
    if (b.getAttribute('data-lang') === saved) b.classList.add('active');
  }});

  // ── Hamburger ─────────────────────────────────
  var nav = document.querySelector('.nav-links');
  if (!nav) return;
  var burger = document.querySelector('.burger');
  if (!burger) {{
    burger = document.createElement('button');
    burger.className = 'burger';
    burger.setAttribute('aria-label','Toggle navigation');
    burger.setAttribute('aria-expanded','false');
    burger.innerHTML = '<span></span><span></span><span></span>';
    var nw = document.querySelector('header .nav') || document.querySelector('header > div') || document.querySelector('header');
    if (nw) nw.appendChild(burger);
  }}
  function cl(){{ nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }}
  burger.addEventListener('click', function(){{ var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o ? 'true':'false'); }});
  nav.querySelectorAll('a').forEach(function(a){{ a.addEventListener('click', cl); }});
  document.addEventListener('keydown', function(e){{ if (e.key==='Escape') cl(); }});
}})();
</script>'''

# Top header (used on sub-pages and to optionally replace original index nav for cross-link safety)
def header_html(active_key=""):
    nav_items = [("home","/"), ("about","/about"), ("programs","/programs"), ("instructors","/instructors"),
                 ("gallery","/gallery"), ("partners","/partners"), ("haircuts","/haircuts"),
                 ("jobplacement","/job-placement"), ("resources","/resources"), ("faq","/faq"), ("contact","/contact")]
    links = "".join(
        f'<a href="{p}" class="{"active" if k==active_key else ""}">{bi(NAV[k])}</a>'
        for k,p in nav_items
    )
    return f'''<header>
  <div class="nav">
    <a class="logo" href="/"><img src="/{LOGO_PATH}" alt="American Barber Institute"><span>American Barber Institute</span></a>
    <nav class="nav-links">{links}</nav>
    <div class="call-row">
      <a class="call-btn" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call English"><span class="flag">EN</span><span class="lang-en">Call</span><span class="lang-es">Llama</span><span class="num">{B["phone_manhattan"]}</span></a>
      <a class="call-btn" href="tel:{tel(B["phone_manhattan_es"])}" aria-label="Llamar Español"><span class="flag">ES</span><span class="lang-en">Call ES</span><span class="lang-es">Llama</span><span class="num">{B["phone_manhattan_es"]}</span></a>
      <div class="lang-toggle" role="group" aria-label="Language">
        <button type="button" data-lang="en" aria-label="English">EN</button>
        <button type="button" data-lang="es" aria-label="Español">ES</button>
      </div>
    </div>
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''

def sticky_call():
    return f'''<div class="sticky-call">
  <a class="en" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call English"><span class="flag">EN</span> {B["phone_manhattan"]}</a>
  <a class="es" href="tel:{tel(B["phone_manhattan_es"])}" aria-label="Llamar Español"><span class="flag">ES</span> {B["phone_manhattan_es"]}</a>
</div>'''

def footer_html():
    return f'''<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>American Barber Institute</h4>
        <p style="margin-bottom:10px"><span class="lang-en">New York's only dedicated barber school. 30+ years. 10,000+ graduates.</span><span class="lang-es">La única escuela de barbería dedicada en NY. 30+ años. 10,000+ graduados.</span></p>
        <p style="font-size:.85rem"><span class="lang-en">Licensed by NY State Department of Education (BPSS). GI Bill® accepted. ACCES-VR accepted.</span><span class="lang-es">Licenciada por el Departamento de Educación del Estado de NY (BPSS). GI Bill® aceptado. ACCES-VR aceptado.</span></p>
      </div>
      <div>
        <h4><span class="lang-en">School</span><span class="lang-es">Escuela</span></h4>
        <a href="/about">{bi(NAV["about"])}</a>
        <a href="/programs">{bi(NAV["programs"])}</a>
        <a href="/instructors">{bi(NAV["instructors"])}</a>
        <a href="/gallery">{bi(NAV["gallery"])}</a>
      </div>
      <div>
        <h4><span class="lang-en">Resources</span><span class="lang-es">Recursos</span></h4>
        <a href="/partners">{bi(NAV["partners"])}</a>
        <a href="/job-placement">{bi(NAV["jobplacement"])}</a>
        <a href="/haircuts">{bi(NAV["haircuts"])}</a>
        <a href="/resources">{bi(NAV["resources"])}</a>
        <a href="/faq">{bi(NAV["faq"])}</a>
      </div>
      <div>
        <h4><span class="lang-en">Contact</span><span class="lang-es">Contacto</span></h4>
        <a href="tel:{tel(B["phone_manhattan"])}">Manhattan EN · {B["phone_manhattan"]}</a>
        <a href="tel:{tel(B["phone_manhattan_es"])}">Manhattan ES · {B["phone_manhattan_es"]}</a>
        <a href="tel:{tel(B["phone_bronx"])}">Bronx · {B["phone_bronx"]}</a>
        <a href="mailto:{B["email"]}">{B["email"]}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 American Barber Institute. <span class="lang-en">All rights reserved.</span><span class="lang-es">Todos los derechos reservados.</span></span>
      <span><span class="lang-en">Licensed by NY State Dept. of Education · GI Bill® accepted</span><span class="lang-es">Licenciada por el Depto. de Educación de NY · GI Bill® aceptado</span></span>
    </div>
  </div>
</footer>'''

# ============== SUB-PAGE TEMPLATE ==============
SUBPAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{head_meta}
{jsonld}
<style>
:root {{ --accent: {accent}; --bg: #07080d; --bg2: #0d1018; --ink: #e9ecff; --mut: #8b91b8; --line: rgba(255,255,255,.08); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
body {{ background: var(--bg); color: var(--ink); font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; line-height: 1.65; overflow-x: hidden; min-height: 100vh; }}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; height: auto; display: block; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 2; }}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .12; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .07; }} }}
.bg-overlay {{ position: fixed; inset: 0; background: radial-gradient(ellipse at center, transparent 0, rgba(0,0,0,.5) 70%, var(--bg) 100%); z-index: 1; pointer-events: none; }}
header {{ position: sticky; top: 0; z-index: 30; background: rgba(7,8,13,.88); backdrop-filter: blur(18px); border-bottom: 1px solid var(--line); }}
.nav {{ display: flex; align-items: center; justify-content: space-between; height: 70px; max-width: 1180px; margin: 0 auto; padding: 0 24px; gap: 14px; }}
.logo {{ display: flex; align-items: center; gap: 12px; font-weight: 900; letter-spacing: .04em; font-size: 1rem; }}
.logo img {{ width: 38px; height: 38px; border-radius: 10px; object-fit: cover; }}
.nav-links {{ display: flex; gap: 16px; font-size: .85rem; font-weight: 600; color: var(--mut); }}
.nav-links a {{ transition: .2s; padding: 6px 2px; white-space: nowrap; }}
.nav-links a:hover, .nav-links a.active {{ color: var(--accent); }}
.subpage-hero {{ padding: 90px 0 50px; text-align: center; position: relative; }}
.eyebrow {{ display: inline-block; padding: 6px 14px; border: 1px solid var(--line); border-radius: 30px; font-size: .68rem; letter-spacing: .3em; text-transform: uppercase; color: var(--accent); }}
.subpage-hero h1 {{ font-family: 'Arial Black', system-ui; font-size: clamp(2.1rem, 6.4vw, 3.8rem); margin: 22px 0 14px; line-height: 1.05; letter-spacing: -.02em; }}
.subpage-hero p.sub {{ max-width: 720px; margin: 0 auto; color: var(--mut); font-size: 1.06rem; }}
section {{ padding: 50px 0; position: relative; z-index: 2; }}
section h2 {{ font-family: 'Arial Black', system-ui; font-size: clamp(1.6rem, 4vw, 2.4rem); line-height: 1.1; margin-bottom: 12px; letter-spacing: -.02em; }}
section p.lead {{ color: var(--mut); max-width: 760px; margin-bottom: 24px; font-size: 1.02rem; }}
.card {{ background: rgba(20,20,30,.55); border: 1px solid var(--line); border-radius: 18px; padding: 26px; backdrop-filter: blur(8px); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
.grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 22px; }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 28px; border-radius: 40px; font-weight: 700; font-size: .94rem; min-height: 48px; transition: .2s; cursor: pointer; border: 0; }}
.btn-primary {{ background: var(--accent); color: var(--bg); }}
.btn-primary:hover {{ filter: brightness(1.08); transform: translateY(-2px); box-shadow: 0 12px 30px rgba(0,0,0,.4); }}
.btn-ghost {{ border: 1px solid var(--line); color: var(--ink); background: transparent; }}
.btn-ghost:hover {{ border-color: var(--accent); color: var(--accent); }}
.input {{ background: rgba(20,20,30,.6); border: 1px solid var(--line); border-radius: 12px; padding: 14px; color: var(--ink); font-size: 1rem; font-family: inherit; }}
.input:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent); }}
.eyebrow-acc {{ color: var(--accent); font-size: .7rem; letter-spacing: .28em; text-transform: uppercase; font-weight: 800; }}
.row-stat {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 22px 0; }}
.row-stat .s {{ padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: rgba(255,255,255,.025); }}
.row-stat .s b {{ display: block; font-size: 1.7rem; color: var(--accent); font-weight: 800; line-height: 1.1; }}
.row-stat .s small {{ color: var(--mut); font-size: .8rem; }}
.list-clean {{ list-style: none; padding: 0; }}
.list-clean li {{ padding: 10px 0; border-bottom: 1px solid var(--line); color: var(--mut); }}
.list-clean li:last-child {{ border-bottom: 0; }}
.list-clean li::before {{ content: "▸"; color: var(--accent); margin-right: 10px; font-weight: 800; }}
.contact-strip {{ display: flex; gap: 14px; flex-wrap: wrap; padding: 18px; border: 1px solid var(--accent); border-radius: 16px; background: rgba(255,255,255,.03); margin: 20px 0; }}
.contact-strip a {{ color: var(--accent); font-weight: 700; }}
footer {{ padding: 60px 0 100px; border-top: 1px solid var(--line); margin-top: 60px; color: var(--mut); font-size: .9rem; position: relative; z-index: 2; background: rgba(0,0,0,.4); }}
.footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 32px; margin-bottom: 30px; }}
.footer-grid h4 {{ font-size: .85rem; text-transform: uppercase; letter-spacing: .15em; color: var(--ink); margin-bottom: 12px; }}
.footer-grid a {{ display: block; padding: 4px 0; color: var(--mut); }}
.footer-grid a:hover {{ color: var(--accent); }}
.footer-bottom {{ display: flex; justify-content: space-between; padding-top: 24px; border-top: 1px solid var(--line); flex-wrap: wrap; gap: 12px; font-size: .8rem; }}
@media (max-width: 980px) {{ .nav-cta {{ display: none; }} .footer-grid {{ grid-template-columns: 1fr 1fr; }} .subpage-hero {{ padding: 70px 0 40px; }} body {{ padding-bottom: 72px; }} }}
@media (max-width: 480px) {{ .footer-grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body class="lang-en">
<video class="bg-video" autoplay muted loop playsinline poster="/{LOGO_PATH}" aria-hidden="true"><source src="/{VIDEO_PATH}" type="video/mp4"></video>
<div class="bg-overlay"></div>
{header}
<section class="subpage-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</section>
{body}
{footer}
{sticky_call}
{universal_overlay}
{js}
</body>
</html>
'''

def render_subpage(site, page_key, pdata, page_path):
    return SUBPAGE.format(
        LOGO_PATH=LOGO_PATH, VIDEO_PATH=VIDEO_PATH,
        title=PAGE_TITLES[page_path], accent=site["primary_color"],
        head_meta=head_meta(page_path, site), jsonld=jsonld(include_faq=(page_key == "faq")),
        eyebrow=pdata["eyebrow"], h1=pdata["h1"], sub=pdata["sub"], body=pdata["body"],
        header=header_html(page_key), footer=footer_html(), sticky_call=sticky_call(),
        universal_overlay=universal_overlay(site), js=hamburger_js_and_lang_js(),
    )

# ============== PAGE CONTENTS ==============

def p_about():
    instr_cards = "".join(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{bi(i["role"])}</div><h3 style="font-size:1.25rem;margin-bottom:8px">{i["name"]}</h3><p style="color:var(--mut);font-size:.95rem;margin-bottom:10px">{bi(i["bio"])}</p><p style="font-size:.8rem;color:var(--accent)">{" · ".join(bi(t) for t in i["tags"])}</p></div>' for i in CONTENT["instructors"][:3])
    why = "".join(f"<li>{bi(w)}</li>" for w in CONTENT["why_choose"])
    return {"eyebrow": bi({"en":"About ABI","es":"Acerca de ABI"}),
        "h1": bi({"en":"30+ years. 10,000+ graduates. One craft.","es":"30+ años. 10,000+ graduados. Un oficio."}),
        "sub": bi({"en":"American Barber Institute is New York's only dedicated barber school — changing lives in Manhattan and the Bronx for over three decades.","es":"American Barber Institute es la única escuela de barbería dedicada de Nueva York — cambiando vidas en Manhattan y el Bronx por más de tres décadas."}),
        "body": f'''<section><div class="wrap"><div class="grid-2"><div><h2>{bi({"en":"Our story","es":"Nuestra historia"})}</h2><p class="lead">{bi({"en":"ABI was built on a simple idea: barbering deserves a school that does <i>only</i> barbering. No nails. No esthetics. No detours. Just the craft, taught by master barbers, on a working clinic floor, the way the trade has always been passed down.","es":"ABI fue construida con una idea simple: la barbería merece una escuela que se dedique <i>solo</i> a la barbería. Sin uñas. Sin estética. Sin desvíos. Solo el oficio, enseñado por maestros barberos, en un piso de clínica en funcionamiento, como siempre se ha transmitido el oficio."})}</p><p class="lead">{bi({"en":"Three decades and ten thousand graduates later, that idea has produced the people behind some of New York's most respected shops.","es":"Tres décadas y diez mil graduados después, esa idea ha producido a las personas detrás de algunas de las barberías más respetadas de Nueva York."})}</p></div><div class="card"><h3 style="margin-bottom:10px">{bi({"en":"The facility","es":"Las instalaciones"})}</h3><p style="color:var(--mut)">{bi(B["facility"])} — {bi({"en":"designed around the working clinic floor, with classroom space, demonstration chairs, and a second campus at 121 Westchester Square in the Bronx.","es":"diseñada en torno al piso de la clínica, con aulas, sillas de demostración, y un segundo campus en 121 Westchester Square en el Bronx."})}</p><div class="row-stat"><div class="s"><b>{B["years_in_business"]}</b><small>{bi({"en":"Years training barbers","es":"Años entrenando barberos"})}</small></div><div class="s"><b>{B["graduates"]}</b><small>{bi({"en":"Graduates","es":"Graduados"})}</small></div><div class="s"><b>{B["rating"]}</b><small>{bi({"en":"Google rating","es":"Calificación Google"})}</small></div></div></div></div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Leadership","es":"Liderazgo"})}</div><h2 style="margin-bottom:24px">{bi({"en":"The faculty","es":"La facultad"})}</h2><div class="grid">{instr_cards}</div><p style="margin-top:20px"><a class="btn btn-ghost" href="/instructors">{bi({"en":"Meet all instructors →","es":"Conoce a todos los instructores →"})}</a></p></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Why ABI","es":"Por qué ABI"})}</div><h2 style="margin-bottom:18px">{bi({"en":"What makes us different","es":"Lo que nos hace diferentes"})}</h2><ul class="list-clean" style="max-width:820px">{why}</ul></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_programs():
    rows = []
    for p in CONTENT["programs"]:
        flag = f'<span style="position:absolute;top:14px;right:14px;font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;background:var(--accent);color:var(--bg);padding:5px 10px;border-radius:20px;font-weight:800">{bi({"en":"Flagship","es":"Insignia"})}</span>' if p.get("flagship") else ""
        det = f'<p style="color:var(--mut);font-size:.88rem;margin-top:10px">{bi(p["details"])}</p>' if p.get("details") else ""
        price = bi(p["price"]) if isinstance(p["price"], dict) else p["price"]
        rows.append(f'<div class="card" style="position:relative">{flag}<div class="eyebrow-acc">{bi(p["campus"])} · {bi(p["duration"])}</div><h3 style="font-size:1.3rem;margin:8px 0">{bi(p["name"])}</h3><div style="font-size:1.4rem;font-weight:800;color:var(--accent);margin-bottom:10px">{price}</div><p style="color:var(--mut);font-size:.96rem">{bi(p["summary"])}</p>{det}</div>')
    sched = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(s["label"])}</div><h3 style="font-size:1.1rem;margin:8px 0">{bi(s["days"])} · {s["time"]}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:10px 0 6px">{s["tuition"]}</div><p style="color:var(--mut);font-size:.9rem">{bi(s["plan"])}</p></div>' for s in CONTENT["schedules"])
    steps = "".join(f'<div class="card"><div style="font-size:2rem;color:var(--accent);font-weight:800;line-height:1">0{s["step"]}</div><h3 style="margin:8px 0;font-size:1.2rem">{bi(s["title"])}</h3><p style="color:var(--mut);font-size:.94rem">{bi(s["desc"])}</p></div>' for s in CONTENT["enrollment_steps"])
    req = "".join(f"<li>{bi(r)}</li>" for r in CONTENT["requirements"])
    earnings = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(e["window"])}</div><h3 style="font-size:1.2rem;margin:8px 0">{bi(e["stage"])}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:6px 0 8px">{e["range"]}</div><p style="color:var(--mut);font-size:.92rem">{bi(e["desc"])}</p></div>' for e in CONTENT["career_earnings"])
    return {"eyebrow": bi({"en":"Programs & Tuition","es":"Programas y Matrícula"}),
        "h1": bi({"en":"Programs, tuition, and what you'll learn","es":"Programas, matrícula, y qué aprenderás"}),
        "sub": bi({"en":"Five programs across two campuses. Three flexible tracks. NY State Master Barber License at the end.","es":"Cinco programas en dos campus. Tres opciones flexibles. Licencia de Maestro Barbero del Estado de NY al final."}),
        "body": f'''<section><div class="wrap"><h2>{bi({"en":"Choose your program","es":"Elige tu programa"})}</h2><p class="lead">{bi({"en":"Every program is state-licensed and exam-prep ready. Tuition is flexible — every plan includes a down payment and a weekly schedule.","es":"Cada programa está licenciado por el estado y listo para preparación de examen. La matrícula es flexible — cada plan incluye un enganche y un horario semanal."})}</p><div class="grid">{"".join(rows)}</div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Schedule & Tuition","es":"Horario y Matrícula"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three flexible schedules","es":"Tres horarios flexibles"})}</h2><div class="grid">{sched}</div><p style="margin-top:18px;color:var(--mut);font-size:.92rem">{bi({"en":"Veterans &amp; GI Bill® benefits accepted. ACCES-VR accepted.","es":"Beneficios de Veteranos y GI Bill® aceptados. ACCES-VR aceptado."})} <a href="/resources" style="color:var(--accent);text-decoration:underline">{bi({"en":"See full benefits guide →","es":"Ver guía completa →"})}</a></p></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Enrollment","es":"Inscripción"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three steps to your first chair","es":"Tres pasos a tu primer sillón"})}</h2><div class="grid">{steps}</div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Requirements","es":"Requisitos"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Documents to enroll","es":"Documentos para inscribirte"})}</h2><ul class="list-clean" style="max-width:680px">{req}</ul></div></section>
<section><div class="wrap"><div class="eyebrow-acc">{bi({"en":"Career earnings","es":"Ingresos de carrera"})}</div><h2 style="margin-bottom:14px">{bi({"en":"What barbers earn","es":"Lo que ganan los barberos"})}</h2><div class="grid">{earnings}</div><p style="margin-top:18px;color:var(--mut);font-size:.85rem">{bi(CONTENT["earnings_note"])}</p></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">{bi(UI["read_faq"])}</a></div></section>'''}

def p_instructors():
    cards = "".join(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{bi(i["role"])}</div><h3 style="font-size:1.35rem;margin-bottom:10px">{i["name"]}</h3><p style="color:var(--mut);font-size:1rem;line-height:1.7;margin-bottom:14px">{bi(i["bio"])}</p><p style="font-size:.82rem;color:var(--accent);letter-spacing:.06em">{" · ".join(bi(t) for t in i["tags"])}</p></div>' for i in CONTENT["instructors"])
    return {"eyebrow": bi({"en":"Faculty","es":"Profesorado"}),
        "h1": bi({"en":"Master barbers. Master teachers.","es":"Maestros barberos. Maestros instructores."}),
        "sub": bi({"en":"Decades of working-floor experience and a clinic-first style of teaching. You learn by chair time, with an instructor inches away when you need them.","es":"Décadas de experiencia en el piso y un estilo de enseñanza centrado en la clínica. Aprendes con tiempo en la silla, con un instructor a pulgadas de ti cuando lo necesitas."}),
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:14px">{bi({"en":"Train with us","es":"Entrena con nosotros"})}</h2><p class="lead" style="margin:0 auto 20px">{bi({"en":"New cohorts begin the first Monday of every month at both campuses.","es":"Las nuevas generaciones comienzan el primer lunes de cada mes en ambos campus."})}</p><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_gallery():
    # Each site can have a slightly different subset (deterministic by site index)
    return {"eyebrow": bi({"en":"On the floor","es":"En el piso"}),
        "h1": bi({"en":"Student work. Clinic life. Graduation day.","es":"Trabajo de estudiantes. Vida en la clínica. Día de graduación."}),
        "sub": bi({"en":"A glimpse inside the American Barber Institute. Real students. Real chairs. Real fades.","es":"Un vistazo al interior de American Barber Institute. Estudiantes reales. Sillas reales. Degradados reales."}),
        "body": "<!--GALLERY_PLACEHOLDER-->"}

def p_partners():
    cards = "".join(f'<div class="card"><div class="eyebrow-acc">{p["locations"]}</div><h3 style="font-size:1.35rem;margin:10px 0 8px">{p["name"]}</h3><p style="color:var(--mut);font-size:.96rem;margin-bottom:14px">{bi(p["desc"])}</p><p style="font-size:.88rem;color:var(--accent);font-weight:700">→ {bi(p["why"])}</p></div>' for p in CONTENT["partners"])
    return {"eyebrow": bi({"en":"Partner Shops","es":"Barberías Aliadas"}),
        "h1": bi({"en":"Where ABI graduates work.","es":"Dónde trabajan los graduados de ABI."}),
        "sub": bi({"en":"Real shops. Real owners. Many of them started right here on the ABI clinic floor.","es":"Barberías reales. Dueños reales. Muchos comenzaron aquí mismo en el piso clínico de ABI."}),
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:10px">{bi({"en":"Your path to one of these chairs","es":"Tu camino a una de estas sillas"})}</h2><p class="lead" style="margin:0 auto 20px">{bi({"en":"Our Job Placement Office connects every graduate with our partner network and beyond.","es":"Nuestra Oficina de Colocación Laboral conecta a cada graduado con nuestra red de aliados y más allá."})}</p><a class="btn btn-primary" href="/job-placement">{bi({"en":"See job placement","es":"Ver colocación laboral"})}</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">{bi(UI["talk_admissions"])}</a></div></section>'''}

def p_haircuts():
    h = CONTENT["haircut_clinic"]
    services = "".join(f'<span style="display:inline-block;margin:4px 6px 4px 0;padding:7px 14px;border:1px solid var(--line);border-radius:30px;font-size:.85rem;color:var(--mut)">{bi(s)}</span>' for s in h["services"])
    return {"eyebrow": bi({"en":"Public Clinic","es":"Clínica Pública"}),
        "h1": bi({"en":f"{h['price']} student haircuts.","es":f"Cortes de estudiante por {h['price']}."}),
        "sub": bi({"en":"Every cut supervised by a NY-licensed master barber.","es":"Cada corte supervisado por un maestro barbero licenciado por NY."}),
        "body": f'''<section><div class="wrap"><div class="grid-2">
<div><h2>{bi({"en":"Sit in the chair of a future master barber.","es":"Siéntate en la silla de un futuro maestro barbero."})}</h2><p class="lead">{bi(h["intro"])}</p>
<div class="contact-strip"><span><b style="color:var(--ink)">{bi({"en":"Book a chair","es":"Reserva un asiento"})}</b> <a href="tel:{tel(h["booking_phone"])}">{h["booking_phone"]}</a></span><span><b style="color:var(--ink)">{bi({"en":"Hours","es":"Horario"})}</b> {h["hours"]}</span></div>
<p class="lead" style="font-size:.95rem">{bi(h["what_to_expect"])}</p></div>
<div class="card"><div class="eyebrow-acc" style="margin-bottom:10px">{bi({"en":"Services","es":"Servicios"})}</div><div>{services}</div></div></div></div></section>'''}

def p_jobplacement():
    j = CONTENT["job_placement"]
    services = "".join(f"<li>{bi(s)}</li>" for s in j["services"])
    return {"eyebrow": bi({"en":"Job Placement","es":"Colocación Laboral"}),
        "h1": bi({"en":"From license to first chair.","es":"De la licencia a la primera silla."}),
        "sub": bi(j["intro"]),
        "body": f'''<section><div class="wrap"><div class="grid-2"><div><h2>{bi({"en":"What our Job Placement Office does","es":"Qué hace nuestra Oficina de Colocación Laboral"})}</h2><ul class="list-clean">{services}</ul></div><div class="card"><h3 style="font-size:1.3rem;margin-bottom:10px">{bi({"en":"The outcome","es":"El resultado"})}</h3><p style="color:var(--mut);font-size:1rem;line-height:1.7">{bi(j["outcomes"])}</p><a class="btn btn-primary" style="margin-top:18px" href="/partners">{bi({"en":"See partner shops →","es":"Ver barberías aliadas →"})}</a></div></div></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["apply_today"])}</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">{bi(UI["see_programs"])}</a></div></section>'''}

def p_resources():
    r = CONTENT["resources"]
    def block(b):
        items = "".join(f"<li>{bi(i)}</li>" for i in b.get("items", []))
        intro = f'<p style="color:var(--mut);font-size:1rem;line-height:1.7;margin-bottom:14px">{bi(b["intro"])}</p>' if b.get("intro") else ""
        outro = f'<p style="color:var(--mut);font-size:.92rem;margin-top:14px">{bi(b["outro"])}</p>' if b.get("outro") else ""
        title = bi(b["title"]) if isinstance(b["title"], dict) else b["title"]
        return f'<div class="card"><h3 style="font-size:1.25rem;margin-bottom:10px">{title}</h3>{intro}<ul class="list-clean">{items}</ul>{outro}</div>'
    cards = block(r["veterans"]) + block(r["accesvr"]) + block(r["licensing"]) + block(r["tools"])
    return {"eyebrow": bi({"en":"Resources","es":"Recursos"}),
        "h1": bi({"en":"Everything you need to start.","es":"Todo lo que necesitas para empezar."}),
        "sub": bi({"en":"Veterans benefits. ACCES-VR. NY State licensing. Tools.","es":"Beneficios para Veteranos. ACCES-VR. Licencias del Estado de NY. Herramientas."}),
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:14px">{bi({"en":"Still have questions?","es":"¿Aún tienes preguntas?"})}</h2><a class="btn btn-primary" href="/contact">{bi(UI["talk_admissions"])}</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">{bi(UI["read_faq"])}</a></div></section>'''}

def p_faq():
    items = "".join(f'<details class="card" style="margin-bottom:11px"><summary style="cursor:pointer;font-weight:700;font-size:1.05rem;min-height:32px;list-style-position:outside">{bi(q["q"])}</summary><p style="margin-top:12px;color:var(--mut);line-height:1.7">{bi(q["a"])}</p></details>' for q in CONTENT["faqs"])
    return {"eyebrow": bi({"en":"FAQ","es":"Preguntas Frecuentes"}),
        "h1": bi({"en":"Frequently asked questions.","es":"Preguntas frecuentes."}),
        "sub": bi({"en":"Tuition, schedule, licensing, GI Bill®, ACCES-VR, job placement.","es":"Matrícula, horario, licencias, GI Bill®, ACCES-VR, colocación laboral."}),
        "body": f'<section><div class="wrap" style="max-width:820px">{items}</div></section><section><div class="wrap" style="text-align:center"><p class="lead" style="margin:0 auto 18px">{bi({"en":"Still have questions? We answer the phone.","es":"¿Aún tienes preguntas? Respondemos el teléfono."})}</p><a class="btn btn-primary" href="tel:{tel(B["phone_manhattan"])}">{bi(UI["call_admissions"])} · {B["phone_manhattan"]}</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">{bi(UI["send_message"])}</a></div></section>'}

def p_contact():
    c1, c2 = CONTENT["campuses"]
    return {"eyebrow": bi({"en":"Contact","es":"Contacto"}),
        "h1": bi({"en":"Visit ABI.","es":"Visita ABI."}),
        "sub": bi({"en":"Two campuses across NYC. Call, walk in, or send a message — admissions responds same-day.","es":"Dos campus en NYC. Llama, ven sin cita, o envía un mensaje — admisiones responde el mismo día."}),
        "body": f'''<section><div class="wrap"><div class="grid-2">
<div class="card"><div class="eyebrow-acc">{bi({"en":"Manhattan Campus","es":"Campus de Manhattan"})}</div><h3 style="font-size:1.3rem;margin:8px 0">{bi(c1["name"])} — 48 West 39th Street</h3><p style="color:var(--mut);margin-bottom:8px">{c1["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c1["phone"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{c1["phone"]} <span class="lang-en">(English)</span><span class="lang-es">(Inglés)</span></a></p>
<p style="margin-bottom:6px"><a href="tel:{tel(B["phone_manhattan_es"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{B["phone_manhattan_es"]} <span class="lang-en">(Spanish)</span><span class="lang-es">(Español)</span></a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{bi(c1["hours"])}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=48+West+39th+Street+New+York+NY">{bi(UI["get_directions"])}</a></div>
<div class="card"><div class="eyebrow-acc">{bi({"en":"Bronx Campus","es":"Campus del Bronx"})}</div><h3 style="font-size:1.3rem;margin:8px 0">{bi(c2["name"])} — 121 Westchester Square</h3><p style="color:var(--mut);margin-bottom:8px">{c2["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c2["phone"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{c2["phone"]}</a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{bi(c2["hours"])}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=121+Westchester+Square+Bronx+NY">{bi(UI["get_directions"])}</a></div>
</div></div></section>
<section><div class="wrap"><div class="card" style="max-width:680px;margin:0 auto"><h2 style="margin-bottom:8px;font-size:1.6rem">{bi({"en":"Request information","es":"Solicita información"})}</h2><p style="color:var(--mut);margin-bottom:22px">{bi({"en":"Tell us a little about you and an admissions advisor will be in touch within one business day.","es":"Cuéntanos un poco sobre ti y un asesor de admisiones se comunicará contigo en un día hábil."})}</p><form action="mailto:{B["email"]}" method="post" enctype="text/plain" style="display:grid;gap:14px"><input required name="name" placeholder="{L({"en":"Full name","es":"Nombre completo"},"en")} / Nombre" class="input"><input required name="email" type="email" placeholder="Email" class="input"><input required name="phone" placeholder="{L({"en":"Phone","es":"Teléfono"},"en")} / Teléfono" class="input"><select name="program" class="input"><option>500-Hour Master Barber</option><option>50-Hour Refresher</option><option>3-Hour Contagious Diseases</option><option>540-Hour Bronx Master Barber</option></select><textarea name="message" placeholder="{L({"en":"What would you like to know?","es":"¿Qué te gustaría saber?"},"en")}" rows="4" class="input" style="resize:vertical"></textarea><button type="submit" class="btn btn-primary">{bi({"en":"Send to admissions","es":"Enviar a admisiones"})}</button></form></div></div></section>'''}

# ============== ASSET BUNDLER ==============
def bundle_assets(site, site_dir):
    """Copy logo + bg video + gallery subset into <site>/assets/. Each site gets a varied gallery."""
    assets_dir = site_dir / "assets"
    img_dir = assets_dir / "img"
    assets_dir.mkdir(exist_ok=True)
    img_dir.mkdir(exist_ok=True)
    # Logo
    src_logo = SRC_ASSETS / "logos" / site["logo"]
    if src_logo.exists():
        shutil.copy2(src_logo, assets_dir / "logo.jpeg")
    # BG video
    src_vid = SRC_ASSETS / "videos" / site["video"]
    if src_vid.exists():
        shutil.copy2(src_vid, assets_dir / "bg.mp4")
    # Gallery — every site gets ALL gallery images (so each is self-contained)
    src_imgs = SRC_ASSETS / "img"
    if src_imgs.exists():
        for f in sorted(os.listdir(src_imgs)):
            if f.lower().endswith(('.jpeg','.jpg','.png')):
                dst = img_dir / f
                if not dst.exists():
                    shutil.copy2(src_imgs / f, dst)

# ============== INDEX HTML SURGERY ==============
def strip_old_injection(html):
    # Remove all prior injections (v2/v3/v4 markers + sub-page nav)
    html = re.sub(r'<!-- ABI v[234] (SEO )?INJECTED -->\n', '', html)
    html = re.sub(r'<meta name="description"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<meta name="keywords"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<meta name="author"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<meta name="robots"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<meta name="theme-color"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="canonical"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="sitemap"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="icon"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="apple-touch-icon"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="preconnect"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="dns-prefetch"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<meta property="og:[^"]*"[^>]*>\n', '', html, count=0)
    html = re.sub(r'<meta name="twitter:[^"]*"[^>]*>\n', '', html, count=0)
    html = re.sub(r'<meta name="format-detection"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', html, count=0, flags=re.DOTALL)
    # Strip any previous overlay style + js + sticky-call we injected
    html = re.sub(r'<style>\n?/\* (mobile-first responsive overlay|===== ABI v2[^*]*?\*/).*?</style>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r"<script>\s*\(function\(\)\s*\{[^<]*?burger\.className\s*=\s*'burger'[^<]*?\}\)\(\);\s*</script>\n?", '', html, count=0, flags=re.DOTALL)
    html = re.sub(r"<script>\s*\(function\s*\(\)\s*\{[^<]*?abi_lang[^<]*?\}\)\(\);\s*</script>\n?", '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<a class="sticky-call"[^<]*?</a>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<div class="sticky-call"[^>]*>.*?</div>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<video class="bg-video"[^<]*<source[^>]*></video>\n?', '', html, count=0)
    return html

def replace_title(html):
    return re.sub(r'<title>[^<]*</title>', f'<title>{BRAND_TITLE}</title>', html, count=1)

def fix_asset_urls(html):
    """All references to abi-assets.vercel.app become local /assets paths."""
    # Specific asset paths
    html = html.replace("https://abi-assets.vercel.app/", "/assets-cdn-removed/")  # marker
    html = html.replace("../assets/", "/assets/")
    html = html.replace('"assets-cdn-removed/logos/', '"/assets/logos/')  # leave as-is for now
    html = html.replace('"assets-cdn-removed/videos/', '"/assets/videos/')
    html = html.replace('"assets-cdn-removed/img/', '"/assets/img/')
    # Catch anything left
    html = re.sub(r'(["\(])\s*/?assets-cdn-removed/', r'\1/assets/', html)
    # Now point to per-site assets — the site logo and video are at /assets/logo.jpeg and /assets/bg.mp4
    return html

def inject_head(html, site, page_path="/"):
    extras = head_meta(page_path, site) + "\n" + jsonld()
    return re.sub(r'</title>', lambda m: m.group(0) + "\n" + extras, html, count=1)

def inject_body_tail(html, site):
    bundle = universal_overlay(site) + "\n" + hamburger_js_and_lang_js() + "\n" + sticky_call()
    return html.replace('</body>', bundle + '\n</body>', 1)

def replace_nav(html):
    # Replace contents of <nav class="nav-links"> ... </nav> with our nav
    nav_items = [("home","/"), ("about","/about"), ("programs","/programs"), ("instructors","/instructors"),
                 ("gallery","/gallery"), ("partners","/partners"), ("haircuts","/haircuts"),
                 ("jobplacement","/job-placement"), ("resources","/resources"), ("faq","/faq"), ("contact","/contact")]
    links = "".join(f'<a href="{p}">{bi(NAV[k])}</a>' for k,p in nav_items)
    return re.sub(r'<nav class="nav-links">.*?</nav>', f'<nav class="nav-links">{links}</nav>', html, count=1, flags=re.DOTALL)

def inject_bg_video(html, site):
    if 'class="bg-video"' in html: return html
    vid = f'<video class="bg-video" autoplay muted loop playsinline aria-hidden="true" poster="/{LOGO_PATH}"><source src="/{VIDEO_PATH}" type="video/mp4"></video>'
    return html.replace('<body>', '<body class="lang-en">\n' + vid, 1)

def add_lang_class(html):
    """Ensure <body> has 'lang-en' class for default."""
    if 'class="lang-en"' in html or 'class="lang-es"' in html: return html
    # add to <body> tag
    return re.sub(r'<body(\s[^>]*)?>', lambda m: m.group(0).replace('<body', '<body class="lang-en"', 1) if 'class=' not in m.group(0) else m.group(0).replace('class="', 'class="lang-en ', 1), html, count=1)

def inject_dual_call_in_topnav(html):
    """The existing nav has just nav-links. Insert dual call buttons + lang toggle after the nav-links container."""
    # Find the .nav container's closing or insert call-row before the </header>'s nav close
    # Find <a class="nav-cta">...</a> and replace with the call-row block
    call_row = f'''<div class="call-row">
<a class="call-btn" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call English"><span class="flag">EN</span><span class="lang-en">Call</span><span class="lang-es">Llama</span><span class="num">{B["phone_manhattan"]}</span></a>
<a class="call-btn" href="tel:{tel(B["phone_manhattan_es"])}" aria-label="Llamar Español"><span class="flag">ES</span><span class="lang-en">Call ES</span><span class="lang-es">Llama</span><span class="num">{B["phone_manhattan_es"]}</span></a>
<div class="lang-toggle" role="group" aria-label="Language"><button type="button" data-lang="en">EN</button><button type="button" data-lang="es">ES</button></div>
</div>'''
    # Try to replace any existing nav-cta with call-row
    if re.search(r'<a class="nav-cta"[^<]*</a>', html):
        return re.sub(r'<a class="nav-cta"[^<]*</a>', call_row, html, count=1, flags=re.DOTALL)
    # Otherwise insert after .nav-links closing
    return re.sub(r'(</nav>)', r'\1' + call_row, html, count=1)

# ============== BUILD ONE SITE ==============
def build_site(site):
    slug = site["slug"]
    site_dir = ROOT / slug
    if not site_dir.exists():
        print(f"  SKIP (no folder): {slug}"); return

    # 0) Bundle assets per-site
    bundle_assets(site, site_dir)

    # 1) Enhance index.html
    idx = site_dir / "index.html"
    html = idx.read_text(encoding="utf-8", errors="replace")
    html = strip_old_injection(html)
    html = replace_title(html)
    html = fix_asset_urls(html)
    html = replace_nav(html)
    html = inject_dual_call_in_topnav(html)
    html = inject_bg_video(html, site)
    html = add_lang_class(html)
    html = inject_head(html, site, "/")
    html = inject_body_tail(html, site)
    html = html.replace('</head>', '<!-- ABI v4 INJECTED -->\n</head>', 1)
    idx.write_text(html, encoding="utf-8")

    # 2) Sub-pages
    pages_def = [
        ("about.html","about","/about", p_about),
        ("programs.html","programs","/programs", p_programs),
        ("instructors.html","instructors","/instructors", p_instructors),
        ("gallery.html","gallery","/gallery", p_gallery),
        ("partners.html","partners","/partners", p_partners),
        ("haircuts.html","haircuts","/haircuts", p_haircuts),
        ("job-placement.html","jobplacement","/job-placement", p_jobplacement),
        ("resources.html","resources","/resources", p_resources),
        ("faq.html","faq","/faq", p_faq),
        ("contact.html","contact","/contact", p_contact),
    ]
    for fname, key, path, fn in pages_def:
        pdata = fn()
        html = render_subpage(site, key, pdata, path)
        # Gallery placeholder special handling
        if key == "gallery":
            imgs = sorted([f for f in os.listdir(site_dir / "assets" / "img") if f.lower().endswith(('.jpeg','.jpg','.png'))])[:30]
            tiles = "".join(f'<div class="card" style="padding:0;overflow:hidden;background:rgba(0,0,0,.3)"><img src="/assets/img/{f}" loading="lazy" alt="ABI" style="aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:18px"></div>' for f in imgs)
            gallery_body = f'<section><div class="wrap"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">{tiles}</div></div></section><section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">{bi(UI["visit_campus"])}</a></div></section>'
            html = html.replace("<!--GALLERY_PLACEHOLDER-->", gallery_body)
        (site_dir / fname).write_text(html, encoding="utf-8")

    # 3) Sitemap
    base = f"https://{site['vercel_name']}.vercel.app"
    paths = ["/", "/about", "/programs", "/instructors", "/gallery", "/partners", "/haircuts", "/job-placement", "/resources", "/faq", "/contact"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in paths:
        sm += f'  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq><priority>{"1.0" if p=="/" else "0.7"}</priority></url>\n'
    sm += '</urlset>\n'
    (site_dir / "sitemap.xml").write_text(sm)
    (site_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    vercel = {"cleanUrls": True, "trailingSlash": False, "headers": [
        {"source": "/assets/(.*)", "headers": [{"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},
        {"source": "/(.*).html", "headers": [{"key":"Cache-Control","value":"public, max-age=300, must-revalidate"}]},
    ]}
    (site_dir / "vercel.json").write_text(json.dumps(vercel, indent=2))
    print(f"  OK {slug}: assets bundled + index neutralized + 10 subpages + bilingual + sitemap")

if __name__ == "__main__":
    print("Building 10 ABI sites · standalone · bilingual EN/ES · per-site assets")
    for s in SITES:
        build_site(s)
    print("Done.")
