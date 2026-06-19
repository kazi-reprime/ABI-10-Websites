#!/usr/bin/env python3
"""Standalone build file for Midnight HUD (04-midnight-hud).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 04-midnight-hud/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 04-midnight-hud ----
TOKENS = {
    "slug": "04-midnight-hud",
    "logo_dark_bg": True,
    "bg": "#040810",
    "bg2": "rgba(10,18,32,.66)",
    "ink": "#dfeaff",
    "mut": "#6f86ad",
    "accent": "#ffb238",
    "accent2": "#46e6ff",
    "accent3": "#ff7a18",
    "line": "rgba(70,230,255,.18)",
    "glass": "rgba(70,230,255,.07)",
    "body_font": "'Courier New',ui-monospace,monospace",
    "heading_font": "'Arial Black',Impact,sans-serif",
    "heading_ls": ".01em",
    "heading_lh": ".98",
    "card_radius": "6px",
    "button_radius": "4px",
    "button_shape": "clip-blade",
    "ribbon_bg": "#ffb238",
    "ribbon_color": "#040810",
    "ribbon_text": "ABI · TACTICAL TRAINING · OPERATOR-GRADE CRAFT · MANHATTAN + BRONX · FIRST MONDAY START",
    "decoration": "hud-scanlines",
    "vibe": "Tactical sci-fi HUD with amber+cyan on midnight blue, scanlines",
    "h1_effect": "hud",
    "media_style": "hud-reticle"
}

# ---- site identity ----
SITE = {
    "slug": "04-midnight-hud",
    "vercel_name": "abi-app-4",
    "logo": "site-04-badge.jpeg",
    "video": "futuristic_abi_animation_barber_-.mp4",
    "site_index": 3,
    "favicon": "site-04-badge-favicon.png",
    "og": "site-04-badge-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Tactical HUD signature touches. All translucency uses color-mix(...) (NEVER var(--x)NN
# hex-alpha — that was a prior regression). Pseudo-elements .card::before/::after,
# .stat-card::after, .eyebrow-acc::before are confirmed unused by the engine.
SITE_CSS = (
    "/* ===== 04-midnight-hud :: tactical sci-fi HUD ===== */"
    # ---- mono UI font var (reused everywhere a readout/label appears) ----
    ":root{--hud-mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace}"

    # ================================================================
    # SIGNATURE BACKGROUND :: layered tech-grid + scanning sweep + flicker
    # body::before = fixed parallax tech grid (fine + coarse) over a radial glow.
    # body::after  = a single bright scan line that sweeps top->bottom forever.
    # Both pointer-events:none; engine never uses body pseudo-elements.
    # ================================================================
    "body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;"
    "background:"
    "radial-gradient(120% 80% at 50% -10%,color-mix(in srgb,var(--accent2) 11%,transparent),transparent 60%),"
    "radial-gradient(90% 60% at 85% 110%,color-mix(in srgb,var(--accent) 8%,transparent),transparent 55%),"
    "linear-gradient(color-mix(in srgb,var(--accent2) 9%,transparent) 1px,transparent 1px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--accent2) 9%,transparent) 1px,transparent 1px),"
    "linear-gradient(color-mix(in srgb,var(--accent2) 4%,transparent) 1px,transparent 1px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--accent2) 4%,transparent) 1px,transparent 1px);"
    "background-size:100% 100%,100% 100%,72px 72px,72px 72px,18px 18px,18px 18px;"
    "background-position:center;animation:hudGridDrift 26s linear infinite;opacity:.9}"
    "body::after{content:'';position:fixed;left:0;right:0;top:0;height:34vh;z-index:0;pointer-events:none;"
    "background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--accent2) 9%,transparent) 60%,color-mix(in srgb,var(--accent2) 16%,transparent) 92%,transparent);"
    "mix-blend-mode:screen;animation:hudSweep 7.5s cubic-bezier(.45,0,.55,1) infinite,hudFlicker 5.5s steps(1) infinite}"
    "@keyframes hudGridDrift{from{background-position:center,center,0 0,0 0,0 0,0 0}to{background-position:center,center,72px 72px,72px 72px,18px 18px,18px 18px}}"
    "@keyframes hudSweep{0%{transform:translateY(-40vh)}100%{transform:translateY(140vh)}}"
    "@keyframes hudFlicker{0%,93%,100%{opacity:.85}94%{opacity:.55}96%{opacity:.95}98%{opacity:.6}}"
    # corner HUD framing ticks fixed to viewport (cyan L-brackets, pure CSS, decorative)
    ".site-header::after{content:'';position:fixed;top:6px;left:6px;width:26px;height:26px;z-index:60;pointer-events:none;"
    "border-left:1.5px solid color-mix(in srgb,var(--accent2) 50%,transparent);border-top:1.5px solid color-mix(in srgb,var(--accent2) 50%,transparent)}"

    # ---- ensure all real content/chrome sits above the bg layers ----
    ".site-header,main,.site-footer,.cta-band,.media-band,.sticky-call,.lightbox{position:relative;z-index:2}"

    # ================================================================
    # HERO :: targeting readout — mono eyebrow w/ blinking lock dot, HUD h1 glow
    # ================================================================
    ".hero-home,.subpage-hero{position:relative}"
    ".hero-home .eyebrow,.subpage-hero .eyebrow{font-family:var(--hud-mono);border-color:color-mix(in srgb,var(--accent2) 45%,transparent);"
    "color:var(--accent2);background:color-mix(in srgb,var(--accent2) 8%,transparent);clip-path:polygon(8px 0,100% 0,100% calc(100% - 8px),calc(100% - 8px) 100%,0 100%,0 8px)}"
    ".hero-home .eyebrow::before,.subpage-hero .eyebrow::before{content:'\\25C9 ';color:var(--accent);animation:hudBlink 1.6s steps(1) infinite}"
    "@keyframes hudBlink{0%,60%{opacity:1}61%,100%{opacity:.25}}"
    ".hfx-hud h1{text-shadow:0 0 22px color-mix(in srgb,var(--accent) 28%,transparent),0 0 2px color-mix(in srgb,var(--accent2) 50%,transparent)}"
    ".hfx-hud h1 .accent{color:var(--accent);text-shadow:0 0 26px color-mix(in srgb,var(--accent) 55%,transparent)}"

    # ================================================================
    # SECTIONS :: tactical seam lines + mono coordinate stamp on alt sections
    # main section:nth-of-type(odd) gets a faint top scan-rule; (even) a coord tag.
    # ================================================================
    "main section{position:relative}"
    "main section:nth-of-type(odd)>.container::before{content:'';position:absolute;left:clamp(14px,4vw,28px);right:clamp(14px,4vw,28px);top:-2px;height:1px;"
    "background:repeating-linear-gradient(90deg,color-mix(in srgb,var(--accent2) 45%,transparent) 0 14px,transparent 14px 24px)}"
    "main section:nth-of-type(even)>.container::after{content:'[ SEC.0' counter(hudsec) ' \\2022 ABI/NYC ]';counter-increment:hudsec;"
    "position:absolute;right:clamp(14px,4vw,28px);top:-1.4em;font-family:var(--hud-mono);font-size:.6rem;letter-spacing:.22em;"
    "color:color-mix(in srgb,var(--accent2) 70%,transparent);pointer-events:none}"
    "main{counter-reset:hudsec}"

    # ================================================================
    # CARDS :: targeting-reticle corner brackets + clipped polygon corner + scan wash
    # ================================================================
    ".card{position:relative;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px))}"
    ".card::before{content:'';position:absolute;inset:7px;pointer-events:none;z-index:1;border:1.5px solid color-mix(in srgb,var(--accent2) 38%,transparent);"
    "clip-path:polygon(0 0,18px 0,18px 1.5px,1.5px 1.5px,1.5px 18px,0 18px,0 100%,100% 100%,100% calc(100% - 18px),calc(100% - 1.5px) calc(100% - 18px),calc(100% - 1.5px) calc(100% - 1.5px),calc(100% - 18px) calc(100% - 1.5px),calc(100% - 18px) 100%,0 100%);"
    "opacity:.5;transition:opacity .3s,border-color .3s}"
    ".card:hover::before{opacity:1;border-color:color-mix(in srgb,var(--accent) 70%,transparent)}"
    ".card:hover{box-shadow:0 16px 44px rgba(0,0,0,.5),0 0 0 1px color-mix(in srgb,var(--accent) 30%,transparent)}"

    # ================================================================
    # BUTTONS :: clipped tactical blades w/ scan-shimmer on the primary
    # ================================================================
    ".btn{clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px);font-family:var(--hud-mono);"
    "letter-spacing:.06em;text-transform:uppercase;font-weight:800;position:relative;overflow:hidden}"
    ".btn-primary{box-shadow:0 0 18px color-mix(in srgb,var(--accent) 30%,transparent)}"
    ".btn-primary::after{content:'';position:absolute;inset:0;background:linear-gradient(120deg,transparent 30%,color-mix(in srgb,#fff 55%,transparent) 50%,transparent 70%);"
    "transform:translateX(-120%);transition:transform .55s}"
    ".btn-primary:hover::after{transform:translateX(120%)}"
    ".btn-ghost{color:var(--accent2);border-color:var(--accent2)}"
    ".btn-ghost:hover{background:var(--accent2);color:var(--bg)}"

    # ================================================================
    # STATS BAND :: glowing readout numerals + mono cyan labels + scan wash
    # ================================================================
    ".stats-band{position:relative}"
    ".stat-card .label{font-family:var(--hud-mono);color:var(--accent2);letter-spacing:.16em;font-weight:700}"
    ".stat-card .count{text-shadow:0 0 22px color-mix(in srgb,var(--accent) 38%,transparent),0 0 4px color-mix(in srgb,var(--accent) 60%,transparent);font-variant-numeric:tabular-nums}"
    ".stat-card::after{content:'';position:absolute;inset:0;pointer-events:none;z-index:0;"
    "background:repeating-linear-gradient(0deg,transparent 0 3px,color-mix(in srgb,var(--accent2) 6%,transparent) 3px 4px);mix-blend-mode:screen;opacity:.7}"
    ".stat-card>*{position:relative;z-index:1}"

    # ================================================================
    # EYEBROWS + PRICE :: terminal '//' prefix + mono instrument readout
    # ================================================================
    ".eyebrow-acc{font-family:var(--hud-mono)}"
    ".eyebrow-acc::before{content:'// ';color:color-mix(in srgb,var(--accent2) 85%,transparent);font-weight:900}"
    ".price-tag{font-family:var(--hud-mono);font-variant-numeric:tabular-nums;letter-spacing:-.01em;text-shadow:0 0 16px color-mix(in srgb,var(--accent) 26%,transparent)}"

    # ================================================================
    # SHARED COMPONENTS
    # ================================================================
    # -- brand mark + barber pole: dark plate w/ cyan reticle frame --
    ".brand-mark.logo-dark{background:color-mix(in srgb,var(--accent2) 7%,transparent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent2) 28%,transparent)}"
    ".barber-pole{border-color:color-mix(in srgb,var(--accent2) 45%,transparent);box-shadow:0 0 12px color-mix(in srgb,var(--accent2) 30%,transparent),inset 0 0 0 1px rgba(255,255,255,.18)}"
    # -- lang toggle: mono + AA 44px tap target (engine omits min-height) --
    ".lang-toggle{border-radius:0;clip-path:polygon(6px 0,100% 0,100% calc(100% - 6px),calc(100% - 6px) 100%,0 100%,0 6px);font-family:var(--hud-mono)}"
    ".lang-toggle button{min-height:44px;display:inline-flex;align-items:center;justify-content:center}"
    ".lang-toggle button.active{background:color-mix(in srgb,var(--accent) 22%,transparent);color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}"
    # -- next-class countdown: glowing HUD instrument cluster --
    ".next-class{clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px);box-shadow:0 0 0 1px color-mix(in srgb,var(--accent2) 22%,transparent),0 0 28px color-mix(in srgb,var(--accent) 12%,transparent)}"
    ".next-class .nc-label{font-family:var(--hud-mono);color:var(--accent2)}"
    ".next-class .nc-unit{border:1px solid color-mix(in srgb,var(--accent2) 28%,transparent);border-radius:4px}"
    ".next-class .nc-unit b{text-shadow:0 0 16px color-mix(in srgb,var(--accent) 45%,transparent);font-variant-numeric:tabular-nums}"
    ".next-class .nc-unit i{font-family:var(--hud-mono)}"
    # -- home contact: HUD console panel with reticle corner --
    ".home-contact .hc-box{clip-path:polygon(0 0,calc(100% - 16px) 0,100% 16px,100% 100%,16px 100%,0 calc(100% - 16px));position:relative;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent2) 18%,transparent)}"
    ".home-contact .hc-box::before{content:'';position:absolute;top:10px;right:10px;width:20px;height:20px;pointer-events:none;"
    "border-top:1.5px solid color-mix(in srgb,var(--accent) 60%,transparent);border-right:1.5px solid color-mix(in srgb,var(--accent) 60%,transparent)}"
    # -- campus split: mono campus headers + tactical bullet markers --
    ".campus-split .campus-col .campus-progs li::before{content:'\\25B8 ';color:var(--accent2)}"
    ".campus-split .campus-col{position:relative}"
    # -- instructor cards: cyan scan-tint photo + name in heading glow --
    ".ins-card .ins-photo{position:relative}"
    ".ins-card .ins-photo::after{content:'';position:absolute;inset:0;pointer-events:none;"
    "background:repeating-linear-gradient(0deg,transparent 0 3px,color-mix(in srgb,var(--accent2) 7%,transparent) 3px 4px);mix-blend-mode:screen;opacity:.55;transition:opacity .4s}"
    ".ins-card:hover .ins-photo::after{opacity:0}"
    ".ins-card .ins-tags{font-family:var(--hud-mono);color:var(--accent2)}"
    # -- partner cards: name + locations as mono callsign readout --
    ".partner-card .locations{font-family:var(--hud-mono);color:var(--accent2)}"
    ".partner-card .img-wrap .partner-name{font-family:var(--font-head);text-shadow:0 0 18px color-mix(in srgb,var(--accent2) 45%,transparent),0 2px 8px rgba(0,0,0,.7)}"
    ".partner-card .img-wrap::before{content:'';position:absolute;left:10px;top:10px;width:18px;height:18px;z-index:3;pointer-events:none;"
    "border-left:1.5px solid color-mix(in srgb,var(--accent2) 65%,transparent);border-top:1.5px solid color-mix(in srgb,var(--accent2) 65%,transparent)}"
    # -- media band: cyan mono eyebrow + scan-tinted tiles --
    ".media-band .m-head .eyb{font-family:var(--hud-mono);color:var(--accent2)}"

    # ================================================================
    # REDUCED MOTION :: freeze every animation / transition signature
    # ================================================================
    "@media (prefers-reduced-motion:reduce){"
    "body::before{animation:none}"
    "body::after{animation:none;opacity:.18;transform:none}"
    ".hero-home .eyebrow::before,.subpage-hero .eyebrow::before{animation:none}"
    ".card::before,.btn-primary::after,.ins-card .ins-photo::after{transition:none}"
    ".btn-primary::after{display:none}}"

    # ================================================================
    # MOBILE :: lighten brackets, soften grid, no horizontal overflow
    # ================================================================
    "@media (max-width:480px){"
    ".card::before{inset:5px}"
    "body::before{background-size:100% 100%,100% 100%,56px 56px,56px 56px,16px 16px,16px 16px;opacity:.7}"
    "main section:nth-of-type(even)>.container::after{font-size:.54rem;letter-spacing:.16em}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 04-midnight-hud.")
