"""ABI 10-Websites builder. Uses absolute CDN URLs (abi-assets.vercel.app) — no per-site bundling."""
from __future__ import annotations
import json, os, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CDN = "https://abi-assets.vercel.app"
CONTENT = json.loads((ROOT / "_content" / "content.json").read_text())
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]

def tel(p):
    return p.replace("(","").replace(")","").replace(" ","").replace("-","")

# Universal SEO head injection
def head_meta(site, page_path="/", page_title=None, page_desc=None):
    title = page_title or f"{site['name']} · American Barber Institute (ABI) · NYC's Dedicated Barber School"
    desc = page_desc or site["description"]
    url = f"https://{site['vercel_name']}.vercel.app{page_path}"
    image_url = f"{CDN}/logos/{site['logo']}"
    return f'''<meta name="description" content="{desc}">
<meta name="keywords" content="barber school nyc, american barber institute, barbering license new york, abi, master barber program, barber training, {site['name'].lower()}, barber academy, gi bill barber school, weekend barber school">
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
        "description": site["description"],
        "telephone": CONTENT["brand"]["phone_manhattan"],
        "email": CONTENT["brand"]["email"],
        "sameAs": [s["href"] for s in CONTENT["social"]],
        "address": [
            {"@type":"PostalAddress","streetAddress":"48 West 39th Street","addressLocality":"New York","addressRegion":"NY","postalCode":"10018","addressCountry":"US"},
            {"@type":"PostalAddress","streetAddress":"121 Westchester Square","addressLocality":"Bronx","addressRegion":"NY","postalCode":"10461","addressCountry":"US"},
        ],
        "aggregateRating": {"@type":"AggregateRating","ratingValue":"4.3","ratingCount":"100"},
    }
    out = f'<script type="application/ld+json">{json.dumps(school)}</script>'
    if include_faq:
        faq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type":"Question","name":q["q"],"acceptedAnswer":{"@type":"Answer","text":q["a"]}}
                for q in CONTENT["faqs"]
            ],
        }
        out += f'\n<script type="application/ld+json">{json.dumps(faq)}</script>'
    return out

# Universal responsive overlay (mobile-first)
def responsive_overlay(site):
    return f'''<style>
/* ===== ABI v2 mobile-first responsive overlay ===== */
:root {{ --abi-touch: 44px; --abi-accent: {site["primary_color"]}; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{ overflow-x: hidden; }}
img {{ max-width: 100%; height: auto; display: block; }}
video {{ max-width: 100%; height: auto; }}
button, .btn, a.btn, .nav-cta, a.nav-cta {{ min-height: var(--abi-touch); display: inline-flex; align-items: center; justify-content: center; }}
.burger {{ width: var(--abi-touch); height: var(--abi-touch); display: none; flex-direction: column; gap: 5px; cursor: pointer; align-items: center; justify-content: center; background: transparent; border: 0; padding: 0; }}
.burger span {{ width: 26px; height: 2px; background: currentColor; transition: .2s; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}
@media (max-width: 860px) {{
  .nav-links {{ position: fixed !important; inset: 70px 0 auto 0 !important; flex-direction: column !important; align-items: stretch !important; gap: 0 !important; background: rgba(8,8,14,.97) !important; backdrop-filter: blur(20px); padding: 12px 18px 22px !important; transform: translateY(-110%); transition: transform .28s ease; box-shadow: 0 18px 36px rgba(0,0,0,.45); z-index: 24; display: flex !important; }}
  .nav-links a {{ padding: 16px 6px !important; border-bottom: 1px solid rgba(255,255,255,.07); font-size: 1rem !important; min-height: var(--abi-touch); display: flex !important; align-items: center; }}
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
}}
@media (max-width: 480px) {{
  .wrap, .container {{ padding-left: 14px !important; padding-right: 14px !important; }}
  .hero h1, h1 {{ font-size: clamp(1.9rem, 9vw, 2.8rem) !important; }}
}}
@media (min-width: 861px) {{ .burger {{ display: none !important; }} }}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: .001s !important; animation-iteration-count: 1 !important; transition-duration: .001s !important; }}
}}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .14; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .08; }} }}
.hero-logo-mark {{ display: inline-block; max-width: 84px; max-height: 84px; border-radius: 20px; box-shadow: 0 14px 40px rgba(0,0,0,.45); vertical-align: middle; margin-right: 14px; }}
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
    var navwrap = document.querySelector('header .nav') || document.querySelector('header > div') || document.querySelector('header');
    if (navwrap) navwrap.appendChild(burger);
  }
  function close(){ nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); }
  function toggle(){ var open = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', open ? 'true' : 'false'); }
  burger.addEventListener('click', toggle);
  nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', close); });
  document.addEventListener('keydown', function(e){ if (e.key==='Escape') close(); });
})();
</script>'''

def fix_paths(html):
    # ../assets/X/Y  →  CDN/X/Y
    html = re.sub(r'(["\(\'])\.\./assets/', lambda m: m.group(1) + CDN + '/', html)
    return html

def inject_head(html, site):
    extras = head_meta(site) + "\n" + jsonld(site)
    return re.sub(r'</title>', lambda m: m.group(0) + '\n' + extras, html, count=1)

def inject_body_tail(html, site):
    overlay = responsive_overlay(site) + "\n" + hamburger_js()
    return html.replace('</body>', overlay + '\n</body>', 1)

# Inject nav links to subpages (programs/gallery/faq/contact) into existing nav
def inject_nav_subpages(html):
    # Find existing .nav-links and inject sub-page links at the start
    sub_links = '<a href="/programs.html">Programs</a><a href="/gallery.html">Gallery</a><a href="/faq.html">FAQ</a><a href="/contact.html">Contact</a>'
    return re.sub(
        r'(<nav class="nav-links">)',
        lambda m: m.group(0) + sub_links,
        html,
        count=1,
    )

# Inject background video element near top of body, using CDN URL
def inject_bg_video(html, site):
    if 'class="bg-video"' in html:
        return html
    vid = f'<video class="bg-video" autoplay muted loop playsinline aria-hidden="true" poster="{CDN}/logos/{site["logo"]}"><source src="{CDN}/videos/{site["video"]}" type="video/mp4"></video>'
    return html.replace('<body>', '<body>\n' + vid, 1)

# Sub-page template — self-contained
SUBPAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · {site_name} · American Barber Institute</title>
{head_meta}
{jsonld}
<style>
:root {{ --accent: {accent}; --bg: #07080d; --bg2: #0d1018; --ink: #e9ecff; --mut: #8b91b8; --line: rgba(255,255,255,.08); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }}
body {{ background: var(--bg); color: var(--ink); font-family: -apple-system, 'Segoe UI', system-ui, sans-serif; line-height: 1.6; overflow-x: hidden; min-height: 100vh; }}
a {{ color: inherit; text-decoration: none; }}
img {{ max-width: 100%; height: auto; display: block; }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 2; }}
.bg-video {{ position: fixed; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: .14; pointer-events: none; }}
@media (max-width: 768px) {{ .bg-video {{ opacity: .08; }} }}
.bg-overlay {{ position: fixed; inset: 0; background: radial-gradient(ellipse at center, transparent 0, rgba(0,0,0,.45) 70%, var(--bg) 100%); z-index: 1; pointer-events: none; }}
header {{ position: sticky; top: 0; z-index: 30; background: rgba(7,8,13,.85); backdrop-filter: blur(18px); border-bottom: 1px solid var(--line); }}
.nav {{ display: flex; align-items: center; justify-content: space-between; height: 70px; max-width: 1180px; margin: 0 auto; padding: 0 24px; gap: 16px; }}
.logo {{ display: flex; align-items: center; gap: 12px; font-weight: 900; letter-spacing: .04em; font-size: 1rem; }}
.logo img {{ width: 38px; height: 38px; border-radius: 10px; object-fit: cover; }}
.logo b {{ color: var(--accent); }}
.nav-links {{ display: flex; gap: 24px; font-size: .9rem; font-weight: 600; color: var(--mut); }}
.nav-links a {{ transition: .2s; padding: 6px 2px; }}
.nav-links a:hover, .nav-links a.active {{ color: var(--accent); }}
.nav-cta {{ padding: 10px 22px; border: 1px solid var(--accent); border-radius: 40px; color: var(--accent); font-weight: 700; font-size: .82rem; min-height: 44px; display: inline-flex; align-items: center; transition: .2s; }}
.nav-cta:hover {{ background: var(--accent); color: var(--bg); }}
.burger {{ display: none; flex-direction: column; gap: 5px; cursor: pointer; width: 44px; height: 44px; align-items: center; justify-content: center; background: transparent; border: 0; color: var(--accent); }}
.burger span {{ width: 26px; height: 2px; background: currentColor; transition: .2s; }}
.burger[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.burger[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
.burger[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}
.subpage-hero {{ padding: 100px 0 60px; text-align: center; position: relative; }}
.eyebrow {{ display: inline-block; padding: 6px 14px; border: 1px solid var(--line); border-radius: 30px; font-size: .68rem; letter-spacing: .3em; text-transform: uppercase; color: var(--accent); }}
.subpage-hero h1 {{ font-family: 'Arial Black', system-ui; font-size: clamp(2.1rem, 6.4vw, 4rem); margin: 22px 0 14px; line-height: 1.05; letter-spacing: -.02em; }}
.subpage-hero p.sub {{ max-width: 680px; margin: 0 auto; color: var(--mut); font-size: 1.06rem; }}
section {{ padding: 60px 0; position: relative; z-index: 2; }}
.card {{ background: rgba(20,20,30,.55); border: 1px solid var(--line); border-radius: 18px; padding: 28px; backdrop-filter: blur(8px); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
.btn {{ display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 28px; border-radius: 40px; font-weight: 700; font-size: .92rem; min-height: 48px; transition: .25s; cursor: pointer; border: 0; }}
.btn-primary {{ background: var(--accent); color: var(--bg); }}
.btn-primary:hover {{ filter: brightness(1.08); transform: translateY(-2px); box-shadow: 0 12px 30px rgba(0,0,0,.4); }}
.btn-ghost {{ border: 1px solid var(--line); color: var(--ink); background: transparent; }}
.input {{ background: rgba(20,20,30,.55); border: 1px solid var(--line); border-radius: 12px; padding: 14px; color: var(--ink); font-size: 1rem; font-family: inherit; }}
footer {{ padding: 60px 0 40px; border-top: 1px solid var(--line); margin-top: 60px; color: var(--mut); font-size: .9rem; position: relative; z-index: 2; background: rgba(0,0,0,.4); }}
.footer-grid {{ display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 32px; margin-bottom: 30px; }}
.footer-grid h4 {{ font-size: .85rem; text-transform: uppercase; letter-spacing: .15em; color: var(--ink); margin-bottom: 12px; }}
.footer-grid a {{ display: block; padding: 4px 0; color: var(--mut); }}
.footer-grid a:hover {{ color: var(--accent); }}
.footer-bottom {{ display: flex; justify-content: space-between; padding-top: 24px; border-top: 1px solid var(--line); flex-wrap: wrap; gap: 12px; font-size: .8rem; }}
@media (max-width: 860px) {{
  .nav-links {{ position: fixed; inset: 70px 0 auto 0; flex-direction: column; align-items: stretch; background: rgba(7,8,13,.97); backdrop-filter: blur(20px); padding: 12px 22px 22px; transform: translateY(-110%); transition: transform .28s; box-shadow: 0 18px 36px rgba(0,0,0,.45); z-index: 24; gap: 0; }}
  .nav-links a {{ padding: 16px 4px; border-bottom: 1px solid rgba(255,255,255,.07); font-size: 1rem; min-height: 44px; display: flex; align-items: center; }}
  .nav-links a:last-of-type {{ border-bottom: 0; }}
  .nav-links.open {{ transform: translateY(0); }}
  .burger {{ display: inline-flex; }}
  .nav-cta {{ display: none; }}
  .footer-grid {{ grid-template-columns: 1fr 1fr; }}
  .subpage-hero {{ padding: 70px 0 40px; }}
}}
@media (max-width: 480px) {{ .footer-grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<video class="bg-video" autoplay muted loop playsinline poster="{cdn}/logos/{logo}" aria-hidden="true"><source src="{cdn}/videos/{video}" type="video/mp4"></video>
<div class="bg-overlay"></div>
<header>
  <div class="nav">
    <a class="logo" href="/"><img src="{cdn}/logos/{logo}" alt="ABI">ABI · <b>{site_name}</b></a>
    <nav class="nav-links">
      <a href="/">Home</a>
      <a href="/programs.html" class="{nav_programs}">Programs</a>
      <a href="/gallery.html" class="{nav_gallery}">Gallery</a>
      <a href="/faq.html" class="{nav_faq}">FAQ</a>
      <a href="/contact.html" class="{nav_contact}">Contact</a>
    </nav>
    <a class="nav-cta" href="tel:{phone_tel}">Apply Now</a>
    <button class="burger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>
<section class="subpage-hero">
  <div class="wrap">
    <div class="eyebrow">{site_theme}</div>
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
        <p style="font-size:.85rem">Licensed by NY State Department of Education. GI Bill® accepted.</p>
      </div>
      <div>
        <h4>Sitemap</h4>
        <a href="/">Home</a>
        <a href="/programs.html">Programs</a>
        <a href="/gallery.html">Gallery</a>
        <a href="/faq.html">FAQ</a>
        <a href="/contact.html">Contact</a>
      </div>
      <div>
        <h4>Manhattan</h4>
        <a href="tel:{phone_man_tel}">{phone_man}</a>
        <p>48 W 39th St · NY 10018</p>
      </div>
      <div>
        <h4>Bronx</h4>
        <a href="tel:{phone_brx_tel}">{phone_brx}</a>
        <p>121 Westchester Sq · Bronx 10461</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 American Barber Institute · {site_name} edition</span>
      <span>admission@abi.edu</span>
    </div>
  </div>
</footer>
<script>
(function(){{
  var nav = document.querySelector('.nav-links');
  var b = document.querySelector('.burger');
  if (!b || !nav) return;
  b.addEventListener('click', function(){{ var open = nav.classList.toggle('open'); b.setAttribute('aria-expanded', open ? 'true' : 'false'); }});
  nav.querySelectorAll('a').forEach(function(a){{ a.addEventListener('click', function(){{ nav.classList.remove('open'); b.setAttribute('aria-expanded','false'); }}); }});
}})();
</script>
</body>
</html>
'''

def render_subpage(site, page, pdata):
    nav_class = {p: ("" if p != page else "active") for p in ["programs","gallery","faq","contact"]}
    head_extras = head_meta(site, page_path=f"/{page}.html", page_title=pdata["title"], page_desc=pdata["sub"])
    jl = jsonld(site, include_faq=(page == "faq"))
    return SUBPAGE.format(
        site_name=site["name"], site_theme=site["theme_word"],
        title=pdata["title"], accent=site["primary_color"],
        h1=pdata["h1"], sub=pdata["sub"], body=pdata["body"],
        head_meta=head_extras, jsonld=jl,
        nav_programs=nav_class["programs"], nav_gallery=nav_class["gallery"],
        nav_faq=nav_class["faq"], nav_contact=nav_class["contact"],
        phone_tel=tel(CONTENT["brand"]["phone_manhattan"]),
        phone_man=CONTENT["brand"]["phone_manhattan"], phone_man_tel=tel(CONTENT["brand"]["phone_manhattan"]),
        phone_brx=CONTENT["brand"]["phone_bronx"], phone_brx_tel=tel(CONTENT["brand"]["phone_bronx"]),
        cdn=CDN, logo=site["logo"], video=site["video"],
    )

def page_programs():
    rows = [f'<div class="card"><div style="color:var(--accent);font-size:.7rem;letter-spacing:.25em;text-transform:uppercase;font-weight:800">{p["campus"]} · {p["duration"]}</div><h3 style="margin:10px 0 8px;font-size:1.3rem">{p["name"]}</h3><div style="font-size:1.2rem;font-weight:800;color:var(--accent);margin-bottom:10px">{p["price"]}</div><p style="color:var(--mut);font-size:.95rem">{p["summary"]}</p></div>' for p in CONTENT["programs"]]
    sched = [f'<div class="card"><div style="color:var(--accent);font-size:.7rem;letter-spacing:.25em;text-transform:uppercase;font-weight:800">{s["label"]}</div><h3 style="margin:10px 0 8px;font-size:1.1rem">{s["days"]} · {s["time"]}</h3><div style="font-size:1.5rem;font-weight:800;color:var(--accent);margin:10px 0 6px">{s["tuition"]}</div><p style="color:var(--mut);font-size:.9rem">{s["plan"]}</p></div>' for s in CONTENT["schedules"]]
    return {
        "title": "Programs & Tuition",
        "h1": "Programs & Tuition",
        "sub": "State-licensed barbering programs in Manhattan and the Bronx. Three tracks: Morning, Afternoon, Weekend. Pick the pace that fits your life.",
        "body": f'<section><div class="wrap"><div class="eyebrow" style="margin-bottom:16px">Programs</div><h2 style="font-size:clamp(1.6rem,4vw,2.6rem);margin-bottom:24px">Choose your path</h2><div class="grid">{"".join(rows)}</div></div></section><section><div class="wrap"><div class="eyebrow" style="margin-bottom:16px">Schedule &amp; Tuition</div><h2 style="font-size:clamp(1.6rem,4vw,2.6rem);margin-bottom:24px">Three flexible schedules</h2><div class="grid">{"".join(sched)}</div><p style="margin-top:24px;color:var(--mut);font-size:.92rem">Veterans &amp; GI Bill® benefits accepted (ACCES-VR, Post-9/11 GI Bill®, VA). <a href="/contact.html" style="color:var(--accent);text-decoration:underline">Talk to admissions →</a></p></div></section><section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact.html">Apply Today</a> <a class="btn btn-ghost" href="/faq.html" style="margin-left:8px">Read FAQ</a></div></section>',
    }

def page_gallery():
    # use all gallery images from /assets/img/
    imgs = sorted({f for f in os.listdir(ROOT / "assets" / "img") if f.lower().endswith(('.jpeg','.jpg','.png'))})[:30]
    tiles = [f'<div class="card" style="padding:0;overflow:hidden;background:rgba(0,0,0,.3)"><img src="{CDN}/img/{f}" loading="lazy" alt="ABI student work" style="aspect-ratio:4/3;object-fit:cover;width:100%;border-radius:18px"></div>' for f in imgs]
    return {
        "title": "Gallery",
        "h1": "On the floor.",
        "sub": "Real students. Real chairs. Real fades. A glimpse inside the American Barber Institute clinic floor, cohorts, and graduation moments.",
        "body": f'<section><div class="wrap"><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">{"".join(tiles)}</div></div></section><section><div class="wrap" style="text-align:center"><a class="btn btn-primary" href="/contact.html">Visit Our Campus</a></div></section>',
    }

def page_faq():
    items = [f'<details class="card" style="margin-bottom:11px"><summary style="cursor:pointer;font-weight:700;font-size:1.05rem;min-height:32px;list-style-position:outside">{q["q"]}</summary><p style="margin-top:12px;color:var(--mut);line-height:1.7">{q["a"]}</p></details>' for q in CONTENT["faqs"]]
    return {
        "title": "Frequently Asked Questions",
        "h1": "Frequently Asked",
        "sub": "Tuition, schedule, licensing, GI Bill, job placement — everything you've wondered about the American Barber Institute, answered.",
        "body": f'<section><div class="wrap" style="max-width:820px">{"".join(items)}</div></section><section><div class="wrap" style="text-align:center"><p style="color:var(--mut);margin-bottom:22px">Still have questions? We answer the phone.</p><a class="btn btn-primary" href="tel:{tel(CONTENT["brand"]["phone_manhattan"])}">Call Admissions</a> <a class="btn btn-ghost" href="/contact.html" style="margin-left:8px">Send Message</a></div></section>',
    }

def page_contact():
    c1, c2 = CONTENT["campuses"]
    return {
        "title": "Contact & Locations",
        "h1": "Visit ABI.",
        "sub": "Two campuses across New York City. Walk in, call, or send a message — our admissions team responds same-day during business hours.",
        "body": f'''<section><div class="wrap"><div class="grid">
<div class="card"><div class="eyebrow" style="margin-bottom:12px">Manhattan Campus</div><h3 style="font-size:1.4rem;margin-bottom:10px">{c1["name"]}</h3><p style="color:var(--mut);margin-bottom:6px">{c1["address"]}</p><p style="margin-bottom:6px"><a href="tel:{tel(c1["phone"])}" style="color:var(--accent);font-weight:700">{c1["phone"]}</a></p><p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{c1["hours"]}</p><a class="btn btn-primary" href="https://www.google.com/maps?q=48+West+39th+Street+New+York+NY">Get Directions</a></div>
<div class="card"><div class="eyebrow" style="margin-bottom:12px">Bronx Campus</div><h3 style="font-size:1.4rem;margin-bottom:10px">{c2["name"]}</h3><p style="color:var(--mut);margin-bottom:6px">{c2["address"]}</p><p style="margin-bottom:6px"><a href="tel:{tel(c2["phone"])}" style="color:var(--accent);font-weight:700">{c2["phone"]}</a></p><p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{c2["hours"]}</p><a class="btn btn-primary" href="https://www.google.com/maps?q=121+Westchester+Square+Bronx+NY">Get Directions</a></div>
</div></div></section>
<section><div class="wrap"><div class="card" style="max-width:680px;margin:0 auto"><h2 style="margin-bottom:8px;font-size:1.6rem">Request information</h2><p style="color:var(--mut);margin-bottom:22px">Tell us a little about you and we will be in touch within one business day.</p><form action="mailto:{CONTENT["brand"]["email"]}" method="post" enctype="text/plain" style="display:grid;gap:14px"><input required name="name" placeholder="Full name" class="input"><input required name="email" type="email" placeholder="Email" class="input"><input required name="phone" placeholder="Phone" class="input"><select name="program" class="input"><option>500-Hour Master Barber</option><option>50-Hour Refresher</option><option>3-Hour Contagious Diseases</option><option>540-Hour Bronx Master Barber</option></select><textarea name="message" placeholder="What would you like to know?" rows="4" class="input" style="resize:vertical"></textarea><button type="submit" class="btn btn-primary">Send to Admissions</button></form></div></div></section>''',
    }

def build_site(site):
    slug = site["slug"]
    site_dir = ROOT / slug
    if not site_dir.exists():
        print(f"  SKIP (no folder): {slug}")
        return
    # 1. enhance index.html (only if not already enhanced)
    idx = site_dir / "index.html"
    html = idx.read_text(encoding="utf-8", errors="replace")
    if "<!-- ABI v2 SEO INJECTED -->" not in html:
        html = fix_paths(html)
        html = inject_head(html, site)
        html = inject_nav_subpages(html)
        html = inject_bg_video(html, site)
        html = inject_body_tail(html, site)
        html = html.replace('</head>', '<!-- ABI v2 SEO INJECTED -->\n</head>', 1)
    idx.write_text(html, encoding="utf-8")

    # 2. sub-pages
    pages = {
        "programs.html": page_programs(),
        "gallery.html": page_gallery(),
        "faq.html": page_faq(),
        "contact.html": page_contact(),
    }
    for fname, pdata in pages.items():
        page_name = fname.replace(".html","")
        (site_dir / fname).write_text(render_subpage(site, page_name, pdata), encoding="utf-8")

    # 3. sitemap.xml
    base = f"https://{site['vercel_name']}.vercel.app"
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for path in ["/", "/programs.html", "/gallery.html", "/faq.html", "/contact.html"]:
        sm += f'  <url><loc>{base}{path}</loc><changefreq>weekly</changefreq><priority>{"1.0" if path=="/" else "0.8"}</priority></url>\n'
    sm += '</urlset>\n'
    (site_dir / "sitemap.xml").write_text(sm)

    # 4. robots.txt
    (site_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

    # 5. vercel.json (clean URLs)
    vercel = {
        "cleanUrls": True,
        "trailingSlash": False,
        "headers": [
            {"source": "/(.*).html", "headers": [{"key": "Cache-Control", "value": "public, max-age=300, must-revalidate"}]}
        ],
    }
    (site_dir / "vercel.json").write_text(json.dumps(vercel, indent=2))

    print(f"  OK {slug}: index enhanced + 4 subpages + sitemap + robots + vercel.json")

if __name__ == "__main__":
    print(f"Building 10 ABI sites with CDN at {CDN} ...")
    for s in SITES:
        build_site(s)
    print("Done.")
