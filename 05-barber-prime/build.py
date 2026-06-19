#!/usr/bin/env python3
"""Standalone build file for Barber Prime (05-barber-prime).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 05-barber-prime/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 05-barber-prime ----
TOKENS = {
    "slug": "05-barber-prime",
    "logo_dark_bg": True,
    "bg": "#0a0807",
    "bg2": "#13100d",
    "ink": "#f3e9d6",
    "mut": "#9c8f78",
    "accent": "#e8b54a",
    "accent2": "#fff0c4",
    "accent3": "#a87a1e",
    "line": "rgba(232,181,74,.2)",
    "glass": "rgba(10,8,7,.78)",
    "body_font": "Georgia,'Times New Roman',serif",
    "heading_font": "'Times New Roman',Georgia,serif",
    "heading_ls": "-.01em",
    "heading_lh": ".98",
    "card_radius": "3px",
    "button_radius": "2px",
    "button_shape": "sharp",
    "ribbon_bg": "repeating-linear-gradient(45deg,#e8b54a 0 30px,#0a0807 30px 60px)",
    "ribbon_color": "#f3e9d6",
    "ribbon_text": "American Barber Institute · Prime craft. Prime career. · Manhattan + Bronx",
    "decoration": "luxe-gold",
    "vibe": "Black-and-gold luxury with serif typography and barber-pole stripe ribbon",
    "h1_effect": "gold-sheen",
    "media_style": "gold-curtain"
}

# ---- site identity ----
SITE = {
    "slug": "05-barber-prime",
    "vercel_name": "abi-app-5",
    "logo": "site-05-gold.jpeg",
    "video": "gold_abi_monogram_in_dark.mp4",
    "site_index": 4,
    "favicon": "site-05-gold-favicon.png",
    "og": "site-05-gold-og.png"
}

# ---- per-site unique polish (engine appends this last; overrides the engine) ----
# Luxe black + gold serif identity. All accent text already clears WCAG AA on the
# near-black surfaces (#e8b54a => 10.6:1), so polish is purely decorative.
# Rules: color-mix() only (never var(--x)NN), responsive, reduced-motion respected.
SITE_CSS = (
    "/* ===== unique polish for 05-barber-prime — luxe black/gold editorial ===== */"

    # ---- 0) Type: editorial luxury. Tighter serif display, refined body rhythm,
    #         small-caps gold eyebrows, hairline-gold accents on key headings.
    "body{letter-spacing:.005em}"
    "h1,h2,h3{font-weight:700}"
    "h1{letter-spacing:-.018em}"
    ".subpage-hero h1,.hero-home h1{font-size:clamp(2.5rem,7vw,5rem);font-weight:700}"
    "section p.lead,.subpage-hero p.sub{font-style:italic;color:color-mix(in srgb,var(--mut) 88%,var(--ink))}"
    ".eyebrow,.eyebrow-acc,.media-band .m-head .eyb,.next-class .nc-label{font-variant:small-caps;letter-spacing:.34em}"
    ".eyebrow{border-color:color-mix(in srgb,var(--accent) 38%,transparent);"
    "background:color-mix(in srgb,var(--accent) 6%,transparent)}"

    # ---- 1) Animated background: drifting gold bokeh over a deep vignette.
    #         Layered atop the engine's .deco-gold radial. Pure CSS, GPU-cheap,
    #         gated behind prefers-reduced-motion.
    "body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;"
    "background:"
    "radial-gradient(circle at 18% 22%,color-mix(in srgb,var(--accent) 16%,transparent) 0,transparent 9%),"
    "radial-gradient(circle at 82% 30%,color-mix(in srgb,var(--accent2) 13%,transparent) 0,transparent 7%),"
    "radial-gradient(circle at 70% 78%,color-mix(in srgb,var(--accent) 12%,transparent) 0,transparent 8%),"
    "radial-gradient(circle at 32% 84%,color-mix(in srgb,var(--accent2) 10%,transparent) 0,transparent 6%);"
    "background-repeat:no-repeat;opacity:.6;filter:blur(2px)}"
    "body::after{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;"
    "background:radial-gradient(ellipse 120% 80% at 50% -10%,transparent 55%,color-mix(in srgb,#000 60%,transparent) 100%)}"
    "@media (prefers-reduced-motion:no-preference){"
    "body::before{animation:goldDrift 26s ease-in-out infinite alternate}"
    "@keyframes goldDrift{0%{transform:translate3d(0,0,0) scale(1)}"
    "50%{transform:translate3d(-1.5%,2%,0) scale(1.05)}"
    "100%{transform:translate3d(1.5%,-1.5%,0) scale(1.02)}}}"

    # ---- 2) EN/ES toggle: squared gold-underline tabs.
    ".lang-toggle{border-radius:0;border-width:0 0 2px 0;border-color:var(--accent)}"
    ".lang-toggle button{transition:color .25s,box-shadow .25s}"
    ".lang-toggle button.active{background:transparent;color:var(--accent);box-shadow:inset 0 -3px 0 var(--accent)}"

    # ---- 3) Engraved gold rule under section + media headings.
    "section>.container>h2,.media-band .m-head h2{position:relative;padding-bottom:.42em}"
    "section>.container>h2::after,.media-band .m-head h2::after{content:'';position:absolute;"
    "left:0;bottom:0;width:54px;height:2px;"
    "background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 12%,transparent))}"
    ".media-band .m-head h2::after{left:50%;transform:translateX(-50%);"
    "background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 12%,transparent),"
    "var(--accent),color-mix(in srgb,var(--accent) 12%,transparent))}"

    # ---- 4) Hero: a gold foil hairline + small ornamental flourish above the eyebrow.
    ".hero-home .eyebrow,.subpage-hero .eyebrow{position:relative}"
    ".hero-home::after{content:'';display:block;width:120px;height:1px;margin:clamp(26px,5vw,46px) auto 0;"
    "background:linear-gradient(90deg,transparent,var(--accent),transparent)}"

    # ---- 5) Gold-sheen sweep on the primary button.
    ".btn-primary{position:relative;overflow:hidden;letter-spacing:.04em;"
    "box-shadow:0 6px 20px color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".btn-primary::after{content:'';position:absolute;top:0;left:-130%;width:60%;height:100%;"
    "background:linear-gradient(100deg,transparent,color-mix(in srgb,#ffffff 55%,transparent),transparent);"
    "transform:skewX(-18deg);pointer-events:none}"
    ".btn-ghost{letter-spacing:.04em}"
    "@media (prefers-reduced-motion:no-preference){"
    ".btn-primary::after{transition:left .6s cubic-bezier(.7,0,.2,1)}"
    ".btn-primary:hover::after{left:130%}}"

    # ---- 6) Cards: framed luxury. Gold corner-bracket fades in; refined hover lift;
    #         a quiet top gold hairline reads as a foil-stamped frame.
    ".card,.stat-card{position:relative;background:"
    "linear-gradient(180deg,color-mix(in srgb,var(--accent) 4%,transparent),transparent 40%),var(--glass)}"
    ".card::before{content:'';position:absolute;left:0;right:0;top:0;height:1px;"
    "background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 55%,transparent),transparent);"
    "opacity:.5;transition:opacity .3s}"
    ".card:hover{transform:translateY(-6px);box-shadow:0 22px 50px rgba(0,0,0,.5),"
    "0 0 0 1px color-mix(in srgb,var(--accent) 30%,transparent)}"
    ".card:hover::before{opacity:1}"
    ".card::after,.stat-card::after{content:'';position:absolute;top:8px;right:8px;width:14px;height:14px;"
    "border-top:1.5px solid color-mix(in srgb,var(--accent) 70%,transparent);"
    "border-right:1.5px solid color-mix(in srgb,var(--accent) 70%,transparent);"
    "opacity:0;transition:opacity .3s;pointer-events:none}"
    ".card:hover::after,.stat-card:hover::after{opacity:1}"

    # ---- 7) Stats band: gold-foil top/bottom hairlines framing the whole band.
    ".stats-band{border-top:1px solid color-mix(in srgb,var(--accent) 22%,transparent);"
    "border-bottom:1px solid color-mix(in srgb,var(--accent) 22%,transparent);"
    "background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 5%,transparent),transparent)}"

    # ---- 8) Next-class countdown: framed gold ticket with foil units.
    ".next-class{border-color:color-mix(in srgb,var(--accent) 32%,transparent);"
    "box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 10%,transparent),0 10px 30px rgba(0,0,0,.4)}"
    ".next-class .nc-unit{border:1px solid color-mix(in srgb,var(--accent) 24%,transparent)}"

    # ---- 9) Home contact box: framed luxury panel with gold hairline.
    ".home-contact .hc-box{box-shadow:0 18px 48px rgba(0,0,0,.45),"
    "inset 0 0 0 1px color-mix(in srgb,var(--accent) 12%,transparent);position:relative}"
    ".home-contact .hc-box::before{content:'';position:absolute;left:clamp(20px,3.5vw,40px);"
    "right:clamp(20px,3.5vw,40px);top:0;height:2px;"
    "background:linear-gradient(90deg,transparent,var(--accent),transparent)}"

    # ---- 10) Campus split: gold accent bar marking each campus column.
    ".campus-split .campus-col{position:relative;overflow:hidden}"
    ".campus-split .campus-col::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;"
    "background:linear-gradient(180deg,var(--accent),transparent);opacity:.8}"
    ".campus-split .campus-col .campus-progs li::before{color:var(--accent)}"

    # ---- 11) Instructor cards: gold under-line on the photo, refined name treatment.
    ".ins-card .ins-photo{position:relative}"
    ".ins-card .ins-photo::after{content:'';position:absolute;left:0;right:0;bottom:0;height:3px;"
    "background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 8%,transparent))}"
    ".ins-card .ins-name{font-style:normal;letter-spacing:-.01em}"
    ".ins-card .ins-tags{font-variant:small-caps;letter-spacing:.12em}"

    # ---- 12) Partner cards: gold title + foil hairline under image.
    ".partner-card .partner-title,.partner-card .partner-name{font-weight:700}"
    ".partner-card .img-wrap{border-bottom:2px solid color-mix(in srgb,var(--accent) 45%,transparent)}"

    # ---- 13) Media band: framed gold hairline around the band.
    ".media-band{border-top:1px solid color-mix(in srgb,var(--accent) 16%,transparent)}"

    # ---- 14) Links & list ticks: refined gold.
    ".list-clean li::before{color:var(--accent)}"
    ".footer-grid a:hover,.primary-nav a:hover{color:var(--accent2)}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 05-barber-prime.")
