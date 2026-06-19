"""ABI shared rendering engine (v6).

One mobile-first responsive system that generates ALL 11 pages — INCLUDING the home
page — from templates. No more surgical injection into scraped HTML (that was the root
cause of the home page not being mobile-responsive).

Per-site build files (<slug>/build.py) import this engine, pass their own design tokens
+ site meta + optional extra CSS, and call build_site(). Content is single-sourced from
_content/content.json (the authoritative source of truth).
"""
from __future__ import annotations
import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_ASSETS = ROOT / "assets"
ASSET_BASE = "https://assets-lilac-five.vercel.app"  # shared media host (deployed once)

CONTENT = json.loads((ROOT / "_content" / "content.json").read_text())
B, UI, NAV = CONTENT["brand"], CONTENT["ui"], CONTENT["nav"]


def tel(p: str) -> str:
    return p.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")


def bi(d) -> str:
    """Wrap a {"en","es"} dict into bilingual spans; pass strings through.
    NEVER use inside an HTML attribute (placeholder/alt/title/aria-*/value) — the
    spans leak as literal text and break the attribute. Use bt() for attributes."""
    if isinstance(d, str):
        return d
    return f'<span class="lang-en">{d.get("en","")}</span><span class="lang-es">{d.get("es","")}</span>'


def bt(d) -> str:
    """Plain-text bilingual for ATTRIBUTE contexts (placeholder/alt/title/aria-*).
    Lang spans cannot live in attributes, so collapse to a single string: English,
    plus the Spanish in parentheses where both differ and it still reads cleanly."""
    if isinstance(d, str):
        return d
    en, es = d.get("en", ""), d.get("es", "")
    if not es or es == en:
        return en
    return f"{en} / {es}"


# Nav order mirrors the reference site: About, Programs, Resources, FAQs, Jobs, Haircuts,
# Gallery, Contact — plus Partners + Instructors (kept per request).
NAV_ITEMS = [
    ("home", "/"), ("about", "/about"), ("programs", "/programs"), ("resources", "/resources"),
    ("faq", "/faq"), ("jobplacement", "/job-placement"), ("haircuts", "/haircuts"),
    ("gallery", "/gallery"), ("blog", "/blog"), ("partners", "/partners"),
    ("instructors", "/instructors"), ("contact", "/contact"),
]
PAGE_ORDER = [k for k, _ in NAV_ITEMS]

BRAND_TITLE = "American Barber Institute · New York's Dedicated Barber School"
BRAND_DESC_EN = ("American Barber Institute (ABI) — New York's only dedicated barber school. "
                 "NY State licensed. 30+ years, 10,000+ graduates. GI Bill® accepted. Manhattan & Bronx campuses.")
PAGE_TITLES = {
    "/": BRAND_TITLE,
    "/about": "About · American Barber Institute · NYC",
    "/programs": "Barber Programs & Tuition · American Barber Institute",
    "/resources": "Student Resources · Veterans · ACCES-VR · ABI",
    "/faq": "Frequently Asked Questions · American Barber Institute",
    "/job-placement": "Barber Job Placement · American Barber Institute NYC",
    "/haircuts": "Student Haircuts · American Barber Institute · NYC",
    "/gallery": "Gallery · American Barber Institute",
    "/blog": "ABI Journal · Barbering Tips, News & Career Advice · American Barber Institute",
    "/partners": "Partner Shops · American Barber Institute",
    "/instructors": "Instructors · American Barber Institute",
    "/contact": "Contact · American Barber Institute · NYC",
}

# ---- shared media pools (served from the asset host) ----
GALLERY_FILES = sorted(
    [f for f in os.listdir(SRC_ASSETS / "img") if f.lower().endswith((".jpeg", ".jpg", ".png"))]
) if (SRC_ASSETS / "img").exists() else []
PARTNER_IMGS = (GALLERY_FILES[:6] if len(GALLERY_FILES) >= 6 else GALLERY_FILES * 2) or ["logo.jpeg"]

SHOWCASE_DIR = SRC_ASSETS / "showcase"
def _ls(sub):
    d = SHOWCASE_DIR / sub
    return sorted([f for f in os.listdir(d) if not f.startswith(".")]) if d.exists() else []
SHOWCASE_VID = _ls("vid")
_IMG_ALL = _ls("img")
SHOWCASE_IMG = [f for f in _IMG_ALL if f and f[0].isalpha()] + [f for f in _IMG_ALL if f and not f[0].isalpha()]


def pick(pool, start, count):
    return [pool[(start + i) % len(pool)] for i in range(count)] if pool else []


def caption(fn):
    s = re.sub(r"\.(mp4|jpe?g|png)$", "", fn, flags=re.I)
    s = re.sub(r"-2$", "", s)
    if re.search(r"whatsapp|img-\d|^\d", s):
        return "American Barber Institute"
    s = s.replace("client-s", "client's").replace("-", " ").strip()
    return s[:1].upper() + s[1:] if s else "American Barber Institute"


MEDIA_HEADINGS = {
    "_default": {"eyb": {"en": "Inside ABI", "es": "Dentro de ABI"}, "h2": {"en": "Life on the clinic floor", "es": "La vida en el piso clínico"}, "p": {"en": "Real students, real chairs, real cuts — a look inside American Barber Institute.", "es": "Estudiantes reales, sillas reales, cortes reales — un vistazo dentro de American Barber Institute."}},
    "home": {"eyb": {"en": "Inside ABI", "es": "Dentro de ABI"}, "h2": {"en": "This is the floor", "es": "Este es el piso"}, "p": {"en": "Step inside our Manhattan and Bronx clinics — where future master barbers train every day.", "es": "Entra a nuestras clínicas de Manhattan y el Bronx — donde los futuros maestros barberos entrenan cada día."}},
    "about": {"eyb": {"en": "Our people", "es": "Nuestra gente"}, "h2": {"en": "Three decades, one craft", "es": "Tres décadas, un oficio"}, "p": {"en": "The faces, the chairs, and the community behind 10,000+ graduates.", "es": "Los rostros, las sillas y la comunidad detrás de más de 10,000 graduados."}},
    "programs": {"eyb": {"en": "In training", "es": "En entrenamiento"}, "h2": {"en": "What your day looks like", "es": "Cómo es tu día"}, "p": {"en": "Hands-on from week one — fades, beard work, straight-razor, and the full board-exam path.", "es": "Práctico desde la primera semana — degradados, barba, navaja y el camino completo al examen."}},
    "instructors": {"eyb": {"en": "Masters at work", "es": "Maestros en acción"}, "h2": {"en": "Learn beside the best", "es": "Aprende junto a los mejores"}, "p": {"en": "Master barbers on the floor with you, every cut, every day.", "es": "Maestros barberos en el piso contigo, en cada corte, cada día."}},
    "gallery": {"eyb": {"en": "More from the shop", "es": "Más de la barbería"}, "h2": {"en": "In motion", "es": "En movimiento"}, "p": {"en": "Clips and frames from the clinic, the classroom, and graduation day.", "es": "Clips e imágenes de la clínica, el aula y el día de graduación."}},
    "blog": {"eyb": {"en": "From the floor", "es": "Desde el piso"}, "h2": {"en": "Where the stories happen", "es": "Donde nacen las historias"}, "p": {"en": "The clinic, the chairs, and the careers our articles are written about.", "es": "La clínica, los sillones y las carreras sobre las que escribimos."}},
    "partners": {"eyb": {"en": "The network", "es": "La red"}, "h2": {"en": "Where the craft leads", "es": "A dónde lleva el oficio"}, "p": {"en": "From our chairs to shops across the five boroughs and beyond.", "es": "De nuestras sillas a barberías en los cinco condados y más allá."}},
    "haircuts": {"eyb": {"en": "See a cut in action", "es": "Mira un corte en acción"}, "h2": {"en": "Fresh cuts, real students", "es": "Cortes frescos, estudiantes reales"}, "p": {"en": "Every cut in our student clinic is supervised by a NY-licensed instructor.", "es": "Cada corte en nuestra clínica estudiantil es supervisado por un instructor licenciado de NY."}},
    "jobplacement": {"eyb": {"en": "Chair to career", "es": "De la silla a la carrera"}, "h2": {"en": "Built to work", "es": "Listos para trabajar"}, "p": {"en": "Graduates step straight onto working floors across New York.", "es": "Los graduados pasan directo a pisos de trabajo en Nueva York."}},
    "resources": {"eyb": {"en": "Real support", "es": "Apoyo real"}, "h2": {"en": "We've got your back", "es": "Te respaldamos"}, "p": {"en": "Veterans, ACCES-VR, licensing — and a community around you.", "es": "Veteranos, ACCES-VR, licencias — y una comunidad a tu alrededor."}},
    "faq": {"eyb": {"en": "A look inside", "es": "Un vistazo adentro"}, "h2": {"en": "Still curious?", "es": "¿Aún con curiosidad?"}, "p": {"en": "See the floor for yourself before you ask.", "es": "Mira el piso por ti mismo antes de preguntar."}},
    "contact": {"eyb": {"en": "Come see us", "es": "Ven a vernos"}, "h2": {"en": "Two campuses, one craft", "es": "Dos campus, un oficio"}, "p": {"en": "Walk in, watch a cut, and meet the team in Manhattan or the Bronx.", "es": "Ven, mira un corte y conoce al equipo en Manhattan o el Bronx."}},
}


def media_band(t, site_index, page_key, n_vid=1, n_img=4):
    if not SHOWCASE_VID and not SHOWCASE_IMG:
        return ""
    style = t.get("media_style", "fade")
    pi = PAGE_ORDER.index(page_key) if page_key in PAGE_ORDER else 0
    vids = pick(SHOWCASE_VID, site_index * 3 + pi * 2, n_vid)
    imgs = pick(SHOWCASE_IMG, site_index * 5 + pi * 3 + 2, n_img)
    h = MEDIA_HEADINGS.get(page_key, MEDIA_HEADINGS["_default"])
    items, mx = [], max(len(vids), len(imgs))
    for k in range(mx):
        if k < len(vids):
            items.append(("vid", vids[k]))
        if k < len(imgs):
            items.append(("img", imgs[k]))
    tiles = []
    for kind, fn in items:
        cap = caption(fn)
        if kind == "vid":
            tiles.append(f'<figure class="m-tile m-vid"><video class="m-media" muted loop playsinline preload="none" data-src="/assets/showcase/vid/{fn}" poster="/assets/logo.jpeg" aria-label="{cap}"></video><figcaption class="m-cap">{cap}</figcaption></figure>')
        else:
            tiles.append(f'<figure class="m-tile m-img"><img class="m-media" loading="lazy" decoding="async" src="/assets/showcase/img/{fn}" alt="{cap}"><figcaption class="m-cap">{cap}</figcaption></figure>')
    return (f'<section class="media-band ms-{style}"><div class="container">'
            f'<div class="m-head"><div class="eyb">{bi(h["eyb"])}</div><h2>{bi(h["h2"])}</h2><p>{bi(h["p"])}</p></div>'
            f'<div class="m-grid">{"".join(tiles)}</div></div></section>')


# ===================== CSS =====================
# The bulk of the CSS is theme-agnostic and references CSS custom properties only, so it is a
# shared constant string (no per-site substitution, no f-string brace-doubling). Per-site theming
# happens entirely through :root variables + the body's hfx-* class. Per-site EXTRA css is appended.

def root_vars(t):
    return (
        ":root{"
        f"--bg:{t['bg']};--bg2:{t['bg2']};--ink:{t['ink']};--mut:{t['mut']};"
        f"--accent:{t['accent']};--accent2:{t.get('accent2', t['accent'])};--accent3:{t.get('accent3', t['accent'])};"
        f"--line:{t['line']};--glass:{t['glass']};"
        f"--card-r:{t['card_radius']};--btn-r:{t['button_radius']};"
        f"--font-body:{t['body_font']};--font-head:{t['heading_font']};"
        f"--head-ls:{t.get('heading_ls', '0')};--head-lh:{t.get('heading_lh', '1.05')};"
        f"--ribbon-bg:{t.get('ribbon_bg', 'var(--accent)')};--ribbon-color:{t.get('ribbon_color', '#fff')};"
        "--touch:48px;--safe-top:env(safe-area-inset-top);--safe-bottom:env(safe-area-inset-bottom);"
        "}"
    )

CSS_BASE = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--ink);font-family:var(--font-body);line-height:1.65;font-size:16px;overflow-x:hidden;width:100%;max-width:100%;min-height:100vh;min-height:100svh;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;padding-bottom:calc(82px + var(--safe-bottom))}
@media (min-width:981px){body{padding-bottom:0}}
body.nav-open{overflow:hidden}
a{color:inherit;text-decoration:none}
img{max-width:100%;height:auto;display:block}
video{max-width:100%}
button{font-family:inherit;cursor:pointer}
h1,h2,h3,h4{font-family:var(--font-head);letter-spacing:var(--head-ls);line-height:var(--head-lh);color:var(--ink);overflow-wrap:break-word;word-wrap:break-word}
h1{font-size:clamp(2rem,7vw,4.4rem)}
h2{font-size:clamp(1.5rem,4.4vw,2.6rem)}
h3{font-size:clamp(1.12rem,2.8vw,1.4rem)}
p{overflow-wrap:break-word;word-wrap:break-word}
body.lang-en .lang-es,body.lang-es .lang-en{display:none!important}

@media (prefers-reduced-motion:no-preference){
  body{animation:pageIn .42s cubic-bezier(.2,.8,.2,1) both}
  @keyframes pageIn{from{opacity:0}to{opacity:1}}
  .reveal{animation:revealUp .6s cubic-bezier(.2,.8,.2,1) both}
  @keyframes revealUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.001s!important;transition-duration:.001s!important}}

.bg-video{position:fixed;inset:0;width:100%;height:100vh;height:100svh;object-fit:cover;z-index:0;opacity:.14;pointer-events:none}
@media (max-width:768px){.bg-video{opacity:.06}}
.bg-overlay{position:fixed;inset:0;background:radial-gradient(ellipse at center,transparent 0,rgba(0,0,0,.4) 70%,var(--bg) 100%);z-index:1;pointer-events:none}

/* ---- decorations (all variants; toggled by the deco element present) ---- */
.deco-neon{position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(ellipse 80% 60% at 20% 0%,color-mix(in srgb,var(--accent) 13%,transparent) 0,transparent 50%),radial-gradient(ellipse 60% 50% at 90% 100%,color-mix(in srgb,var(--accent2) 13%,transparent) 0,transparent 50%)}
.deco-chrome{position:fixed;inset:0;pointer-events:none;z-index:1;background:linear-gradient(135deg,transparent 0,transparent 49%,var(--line) 49%,var(--line) 51%,transparent 51%,transparent 100%);background-size:80px 80px;opacity:.4}
.deco-holo{position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(circle at 25% 25%,color-mix(in srgb,var(--accent) 20%,transparent) 0,transparent 40%),radial-gradient(circle at 75% 75%,color-mix(in srgb,var(--accent2) 20%,transparent) 0,transparent 40%)}
.deco-hud{position:fixed;inset:0;pointer-events:none;z-index:1;background:repeating-linear-gradient(0deg,transparent 0 3px,color-mix(in srgb,var(--accent2) 4%,transparent) 3px 4px);mix-blend-mode:screen}
.deco-gold{position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(ellipse 50% 40% at 50% 0%,color-mix(in srgb,var(--accent) 13%,transparent) 0,transparent 60%)}
.deco-grid{position:fixed;inset:0;pointer-events:none;z-index:1;background-image:linear-gradient(color-mix(in srgb,var(--accent) 7%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,var(--accent) 7%,transparent) 1px,transparent 1px);background-size:64px 64px;-webkit-mask-image:radial-gradient(circle at center,black 0,transparent 70%);mask-image:radial-gradient(circle at center,black 0,transparent 70%)}
.deco-flat{position:fixed;inset:0;pointer-events:none;z-index:1;background:linear-gradient(180deg,transparent 0,transparent 70%,color-mix(in srgb,var(--accent) 4%,transparent) 100%)}
.deco-orbs{position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden}
.deco-orbs .orb{position:absolute;width:480px;height:480px;border-radius:50%;filter:blur(120px);opacity:.32;animation:orbDrift 20s ease-in-out infinite}
.deco-orbs .o1{background:var(--accent);top:-20%;left:-10%}
.deco-orbs .o2{background:var(--accent2);top:40%;right:-10%;animation-delay:-7s}
.deco-orbs .o3{background:var(--accent3);bottom:-10%;left:30%;animation-delay:-14s}
@keyframes orbDrift{0%,100%{transform:translate(0,0)}33%{transform:translate(40px,-40px)}66%{transform:translate(-30px,30px)}}
.deco-spotlight{position:fixed;inset:0;pointer-events:none;z-index:1;background:radial-gradient(circle 560px at var(--spot-x,50%) var(--spot-y,30%),color-mix(in srgb,var(--accent) 13%,transparent) 0,transparent 100%);transition:background .3s}
.deco-vapor{position:fixed;inset:0;pointer-events:none;z-index:1;perspective:800px;overflow:hidden}
.deco-vapor::before{content:"";position:absolute;bottom:0;left:-50%;right:-50%;height:50%;background-image:linear-gradient(color-mix(in srgb,var(--accent) 40%,transparent) 1px,transparent 1px),linear-gradient(90deg,color-mix(in srgb,var(--accent) 40%,transparent) 1px,transparent 1px);background-size:50px 50px;transform:rotateX(60deg);-webkit-mask-image:linear-gradient(180deg,transparent 0,black 50%,black 100%);mask-image:linear-gradient(180deg,transparent 0,black 50%,black 100%)}
.deco-vapor .vsun{position:absolute;left:50%;top:50%;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,var(--accent2) 0,var(--accent) 70%,transparent 100%);transform:translate(-50%,-75%);filter:blur(2px);opacity:.22}

/* ---- top banner ---- */
.top-banner{position:relative;z-index:40;background:var(--ribbon-bg);color:var(--ribbon-color);padding:10px 14px calc(10px + var(--safe-top));display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}
.promo-line{flex-basis:100%;text-align:center;font-size:.74rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;opacity:.95}
.cta-call{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;min-height:44px;background:rgba(0,0,0,.18);color:inherit;border-radius:999px;font-weight:800;font-size:.82rem;border:2px solid currentColor;white-space:nowrap;transition:transform .2s,background .2s}
.cta-call:hover{background:rgba(0,0,0,.35);transform:translateY(-1px)}
.cta-call .cta-flag{font-size:.66rem;padding:2px 7px;border:1.5px solid currentColor;border-radius:999px;font-weight:900;letter-spacing:.08em}
.cta-call .cta-label{font-size:.78rem;font-weight:700;letter-spacing:.04em}
.cta-call .cta-num{font-family:ui-monospace,'SF Mono',Menlo,monospace;font-size:.86rem;font-weight:900}
.lang-toggle{display:inline-flex;align-items:stretch;min-height:44px;border-radius:999px;border:2px solid currentColor;overflow:hidden}
.lang-toggle button{background:transparent;border:0;color:inherit;padding:0 14px;min-width:44px;min-height:44px;cursor:pointer;font-weight:900;letter-spacing:.12em;font-family:inherit;font-size:.78rem}
.lang-toggle button.active{background:rgba(0,0,0,.35)}

/* ---- header ---- */
.site-header{position:sticky;top:0;z-index:30;background:var(--glass);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.header-inner{display:flex;align-items:center;gap:14px;height:68px;padding:0 18px;max-width:1280px;margin:0 auto}
.brand-logo{display:flex;align-items:center;gap:12px;flex-shrink:0;min-width:0}
.brand-logo img{width:clamp(34px,4.6vw,44px);height:clamp(34px,4.6vw,44px);border-radius:clamp(8px,1vw,11px);object-fit:cover;flex-shrink:0;box-shadow:0 6px 18px rgba(0,0,0,.25);border:1px solid var(--line)}
.brand-name{font-family:var(--font-head);font-weight:800;letter-spacing:.02em;line-height:1.1;display:flex;flex-direction:column;font-size:clamp(.78rem,1.7vw,.98rem)}
.brand-name .brand-line1{color:var(--ink)}
.brand-name .brand-line2{color:var(--accent)}
.primary-nav{display:flex;align-items:center;gap:2px;flex:1;justify-content:center;flex-wrap:nowrap}
.primary-nav a{color:var(--mut);padding:8px 9px;min-height:44px;display:inline-flex;align-items:center;font-size:.8rem;font-weight:600;letter-spacing:.01em;white-space:nowrap;border-radius:8px;transition:color .2s,background .2s}
.primary-nav a:hover,.primary-nav a.active{color:var(--accent);background:color-mix(in srgb,var(--accent) 10%,transparent)}
.burger{width:48px;height:48px;display:none;flex-direction:column;gap:5px;align-items:center;justify-content:center;background:transparent;border:0;flex-shrink:0}
.burger span{width:26px;height:2px;background:var(--accent);transition:.2s;border-radius:2px}
.burger[aria-expanded="true"] span:nth-child(1){transform:translateY(7px) rotate(45deg)}
.burger[aria-expanded="true"] span:nth-child(2){opacity:0}
.burger[aria-expanded="true"] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}

/* ---- mobile nav drawer: anchored under the header via JS-measured --nav-top
   (robust to the top-banner wrapping to multiple rows on small screens) ---- */
@media (max-width:1280px){
  .primary-nav{position:fixed;left:0;right:0;top:100%;z-index:29;flex-direction:column;align-items:stretch;gap:0;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 16px calc(24px + var(--safe-bottom));max-height:calc(100dvh - 100%);overflow-y:auto;-webkit-overflow-scrolling:touch;opacity:0;visibility:hidden;transform:translateY(-10px);transition:opacity .25s,transform .25s,visibility .25s;box-shadow:0 24px 48px rgba(0,0,0,.5)}
  .primary-nav.open{opacity:1;visibility:visible;transform:none}
  .primary-nav a{padding:15px 8px;border-bottom:1px solid var(--line);font-size:1.02rem;min-height:54px;width:100%}
  .primary-nav a:last-child{border-bottom:0}
  .burger{display:inline-flex;margin-left:auto}
}
@media (max-width:760px){
  .header-inner{height:62px;padding:0 14px}
  .top-banner{padding:8px 10px calc(8px + var(--safe-top));gap:6px}
  .promo-line{font-size:.66rem}
  .cta-call{padding:7px 12px;min-height:44px;font-size:.76rem;gap:6px}
}
@media (max-width:480px){
  .header-inner{height:58px;padding:0 12px}
  .brand-name .brand-line2{display:none}
  .top-banner{padding:7px 8px calc(7px + var(--safe-top));gap:5px}
  .cta-call{padding:6px 10px;min-height:44px;font-size:.72rem}
  .cta-call .cta-label{display:none}
  .cta-call .cta-num{font-size:.78rem}
  .cta-call .cta-flag{font-size:.6rem;padding:1px 5px}
}
@media (max-width:360px){.brand-name{display:none}.cta-call{padding:6px 8px}.cta-call .cta-num{font-size:.74rem}}

/* ---- hero ---- */
.subpage-hero{position:relative;z-index:2;padding:clamp(44px,8vw,96px) 0 clamp(30px,5vw,52px);text-align:center}
.subpage-hero .container{max-width:940px}
.hero-home{text-align:center;padding:clamp(52px,9vw,120px) 0 clamp(34px,6vw,64px)}
.eyebrow{display:inline-block;padding:7px 16px;border:1px solid var(--line);border-radius:999px;font-size:.7rem;letter-spacing:.3em;text-transform:uppercase;color:var(--accent);font-weight:800}
.subpage-hero h1{margin:20px 0 14px}
.subpage-hero p.sub{max-width:720px;margin:0 auto;color:var(--mut);font-size:clamp(1rem,2.2vw,1.12rem)}
.hero-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:26px}

/* ---- h1 effects (toggled by body hfx-* class) ---- */
.hfx-glow h1{text-shadow:0 0 24px color-mix(in srgb,var(--accent) 40%,transparent),0 0 48px color-mix(in srgb,var(--accent) 20%,transparent)}
.hfx-neon h1{text-shadow:0 0 20px color-mix(in srgb,var(--accent) 40%,transparent)}
.hfx-holo h1{background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3),var(--accent));background-size:300% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:holoflow 8s linear infinite}
@keyframes holoflow{from{background-position:0 50%}to{background-position:300% 50%}}
.hfx-gold h1{background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent));background-size:200% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sheen 6s ease infinite}
@keyframes sheen{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}
.hfx-chrome h1{background:linear-gradient(180deg,#fff 0,var(--mut) 50%,#fff 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.hfx-vapor h1{text-shadow:3px 3px 0 var(--accent2),-2px -2px 0 var(--accent)}
.hfx-hud h1 .accent{color:var(--accent)}

section{padding:clamp(34px,6vw,64px) 0;position:relative;z-index:2}
section h2{margin-bottom:14px}
section p.lead{color:var(--mut);max-width:780px;margin-bottom:24px;font-size:clamp(1rem,2.2vw,1.08rem)}
.container{width:100%;max-width:1200px;margin:0 auto;padding:0 clamp(14px,4vw,28px);position:relative;z-index:2}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:clamp(12px,2.4vw,20px)}
.grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:clamp(14px,2.6vw,22px)}
.grid-4{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:clamp(10px,2vw,18px)}
.gallery-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:clamp(8px,1.6vw,14px)}
.center{text-align:center}

.card{background:var(--glass);border:1px solid var(--line);border-radius:var(--card-r);padding:clamp(18px,3vw,28px);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);transition:transform .3s,border-color .3s,box-shadow .3s}
.card:hover{transform:translateY(-4px);border-color:var(--accent);box-shadow:0 16px 40px rgba(0,0,0,.35)}
.eyebrow-acc{color:var(--accent);font-size:.72rem;letter-spacing:.28em;text-transform:uppercase;font-weight:800;display:block}
.price-tag{font-size:1.4rem;font-weight:800;color:var(--accent);margin:8px 0}
.badge{position:absolute;top:14px;right:14px;font-size:.58rem;letter-spacing:.16em;text-transform:uppercase;background:var(--accent);color:var(--bg);padding:5px 10px;border-radius:999px;font-weight:800}

.partner-card{overflow:hidden;padding:0;display:flex;flex-direction:column}
.partner-card .img-wrap{position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--bg2)}
.partner-card .img-wrap img{width:100%;height:100%;object-fit:cover;transition:transform .5s}
.partner-card:hover .img-wrap img{transform:scale(1.06)}
.partner-card .img-wrap::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(0,0,0,.55) 100%)}
.partner-card .img-wrap .partner-name{position:absolute;left:18px;bottom:14px;z-index:2;font-family:var(--font-head);font-size:1.3rem;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.6)}
.partner-card .body{padding:22px}
.partner-card .locations{font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:10px}
.partner-card .desc{color:var(--mut);font-size:.94rem;margin-bottom:12px}
.partner-card .why{font-size:.88rem;color:var(--accent);font-weight:700}

.gallery-tile{position:relative;aspect-ratio:4/3;overflow:hidden;border-radius:var(--card-r);background:var(--bg2);border:1px solid var(--line);cursor:zoom-in}
.gallery-tile img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.gallery-tile:hover img{transform:scale(1.08)}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 26px;min-height:48px;border-radius:var(--btn-r);font-weight:800;font-size:.94rem;text-decoration:none;border:0;cursor:pointer;transition:transform .2s,filter .2s,background .2s,box-shadow .2s;text-align:center}
.btn-primary{background:var(--accent);color:var(--bg)}
.btn-primary:hover{filter:brightness(1.08);transform:translateY(-2px);box-shadow:0 14px 28px rgba(0,0,0,.32)}
.btn-ghost{border:2px solid var(--accent);color:var(--accent);background:transparent}
.btn-ghost:hover{background:var(--accent);color:var(--bg)}
.btn-wrap{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}

.input{width:100%;background:var(--bg2);border:1px solid var(--line);border-radius:var(--card-r);padding:14px;color:var(--ink);font-size:1rem;font-family:inherit;min-height:48px;-webkit-appearance:none;appearance:none}
.input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.row-stat{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:22px 0}
.row-stat .s{padding:18px 14px;border:1px solid var(--line);border-radius:var(--card-r);background:var(--glass)}
.row-stat .s b{display:block;font-size:clamp(1.4rem,4vw,2rem);color:var(--accent);font-weight:800;line-height:1.1;font-family:var(--font-head)}
.row-stat .s small{color:var(--mut);font-size:.82rem}
.list-clean{list-style:none;padding:0}
.list-clean li{padding:12px 0;border-bottom:1px solid var(--line);color:var(--mut)}
.list-clean li:last-child{border-bottom:0}
.list-clean li::before{content:"▸ ";color:var(--accent);font-weight:800}
details.card{margin-bottom:11px}
details.card summary{cursor:pointer;font-weight:800;font-size:1.04rem;min-height:32px;list-style:none;padding-right:20px;position:relative}
details.card summary::-webkit-details-marker{display:none}
details.card summary::after{content:"+";position:absolute;right:4px;top:0;color:var(--accent);font-size:1.4rem;transition:transform .2s}
details.card[open] summary::after{transform:rotate(45deg)}

/* ---- stat counters ---- */
.stats-band{padding:clamp(28px,5vw,56px) 0}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));gap:clamp(10px,2vw,18px)}
.stat-card{padding:clamp(20px,3vw,32px) clamp(14px,2.4vw,22px);border:1px solid var(--line);border-radius:var(--card-r);background:var(--glass);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);position:relative;overflow:hidden;transition:transform .3s,border-color .3s;text-align:center}
.stat-card:hover{transform:translateY(-4px);border-color:var(--accent)}
.stat-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent);transform:scaleY(0);transform-origin:top;transition:transform .4s cubic-bezier(.2,.8,.2,1)}
.stat-card.in::before,.stat-card:hover::before{transform:scaleY(1)}
.stat-card .count{display:block;font-size:clamp(2rem,7vw,3.6rem);font-weight:900;color:var(--accent);line-height:1;font-family:var(--font-head);letter-spacing:-.02em;margin-bottom:6px;font-variant-numeric:tabular-nums}
.stat-card .label{display:block;font-size:clamp(.76rem,1.6vw,.9rem);color:var(--mut);font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.stat-card .sublabel{display:block;font-size:.7rem;color:var(--mut);opacity:.65;margin-top:4px}

/* ---- contact form ---- */
.form-grid{display:grid;gap:14px}
.form-grid .row-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:540px){.form-grid .row-2{grid-template-columns:1fr}}
.field-group{display:flex;flex-direction:column;gap:6px}
.field-group label{font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:800}
.radio-row{display:flex;gap:8px;flex-wrap:wrap}
.radio-pill{position:relative;cursor:pointer}
.radio-pill input{position:absolute;opacity:0;pointer-events:none}
.radio-pill span{display:inline-block;padding:10px 18px;min-height:44px;line-height:24px;border:1.5px solid var(--line);border-radius:999px;font-size:.88rem;font-weight:700;color:var(--mut);transition:all .2s;user-select:none}
.radio-pill input:checked+span{background:var(--accent);color:var(--bg);border-color:var(--accent)}
.radio-pill:hover span{border-color:var(--accent);color:var(--accent)}
.form-cta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:8px}
.form-cta .privacy{font-size:.78rem;color:var(--mut);flex:1;min-width:200px}
.hc-pills{display:flex;flex-wrap:wrap;gap:10px}
.hc-pill{display:inline-block;padding:9px 16px;border:1.5px solid var(--line);border-radius:999px;font-size:.86rem;font-weight:700;color:var(--mut);background:var(--glass);transition:border-color .2s,color .2s}
.hc-pill:hover{border-color:var(--accent);color:var(--accent)}

/* ---- CTA band ---- */
.cta-band{text-align:center}
.cta-band .quote{max-width:760px;margin:0 auto 8px;font-size:clamp(1.1rem,2.6vw,1.5rem);font-style:italic;color:var(--ink)}

/* ---- footer ---- */
.site-footer{padding:clamp(40px,6vw,60px) 0 clamp(80px,9vw,100px);border-top:1px solid var(--line);margin-top:50px;background:color-mix(in srgb,var(--bg) 86%,#000);color:var(--mut);position:relative;z-index:2;font-size:.9rem}
.footer-grid{display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.2fr;gap:clamp(20px,3vw,32px);margin-bottom:26px}
.footer-grid h4{font-size:.78rem;text-transform:uppercase;letter-spacing:.18em;color:var(--ink);margin-bottom:12px;font-family:var(--font-head)}
.footer-grid a{display:block;padding:4px 0;color:var(--mut)}
.footer-grid a:hover{color:var(--accent)}
.footer-grid p{margin-bottom:6px}
.footer-bottom{padding-top:22px;border-top:1px solid var(--line);font-size:.78rem;text-align:center;line-height:1.7}
.footer-bottom .tm{opacity:.7;font-size:.72rem}
@media (max-width:860px){.footer-grid{grid-template-columns:1fr 1fr}}
@media (max-width:480px){.footer-grid{grid-template-columns:1fr}}

/* ---- sticky mobile call bar ---- */
.sticky-call{display:none;position:fixed;left:12px;right:12px;bottom:calc(12px + var(--safe-bottom));z-index:50;gap:8px}
.sticky-call a{flex:1;padding:14px 10px;min-height:52px;border-radius:999px;font-weight:800;font-size:.86rem;text-align:center;box-shadow:0 16px 40px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.06);display:inline-flex;align-items:center;justify-content:center;gap:6px}
.sticky-call a.call{background:var(--bg2);color:var(--ink);border:2px solid var(--accent)}
.sticky-call a.apply{background:var(--accent);color:var(--bg)}
.sticky-call a .ico{font-size:1rem;line-height:1}
@media (max-width:980px){.sticky-call{display:flex}}

@media (max-width:480px){
  .row-stat{grid-template-columns:1fr 1fr;gap:8px}
  .row-stat .s{padding:14px 10px}
  .hero-ctas .btn,.btn-wrap .btn{width:100%}
}

/* ---- media band ---- */
.media-band{position:relative;z-index:2;padding:clamp(34px,6vw,72px) 0}
.media-band .m-head{max-width:760px;margin:0 auto clamp(18px,3vw,34px);text-align:center}
.media-band .m-head .eyb{font-size:.72rem;letter-spacing:.3em;text-transform:uppercase;color:var(--accent);font-weight:800}
.media-band .m-head h2{margin:10px 0}
.media-band .m-head p{color:var(--mut);max-width:640px;margin:0 auto}
.m-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr));gap:clamp(12px,2vw,18px)}
.m-tile{position:relative;overflow:hidden;border-radius:var(--card-r);background:var(--bg2);border:1px solid var(--line);aspect-ratio:4/3;opacity:0;transition:opacity .7s cubic-bezier(.2,.8,.2,1),transform .7s cubic-bezier(.2,.8,.2,1),box-shadow .3s,filter .3s}
.m-tile.shown{opacity:1}
.m-tile .m-media{width:100%;height:100%;object-fit:cover;display:block}
.m-tile .m-cap{position:absolute;left:12px;right:12px;bottom:10px;z-index:4;font-size:.8rem;font-weight:700;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.75);opacity:0;transform:translateY(6px);transition:.3s}
.m-tile::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.55));opacity:0;transition:opacity .3s}
.m-tile:hover::after{opacity:1}
.m-tile:hover .m-cap{opacity:1;transform:none}
.m-vid::before{content:'\25B6';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:4;width:52px;height:52px;display:grid;place-items:center;border-radius:50%;background:rgba(0,0,0,.45);color:#fff;font-size:1rem;border:2px solid rgba(255,255,255,.75);transition:.3s;pointer-events:none}
.m-vid:hover::before{background:var(--accent);color:var(--bg);transform:translate(-50%,-50%) scale(1.08)}
.m-vid.playing::before{opacity:0}
@media (prefers-reduced-motion:reduce){.m-tile,.m-tile.shown{opacity:1!important;transform:none!important;animation:none!important}}
/* ---- animated barber pole (brand mark; blue stripe tinted per site via --accent) ---- */
.barber-pole{position:relative;display:inline-block;width:14px;height:clamp(34px,4.6vw,44px);border-radius:8px;flex-shrink:0;overflow:hidden;border:1.5px solid var(--line);background:repeating-linear-gradient(45deg,#e11d2a 0 8px,#fff 8px 16px,var(--accent) 16px 24px,#fff 24px 32px);background-size:100% 46px;animation:poleSpin 1s linear infinite;box-shadow:0 2px 8px rgba(0,0,0,.35),inset 0 0 0 1px rgba(255,255,255,.18)}
@keyframes poleSpin{to{background-position:0 -46px}}
@media (prefers-reduced-motion:reduce){.barber-pole{animation:none}}
/* ---- footer social row ---- */
.social-row{display:flex;gap:9px;margin-top:14px;flex-wrap:wrap}
.social-row a{width:36px;height:36px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:50%;color:var(--mut);font-weight:800;font-size:.66rem;transition:color .2s,background .2s,border-color .2s,transform .2s}
.social-row a:hover{color:var(--bg);background:var(--accent);border-color:var(--accent);transform:translateY(-2px)}

/* ============ FINAL-PASS additions ============ */
/* 1-line brand & headings — never wrap, scale to fit instead */
.nowrap-fit{white-space:nowrap}
.footer-grid h4.nowrap-fit{white-space:nowrap}

/* header brand = logo image + spinning pole (no wordmark). Override base .brand-logo img. */
.brand-logo{display:flex;align-items:center;gap:10px;flex-shrink:0;min-width:0}
.brand-mark{display:inline-flex;align-items:center;justify-content:center;height:46px;width:46px;flex-shrink:0;position:relative;border-radius:10px;overflow:hidden}
.brand-logo .brand-mark img{height:100%;width:100%;object-fit:cover;border-radius:10px;box-shadow:none;border:0}
.brand-mark.logo-light{background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.16);border:1px solid rgba(0,0,0,.08)}
.brand-mark.logo-dark{background:transparent}
.brand-mark.has-ovl .logo-pole-ovl{position:absolute;pointer-events:none;border-radius:3px;background:repeating-linear-gradient(45deg,#e11d2a 0 6px,#fff 6px 12px,var(--accent) 12px 18px,#fff 18px 24px);background-size:100% 34px;animation:poleSpin 1s linear infinite;opacity:.95;box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)}
.brand-mark.has-ovl + .brand-pole{display:none}
@media (max-width:760px){.brand-mark{height:42px;width:42px}}
@media (max-width:480px){.brand-mark{height:38px;width:38px}}

/* EN/ES toggle in the sticky header — ALWAYS visible */
.lang-toggle-header{flex-shrink:0;margin-left:6px}
@media (max-width:1280px){.lang-toggle-header{margin-left:auto}}
@media (max-width:480px){.lang-toggle-header button{padding:0 10px;min-width:38px;font-size:.72rem}}

/* next-class countdown */
.next-class{margin-top:22px;display:inline-flex;flex-direction:column;gap:8px;padding:16px 22px;border:1px solid var(--line);border-radius:var(--card-r);background:var(--glass);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.next-class.nc-center{margin-left:auto;margin-right:auto;align-items:center}
.next-class .nc-label{font-size:.7rem;letter-spacing:.28em;text-transform:uppercase;color:var(--accent);font-weight:800}
.next-class .nc-date{font-family:var(--font-head);font-weight:800;font-size:clamp(1.05rem,3vw,1.45rem);color:var(--ink)}
.next-class .nc-timer{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.next-class .nc-unit{display:inline-flex;flex-direction:column;align-items:center;min-width:52px;padding:8px 6px;border-radius:10px;background:color-mix(in srgb,var(--accent) 10%,transparent)}
.next-class .nc-unit b{font-family:var(--font-head);font-size:clamp(1.2rem,4vw,1.7rem);font-weight:900;color:var(--accent);line-height:1;font-variant-numeric:tabular-nums}
.next-class .nc-unit i{font-style:normal;font-size:.64rem;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-top:3px}

/* home contact box (desktop + mobile) */
.home-contact .hc-box{display:grid;grid-template-columns:1fr 1fr;gap:clamp(18px,3vw,40px);align-items:center;background:var(--glass);border:1px solid var(--line);border-radius:var(--card-r);padding:clamp(20px,3.5vw,40px);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.home-contact .hc-form .btn{margin-top:4px}
@media (max-width:760px){.home-contact .hc-box{grid-template-columns:1fr;gap:18px}}

/* instructor cards — photo + bio, fits mobile & desktop */
.ins-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:clamp(14px,2.6vw,22px)}
.ins-card{padding:0;overflow:hidden;display:flex;flex-direction:column}
.ins-card .ins-photo{aspect-ratio:4/5;overflow:hidden;background:var(--bg2)}
.ins-card .ins-photo img{width:100%;height:100%;object-fit:cover;object-position:top center;transition:transform .5s}
.ins-card:hover .ins-photo img{transform:scale(1.05)}
.ins-card .ins-body{padding:clamp(16px,2.4vw,22px)}
.ins-card .ins-name{margin:6px 0 10px}
.ins-card .ins-bio{color:var(--mut);line-height:1.7;margin-bottom:12px;font-size:.95rem}
.ins-card .ins-tags{font-size:.82rem;color:var(--accent);font-weight:700}

/* partner cards — logos/photos use contain so nothing is mis-cropped; name below image */
.partner-card .img-wrap{aspect-ratio:16/10;background:#fff;display:flex;align-items:center;justify-content:center;padding:16px;overflow:hidden}
.partner-card .img-wrap img{width:100%;height:100%;object-fit:contain}
.partner-card .partner-title{margin:0 0 6px;font-size:1.25rem}
.partner-card .p-phone{margin-top:10px}
.partner-card .p-phone a{color:var(--accent);font-weight:800}

/* Manhattan | Bronx split */
.campus-split .campus-col .campus-progs li{padding:10px 0}
.campus-split .campus-col .campus-progs li::before{content:"▸ "}

/* footer logo emblem */
.footer-logo{height:54px;width:auto;max-width:200px;object-fit:contain;margin-bottom:14px;border-radius:8px}
"""

MEDIA_STYLE_CSS = {
    "neon-scan": ".ms-neon-scan .m-tile{border-color:var(--accent);transform:translateY(26px) skewX(-2.5deg)}.ms-neon-scan .m-tile.shown{transform:none}.ms-neon-scan .m-tile::before{content:'';position:absolute;inset:0;z-index:3;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 2px,#ffffff0d 2px 3px)}.ms-neon-scan .m-tile:hover{box-shadow:0 0 22px var(--accent),0 0 46px var(--accent2)}.ms-neon-scan .m-tile:hover .m-media{filter:saturate(1.3) contrast(1.06)}",
    "metal-slab": ".ms-metal-slab .m-tile{border:2px solid var(--line);border-radius:4px;transform:translateX(-44px)}.ms-metal-slab .m-tile:nth-child(even){transform:translateX(44px)}.ms-metal-slab .m-tile.shown{transform:none}.ms-metal-slab .m-tile::before{content:'';position:absolute;top:0;left:-70%;width:45%;height:100%;z-index:3;pointer-events:none;background:linear-gradient(100deg,transparent,#ffffff59,transparent);transform:skewX(-20deg);transition:left .65s}.ms-metal-slab .m-tile:hover::before{left:130%}",
    "holo-float": ".ms-holo-float .m-tile{border:0;border-radius:18px;transform:translateY(30px) scale(.96)}.ms-holo-float .m-tile.shown{transform:none;animation:mfloat 7s ease-in-out infinite}.ms-holo-float .m-tile:nth-child(even).shown{animation-delay:-3.5s}.ms-holo-float .m-tile::after{background:linear-gradient(140deg,color-mix(in srgb,var(--accent) 18%,transparent),transparent 45%,color-mix(in srgb,var(--accent2) 18%,transparent));opacity:.5}@keyframes mfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}",
    "hud-reticle": ".ms-hud-reticle .m-tile{border-color:var(--accent2);border-radius:6px;transform:translateY(24px)}.ms-hud-reticle .m-tile.shown{transform:none}.ms-hud-reticle .m-tile::before{content:'';position:absolute;inset:8px;z-index:3;pointer-events:none;border:1px solid color-mix(in srgb,var(--accent) 40%,transparent);clip-path:polygon(0 0,22px 0,22px 2px,2px 2px,2px 22px,0 22px,0 100%,22px 100%,22px calc(100% - 2px),2px calc(100% - 2px),2px calc(100% - 22px),0 calc(100% - 22px))}.ms-hud-reticle .m-tile:hover{box-shadow:0 0 0 1px var(--accent),0 14px 36px #000}",
    "gold-curtain": ".ms-gold-curtain .m-tile{transform:translateY(26px);border-color:color-mix(in srgb,var(--accent) 33%,transparent)}.ms-gold-curtain .m-tile.shown{transform:none}.ms-gold-curtain .m-tile::before{content:'';position:absolute;inset:0;z-index:4;pointer-events:none;background:linear-gradient(90deg,var(--accent),#7a5a17);transform:scaleX(1);transform-origin:right;transition:transform .8s cubic-bezier(.7,0,.2,1)}.ms-gold-curtain .m-tile.shown::before{transform:scaleX(0)}.ms-gold-curtain .m-tile .m-media{transform:scale(1.12);transition:transform 1.2s}.ms-gold-curtain .m-tile.shown .m-media{transform:scale(1)}",
    "grid-tilt": ".ms-grid-tilt .m-grid{perspective:1100px}.ms-grid-tilt .m-tile{transform:translateY(30px) rotateX(12deg);transform-style:preserve-3d;border-color:color-mix(in srgb,var(--accent) 30%,transparent)}.ms-grid-tilt .m-tile.shown{transform:none}.ms-grid-tilt .m-tile:hover{transform:rotateX(-6deg) rotateY(6deg) translateY(-4px);box-shadow:0 22px 50px color-mix(in srgb,var(--accent) 25%,transparent)}",
    "brutal-offset": ".ms-brutal-offset .m-tile{border:2px solid var(--ink);border-radius:0;transform:translate(18px,18px);box-shadow:-10px 10px 0 var(--accent)}.ms-brutal-offset .m-tile.shown{transform:none}.ms-brutal-offset .m-tile:hover{box-shadow:-16px 16px 0 var(--accent);transform:translate(2px,-2px)}@media (max-width:600px){.ms-brutal-offset .m-tile{transform:translate(7px,7px);box-shadow:-5px 5px 0 var(--accent)}.ms-brutal-offset .m-tile.shown{transform:none}}",
    "glass-rotate": ".ms-glass-rotate .m-grid{perspective:1200px}.ms-glass-rotate .m-tile{border-radius:16px;transform:rotateY(22deg) translateY(24px);transform-origin:left}.ms-glass-rotate .m-tile.shown{transform:none}.ms-glass-rotate .m-tile::after{background:linear-gradient(120deg,color-mix(in srgb,var(--accent) 20%,transparent),transparent 40%,color-mix(in srgb,var(--accent2) 20%,transparent));opacity:.55}.ms-glass-rotate .m-tile:hover{transform:rotateY(-8deg);box-shadow:0 20px 50px color-mix(in srgb,var(--accent) 25%,transparent)}",
    "spotlight-cine": ".ms-spotlight-cine .m-tile{transform:translateY(26px);filter:brightness(.6);transition:opacity .7s,transform .7s,filter 1s}.ms-spotlight-cine .m-tile.shown{transform:none;filter:brightness(1)}.ms-spotlight-cine .m-tile .m-media{transform:scale(1.08);transition:transform 6s ease-out}.ms-spotlight-cine .m-tile.shown .m-media{transform:scale(1)}.ms-spotlight-cine .m-tile:hover{box-shadow:0 0 60px color-mix(in srgb,var(--accent) 33%,transparent)}",
    "vhs-flip": ".ms-vhs-flip .m-grid{perspective:1000px}.ms-vhs-flip .m-tile{transform:rotateX(-25deg) translateY(28px);transform-origin:bottom}.ms-vhs-flip .m-tile.shown{transform:none}.ms-vhs-flip .m-tile::before{content:'';position:absolute;inset:0;z-index:3;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 2px,#0000001a 2px 4px);mix-blend-mode:overlay}.ms-vhs-flip .m-tile:hover .m-media{filter:hue-rotate(8deg) saturate(1.25)}.ms-vhs-flip .m-tile:hover{box-shadow:3px 0 0 var(--accent2),-3px 0 0 var(--accent)}",
}

H1FX_MAP = {
    "glow": "hfx-glow", "neon-shadow": "hfx-neon", "holo-gradient": "hfx-holo",
    "gold-sheen": "hfx-gold", "chrome": "hfx-chrome", "vapor-shadow": "hfx-vapor", "hud": "hfx-hud",
}
DECO_MAP = {
    "neon-glow": "deco-neon", "chrome-brutalism": "deco-chrome", "holographic": "deco-holo",
    "hud-scanlines": "deco-hud", "luxe-gold": "deco-gold", "particle-network": "deco-grid",
    "flat-brutalist": "deco-flat", "aurora-orbs": "deco-orbs", "noir-spotlight": "deco-spotlight",
    "vapor-grid": "deco-vapor",
}


def css_for_site(t, extra_css=""):
    style = t.get("media_style", "")
    return ("<style>" + root_vars(t) + CSS_BASE + MEDIA_STYLE_CSS.get(style, "") + (extra_css or "") + "</style>")


def decoration_layer(t):
    cls = DECO_MAP.get(t.get("decoration", ""), "")
    if not cls:
        return ""
    if cls == "deco-orbs":
        return '<div class="deco-orbs" aria-hidden="true"><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span></div>'
    if cls == "deco-vapor":
        return '<div class="deco-vapor" aria-hidden="true"><span class="vsun"></span></div>'
    return f'<div class="{cls}" aria-hidden="true"></div>'


# ===================== chrome =====================
def head_meta(page_path, title=None):
    title = title or PAGE_TITLES.get(page_path, BRAND_TITLE)
    canon = page_path if page_path != "/" else "/"
    return f'''<meta name="description" content="{BRAND_DESC_EN}">
<meta name="keywords" content="barber school nyc, american barber institute, abi, master barber program, gi bill barber school, escuela de barberia nueva york">
<meta name="author" content="American Barber Institute">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canon}">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{BRAND_DESC_EN}">
<meta property="og:image" content="/assets/og.png">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{BRAND_DESC_EN}">
<meta name="twitter:image" content="/assets/og.png">
<meta name="format-detection" content="telephone=yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">'''


def jsonld(include_faq=False, article=None):
    school = {"@context": "https://schema.org", "@type": "EducationalOrganization", "name": "American Barber Institute", "alternateName": "ABI", "description": BRAND_DESC_EN, "telephone": B["phone_manhattan"], "email": B["email"], "foundingDate": "1995", "address": [{"@type": "PostalAddress", "streetAddress": "48 West 39th Street", "addressLocality": "New York", "addressRegion": "NY", "postalCode": "10018", "addressCountry": "US"}, {"@type": "PostalAddress", "streetAddress": "121 Westchester Square", "addressLocality": "Bronx", "addressRegion": "NY", "postalCode": "10461", "addressCountry": "US"}], "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.3", "ratingCount": "100"}}
    out = f'<script type="application/ld+json">{json.dumps(school)}</script>'
    if include_faq:
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"]["en"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]["en"]}} for q in CONTENT["faqs"]]}
        out += f'<script type="application/ld+json">{json.dumps(faq)}</script>'
    if article:
        post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": article["title"]["en"], "datePublished": article["iso"], "dateModified": article["iso"], "description": article["excerpt"]["en"], "author": {"@type": "Organization", "name": "American Barber Institute"}, "publisher": {"@type": "Organization", "name": "American Barber Institute"}}
        out += f'<script type="application/ld+json">{json.dumps(post)}</script>'
    return out


# ---- optional analytics (off until IDs are set; empty ships nothing) ----
ANALYTICS = {"gtm": "GTM-NKLLGPC", "ga4": "", "pixel": ""}
FORM_NEXT = ""  # set per-site in build_site() so the contact form returns the visitor to their own site
_GTM_HEAD = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
             "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
             "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
             "(window,document,'script','dataLayer','__GTM__');</script>")
_GTM_BODY = ('<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=__GTM__" height="0" width="0" '
             'style="display:none;visibility:hidden"></iframe></noscript>')
_GA4_TPL = ('<script async src="https://www.googletagmanager.com/gtag/js?id=__GA__"></script>'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
            'gtag("js",new Date());gtag("config","__GA__")</script>')
_PIXEL_TPL = ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
              "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;"
              "n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;"
              "t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}"
              "(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
              "fbq('init','__PIXEL__');fbq('track','PageView')</script>")
def analytics_snippet():
    out = ""
    if ANALYTICS.get("gtm"):
        out += _GTM_HEAD.replace("__GTM__", ANALYTICS["gtm"])
    if ANALYTICS.get("ga4"):
        out += _GA4_TPL.replace("__GA__", ANALYTICS["ga4"])
    if ANALYTICS.get("pixel"):
        out += _PIXEL_TPL.replace("__PIXEL__", ANALYTICS["pixel"])
    return out


def gtm_body():
    return _GTM_BODY.replace("__GTM__", ANALYTICS["gtm"]) if ANALYTICS.get("gtm") else ""


def top_banner():
    return f'''<div class="top-banner">
  <div class="promo-line">{bi(B["promo"])}</div>
  <a class="cta-call cta-en" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call English admissions">
    <span class="cta-flag">EN</span>
    <span class="cta-label"><span class="lang-en">Call Admissions</span><span class="lang-es">Llama a Admisiones</span></span>
    <span class="cta-num">{B["phone_manhattan"]}</span>
  </a>
  <a class="cta-call cta-es" href="tel:{tel(B["phone_manhattan_es"])}" aria-label="Call Spanish admissions">
    <span class="cta-flag">ES</span>
    <span class="cta-label"><span class="lang-en">En Español</span><span class="lang-es">En Español</span></span>
    <span class="cta-num">{B["phone_manhattan_es"]}</span>
  </a>
</div>'''


def lang_toggle(extra_cls=""):
    """EN/ES segmented toggle. Rendered in the sticky header so it is ALWAYS visible.
    All .lang-toggle instances stay in sync via the shared JS."""
    return (f'<div class="lang-toggle {extra_cls}" role="group" aria-label="Language / Idioma">'
            f'<button type="button" data-lang="en" aria-label="English">EN</button>'
            f'<button type="button" data-lang="es" aria-label="Español">ES</button></div>')


def header_html(active_key="", t=None):
    t = t or {}
    links = "".join(
        f'<a href="{p}" class="{"active" if k == active_key else ""}">{bi(NAV[k])}</a>'
        for k, p in NAV_ITEMS
    )
    # Brand mark = logo image + a spinning barber pole. No text wordmark (the logo carries
    # the name). frame class tones the logo to its baked background so it never looks like a
    # floating box on the theme. If the site sets t["logo_pole"] = {"l","t","w","h"} (percent
    # box over the logo's own pole), an animated pole is overlaid there and the standalone pole
    # is dropped — i.e. the logo's OWN pole appears to spin. Otherwise a crisp animated pole
    # sits beside the logo so every header has a moving pole.
    frame_cls = "logo-dark" if t.get("logo_dark_bg") else "logo-light"
    pole = t.get("logo_pole")
    # Header uses the square (padded) favicon so every site shows a tidy square logo chip —
    # the source logos are mixed portrait/landscape and would render as a thin sliver at 46px.
    # The full detailed logo still appears (larger, contained) in the footer + OG image.
    img = ('<img src="/assets/favicon.png" alt="American Barber Institute — New York\'s dedicated barber school" '
           'width="46" height="46" decoding="async">')
    if pole:
        ovl = (f'<span class="logo-pole-ovl" aria-hidden="true" '
               f'style="left:{pole["l"]}%;top:{pole["t"]}%;width:{pole["w"]}%;height:{pole["h"]}%"></span>')
        brand = f'<span class="brand-mark has-ovl {frame_cls}">{img}{ovl}</span>'
    else:
        brand = (f'<span class="barber-pole" role="img" aria-label="Barber pole"></span>'
                 f'<span class="brand-mark {frame_cls}">{img}</span>')
    return f'''<header class="site-header">
  <div class="header-inner">
    <a class="brand-logo" href="/" aria-label="American Barber Institute home">{brand}</a>
    <nav class="primary-nav" id="primary-nav">{links}</nav>
    {lang_toggle("lang-toggle-header")}
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def sticky_call():
    """Mobile-only fixed bottom bar — the two end actions: Call Now + Become a Barber."""
    return f'''<div class="sticky-call" role="region" aria-label="Quick actions">
  <a class="call" href="tel:{tel(B["phone_manhattan"])}" aria-label="Call admissions now"><span class="ico" aria-hidden="true">📞</span> {bi({"en":"Call Now","es":"Llama Ahora"})}</a>
  <a class="apply" href="/contact" aria-label="Become a barber — apply now">{bi(UI["become_barber"])} <span class="ico" aria-hidden="true">✂</span></a>
</div>'''


def cta_band():
    return f'''<section class="cta-band"><div class="container">
  <div class="eyebrow-acc">{bi({"en": "Ready to Begin?", "es": "¿Listo para Empezar?"})}</div>
  <h2 style="margin:10px 0 12px">{bi({"en": "Ready to Start Your Barber Career?", "es": "¿Listo para Comenzar Tu Carrera de Barbero?"})}</h2>
  <p class="lead" style="margin:0 auto 22px">{bi({"en": "New classes begin the first Monday of every month. Apply today and take the first step toward your new career.", "es": "Las nuevas clases comienzan el primer lunes de cada mes. Aplica hoy y da el primer paso hacia tu nueva carrera."})}</p>
  <div class="btn-wrap"><a class="btn btn-primary" href="/contact">{bi(UI["become_barber"])} ✂</a><a class="btn btn-ghost" href="tel:{tel(B["phone_manhattan"])}">{bi(UI["call_admissions"])} · {B["phone_manhattan"]}</a></div>
</div></section>'''


def footer_html():
    f = CONTENT["footer"]
    nav_html = "".join(f'<a href="{p}">{bi(NAV[k])}</a>' for k, p in NAV_ITEMS if k != "home")
    hours = "".join(f'<p>{bi(h)}</p>' for h in f["hours"])
    _abbr = {"Facebook": "f", "Instagram": "IG", "YouTube": "YT", "X": "X", "Pinterest": "P"}
    socials = "".join(f'<a href="{s["url"]}" target="_blank" rel="noopener" aria-label="{s["name"]}">{_abbr.get(s["name"], s["name"][:2])}</a>' for s in CONTENT.get("social", []))
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img class="footer-logo" src="/assets/logo.jpeg" alt="American Barber Institute" width="200" height="64" loading="lazy">
        <h4 class="nowrap-fit">American Barber Institute</h4>
        <p>{bi(f["tagline"])}</p>
        <p style="margin-top:10px;font-size:.85rem">{bi({"en": "GI Bill® · ACCES-VR · VA benefits accepted.", "es": "GI Bill® · ACCES-VR · beneficios de la VA aceptados."})}</p>
        <div class="social-row">{socials}</div>
      </div>
      <div>
        <h4>{bi({"en": "Links", "es": "Enlaces"})}</h4>
        {nav_html}
      </div>
      <div>
        <h4>{bi({"en": "Locations", "es": "Ubicaciones"})}</h4>
        <p><b>Manhattan</b><br>48 West 39th Street<br>New York, NY 10018</p>
        <p style="margin-top:8px"><b>Bronx</b><br>121 Westchester Square<br>Bronx, NY 10461</p>
      </div>
      <div>
        <h4>{bi({"en": "Contact", "es": "Contacto"})}</h4>
        <a href="tel:{tel(B["phone_manhattan"])}">{B["phone_manhattan"]} <span class="lang-en">(English)</span><span class="lang-es">(Inglés)</span></a>
        <a href="tel:{tel(B["phone_manhattan_es"])}">{B["phone_manhattan_es"]} (Español)</a>
        <a href="tel:{tel(B["phone_bronx"])}">{B["phone_bronx"]} (Bronx)</a>
        <a href="mailto:{B["email"]}">{B["email"]}</a>
        <div style="margin-top:10px;font-size:.82rem">{hours}</div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{bi(f["copyright"])}</span>
      <div class="tm" style="margin-top:6px">{bi(f["gibill_note"])}</div>
    </div>
  </div>
</footer>'''


JS = r'''<script>
(function(){
  var saved = localStorage.getItem('abi_lang') || 'en';
  document.body.classList.remove('lang-en','lang-es');
  document.body.classList.add('lang-' + saved);
  document.documentElement.lang = saved;
  function setLang(lang){
    document.body.classList.remove('lang-en','lang-es');
    document.body.classList.add('lang-' + lang);
    document.documentElement.lang = lang;
    localStorage.setItem('abi_lang', lang);
    document.querySelectorAll('.lang-toggle button').forEach(function(b){ b.classList.toggle('active', b.getAttribute('data-lang') === lang); });
  }
  document.querySelectorAll('.lang-toggle button').forEach(function(b){
    b.addEventListener('click', function(){ setLang(this.getAttribute('data-lang')); });
    if (b.getAttribute('data-lang') === saved) b.classList.add('active');
  });

  // Hamburger drawer — anchor it under the header by measuring header.bottom (robust to a
  // top-banner that wraps to 2-3 rows on small screens).
  var nav = document.querySelector('.primary-nav');
  var burger = document.querySelector('.burger');
  var header = document.querySelector('.site-header');
  function setNavTop(){ if (header) document.documentElement.style.setProperty('--nav-top', Math.max(0, header.getBoundingClientRect().bottom) + 'px'); }
  if (nav && burger){
    function close(){ nav.classList.remove('open'); burger.setAttribute('aria-expanded','false'); document.body.classList.remove('nav-open'); }
    burger.addEventListener('click', function(){
      setNavTop();
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('nav-open', open);
    });
    nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', close); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') close(); });
    window.addEventListener('resize', function(){ setNavTop(); if (window.innerWidth > 1280) close(); });
  }

  if (document.querySelector('.deco-spotlight')){
    var el = document.querySelector('.deco-spotlight');
    document.addEventListener('mousemove', function(e){
      el.style.setProperty('--spot-x', e.clientX + 'px');
      el.style.setProperty('--spot-y', e.clientY + 'px');
    });
  }

  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('reveal'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('section, .card').forEach(function(el){ io.observe(el); });

    var countObs = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (!en.isIntersecting) return;
        var el = en.target, target = parseInt(el.getAttribute('data-target'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '', prefix = el.getAttribute('data-prefix') || '';
        var start = performance.now();
        el.parentElement.classList.add('in');
        function step(t){
          var p = Math.min(1, (t - start) / 1400), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.floor(target * eased).toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(step); else el.textContent = prefix + target.toLocaleString() + suffix;
        }
        requestAnimationFrame(step);
        countObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.stat-card .count[data-target]').forEach(function(c){ countObs.observe(c); });

    var mio = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (!en.isIntersecting) return;
        var tile = en.target; tile.classList.add('shown');
        var v = tile.querySelector('video[data-src]');
        if (v && !v.getAttribute('data-loaded')){
          v.setAttribute('data-loaded','1'); v.src = v.getAttribute('data-src');
          var pr = v.play(); if (pr && pr.then) pr.then(function(){ tile.classList.add('playing'); }).catch(function(){});
        }
        mio.unobserve(tile);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.m-tile').forEach(function(t){ mio.observe(t); });
  }
})();

/* ---- next-class countdown: live to the first Monday of every month ---- */
(function(){
  var els = document.querySelectorAll('[data-next-class]');
  if (!els.length) return;
  function firstMonday(y,m){ var d=new Date(y,m,1); var delta=(1-d.getDay()+7)%7; d.setDate(1+delta); d.setHours(0,0,0,0); return d; }
  function nextStart(now){
    var y=now.getFullYear(), m=now.getMonth(), fm=firstMonday(y,m);
    if (fm.getTime()<=now.getTime()){ m+=1; if(m>11){m=0;y+=1;} fm=firstMonday(y,m); }
    return fm;
  }
  function pad(v){ return (v<10?'0':'')+v; }
  function tick(){
    var now=new Date(), t=nextStart(now), diff=Math.max(0,t-now);
    var lang=(document.documentElement.lang==='es')?'es-US':'en-US';
    var dstr=t.toLocaleDateString(lang,{weekday:'long',month:'long',day:'numeric'});
    var d=Math.floor(diff/864e5), h=Math.floor(diff/36e5)%24, mi=Math.floor(diff/6e4)%60, s=Math.floor(diff/1e3)%60;
    els.forEach(function(el){
      var dt=el.querySelector('[data-nc-date]'); if(dt) dt.textContent=dstr;
      ['days','hours','mins','secs'].forEach(function(k,idx){ var n=el.querySelector('[data-nc="'+k+'"]'); if(n) n.textContent=pad([d,h,mi,s][idx]); });
    });
  }
  tick(); setInterval(tick,1000);
})();
</script>'''


# ===================== page template =====================
PAGE_TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=5">
<title>{title}</title>
{head_meta}
{jsonld}
{analytics}
{css}
</head>
<body class="lang-en {hfx}">
{gtm_body}
<video class="bg-video" autoplay muted loop playsinline poster="/assets/logo.jpeg" aria-hidden="true"><source src="/assets/bg.mp4" type="video/mp4"></video>
<div class="bg-overlay"></div>
{decoration}
{top_banner}
{header}
<main>
  <section class="subpage-hero {hero_cls}">
    <div class="container">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
      {hero_ctas}
    </div>
  </section>
  {body}
  {media}
  {cta_band}
</main>
{footer}
{sticky_call}
{js}
</body>
</html>'''


def render_page(t, page_key, pdata, site_index=0, article=None):
    nvm = {"home": (2, 6), "gallery": (3, 8), "about": (2, 5), "haircuts": (2, 6), "faq": (1, 3), "contact": (1, 3)}
    nv, ni = nvm.get(page_key, (1, 4))
    hfx = H1FX_MAP.get(t.get("h1_effect", ""), "")
    title = pdata.get("title") or PAGE_TITLES.get(pdata["path"], BRAND_TITLE)
    return PAGE_TPL.format(
        title=title,
        head_meta=head_meta(pdata["path"], title),
        jsonld=jsonld(include_faq=(page_key == "faq"), article=article),
        analytics=analytics_snippet(),
        gtm_body=gtm_body(),
        css=css_for_site(t, pdata.get("_extra_css", "")),
        hfx=hfx,
        decoration=decoration_layer(t),
        top_banner=top_banner(),
        header=header_html(page_key, t),
        hero_cls="hero-home" if page_key == "home" else "",
        eyebrow=pdata["eyebrow"], h1=pdata["h1"], sub=pdata["sub"],
        hero_ctas=pdata.get("hero_ctas", ""),
        body=pdata["body"],
        media=media_band(t, site_index, page_key, n_vid=nv, n_img=ni),
        cta_band=cta_band(),
        footer=footer_html(),
        sticky_call=sticky_call(),
        js=JS,
    )


# ===================== page content builders =====================
def _instructor_card(i, compact=False):
    photo = (f'<div class="ins-photo"><img src="/assets/instructors/{i["image"]}" loading="lazy" '
             f'alt="{bt(i["name"])} — American Barber Institute instructor"></div>') if i.get("image") else ""
    tags = " · ".join(bi(tg) for tg in i.get("tags", []))
    tagline = "" if compact or not tags else f'<p class="ins-tags">{tags}</p>'
    bio = "" if compact else f'<p class="ins-bio">{bi(i["bio"])}</p>'
    return (f'<div class="card ins-card">{photo}<div class="ins-body">'
            f'<div class="eyebrow-acc">{bi(i["role"])}</div>'
            f'<h3 class="ins-name">{i["name"]}</h3>{bio}{tagline}</div></div>')


def _campus_split():
    """Manhattan | Bronx side-by-side — shown wherever programs/campuses appear, per request."""
    c1, c2 = CONTENT["campuses"]
    progs = CONTENT["programs"]
    def col(campus_en, c):
        items = [p for p in progs if campus_en in p["campus"]["en"]]
        li = "".join(f'<li><b>{bi(p["name"])}</b> — <span style="color:var(--accent);font-weight:800">{p["price"]}</span><br><span style="color:var(--mut);font-size:.85rem">{bi(p["duration"])}</span></li>' for p in items)
        return (f'<div class="card campus-col"><div class="eyebrow-acc">{bi(c["name"])} {bi({"en":"Campus","es":"Campus"})}</div>'
                f'<h3 style="margin:8px 0">{bi(c["name"])}</h3>'
                f'<p style="color:var(--mut);font-size:.92rem;margin-bottom:6px">{c["address"]}</p>'
                f'<p style="margin-bottom:12px"><a href="tel:{tel(c["phone"])}" style="color:var(--accent);font-weight:800">{c["phone"]}</a></p>'
                f'<ul class="list-clean campus-progs">{li}</ul></div>')
    return (f'<section class="campus-split"><div class="container">'
            f'<div class="eyebrow-acc">{bi({"en":"Two NYC Campuses","es":"Dos Campus en NYC"})}</div>'
            f'<h2 style="margin-bottom:16px"><span class="nowrap-fit">Manhattan</span> &nbsp;|&nbsp; <span class="nowrap-fit">Bronx</span></h2>'
            f'<div class="grid-2">{col("Manhattan", c1)}{col("Bronx", c2)}</div></div></section>')


def _program_card(p):
    badge = f'<span class="badge">{bi(p["badge"])}</span>' if p.get("badge") else ""
    return (f'<div class="card" style="position:relative">{badge}'
            f'<div class="eyebrow-acc">{bi(p["campus"])} · {bi(p["duration"])}</div>'
            f'<h3 style="margin:8px 0">{bi(p["name"])}</h3>'
            f'<div class="price-tag">{bi(p["price"]) if isinstance(p["price"], dict) else p["price"]}</div>'
            f'<p style="color:var(--mut)">{bi(p["summary"])}</p></div>')


def next_class_counter(center=True):
    """Live countdown to the next class start (first Monday of every month). JS fills it in."""
    cls = "nc-center" if center else ""
    return (f'<div class="next-class {cls}" data-next-class aria-live="polite">'
            f'<span class="nc-label">{bi({"en": "Next class starts", "es": "Próxima clase"})}</span>'
            f'<span class="nc-date" data-nc-date>—</span>'
            f'<div class="nc-timer">'
            f'<span class="nc-unit"><b data-nc="days">--</b><i>{bi({"en": "days", "es": "días"})}</i></span>'
            f'<span class="nc-unit"><b data-nc="hours">--</b><i>{bi({"en": "hrs", "es": "hrs"})}</i></span>'
            f'<span class="nc-unit"><b data-nc="mins">--</b><i>{bi({"en": "min", "es": "min"})}</i></span>'
            f'<span class="nc-unit"><b data-nc="secs">--</b><i>{bi({"en": "sec", "es": "seg"})}</i></span>'
            f'</div></div>')


def home_contact_section():
    """Lead-capture contact box shown on the home page (desktop + mobile), posts to FormSubmit."""
    progs = "".join(f"<option>{(p['name']['en'] if isinstance(p['name'], dict) else p['name'])}</option>" for p in CONTENT["programs"])
    return f'''<section class="home-contact" id="home-contact"><div class="container"><div class="hc-box">
  <div class="hc-copy">
    <div class="eyebrow-acc">{bi({"en": "Get Started", "es": "Empieza Hoy"})}</div>
    <h2 style="margin:8px 0 10px">{bi({"en": "Talk to admissions today", "es": "Habla con admisiones hoy"})}</h2>
    <p style="color:var(--mut);margin-bottom:16px">{bi({"en": "Tell us how to reach you and an ABI advisor calls you back — same day during business hours.", "es": "Dinos cómo contactarte y un asesor de ABI te devuelve la llamada — el mismo día en horario laboral."})}</p>
    <p style="margin-bottom:6px"><a href="tel:{tel(B["phone_manhattan"])}" style="color:var(--accent);font-weight:800;font-size:1.12rem">📞 {B["phone_manhattan"]}</a></p>
    <p style="color:var(--mut);font-size:.86rem">{bi({"en": "Manhattan &amp; Bronx · Open 7 days", "es": "Manhattan y Bronx · Abierto 7 días"})}</p>
  </div>
  <form class="hc-form form-grid" action="https://formsubmit.co/{B["email"]}" method="POST" novalidate>
    <input type="hidden" name="_subject" value="New ABI website inquiry (home)">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="{FORM_NEXT}">
    <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
    <div class="field-group"><label for="hc-name">{bi({"en": "Name", "es": "Nombre"})} *</label><input required id="hc-name" name="name" autocomplete="name" placeholder="{bt({"en": "Your name", "es": "Tu nombre"})}" class="input"></div>
    <div class="field-group"><label for="hc-phone">{bi({"en": "Phone", "es": "Teléfono"})} *</label><input required id="hc-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="(212) 555-0123" class="input"></div>
    <div class="field-group"><label for="hc-prog">{bi({"en": "Program of interest", "es": "Programa de interés"})}</label><select id="hc-prog" name="program" class="input">{progs}</select></div>
    <button type="submit" class="btn btn-primary" style="width:100%">{bi(UI["become_barber"])} ✂</button>
    <p class="privacy" style="font-size:.76rem;color:var(--mut);text-align:center">{bi({"en": "Same-day response. Never spam.", "es": "Respuesta el mismo día. Nunca spam."})}</p>
  </form>
</div></div></section>'''


def p_home():
    progs = "".join(_program_card(p) for p in CONTENT["programs"])
    why = "".join(f'<div class="card"><h3 style="margin-bottom:8px">{bi(w["title"])}</h3><p style="color:var(--mut)">{bi(w["desc"])}</p></div>' for w in CONTENT["why_choose"])
    sched = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(s["label"])}</div><h3 style="margin:8px 0">{bi(s["days"])} · {s["time"]}</h3><div class="price-tag">{s["tuition"]}</div><p style="color:var(--mut);font-size:.92rem">{bi(s["plan"])}</p></div>' for s in CONTENT["schedules"])
    tcards = "".join(f'<div class="card"><p style="color:var(--ink);font-style:italic;margin-bottom:10px">“{bi(tt["quote"])}”</p><p style="font-weight:800">{tt["name"]}</p><p style="color:var(--accent);font-size:.84rem">{bi(tt["role"])}</p></div>' for tt in CONTENT["testimonials"])
    ce = CONTENT["career_earnings"]
    earn = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(t["window"])}</div><h3 style="margin:8px 0">{bi(t["stage"])}</h3><div class="price-tag">{t["range"]}</div></div>' for t in ce["tiers"])
    grads = " · ".join(p["name"] for p in CONTENT["partners"])
    hero_ctas = (f'<div class="hero-ctas"><a class="btn btn-primary" href="/contact">{bi(UI["become_barber"])} ✂</a>'
                 f'<a class="btn btn-ghost" href="/programs">{bi(UI["view_all_programs"])}</a></div>'
                 + next_class_counter())
    return {"path": "/",
            "eyebrow": bi({"en": "NY State Licensed", "es": "Licenciada por el Estado de NY"}),
            "h1": bi(B["tagline"]),
            "sub": bi(B["subtitle"]),
            "hero_ctas": hero_ctas,
            "body": f'''<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Barber Programs — NYC","es":"Programas de Barbería — NYC"})}</div><h2 style="margin-bottom:8px">{bi({"en":"Choose your path to a Master Barber License","es":"Elige tu camino a la Licencia de Maestro Barbero"})}</h2><p class="lead">{bi({"en":"Four state-licensed programs across two NYC campuses. Flexible weekly payment plans on every track.","es":"Cuatro programas licenciados por el estado en dos campus de NYC. Planes de pago semanales flexibles en cada opción."})}</p><div class="grid">{progs}</div><div class="btn-wrap" style="justify-content:flex-start;margin-top:22px"><a class="btn btn-primary" href="/programs">{bi(UI["view_all_programs"])}</a><a class="btn btn-ghost" href="/programs">{bi(UI["class_schedule"])}</a></div></div></section>
{_campus_split()}
<section class="stats-band"><div class="container"><div class="eyebrow-acc center">{bi({"en":"By the numbers","es":"En cifras"})}</div><h2 class="center" style="margin-bottom:24px">{bi({"en":"Built on three decades","es":"Construido sobre tres décadas"})}</h2><div class="stats-grid">
<div class="stat-card"><b class="count" data-target="30" data-suffix="+">0</b><span class="label">{bi({"en":"Years in business","es":"Años en activo"})}</span></div>
<div class="stat-card"><b class="count" data-target="10000" data-suffix="+">0</b><span class="label">{bi({"en":"Graduates trained","es":"Graduados entrenados"})}</span></div>
<div class="stat-card"><b class="count" data-target="90" data-suffix="%+">0</b><span class="label">{bi({"en":"Job placement rate","es":"Tasa de colocación"})}</span></div>
<div class="stat-card"><b class="count" data-target="2" data-suffix="">0</b><span class="label">{bi({"en":"NYC campuses","es":"Campus en NYC"})}</span></div>
</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Why Choose ABI","es":"Por Qué Elegir ABI"})}</div><h2 style="margin-bottom:18px">{bi({"en":"Everything you need to succeed","es":"Todo lo que necesitas para triunfar"})}</h2><div class="grid">{why}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Schedule & Tuition","es":"Horario y Matrícula"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three flexible schedules","es":"Tres horarios flexibles"})}</h2><div class="grid">{sched}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi(ce["headline"])}</div><h2 style="margin-bottom:14px">{bi({"en":"What barbers earn","es":"Lo que ganan los barberos"})}</h2><div class="grid">{earn}</div><p class="lead" style="margin-top:14px;font-size:.84rem">{bi(ce["note"])}</p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Where Our Graduates Work","es":"Dónde Trabajan Nuestros Graduados"})}</div><h2 style="margin-bottom:12px">{bi({"en":"From our chairs to NYC's best shops","es":"De nuestras sillas a las mejores barberías de NYC"})}</h2><p class="lead">{grads}.</p><p><a class="btn btn-ghost" href="/partners">{bi({"en":"Meet our partner shops →","es":"Conoce nuestras barberías aliadas →"})}</a></p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Student voices","es":"Voces estudiantiles"})}</div><h2 style="margin-bottom:18px">{bi({"en":"What our students say","es":"Lo que dicen nuestros estudiantes"})}</h2><div class="grid">{tcards}</div></div></section>
{home_contact_section()}'''}


def p_about():
    instr = "".join(_instructor_card(i) for i in CONTENT["instructors"][:3])
    why = "".join(f'<div class="card"><h3 style="margin-bottom:8px">{bi(w["title"])}</h3><p style="color:var(--mut)">{bi(w["desc"])}</p></div>' for w in CONTENT["why_choose"])
    return {"path": "/about",
            "eyebrow": bi({"en": "About ABI", "es": "Acerca de ABI"}),
            "h1": bi({"en": "30+ years. 10,000+ graduates. One craft.", "es": "30+ años. 10,000+ graduados. Un oficio."}),
            "sub": bi({"en": "American Barber Institute is New York's only dedicated barber school — changing lives in Manhattan and the Bronx for over three decades.", "es": "American Barber Institute es la única escuela de barbería dedicada de Nueva York — cambiando vidas en Manhattan y el Bronx por más de tres décadas."}),
            "body": f'''<section><div class="container"><div class="grid-2">
<div><h2>{bi({"en":"Our story","es":"Nuestra historia"})}</h2><p class="lead">{bi({"en":"ABI was built on a simple idea: barbering deserves a school that does <em>only</em> barbering. No nails. No esthetics. No detours. Just the craft, taught by master barbers, on a working clinic floor.","es":"ABI fue construida con una idea simple: la barbería merece una escuela que se dedique <em>solo</em> a la barbería. Sin uñas. Sin estética. Sin desvíos. Solo el oficio, enseñado por maestros barberos."})}</p><p class="lead">{bi({"en":"Three decades and ten thousand graduates later, that idea has produced the people behind some of New York's most respected shops.","es":"Tres décadas y diez mil graduados después, esa idea ha producido a las personas detrás de algunas de las barberías más respetadas de Nueva York."})}</p></div>
<div class="card"><h3 style="margin-bottom:10px">{bi({"en":"The facility","es":"Las instalaciones"})}</h3><p style="color:var(--mut)">{bi(B["facility"])}.</p>
<div class="row-stat"><div class="s"><b>{B["years_in_business"]}</b><small>{bi({"en":"Years","es":"Años"})}</small></div><div class="s"><b>{B["graduates"]}</b><small>{bi({"en":"Graduates","es":"Graduados"})}</small></div><div class="s"><b>{B["rating"]}</b><small>Google</small></div></div></div>
</div></div></section>
<section class="stats-band"><div class="container"><div class="eyebrow-acc center">{bi({"en":"By the numbers","es":"En cifras"})}</div><h2 class="center" style="margin-bottom:24px">{bi({"en":"Built on three decades.","es":"Construido sobre tres décadas."})}</h2><div class="stats-grid">
<div class="stat-card"><b class="count" data-target="30" data-suffix="+">0</b><span class="label">{bi({"en":"Years in business","es":"Años en activo"})}</span><span class="sublabel">{bi({"en":"NY State licensed","es":"Licenciado por NY"})}</span></div>
<div class="stat-card"><b class="count" data-target="10000" data-suffix="+">0</b><span class="label">{bi({"en":"Graduates trained","es":"Graduados entrenados"})}</span><span class="sublabel">{bi({"en":"& counting","es":"y subiendo"})}</span></div>
<div class="stat-card"><b class="count" data-target="2" data-suffix="">0</b><span class="label">{bi({"en":"NYC campuses","es":"Campus en NYC"})}</span><span class="sublabel">{bi({"en":"Manhattan + Bronx","es":"Manhattan + Bronx"})}</span></div>
<div class="stat-card"><b class="count" data-target="17" data-suffix="">0</b><span class="label">{bi({"en":"Weeks to license","es":"Semanas a la licencia"})}</span><span class="sublabel">{bi({"en":"Full-time track","es":"Tiempo completo"})}</span></div>
</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Leadership","es":"Liderazgo"})}</div><h2 style="margin-bottom:24px">{bi({"en":"The faculty","es":"La facultad"})}</h2><div class="ins-grid">{instr}</div><p style="margin-top:20px"><a class="btn btn-ghost" href="/instructors">{bi({"en":"Meet all instructors →","es":"Conoce a todos →"})}</a></p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Why ABI","es":"Por qué ABI"})}</div><h2 style="margin-bottom:18px">{bi({"en":"What makes us different","es":"Lo que nos hace diferentes"})}</h2><div class="grid">{why}</div></div></section>'''}


def p_programs():
    rows = "".join(_program_card(p) for p in CONTENT["programs"])
    sched = "".join(f'<div class="card"><div class="eyebrow-acc">{bi(s["label"])}</div><h3 style="margin:8px 0">{bi(s["days"])} · {s["time"]}</h3><div class="price-tag" style="font-size:1.5rem">{s["tuition"]}</div><p style="color:var(--mut);font-size:.92rem">{bi(s["plan"])}</p></div>' for s in CONTENT["schedules"])
    steps = "".join(f'<div class="card"><div style="font-size:2.4rem;color:var(--accent);font-weight:800;line-height:1">0{s["step"]}</div><h3 style="margin:8px 0">{bi(s["title"])}</h3><p style="color:var(--mut);font-size:.94rem">{bi(s["desc"])}</p></div>' for s in CONTENT["enrollment_steps"])
    req = "".join(f"<li>{bi(r)}</li>" for r in CONTENT["requirements"])
    return {"path": "/programs",
            "eyebrow": bi({"en": "Programs & Tuition", "es": "Programas y Matrícula"}),
            "h1": f'<span class="nowrap-fit">{bi({"en": "Barber Programs — NYC", "es": "Programas de Barbería — NYC"})}</span>',
            "sub": bi({"en": "Licensed by the New York State Department of Education. New classes start the first Monday of every month.", "es": "Licenciada por el Departamento de Educación del Estado de Nueva York. Las nuevas clases comienzan el primer lunes de cada mes."}),
            "hero_ctas": next_class_counter(),
            "body": f'''<section><div class="container"><h2>{bi({"en":"Choose your program","es":"Elige tu programa"})}</h2><p class="lead">{bi({"en":"Every program is state-licensed and exam-prep ready. Flexible weekly payment plans on every track.","es":"Cada programa está licenciado por el estado y listo para el examen. Planes de pago semanales flexibles."})}</p><div class="grid">{rows}</div></div></section>
{_campus_split()}
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Schedule & Tuition","es":"Horario y Matrícula"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three flexible schedules","es":"Tres horarios flexibles"})}</h2><div class="grid">{sched}</div><p style="margin-top:18px;color:var(--mut);font-size:.92rem">{bi({"en":"Start your barber journey today for only $150 per week. GI Bill® and ACCES-VR accepted.","es":"Comienza tu camino de barbero hoy por solo $150 por semana. GI Bill® y ACCES-VR aceptados."})} <a href="/resources" style="color:var(--accent);text-decoration:underline">{bi({"en":"See full benefits guide →","es":"Ver guía completa →"})}</a></p></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Enrollment","es":"Inscripción"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Three steps to your first chair","es":"Tres pasos a tu primer sillón"})}</h2><div class="grid">{steps}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Requirements","es":"Requisitos"})}</div><h2 style="margin-bottom:14px">{bi({"en":"Documents to enroll","es":"Documentos para inscribirte"})}</h2><ul class="list-clean" style="max-width:680px">{req}</ul></div></section>'''}


def p_resources():
    r = CONTENT["resources"]
    def block(b):
        items = "".join(f"<li>{bi(i)}</li>" for i in b.get("items", []))
        intro = f'<p style="color:var(--mut);margin-bottom:14px">{bi(b["intro"])}</p>' if b.get("intro") else ""
        title = bi(b["title"]) if isinstance(b["title"], dict) else b["title"]
        return f'<div class="card"><h3 style="margin-bottom:10px">{title}</h3>{intro}<ul class="list-clean">{items}</ul></div>'
    cards = block(r["accesvr"]) + block(r["veterans"]) + block(r["licensing"]) + block(r["tools"])
    return {"path": "/resources",
            "eyebrow": bi({"en": "Resources", "es": "Recursos"}),
            "h1": bi({"en": "Student Resources", "es": "Recursos para Estudiantes"}),
            "sub": bi({"en": "Financial assistance options, licensing information, and everything you need to make the most of your ABI education.", "es": "Opciones de asistencia financiera, información de licencias, y todo lo que necesitas para aprovechar tu educación en ABI."}),
            "body": f'''<section><div class="container"><div class="grid-2">{cards}</div></div></section>
<section><div class="container center"><h2 style="margin-bottom:14px">{bi({"en":"Need help navigating your options?","es":"¿Necesitas ayuda con tus opciones?"})}</h2><p class="lead" style="margin:0 auto 20px">{bi({"en":"Our admissions team can guide you through financial assistance applications, VA benefits, and enrollment paperwork. Don't let finances be a barrier to your future.","es":"Nuestro equipo de admisiones puede guiarte por las solicitudes de asistencia financiera, beneficios de la VA, y la documentación de inscripción. No dejes que las finanzas sean una barrera para tu futuro."})}</p><div class="btn-wrap"><a class="btn btn-primary" href="/contact">{bi(UI["talk_admissions"])}</a><a class="btn btn-ghost" href="/faq">{bi(UI["read_faq"])}</a></div></div></section>'''}


def p_jobplacement():
    j = CONTENT["job_placement"]
    services = "".join(f"<li>{bi(s)}</li>" for s in j["services"])
    stats = "".join(f'<div class="stat-card"><b style="display:block;font-size:clamp(1.8rem,6vw,3rem);color:var(--accent);font-weight:900;font-family:var(--font-head);line-height:1">{bi(s["value"]) if isinstance(s["value"], dict) else s["value"]}</b><span class="label">{bi(s["label"])}</span></div>' for s in j["stats"])
    return {"path": "/job-placement",
            "eyebrow": bi({"en": "Career Placement Program", "es": "Programa de Colocación Profesional"}),
            "h1": bi(j["headline"]),
            "sub": bi(j["intro"]),
            "body": f'''<section class="stats-band"><div class="container"><div class="stats-grid">{stats}</div></div></section>
<section><div class="container"><div class="grid-2"><div><h2>{bi({"en":"What our placement office offers","es":"Lo que ofrece nuestra oficina de colocación"})}</h2><ul class="list-clean">{services}</ul></div>
<div class="card"><p class="quote" style="font-style:italic;color:var(--ink);font-size:1.15rem;margin-bottom:12px">“{bi(j["testimonial"]["quote"])}”</p><p style="font-weight:800">— {j["testimonial"]["name"]}</p><p style="color:var(--accent);font-size:.84rem">{bi(j["testimonial"]["role"])}</p></div></div></div></section>
<section><div class="container"><div class="grid-2">
<div class="card"><h3 style="margin-bottom:8px">{bi(j["browse"]["title"])}</h3><p style="color:var(--mut);margin-bottom:16px">{bi(j["browse"]["desc"])}</p><a class="btn btn-primary" href="/partners">{bi({"en":"See partner shops →","es":"Ver barberías aliadas →"})}</a></div>
<div class="card"><h3 style="margin-bottom:8px">{bi(j["employers"]["title"])}</h3><p style="color:var(--mut);margin-bottom:16px">{bi(j["employers"]["desc"])}</p><a class="btn btn-ghost" href="/contact">{bi(UI["talk_admissions"])}</a></div>
</div></div></section>'''}


def p_haircuts():
    hc = CONTENT["haircut_clinic"]
    c1, c2 = CONTENT["campuses"]
    services = "".join(f'<span class="hc-pill">{bi(s)}</span>' for s in hc["services"])
    steps = [
        ({"en": "Call or walk in", "es": "Llama o ven sin cita"}, {"en": f"Book by phone at {hc['booking_phone']}, or walk in based on availability.", "es": f"Reserva por teléfono al {hc['booking_phone']}, o ven sin cita según disponibilidad."}),
        ({"en": "Tell us your style", "es": "Dinos tu estilo"}, {"en": "Consult with your student barber about exactly the cut you want.", "es": "Consulta con tu barbero estudiante sobre el corte exacto que quieres."}),
        ({"en": "Relax — you're supervised", "es": "Relájate — bajo supervisión"}, {"en": "Every cut is supervised by a NY-licensed instructor on the floor.", "es": "Cada corte es supervisado por un instructor licenciado de NY en el piso."}),
    ]
    step_cards = "".join(f'<div class="card"><div style="font-size:2rem;color:var(--accent);font-weight:800;line-height:1">0{i+1}</div><h3 style="margin:8px 0">{bi(tt)}</h3><p style="color:var(--mut);font-size:.94rem">{bi(dd)}</p></div>' for i, (tt, dd) in enumerate(steps))
    return {"path": "/haircuts",
            "eyebrow": bi({"en": "Student Clinic", "es": "Clínica Estudiantil"}),
            "h1": bi({"en": "Get a fresh cut at ABI.", "es": "Recibe un corte fresco en ABI."}),
            "sub": bi(hc["intro"]),
            "body": f'''<section><div class="container"><div class="eyebrow-acc">{bi({"en":"How it works","es":"Cómo funciona"})}</div><h2 style="margin-bottom:18px">{bi({"en":"Three steps to the chair","es":"Tres pasos al sillón"})}</h2><div class="grid">{step_cards}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Styles available","es":"Estilos disponibles"})}</div><h2 style="margin-bottom:16px">{bi({"en":"Every cut, every style","es":"Cada corte, cada estilo"})}</h2><div class="hc-pills">{services}</div></div></section>
<section><div class="container"><div class="grid-2">
<div class="card"><h3 style="margin-bottom:10px">{bi({"en":"Visit us","es":"Visítanos"})}</h3><p style="color:var(--mut);margin-bottom:8px">{bi(c1["name"])} — 48 W 39th St · {bi(c2["name"])} — 121 Westchester Sq</p>
<p style="margin-bottom:6px"><a href="tel:{tel(hc["booking_phone"])}" style="color:var(--accent);font-weight:800;font-size:1.05rem">{hc["booking_phone"]}</a></p>
<p style="color:var(--mut);font-size:.9rem;margin-bottom:14px">{hc["hours"]}</p>
<a class="btn btn-primary" href="tel:{tel(hc["booking_phone"])}">{bi(UI["book_chair"])}</a></div>
<div class="card"><h3 style="margin-bottom:10px">{bi({"en":"What to expect","es":"Qué esperar"})}</h3><p style="color:var(--mut);line-height:1.7">{bi(hc["what_to_expect"])}</p><p style="color:var(--mut);font-size:.84rem;margin-top:12px;opacity:.85">{bi({"en":"Haircuts are performed by students under the supervision of licensed instructors. Student barbers are not yet licensed professionals.","es":"Los cortes son realizados por estudiantes bajo la supervisión de instructores licenciados. Los barberos estudiantes aún no son profesionales licenciados."})}</p></div>
</div></div></section>'''}


def p_gallery():
    imgs = GALLERY_FILES[:30]
    tiles = "".join(f'<a class="gallery-tile" href="/assets/img/{f}" target="_blank" rel="noopener"><img src="/assets/img/{f}" loading="lazy" alt="ABI student work"></a>' for f in imgs)
    return {"path": "/gallery",
            "eyebrow": bi({"en": "On the floor", "es": "En el piso"}),
            "h1": bi({"en": "Student work. Clinic life. Graduation day.", "es": "Trabajo de estudiantes. Vida en la clínica. Día de graduación."}),
            "sub": bi({"en": "A glimpse inside the American Barber Institute. Real students. Real chairs. Real fades.", "es": "Un vistazo al interior de American Barber Institute. Estudiantes reales. Sillas reales. Degradados reales."}),
            "body": f'<section><div class="container"><div class="gallery-grid">{tiles}</div></div></section>'}


def p_blog():
    bl = CONTENT["blog"]
    fe = bl["featured"]
    highlights = "".join(
        f'<a class="card" href="/programs" style="display:block"><div class="eyebrow-acc">{bi(h["tag"])}</div>'
        f'<h3 style="margin:8px 0">{bi(h["title"])}</h3><p style="color:var(--mut);margin-bottom:10px">{bi(h["desc"])}</p>'
        f'<p style="color:var(--accent);font-weight:800;font-size:.86rem">{bi(h["meta"])} · {bi({"en":"Explore program →","es":"Ver programa →"})}</p></a>'
        for h in bl["highlights"]
    )
    articles = "".join(
        f'<a class="card" href="/blog/{a["slug"]}" style="display:block"><div class="eyebrow-acc">{bi(a["date"])}</div>'
        f'<h3 style="margin:8px 0">{bi(a["title"])}</h3>'
        f'<p style="color:var(--mut);font-size:.94rem">{bi(a["excerpt"])}</p>'
        f'<p style="color:var(--accent);font-weight:800;font-size:.84rem;margin-top:10px">{bi({"en":"Read article →","es":"Leer artículo →"})}</p></a>'
        for a in bl["articles"]
    )
    return {"path": "/blog",
            "eyebrow": bi(bl["eyebrow"]),
            "h1": bi(bl["headline"]),
            "sub": bi(bl["intro"]),
            "body": f'''<section><div class="container"><a class="card" href="/blog/{fe["slug"]}" style="border-color:var(--accent);display:block">
<div class="eyebrow-acc">{bi({"en":"Featured · Latest Article","es":"Destacado · Último Artículo"})}</div>
<h2 style="margin:10px 0">{bi(fe["title"])}</h2>
<p style="color:var(--accent);font-weight:700;font-size:.84rem;margin-bottom:12px">{bi(fe["date"])} · {bi(fe["read"])}</p>
<p style="color:var(--mut);max-width:760px">{bi(fe["excerpt"])}</p>
<p style="color:var(--accent);font-weight:800;font-size:.86rem;margin-top:12px">{bi({"en":"Read article →","es":"Leer artículo →"})}</p></a></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"From the programs","es":"De los programas"})}</div><h2 style="margin-bottom:16px">{bi({"en":"Built around real training","es":"Basado en entrenamiento real"})}</h2><div class="grid-2">{highlights}</div></div></section>
<section><div class="container"><div class="eyebrow-acc">{bi({"en":"Latest articles","es":"Últimos artículos"})}</div><h2 style="margin-bottom:18px">{bi({"en":"More from the journal","es":"Más del diario"})}</h2><div class="grid">{articles}</div></div></section>'''}


def article_pages():
    """One pdata per blog article — each rendered to <slug>/blog/<article-slug>.html."""
    bl = CONTENT["blog"]
    pages = []
    for a in [bl["featured"]] + bl["articles"]:
        paras = "".join(f'<p style="margin-bottom:16px">{bi(p)}</p>' for p in a["body"])
        meta = bi(a["date"]) + (f' · {bi(a["read"])}' if a.get("read") else "")
        body = (f'<section><div class="container" style="max-width:760px">'
                f'<p style="color:var(--accent);font-weight:700;font-size:.86rem;margin-bottom:20px">{meta}</p>'
                f'<div style="color:var(--mut);font-size:1.05rem;line-height:1.85">{paras}</div>'
                f'<p style="margin-top:30px"><a class="btn btn-ghost" href="/blog">← {bi({"en": "Back to the Journal", "es": "Volver al Diario"})}</a></p>'
                f'</div></section>')
        title = (a["title"]["en"] if isinstance(a["title"], dict) else a["title"]) + " · ABI Journal"
        pdata = {"path": f"/blog/{a['slug']}", "title": title, "eyebrow": bi(bl["eyebrow"]),
                 "h1": bi(a["title"]), "sub": bi(a["excerpt"]), "body": body}
        pages.append((a["slug"], pdata, a))
    return pages


def p_partners():
    def card(p):
        img = (f'<div class="img-wrap"><img src="/assets/partners/{p["image"]}" loading="lazy" alt="{bt(p["name"])} — American Barber Institute partner shop"></div>') if p.get("image") else ""
        phone = (f'<p class="p-phone"><a href="tel:{tel(p["phone"])}">{p["phone"]}</a></p>') if p.get("phone") else ""
        loc = f'<div class="locations">{p["locations"]}</div>' if p.get("locations") else ""
        return (f'<div class="card partner-card">{img}<div class="body">'
                f'<h3 class="partner-title">{p["name"]}</h3>{loc}'
                f'<p class="desc">{bi(p["desc"])}</p>'
                f'<p class="why">→ {bi(p["why"])}</p>{phone}</div></div>')
    cards = "".join(card(p) for p in CONTENT["partners"])
    return {"path": "/partners",
            "eyebrow": bi({"en": "Partner Shops", "es": "Barberías Aliadas"}),
            "h1": bi({"en": "Where ABI graduates work.", "es": "Dónde trabajan los graduados de ABI."}),
            "sub": bi({"en": "Real shops. Real owners. Many of them started right here on the ABI clinic floor.", "es": "Barberías reales. Dueños reales. Muchos comenzaron aquí mismo en el piso clínico de ABI."}),
            "body": f'<section><div class="container"><div class="grid-2">{cards}</div></div></section>'}


def p_instructors():
    mh = [i for i in CONTENT["instructors"] if i["team"]["en"] == "Manhattan"]
    bx = [i for i in CONTENT["instructors"] if i["team"]["en"] == "Bronx"]
    def group(title, lst):
        cards = "".join(_instructor_card(i) for i in lst)
        return (f'<section><div class="container"><div class="eyebrow-acc">{bi(title)}</div>'
                f'<h2 style="margin-bottom:20px">{bi(title)}</h2><div class="ins-grid">{cards}</div></div></section>')
    body = (group({"en": "Manhattan Campus", "es": "Campus de Manhattan"}, mh)
            + group({"en": "Bronx Campus", "es": "Campus del Bronx"}, bx))
    return {"path": "/instructors",
            "eyebrow": bi({"en": "Faculty", "es": "Profesorado"}),
            "h1": bi({"en": "Master barbers. Master teachers.", "es": "Maestros barberos. Maestros instructores."}),
            "sub": bi({"en": "Decades of working-floor experience and a clinic-first teaching style. You learn by chair time, with an instructor inches away.", "es": "Décadas de experiencia en el piso y un estilo de enseñanza centrado en la clínica. Aprendes con tiempo en la silla."}),
            "body": body}


def p_faq():
    items = "".join(f'<details class="card"><summary>{bi(q["q"])}</summary><p style="margin-top:12px;color:var(--mut);line-height:1.7">{bi(q["a"])}</p></details>' for q in CONTENT["faqs"])
    return {"path": "/faq",
            "eyebrow": bi({"en": "FAQs", "es": "Preguntas Frecuentes"}),
            "h1": bi({"en": "Frequently asked questions.", "es": "Preguntas frecuentes."}),
            "sub": bi({"en": "Tuition, schedule, licensing, GI Bill®, ACCES-VR, job placement.", "es": "Matrícula, horario, licencias, GI Bill®, ACCES-VR, colocación laboral."}),
            "body": f'<section><div class="container" style="max-width:820px">{items}</div></section>'}


def p_contact():
    c1, c2 = CONTENT["campuses"]
    return {"path": "/contact",
            "eyebrow": bi({"en": "Contact", "es": "Contacto"}),
            "h1": bi({"en": "Visit ABI.", "es": "Visita ABI."}),
            "sub": bi({"en": "Two campuses across NYC. Call, walk in, or send a message — admissions responds same-day.", "es": "Dos campus en NYC. Llama, ven sin cita, o envía un mensaje — admisiones responde el mismo día."}),
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
<section><div class="container"><div class="card" style="max-width:680px;margin:0 auto"><h2 style="margin-bottom:8px">{bi({"en":"Request information","es":"Solicita información"})}</h2><p style="color:var(--mut);margin-bottom:22px">{bi({"en":"Fill out the form and an ABI admissions agent will call you within 24 hours.","es":"Completa el formulario y un agente de admisiones de ABI te llamará dentro de 24 horas."})}</p><form action="https://formsubmit.co/{B["email"]}" method="POST" class="form-grid" novalidate>
<input type="hidden" name="_subject" value="New ABI website inquiry">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_next" value="{FORM_NEXT}">
<input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
<div class="row-2"><div class="field-group"><label for="f-first">{bi({"en":"First name","es":"Nombre"})} *</label><input required id="f-first" name="firstName" autocomplete="given-name" placeholder="John / Juan" class="input"></div><div class="field-group"><label for="f-last">{bi({"en":"Last name","es":"Apellido"})} *</label><input required id="f-last" name="lastName" autocomplete="family-name" placeholder="Smith / Garcia" class="input"></div></div>
<div class="row-2"><div class="field-group"><label for="f-email">Email *</label><input required id="f-email" name="email" type="email" autocomplete="email" inputmode="email" placeholder="you@example.com" class="input"></div><div class="field-group"><label for="f-phone">{bi({"en":"Phone","es":"Teléfono"})} *</label><input required id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(212) 555-0123" class="input"></div></div>
<div class="field-group"><label>{bi({"en":"Preferred language","es":"Idioma preferido"})}</label><div class="radio-row"><label class="radio-pill"><input type="radio" name="lang" value="EN" checked><span>English</span></label><label class="radio-pill"><input type="radio" name="lang" value="ES"><span>Español</span></label></div></div>
<div class="field-group"><label>{bi({"en":"Best way to reach you","es":"Cómo prefieres que te contactemos"})}</label><div class="radio-row"><label class="radio-pill"><input type="radio" name="contactBy" value="call" checked><span>{bi({"en":"Call","es":"Llamada"})}</span></label><label class="radio-pill"><input type="radio" name="contactBy" value="text"><span>{bi({"en":"Text","es":"Texto"})}</span></label><label class="radio-pill"><input type="radio" name="contactBy" value="email"><span>Email</span></label></div></div>
<div class="row-2"><div class="field-group"><label for="f-program">{bi({"en":"Program of interest","es":"Programa de interés"})}</label><select id="f-program" name="program" class="input"><option>500-Hour Master Barber (Manhattan)</option><option>500-Hour Master Barber (Bronx)</option><option>50-Hour Refresher</option><option>3-Hour Contagious Diseases</option><option>{bi({"en":"Not sure yet","es":"Aún no estoy seguro"})}</option></select></div><div class="field-group"><label for="f-schedule">{bi({"en":"Preferred schedule","es":"Horario preferido"})}</label><select id="f-schedule" name="schedule" class="input"><option>{bi({"en":"Morning (Mon–Fri 8AM–2PM)","es":"Mañana (Lun–Vie 8AM–2PM)"})}</option><option>{bi({"en":"Afternoon (Mon–Fri 2PM–8PM)","es":"Tarde (Lun–Vie 2PM–8PM)"})}</option><option>{bi({"en":"Weekend (Sat–Sun 9AM–7PM)","es":"Fin de Semana (Sáb–Dom 9AM–7PM)"})}</option><option>{bi({"en":"Flexible","es":"Flexible"})}</option></select></div></div>
<div class="field-group"><label for="f-funding">{bi({"en":"Funding (optional)","es":"Financiamiento (opcional)"})}</label><select id="f-funding" name="funding" class="input"><option>{bi({"en":"Self-pay / weekly plan","es":"Pago propio / plan semanal"})}</option><option>GI Bill® (Post-9/11 / VR&E / Montgomery / DEA)</option><option>ACCES-VR</option><option>{bi({"en":"Not sure yet","es":"Aún no estoy seguro"})}</option></select></div>
<div class="field-group"><label for="f-msg">{bi({"en":"What would you like to know?","es":"¿Qué te gustaría saber?"})}</label><textarea id="f-msg" name="message" placeholder="{bt({"en":"Optional — any questions for admissions","es":"Opcional — preguntas para admisiones"})}" rows="4" class="input" style="resize:vertical"></textarea></div>
<div class="form-cta"><button type="submit" class="btn btn-primary">{bi({"en":"Send to admissions","es":"Enviar a admisiones"})}</button><p class="privacy">{bi({"en":"We respond same-day during business hours. Never spam.","es":"Respondemos el mismo día en horario laboral. Nunca spam."})}</p></div>
</form></div></div></section>'''}


PAGE_BUILDERS = {
    "home": ("index.html", p_home),
    "about": ("about.html", p_about),
    "programs": ("programs.html", p_programs),
    "resources": ("resources.html", p_resources),
    "faq": ("faq.html", p_faq),
    "jobplacement": ("job-placement.html", p_jobplacement),
    "haircuts": ("haircuts.html", p_haircuts),
    "gallery": ("gallery.html", p_gallery),
    "blog": ("blog.html", p_blog),
    "partners": ("partners.html", p_partners),
    "instructors": ("instructors.html", p_instructors),
    "contact": ("contact.html", p_contact),
}


def route_assets(html, site):
    """Point every local /assets/... URL at the shared asset host, so sites carry no media."""
    html = html.replace("/assets/showcase/", f"{ASSET_BASE}/showcase/")
    html = html.replace("/assets/instructors/", f"{ASSET_BASE}/instructors/")
    html = html.replace("/assets/partners/", f"{ASSET_BASE}/partners/")
    html = html.replace("/assets/img/", f"{ASSET_BASE}/img/")
    html = html.replace("/assets/favicon.png", f"{ASSET_BASE}/logos/{site.get('favicon', site['logo'])}")
    html = html.replace("/assets/og.png", f"{ASSET_BASE}/logos/{site.get('og', site['logo'])}")
    html = html.replace("/assets/logo.jpeg", f"{ASSET_BASE}/logos/{site['logo']}")
    html = html.replace("/assets/bg.mp4", f"{ASSET_BASE}/videos/{site['video']}")
    return html


def build_site(tokens, site, extra_css=""):
    """Generate one full site (all 11 pages + sitemap/robots/vercel.json). Called by <slug>/build.py."""
    slug = site["slug"]
    site_dir = ROOT / slug
    site_dir.mkdir(parents=True, exist_ok=True)
    site_index = site.get("site_index", 0)
    global FORM_NEXT
    FORM_NEXT = f"https://{site['vercel_name']}.vercel.app/contact"

    (site_dir / ".vercelignore").write_text("assets/\n")

    for key, (fname, fn) in PAGE_BUILDERS.items():
        pdata = fn()
        pdata["_extra_css"] = extra_css
        html = route_assets(render_page(tokens, key, pdata, site_index), site)
        (site_dir / fname).write_text(html, encoding="utf-8")

    # Blog article pages -> <slug>/blog/<article-slug>.html (cleanUrls serves them at /blog/<slug>)
    blog_dir = site_dir / "blog"
    blog_dir.mkdir(exist_ok=True)
    article_paths = []
    for aslug, pdata, art in article_pages():
        pdata["_extra_css"] = extra_css
        html = route_assets(render_page(tokens, "blog", pdata, site_index, article=art), site)
        (blog_dir / f"{aslug}.html").write_text(html, encoding="utf-8")
        article_paths.append(f"/blog/{aslug}")

    base = f"https://{site['vercel_name']}.vercel.app"
    paths = [p for _, p in NAV_ITEMS] + article_paths
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in paths:
        sm += f'  <url><loc>{base}{p}</loc><changefreq>weekly</changefreq><priority>{"1.0" if p == "/" else "0.7"}</priority></url>\n'
    sm += "</urlset>\n"
    (site_dir / "sitemap.xml").write_text(sm)
    (site_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    (site_dir / "vercel.json").write_text(json.dumps({"cleanUrls": True, "trailingSlash": False, "headers": [
        {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        {"source": "/(.*).html", "headers": [{"key": "Cache-Control", "value": "public, max-age=300, must-revalidate"}]},
    ]}, indent=2))
    print(f"  OK {slug}: 12 pages + {len(article_paths)} blog articles, mobile-first responsive")
