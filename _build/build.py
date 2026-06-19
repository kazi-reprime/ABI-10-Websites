"""ABI 10-Websites builder v3 — neutral branding (no theme leaks), full page set, sticky call button."""
from __future__ import annotations
import json, os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CDN = "https://abi-assets.vercel.app"
CONTENT = json.loads((ROOT / "_content" / "content.json").read_text())
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]

def tel(p): return p.replace("(","").replace(")","").replace(" ","").replace("-","")

# Standard SEO — same brand identity across ALL 10 sites (no theme name leak)
BRAND_TITLE = "American Barber Institute · NYC's Dedicated Barber School · 30+ Years"
BRAND_DESC = "American Barber Institute (ABI) — New York's only dedicated barber school. NY State licensed. 30+ years, 10,000+ graduates. GI Bill® accepted. Manhattan & Bronx campuses. Start the first Monday of every month."

PAGE_META = {
    "/":           {"title": BRAND_TITLE, "desc": BRAND_DESC},
    "/about":      {"title": "About · American Barber Institute · NYC", "desc": "30+ years training master barbers in New York. 10,000+ graduates. Licensed by the NY State Department of Education. Meet our school, our leadership, and our story."},
    "/programs":   {"title": "Programs & Tuition · American Barber Institute", "desc": "500-Hour Master Barber, 50-Hour Refresher, 3-Hour Contagious Diseases, and 540-Hour Bronx Master Barber. Morning, Afternoon, and Weekend tracks. $4,600–$5,600 tuition with flexible weekly plans."},
    "/instructors":{"title": "Instructors · American Barber Institute", "desc": "Meet King David, Barkim, Barry, Richard, and the master-barber faculty training the next generation in NYC. 50+ years of combined experience on the clinic floor."},
    "/gallery":    {"title": "Gallery · American Barber Institute", "desc": "Student work, campus life, and everyday moments from the American Barber Institute Manhattan and Bronx campuses."},
    "/partners":   {"title": "Partner Shops · American Barber Institute", "desc": "Where ABI graduates work: Levels Barbershop, Diamond Fadez, Untouchable Cutz, Expo Gentlemen Salon, Otis & Finn, NYC Barber Shop Museum. Real shops. Real careers."},
    "/haircuts":   {"title": "Public Student Clinic Haircuts · ABI · $3", "desc": "Get a $3 student haircut at the American Barber Institute Manhattan or Bronx campus. Fades, tapers, beard work, shaves — every cut supervised by a NY-licensed master barber. Book: (856) 316-1551."},
    "/job-placement":{"title": "Job Placement · American Barber Institute", "desc": "Every ABI graduate meets with our Job Placement Office. 1-on-1 counseling, partner-shop referrals, resume review, mock interviews, and shop-owner mentorship."},
    "/resources": {"title": "Resources · Veterans · ACCES-VR · Licensing · ABI", "desc": "Veterans & GI Bill® (Ch. 33, 31, 35, Montgomery). ACCES-VR. NY State Board of Barbering. Tools and supplies. Everything you need to start at ABI."},
    "/faq":        {"title": "Frequently Asked Questions · American Barber Institute", "desc": "Tuition, schedule, licensing, GI Bill, ACCES-VR, job placement, tools — every question we hear, answered. American Barber Institute, NYC."},
    "/contact":    {"title": "Contact · American Barber Institute · NYC", "desc": "Two campuses: Manhattan (48 W 39th St) and the Bronx (121 Westchester Sq). Call admissions: (212) 290-2289 (English) · (212) 290-0278 (Spanish) · (718) 676-0640 (Bronx)."},
}

# Universal SEO head — same across all 10 sites and all 11 pages (varies only by page path)
def head_meta(site, page_path="/"):
    meta = PAGE_META.get(page_path, PAGE_META["/"])
    title, desc = meta["title"], meta["desc"]
    url = f"https://{site['vercel_name']}.vercel.app{page_path}"
    image_url = f"{CDN}/logos/{site['logo']}"
    return f'''<meta name="description" content="{desc}">
<meta name="keywords" content="barber school nyc, american barber institute, abi, barber school new york, master barber program, master barber license ny, barber academy nyc, gi bill barber school, weekend barber school, barber training new york, manhattan barber school, bronx barber school">
<meta name="author" content="American Barber Institute">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="{site['primary_color']}">
<link rel="canonical" href="{url}">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="icon" type="image/jpeg" href="{CDN}/logos/{site['logo']}">
<link rel="apple-touch-icon" href="{CDN}/logos/{site['logo']}">
<link rel="preconnect" href="{CDN}">
<link rel="dns-prefetch" href="{CDN}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image_url}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image_url}">
<meta name="format-detection" content="telephone=yes">'''

def jsonld(site, include_faq=True):
    school = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "American Barber Institute",
        "alternateName": "ABI",
        "url": f"https://{site['vercel_name']}.vercel.app",
        "logo": f"{CDN}/logos/{site['logo']}",
        "description": BRAND_DESC,
        "telephone": CONTENT["brand"]["phone_manhattan"],
        "email": CONTENT["brand"]["email"],
        "foundingDate": "1995",
        "address": [
            {"@type":"PostalAddress","streetAddress":"48 West 39th Street","addressLocality":"New York","addressRegion":"NY","postalCode":"10018","addressCountry":"US"},
            {"@type":"PostalAddress","streetAddress":"121 Westchester Square","addressLocality":"Bronx","addressRegion":"NY","postalCode":"10461","addressCountry":"US"},
        ],
        "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.3","ratingCount":"100"},
    }
    out = f'<script type="application/ld+json">{json.dumps(school)}</script>'
    if include_faq:
        faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q["q"],"acceptedAnswer":{"@type":"Answer","text":q["a"]}} for q in CONTENT["faqs"]]}
        out += f'\n<script type="application/ld+json">{json.dumps(faq)}</script>'
    return out

def responsive_overlay(site):
    return f'''<style>
/* mobile-first responsive overlay */
:root {{ --abi-touch: 44px; --abi-accent: {site["primary_color"]}; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ overflow-x: hidden; padding-bottom: 0; }}
img {{ max-width: 100%; height: auto; display: block; }}
video {{ max-width: 100%; height: auto; }}
button, .btn, a.btn, .nav-cta, a.nav-cta {{ min-height: var(--abi-touch); display: inline-flex; align-items: center; justify-content: center; }}
.burger {{ width: var(--abi-touch); height: var(--abi-touch); display: none; flex-direction: column; gap: 5px; cursor: pointer; align-items: center; justify-content: center; background: transparent; border: 0; padding: 0; }}
.burger span {{ width: 26px; height: 2px; background: currentColor; transition: .2s; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}
@media (max-width: 980px) {{
  .nav-links {{ position: fixed !important; inset: 70px 0 auto 0 !important; flex-direction: column !important; align-items: stretch !important; gap: 0 !important; background: rgba(8,8,14,.97) !important; backdrop-filter: blur(20px); padding: 12px 18px 22px !important; transform: translateY(-110%); transition: transform .28s ease; box-shadow: 0 18px 36px rgba(0,0,0,.45); z-index: 24; display: flex !important; max-height: calc(100vh - 70px); overflow-y: auto; }}
  .nav-links a {{ padding: 14px 6px !important; border-bottom: 1px solid rgba(255,255,255,.07); font-size: 1rem !important; min-height: var(--abi-touch); display: flex !important; align-items: center; }}
  .nav-links a:last-child {{ border-bottom: 0; }}
  .nav-links.open {{ transform: translateY(0); }}
  .burger {{ display: inline-flex; color: var(--abi-accent); }}
  h1 {{ font-size: clamp(2.1rem, 9vw, 3.4rem) !important; }}
  h2 {{ font-size: clamp(1.55rem, 6.4vw, 2.2rem) !important; }}
  .wrap, .container {{ padding-left: 18px !important; padding-right: 18px !important; }}
  section {{ padding-top: 48px !important; padding-bottom: 48px !important; }}
  .hero {{ min-height: 86vh !important; padding-top: 80px !important; padding-bottom: 40px !important; }}
  .btn-row, .actions, .hero-actions {{ flex-direction: column !important; align-items: stretch !important; gap: 12px !important; }}
  .btn-row > *, .actions > *, .hero-actions > * {{ width: 100%; text-align: center; }}
  .grid, [class*="grid"] {{ grid-template-columns: 1fr !important; }}
  .row, .two-col, .three-col {{ flex-direction: column !important; }}
  .ticker {{ font-size: .65rem !important; }}
  body {{ padding-bottom: 64px; }}
  .sticky-call {{ display: flex !important; }}
}}
@media (max-width: 480px) {{
  .wrap, .container {{ padding-left: 14px !important; padding-right: 14px !important; }}
  .hero h1, h1 {{ font-size: clamp(1.9rem, 9vw, 2.8rem) !important; }}
}}
@media (min-width: 981px) {{ .burger {{ display: none !important; }} }}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation-duration: .001s !important; animation-iteration-count: 1 !important; transition-duration: .001s !important; }} }}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .14; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .08; }} }}

/* Sticky mobile call button */
.sticky-call {{ display: none; position: fixed; left: 14px; right: 14px; bottom: 14px; z-index: 50; padding: 14px 18px; border-radius: 999px; background: var(--abi-accent); color: #06070c; font-weight: 800; font-size: 1rem; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06); text-decoration: none; align-items: center; justify-content: center; gap: 8px; }}
.sticky-call svg {{ width: 18px; height: 18px; }}
.sticky-call:active {{ transform: scale(.98); }}
</style>'''

def hamburger_js():
    return '''<script>
(function(){
  var nav = document.querySelector('.nav-links');
  if (!nav) return;
  var burger = document.querySelector('.burger');
  if (!burger) {
    burger = document.createElement('button');
    burger.className = 'burger';
    burger.setAttribute('aria-label','Toggle navigation');
    burger.setAttribute('aria-expanded','false');
    burger.innerHTML = '<span></span><span></span><span></span>';
    var nw = document.querySelector('header .nav') || document.querySelector('header > div') || document.querySelector('header');
    if (nw) nw.appendChild(burger);
  }
  function cl(){ nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }
  burger.addEventListener('click', function(){ var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o ? 'true':'false'); });
  nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', cl); });
  document.addEventListener('keydown', function(e){ if (e.key==='Escape') cl(); });
})();
</script>'''

# Sticky call button HTML (added to body)
def sticky_call_html():
    return f'''<a class="sticky-call" href="tel:{tel(CONTENT["brand"]["phone_manhattan"])}" aria-label="Call admissions">
<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A18 18 0 0 1 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.2 2.2z"/></svg>
Call admissions · {CONTENT["brand"]["phone_manhattan"]}
</a>'''

# Replace existing <title>...</title> with neutral brand title (no theme name)
def replace_title(html):
    return re.sub(r'<title>[^<]*</title>', f'<title>{BRAND_TITLE}</title>', html, count=1)

# Replace ../assets/ with CDN
def fix_paths(html):
    return re.sub(r'(["\(\'])\.\./assets/', lambda m: m.group(1) + CDN + '/', html)

# Strip the "v2 SEO INJECTED" marker and the head we previously injected (so we can re-inject clean)
def strip_old_injection(html):
    # Remove the marker
    html = html.replace('<!-- ABI v2 SEO INJECTED -->\n', '')
    html = html.replace('<!-- ABI v2 SEO INJECTED -->', '')
    # Remove all lines between </title> and </head> that match our injection
    # Simpler: remove every <meta name="description">…<meta name="format-detection"> block plus <link rel="canonical">… plus <script type="application/ld+json">…
    html = re.sub(r'<meta name="description" content="[^"]*">\n', '', html, count=1)
    html = re.sub(r'<meta name="keywords" content="[^"]*">\n', '', html, count=1)
    html = re.sub(r'<meta name="author" content="American Barber Institute">\n', '', html, count=1)
    html = re.sub(r'<meta name="robots" content="index, follow">\n', '', html, count=1)
    html = re.sub(r'<meta name="theme-color"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="canonical"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="sitemap"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="icon" type="image/jpeg"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="apple-touch-icon"[^>]*>\n', '', html, count=1)
    html = re.sub(r'<link rel="preconnect" href="https://abi-assets[^"]*">\n', '', html, count=1)
    html = re.sub(r'<link rel="dns-prefetch" href="https://abi-assets[^"]*">\n', '', html, count=1)
    html = re.sub(r'<meta property="og:[^"]*"[^>]*>\n', '', html, count=0)
    html = re.sub(r'<meta name="twitter:[^"]*"[^>]*>\n', '', html, count=0)
    html = re.sub(r'<meta name="format-detection"[^>]*>\n', '', html, count=1)
    # Remove our JSON-LD scripts (the BIG ones)
    html = re.sub(r'<script type="application/ld\+json">[^<]*</script>\n', '', html, count=0)
    # Remove our previous responsive overlay style + JS (between known markers if present)
    # Easier: drop everything starting from "/* ===== ABI v2 mobile-first" up to its </style>
    html = re.sub(r'<style>\n?/\* ===== ABI v2 mobile-first[^*]*?\*/.*?</style>\n?', '', html, count=0, flags=re.DOTALL)
    html = re.sub(r'<style>\n?/\* mobile-first responsive overlay.*?</style>\n?', '', html, count=0, flags=re.DOTALL)
    # Remove our hamburger script (heuristic — find script with .burger creation)
    html = re.sub(r"<script>\s*\(function\(\)\{[^<]*burger\.className = 'burger'[^<]*\}\)\(\);\s*</script>\n?", '', html, count=0, flags=re.DOTALL)
    # Remove sticky-call existing
    html = re.sub(r'<a class="sticky-call"[^<]*</a>\n?', '', html, count=0, flags=re.DOTALL)
    # Remove background video we injected
    html = re.sub(r'<video class="bg-video"[^<]*<source[^>]*></video>\n?', '', html, count=0)
    return html

def inject_head(html, site, page_path="/"):
    extras = head_meta(site, page_path) + "\n" + jsonld(site)
    return re.sub(r'</title>', lambda m: m.group(0) + "\n" + extras, html, count=1)

def inject_body_tail(html, site, page_path="/"):
    overlay = responsive_overlay(site) + "\n" + hamburger_js()
    sticky = sticky_call_html()
    return html.replace('</body>', f'{overlay}\n{sticky}\n</body>', 1)

# Inject background video near top of body
def inject_bg_video(html, site):
    if 'class="bg-video"' in html: return html
    vid = f'<video class="bg-video" autoplay muted loop playsinline aria-hidden="true" poster="{CDN}/logos/{site["logo"]}"><source src="{CDN}/videos/{site["video"]}" type="video/mp4"></video>'
    return html.replace('<body>', '<body>\n' + vid, 1)

# Inject expanded nav links into existing .nav-links container
NEW_NAV = '<a href="/">Home</a><a href="/about">About</a><a href="/programs">Programs</a><a href="/instructors">Instructors</a><a href="/gallery">Gallery</a><a href="/partners">Partners</a><a href="/haircuts">Haircuts</a><a href="/job-placement">Job Placement</a><a href="/resources">Resources</a><a href="/faq">FAQ</a><a href="/contact">Contact</a>'

def replace_nav(html):
    # Replace contents of <nav class="nav-links">...</nav> with NEW_NAV
    return re.sub(r'<nav class="nav-links">.*?</nav>', f'<nav class="nav-links">{NEW_NAV}</nav>', html, count=1, flags=re.DOTALL)

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
:root {{ --accent: {accent}; --bg: #07080d; --bg2: #0d1018; --ink: #e9ecff; --mut: #8b91b8; --line: rgba(255,255,255,.08); --abi-touch: 44px; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
body {{ background: var(--bg); color: var(--ink); font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; line-height: 1.65; overflow-x: hidden; min-height: 100vh; padding-bottom: 0; }}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; height: auto; display: block; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 2; }}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .12; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .07; }} }}
.bg-overlay {{ position: fixed; inset: 0; background: radial-gradient(ellipse at center, transparent 0, rgba(0,0,0,.5) 70%, var(--bg) 100%); z-index: 1; pointer-events: none; }}
header {{ position: sticky; top: 0; z-index: 30; background: rgba(7,8,13,.88); backdrop-filter: blur(18px); border-bottom: 1px solid var(--line); }}
.nav {{ display: flex; align-items: center; justify-content: space-between; height: 70px; max-width: 1180px; margin: 0 auto; padding: 0 24px; gap: 16px; }}
.logo {{ display: flex; align-items: center; gap: 12px; font-weight: 900; letter-spacing: .04em; font-size: 1rem; }}
.logo img {{ width: 38px; height: 38px; border-radius: 10px; object-fit: cover; }}
.nav-links {{ display: flex; gap: 18px; font-size: .88rem; font-weight: 600; color: var(--mut); }}
.nav-links a {{ transition: .2s; padding: 6px 2px; white-space: nowrap; }}
.nav-links a:hover, .nav-links a.active {{ color: var(--accent); }}
.nav-cta {{ padding: 10px 22px; border: 1px solid var(--accent); border-radius: 40px; color: var(--accent); font-weight: 700; font-size: .82rem; min-height: 44px; display: inline-flex; align-items: center; gap: 6px; transition: .2s; }}
.nav-cta:hover {{ background: var(--accent); color: var(--bg); }}
.burger {{ display: none; flex-direction: column; gap: 5px; cursor: pointer; width: 44px; height: 44px; align-items: center; justify-content: center; background: transparent; border: 0; color: var(--accent); }}
.burger span {{ width: 26px; height: 2px; background: currentColor; transition: .2s; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}
.subpage-hero {{ padding: 90px 0 50px; text-align: center; position: relative; }}
.eyebrow {{ display: inline-block; padding: 6px 14px; border: 1px solid var(--line); border-radius: 30px; font-size: .68rem; letter-spacing: .3em; text-transform: uppercase; color: var(--accent); }}
.subpage-hero h1 {{ font-family: 'Arial Black', system-ui; font-size: clamp(2.1rem, 6.4vw, 3.8rem); margin: 22px 0 14px; line-height: 1.05; letter-spacing: -.02em; }}
.subpage-hero p.sub {{ max-width: 680px; margin: 0 auto; color: var(--mut); font-size: 1.06rem; }}
section {{ padding: 50px 0; position: relative; z-index: 2; }}
section h2 {{ font-family: 'Arial Black', system-ui; font-size: clamp(1.6rem, 4vw, 2.4rem); line-height: 1.1; margin-bottom: 12px; letter-spacing: -.02em; }}
section p.lead {{ color: var(--mut); max-width: 720px; margin-bottom: 24px; font-size: 1.02rem; }}
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
.sticky-call {{ display: none; position: fixed; left: 14px; right: 14px; bottom: 14px; z-index: 50; padding: 14px 18px; border-radius: 999px; background: var(--accent); color: var(--bg); font-weight: 800; font-size: 1rem; text-align: center; box-shadow: 0 16px 40px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.06); text-decoration: none; align-items: center; justify-content: center; gap: 8px; }}
.sticky-call svg {{ width: 18px; height: 18px; }}
@media (max-width: 980px) {{
  .nav-links {{ position: fixed; inset: 70px 0 auto 0; flex-direction: column; align-items: stretch; background: rgba(7,8,13,.97); backdrop-filter: blur(20px); padding: 12px 22px 22px; transform: translateY(-110%); transition: transform .28s; box-shadow: 0 18px 36px rgba(0,0,0,.45); z-index: 24; gap: 0; max-height: calc(100vh - 70px); overflow-y: auto; }}
  .nav-links a {{ padding: 14px 4px; border-bottom: 1px solid rgba(255,255,255,.07); font-size: 1rem; min-height: 44px; display: flex; align-items: center; }}
  .nav-links a:last-of-type {{ border-bottom: 0; }}
  .nav-links.open {{ transform: translateY(0); }}
  .burger {{ display: inline-flex; }}
  .nav-cta {{ display: none; }}
  .footer-grid {{ grid-template-columns: 1fr 1fr; }}
  .subpage-hero {{ padding: 70px 0 40px; }}
  body {{ padding-bottom: 64px; }}
  .sticky-call {{ display: flex; }}
}}
@media (max-width: 480px) {{ .footer-grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<video class="bg-video" autoplay muted loop playsinline poster="{cdn}/logos/{logo}" aria-hidden="true"><source src="{cdn}/videos/{video}" type="video/mp4"></video>
<div class="bg-overlay"></div>
<header>
  <div class="nav">
    <a class="logo" href="/"><img src="{cdn}/logos/{logo}" alt="American Barber Institute"><span>American Barber Institute</span></a>
    <nav class="nav-links">
      <a href="/" class="{n_home}">Home</a>
      <a href="/about" class="{n_about}">About</a>
      <a href="/programs" class="{n_programs}">Programs</a>
      <a href="/instructors" class="{n_instructors}">Instructors</a>
      <a href="/gallery" class="{n_gallery}">Gallery</a>
      <a href="/partners" class="{n_partners}">Partners</a>
      <a href="/haircuts" class="{n_haircuts}">Haircuts</a>
      <a href="/job-placement" class="{n_jobplacement}">Job Placement</a>
      <a href="/resources" class="{n_resources}">Resources</a>
      <a href="/faq" class="{n_faq}">FAQ</a>
      <a href="/contact" class="{n_contact}">Contact</a>
    </nav>
    <a class="nav-cta" href="tel:{phone_tel}"><span style="font-size:.9rem">📞</span> Apply Now</a>
    <button class="burger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<section class="subpage-hero">
  <div class="wrap">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
  </div>
</section>
{body}
<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>American Barber Institute</h4>
        <p style="margin-bottom:10px">New York's only dedicated barber school. 30+ years. 10,000+ graduates.</p>
        <p style="font-size:.85rem">Licensed by NY State Department of Education (BPSS). GI Bill® accepted. ACCES-VR accepted.</p>
      </div>
      <div>
        <h4>School</h4>
        <a href="/about">About</a>
        <a href="/programs">Programs</a>
        <a href="/instructors">Instructors</a>
        <a href="/gallery">Gallery</a>
      </div>
      <div>
        <h4>Resources</h4>
        <a href="/partners">Partner Shops</a>
        <a href="/job-placement">Job Placement</a>
        <a href="/haircuts">Haircuts</a>
        <a href="/resources">Veterans / GI Bill / ACCES-VR</a>
        <a href="/faq">FAQ</a>
      </div>
      <div>
        <h4>Contact</h4>
        <a href="tel:{phone_man_tel}">Manhattan: {phone_man}</a>
        <a href="tel:{phone_man_es_tel}">Español: {phone_man_es}</a>
        <a href="tel:{phone_brx_tel}">Bronx: {phone_brx}</a>
        <a href="mailto:{email}">{email}</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 American Barber Institute. All rights reserved.</span>
      <span>Licensed by NY State Dept. of Education · GI Bill® accepted</span>
    </div>
  </div>
</footer>
<a class="sticky-call" href="tel:{phone_tel}" aria-label="Call admissions"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A18 18 0 0 1 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.2 2.2z"/></svg>Call admissions · {phone_man}</a>
<script>
(function(){{
  var nav = document.querySelector('.nav-links');
  var b = document.querySelector('.burger');
  if (!b || !nav) return;
  b.addEventListener('click', function(){{ var o = nav.classList.toggle('open'); b.setAttribute('aria-expanded', o ? 'true' : 'false'); }});
  nav.querySelectorAll('a').forEach(function(a){{ a.addEventListener('click', function(){{ nav.classList.remove('open'); b.setAttribute('aria-expanded','false'); }}); }});
}})();
</script>
</body>
</html>
'''

def render_subpage(site, page, pdata):
    pages = ["home","about","programs","instructors","gallery","partners","haircuts","jobplacement","resources","faq","contact"]
    nav = {p: ("" if p != page else "active") for p in pages}
    head_extras = head_meta(site, page_path=pdata["path"])
    jl = jsonld(site, include_faq=(page == "faq"))
    return SUBPAGE.format(
        title=PAGE_META[pdata["path"]]["title"],
        accent=site["primary_color"],
        h1=pdata["h1"], sub=pdata["sub"], body=pdata["body"], eyebrow=pdata["eyebrow"],
        head_meta=head_extras, jsonld=jl,
        n_home=nav["home"], n_about=nav["about"], n_programs=nav["programs"], n_instructors=nav["instructors"],
        n_gallery=nav["gallery"], n_partners=nav["partners"], n_haircuts=nav["haircuts"],
        n_jobplacement=nav["jobplacement"], n_resources=nav["resources"], n_faq=nav["faq"], n_contact=nav["contact"],
        phone_tel=tel(CONTENT["brand"]["phone_manhattan"]),
        phone_man=CONTENT["brand"]["phone_manhattan"], phone_man_tel=tel(CONTENT["brand"]["phone_manhattan"]),
        phone_man_es=CONTENT["brand"]["phone_manhattan_es"], phone_man_es_tel=tel(CONTENT["brand"]["phone_manhattan_es"]),
        phone_brx=CONTENT["brand"]["phone_bronx"], phone_brx_tel=tel(CONTENT["brand"]["phone_bronx"]),
        email=CONTENT["brand"]["email"],
        cdn=CDN, logo=site["logo"], video=site["video"],
    )

# ============== PAGES ==============
B = CONTENT["brand"]

def page_about():
    inst_cards = []
    for ins in CONTENT["instructors"][:3]:
        tags = " · ".join(ins["tags"])
        inst_cards.append(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{ins["role"]}</div><h3 style="font-size:1.25rem;margin-bottom:8px">{ins["name"]}</h3><p style="color:var(--mut);font-size:.95rem;margin-bottom:10px">{ins["bio"]}</p><p style="font-size:.8rem;color:var(--accent)">{tags}</p></div>')
    return {"path":"/about","eyebrow":"About ABI","h1":"30+ years. 10,000+ graduates. One craft.",
        "sub":"American Barber Institute is New York's only dedicated barber school — changing lives in Manhattan and the Bronx for over three decades.",
        "body": f'''<section><div class="wrap"><div class="grid-2"><div><h2>Our story</h2><p class="lead">ABI was built on a simple idea: barbering deserves a school that does <i>only</i> barbering. No nails. No esthetics. No detours. Just the craft, taught by master barbers, on a working clinic floor, the way the trade has always been passed down.</p><p class="lead">Three decades and ten thousand graduates later, that idea has produced the people behind some of New York's most respected shops — from Harlem to Long Island City, from Staten Island to Westchester Square.</p></div><div class="card"><h3 style="margin-bottom:10px">The facility</h3><p style="color:var(--mut)">{B["facility"]} — designed around the working clinic floor, with classroom space, demonstration chairs, and a second campus at 121 Westchester Square in the Bronx.</p><div class="row-stat"><div class="s"><b>{B["years_in_business"]}</b><small>Years training barbers</small></div><div class="s"><b>{B["graduates"]}</b><small>Graduates</small></div><div class="s"><b>{B["rating"]}</b><small>Google rating</small></div></div></div></div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">Leadership</div><h2 style="margin-bottom:24px">The faculty</h2><div class="grid">{"".join(inst_cards)}</div><p style="margin-top:20px"><a class="btn btn-ghost" href="/instructors">Meet all instructors →</a></p></div></section>
<section><div class="wrap"><div class="eyebrow-acc">Why ABI</div><h2 style="margin-bottom:18px">What makes us different</h2><ul class="list-clean" style="max-width:780px">{"".join(f"<li>{w}</li>" for w in CONTENT["why_choose"])}</ul></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">Apply today</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">See programs</a></div></section>'''}

def page_programs():
    rows = []
    for p in CONTENT["programs"]:
        flag = '<span style="position:absolute;top:14px;right:14px;font-size:.6rem;letter-spacing:.18em;text-transform:uppercase;background:var(--accent);color:var(--bg);padding:5px 10px;border-radius:20px;font-weight:800">Flagship</span>' if p.get("flagship") else ""
        det = f'<p style="color:var(--mut);font-size:.88rem;margin-top:10px">{p["details"]}</p>' if p.get("details") else ""
        rows.append(f'<div class="card" style="position:relative">{flag}<div class="eyebrow-acc">{p["campus"]} · {p["duration"]}</div><h3 style="font-size:1.3rem;margin:8px 0">{p["name"]}</h3><div style="font-size:1.4rem;font-weight:800;color:var(--accent);margin-bottom:10px">{p["price"]}</div><p style="color:var(--mut);font-size:.96rem">{p["summary"]}</p>{det}</div>')
    sched = []
    for s in CONTENT["schedules"]:
        sched.append(f'<div class="card"><div class="eyebrow-acc">{s["label"]}</div><h3 style="font-size:1.1rem;margin:8px 0">{s["days"]} · {s["time"]}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:10px 0 6px">{s["tuition"]}</div><p style="color:var(--mut);font-size:.9rem">{s["plan"]}</p></div>')
    enroll_steps = "".join(f'<div class="card"><div style="font-size:2rem;color:var(--accent);font-weight:800;line-height:1">0{s["step"]}</div><h3 style="margin:8px 0;font-size:1.2rem">{s["title"]}</h3><p style="color:var(--mut);font-size:.94rem">{s["desc"]}</p></div>' for s in CONTENT["enrollment_steps"])
    req = "".join(f"<li>{r}</li>" for r in CONTENT["enrollment_requirements"])
    earnings_rows = "".join(f'<div class="card"><div class="eyebrow-acc">{e["window"]}</div><h3 style="font-size:1.2rem;margin:8px 0">{e["stage"]}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:6px 0 8px">{e["range"]}</div><p style="color:var(--mut);font-size:.92rem">{e["desc"]}</p></div>' for e in CONTENT["career_earnings"])
    return {"path":"/programs","eyebrow":"Programs & Tuition","h1":"Programs, tuition, and what you'll learn",
        "sub":"Five programs across two campuses. Three flexible tracks: Morning, Afternoon, Weekend. NY State Master Barber License at the end.",
        "body": f'''<section><div class="wrap"><h2>Choose your program</h2><p class="lead">Every program is state-licensed and exam-prep ready. Tuition is flexible — every plan includes a down payment and a weekly payment schedule.</p><div class="grid">{"".join(rows)}</div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">Schedule & tuition</div><h2 style="margin-bottom:14px">Three flexible schedules</h2><div class="grid">{"".join(sched)}</div><p style="margin-top:18px;color:var(--mut);font-size:.92rem">Veterans &amp; GI Bill® benefits accepted (Post-9/11 Ch. 33, VR&amp;E Ch. 31, Montgomery, DEA Ch. 35). ACCES-VR accepted. <a href="/resources" style="color:var(--accent);text-decoration:underline">See full benefits guide →</a></p></div></section>
<section><div class="wrap"><div class="eyebrow-acc">Enrollment</div><h2 style="margin-bottom:14px">Three steps to your first chair</h2><div class="grid">{enroll_steps}</div></div></section>
<section><div class="wrap"><div class="eyebrow-acc">What you'll need</div><h2 style="margin-bottom:14px">Documents to enroll</h2><ul class="list-clean" style="max-width:680px">{req}</ul></div></section>
<section><div class="wrap"><div class="eyebrow-acc">Career earnings</div><h2 style="margin-bottom:14px">What barbers earn</h2><div class="grid">{earnings_rows}</div><p style="margin-top:18px;color:var(--mut);font-size:.85rem">{CONTENT["earnings_note"]}</p></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">Apply today</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">Read FAQ</a></div></section>'''}

def page_instructors():
    cards = "".join(f'<div class="card"><div class="eyebrow-acc" style="margin-bottom:8px">{i["role"]}</div><h3 style="font-size:1.35rem;margin-bottom:10px">{i["name"]}</h3><p style="color:var(--mut);font-size:1rem;line-height:1.7;margin-bottom:14px">{i["bio"]}</p><p style="font-size:.82rem;color:var(--accent);letter-spacing:.06em">{" · ".join(i["tags"])}</p></div>' for i in CONTENT["instructors"])
    return {"path":"/instructors","eyebrow":"Faculty","h1":"Master barbers. Master teachers.",
        "sub":"Decades of working-floor experience and a clinic-first style of teaching. You learn by chair time, with an instructor inches away when you need them.",
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:14px">Train with us</h2><p class="lead" style="margin:0 auto 20px">New cohorts begin the first Monday of every month at both the Manhattan and Bronx campuses.</p><a class="btn btn-primary" href="/contact">Apply today</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">See programs</a></div></section>'''}

def page_gallery():
    imgs = sorted({f for f in os.listdir(ROOT / "assets" / "img") if f.lower().endswith(('.jpeg','.jpg','.png'))})[:30]
    tiles = "".join(f'<div class="card" style="padding:0;overflow:hidden;background:rgba(0,0,0,.3)"><img src="{CDN}/img/{f}" loading="lazy" alt="ABI student work — barbering training" style="aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:18px"></div>' for f in imgs)
    return {"path":"/gallery","eyebrow":"On the floor","h1":"Student work. Clinic life. Graduation day.",
        "sub":"A glimpse inside the American Barber Institute. Real students. Real chairs. Real fades.",
        "body": f'<section><div class="wrap"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">{tiles}</div></div></section><section><div class="wrap" style="text-align:center"><p class="lead" style="margin:0 auto 18px">Follow us for more from the floor.</p><a class="btn btn-ghost" href="https://instagram.com/americanbarberinstitute" target="_blank">Follow @americanbarberinstitute</a> <a class="btn btn-primary" href="/contact" style="margin-left:8px">Visit our campus</a></div></section>'}

def page_partners():
    cards = "".join(f'<div class="card"><div class="eyebrow-acc">{p["locations"]}</div><h3 style="font-size:1.35rem;margin:10px 0 8px">{p["name"]}</h3><p style="color:var(--mut);font-size:.96rem;margin-bottom:14px">{p["desc"]}</p><p style="font-size:.88rem;color:var(--accent);font-weight:700">→ {p["why"]}</p></div>' for p in CONTENT["partners"])
    return {"path":"/partners","eyebrow":"Partner Shops","h1":"Where ABI graduates work.",
        "sub":"Real shops. Real owners. Many of them — including the people in the chairs — started right here on the ABI clinic floor.",
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:10px">Your path to one of these chairs</h2><p class="lead" style="margin:0 auto 20px">Our Job Placement Office connects every graduate with our partner network and beyond.</p><a class="btn btn-primary" href="/job-placement">See job placement</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">Talk to admissions</a></div></section>'''}

def page_haircuts():
    h = CONTENT["haircut_clinic"]
    services = "".join(f'<span style="display:inline-block;margin:4px 6px 4px 0;padding:7px 14px;border:1px solid var(--line);border-radius:30px;font-size:.85rem;color:var(--mut)">{s}</span>' for s in h["services"])
    return {"path":"/haircuts","eyebrow":"Public Clinic","h1":f"{h['price']} student haircuts.",
        "sub":"Every cut supervised by a NY-licensed master barber. Walk-ins welcome — or book ahead.",
        "body": f'''<section><div class="wrap"><div class="grid-2">
<div><h2>Sit in the chair of a future master barber.</h2><p class="lead">{h["intro"]}</p>
<div class="contact-strip"><span><b style="color:var(--ink)">Book a chair</b> <a href="tel:{tel(h["booking_phone"])}">{h["booking_phone"]}</a></span><span><b style="color:var(--ink)">Hours</b> {h["hours"]}</span></div>
<p class="lead" style="font-size:.95rem">{h["what_to_expect"]}</p></div>
<div class="card"><div class="eyebrow-acc" style="margin-bottom:10px">Services</div><div>{services}</div></div></div></div></section>
<section><div class="wrap"><div class="grid">
<div class="card"><div class="eyebrow-acc">Manhattan Clinic</div><h3 style="font-size:1.2rem;margin:8px 0">48 W 39th St · NY 10018</h3><p style="color:var(--mut);font-size:.9rem">{h["hours"]}</p><a class="btn btn-primary" style="margin-top:12px" href="tel:{tel(h["booking_phone"])}">Book a chair</a></div>
<div class="card"><div class="eyebrow-acc">Bronx Clinic</div><h3 style="font-size:1.2rem;margin:8px 0">121 Westchester Sq · Bronx 10461</h3><p style="color:var(--mut);font-size:.9rem">{h["hours"]}</p><a class="btn btn-primary" style="margin-top:12px" href="tel:{tel(h["booking_phone"])}">Book a chair</a></div>
</div></div></section>'''}

def page_jobplacement():
    j = CONTENT["job_placement"]
    services = "".join(f"<li>{s}</li>" for s in j["services"])
    return {"path":"/job-placement","eyebrow":"Job Placement","h1":"From license to first chair.",
        "sub":j["intro"],
        "body": f'''<section><div class="wrap"><div class="grid-2"><div><h2>What our Job Placement Office does</h2><ul class="list-clean">{services}</ul></div><div class="card"><h3 style="font-size:1.3rem;margin-bottom:10px">The outcome</h3><p style="color:var(--mut);font-size:1rem;line-height:1.7">{j["outcomes"]}</p><a class="btn btn-primary" style="margin-top:18px" href="/partners">See partner shops →</a></div></div></div></section>
<section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact">Apply today</a> <a class="btn btn-ghost" href="/programs" style="margin-left:8px">See programs</a></div></section>'''}

def page_resources():
    r = CONTENT["resources"]
    def block(b):
        items = "".join(f"<li>{i}</li>" for i in b.get("items", []))
        intro = f'<p style="color:var(--mut);font-size:1rem;line-height:1.7;margin-bottom:14px">{b["intro"]}</p>' if b.get("intro") else ""
        outro = f'<p style="color:var(--mut);font-size:.92rem;margin-top:14px">{b["outro"]}</p>' if b.get("outro") else ""
        return f'<div class="card"><h3 style="font-size:1.25rem;margin-bottom:10px">{b["title"]}</h3>{intro}<ul class="list-clean">{items}</ul>{outro}</div>'
    cards = block(r["veterans"]) + block(r["accesvr"]) + block(r["licensing"]) + block(r["tools"])
    return {"path":"/resources","eyebrow":"Resources","h1":"Everything you need to start.",
        "sub":"Veterans benefits. ACCES-VR. NY State licensing. Tools and supplies. We've laid it all out so you know exactly what to do.",
        "body": f'''<section><div class="wrap"><div class="grid-2">{cards}</div></div></section>
<section><div class="wrap" style="text-align:center"><h2 style="margin-bottom:14px">Still have questions?</h2><a class="btn btn-primary" href="/contact">Talk to admissions</a> <a class="btn btn-ghost" href="/faq" style="margin-left:8px">Read FAQ</a></div></section>'''}

def page_faq():
    items = "".join(f'<details class="card" style="margin-bottom:11px"><summary style="cursor:pointer;font-weight:700;font-size:1.05rem;min-height:32px;list-style-position:outside">{q["q"]}</summary><p style="margin-top:12px;color:var(--mut);line-height:1.7">{q["a"]}</p></details>' for q in CONTENT["faqs"])
    return {"path":"/faq","eyebrow":"FAQ","h1":"Frequently asked questions.",
        "sub":"Tuition, schedule, licensing, GI Bill®, ACCES-VR, job placement, tools — everything you've wondered about ABI, answered.",
        "body": f'<section><div class="wrap" style="max-width:820px">{items}</div></section><section><div class="wrap" style="text-align:center"><p class="lead" style="margin:0 auto 18px">Still have questions? We answer the phone.</p><a class="btn btn-primary" href="tel:{tel(B["phone_manhattan"])}">Call admissions · {B["phone_manhattan"]}</a> <a class="btn btn-ghost" href="/contact" style="margin-left:8px">Send a message</a></div></section>'}

def page_contact():
    c1, c2 = CONTENT["campuses"]
    return {"path":"/contact","eyebrow":"Contact","h1":"Visit ABI.",
        "sub":"Two campuses across New York City. Call, walk in, or send a message — admissions responds same-day during business hours.",
        "body": f'''<section><div class="wrap"><div class="grid-2">
<div class="card"><div class="eyebrow-acc">Manhattan Campus</div><h3 style="font-size:1.3rem;margin:8px 0">{c1["name"]} — 48 West 39th Street</h3><p style="color:var(--mut);margin-bottom:8px">{c1["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c1["phone"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{c1["phone"]} (English)</a></p>
<p style="margin-bottom:6px"><a href="tel:{tel(B["phone_manhattan_es"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{B["phone_manhattan_es"]} (Español)</a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{c1["hours"]}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=48+West+39th+Street+New+York+NY">Get directions</a></div>
<div class="card"><div class="eyebrow-acc">Bronx Campus</div><h3 style="font-size:1.3rem;margin:8px 0">{c2["name"]} — 121 Westchester Square</h3><p style="color:var(--mut);margin-bottom:8px">{c2["address"]}</p>
<p style="margin-bottom:6px"><a href="tel:{tel(c2["phone"])}" style="color:var(--accent);font-weight:700;font-size:1.05rem">{c2["phone"]}</a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{c2["hours"]}</p>
<a class="btn btn-primary" href="https://www.google.com/maps?q=121+Westchester+Square+Bronx+NY">Get directions</a></div>
</div></div></section>
<section><div class="wrap"><div class="card" style="max-width:680px;margin:0 auto"><h2 style="margin-bottom:8px;font-size:1.6rem">Request information</h2><p style="color:var(--mut);margin-bottom:22px">Tell us a little about you and an admissions advisor will be in touch within one business day.</p><form action="mailto:{B["email"]}" method="post" enctype="text/plain" style="display:grid;gap:14px"><input required name="name" placeholder="Full name" class="input"><input required name="email" type="email" placeholder="Email" class="input"><input required name="phone" placeholder="Phone" class="input"><select name="program" class="input"><option>500-Hour Master Barber</option><option>50-Hour Refresher</option><option>3-Hour Contagious Diseases</option><option>540-Hour Bronx Master Barber</option></select><textarea name="message" placeholder="What would you like to know?" rows="4" class="input" style="resize:vertical"></textarea><button type="submit" class="btn btn-primary">Send to admissions</button></form><p style="color:var(--mut);font-size:.85rem;margin-top:18px;text-align:center">Or email <a href="mailto:{B["email"]}" style="color:var(--accent)">{B["email"]}</a> directly.</p></div></div></section>'''}

# ============== BUILD ONE SITE ==============
def build_site(site):
    slug = site["slug"]
    site_dir = ROOT / slug
    if not site_dir.exists():
        print(f"  SKIP (no folder): {slug}"); return
    # 1) Enhance index.html — full re-injection
    idx = site_dir / "index.html"
    html = idx.read_text(encoding="utf-8", errors="replace")
    # Strip prior injections
    html = strip_old_injection(html)
    # Fix paths
    html = fix_paths(html)
    # Replace title to neutral
    html = replace_title(html)
    # Replace nav-links to full menu
    html = replace_nav(html)
    # Re-inject head and body tail and bg video
    html = inject_head(html, site, "/")
    html = inject_bg_video(html, site)
    html = inject_body_tail(html, site, "/")
    html = html.replace('</head>', '<!-- ABI v3 INJECTED -->\n</head>', 1)
    idx.write_text(html, encoding="utf-8")

    # 2) Sub-pages
    page_renderers = [
        ("about.html",         page_about),
        ("programs.html",      page_programs),
        ("instructors.html",   page_instructors),
        ("gallery.html",       page_gallery),
        ("partners.html",      page_partners),
        ("haircuts.html",      page_haircuts),
        ("job-placement.html", page_jobplacement),
        ("resources.html",     page_resources),
        ("faq.html",           page_faq),
        ("contact.html",       page_contact),
    ]
    page_keys = {"about.html":"about","programs.html":"programs","instructors.html":"instructors","gallery.html":"gallery","partners.html":"partners","haircuts.html":"haircuts","job-placement.html":"jobplacement","resources.html":"resources","faq.html":"faq","contact.html":"contact"}
    for fname, fn in page_renderers:
        pdata = fn()
        (site_dir / fname).write_text(render_subpage(site, page_keys[fname], pdata), encoding="utf-8")

    # 3) Sitemap
    base = f"https://{site['vercel_name']}.vercel.app"
    paths = ["/", "/about", "/programs", "/instructors", "/gallery", "/partners", "/haircuts", "/job-placement", "/resources", "/faq", "/contact"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in paths:
        sm += f'  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq><priority>{"1.0" if p=="/" else "0.7"}</priority></url>\n'
    sm += '</urlset>\n'
    (site_dir / "sitemap.xml").write_text(sm)
    (site_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    vercel = {"cleanUrls": True, "trailingSlash": False, "headers": [{"source": "/(.*).html", "headers": [{"key": "Cache-Control", "value": "public, max-age=300, must-revalidate"}]}]}
    (site_dir / "vercel.json").write_text(json.dumps(vercel, indent=2))
    print(f"  OK {slug}: index neutralized + 10 subpages + sitemap + robots + vercel.json")

if __name__ == "__main__":
    print(f"Building 10 ABI sites · neutral branding · 11 pages each · CDN at {CDN}")
    for s in SITES:
        build_site(s)
    print("Done.")
