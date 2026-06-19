#!/usr/bin/env python3
"""Standalone build file for Chrome Liquid (07-chrome-liquid).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 07-chrome-liquid/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 07-chrome-liquid ----
TOKENS = {
    "slug": "07-chrome-liquid",
    "logo_dark_bg": False,
    "bg": "#ece9e3",
    "bg2": "#ffffff",
    "ink": "#0a0a0a",
    "mut": "#5a5e66",
    "accent": "#1a3cff",
    "accent2": "#0a0a0a",
    "accent3": "#1a3cff",
    "line": "rgba(0,0,0,.16)",
    "glass": "rgba(236,233,227,.82)",
    "body_font": "'Archivo',sans-serif",
    "heading_font": "'Anton',sans-serif",
    "heading_ls": ".01em",
    "heading_lh": "1.04",
    "card_radius": "0",
    "button_radius": "0",
    "button_shape": "sharp",
    "ribbon_bg": "#1a3cff",
    "ribbon_color": "#ece9e3",
    "ribbon_text": "AMERICAN BARBER INSTITUTE · FLAT. BOLD. NEW YORK. · 30+ YEARS · MANHATTAN + BRONX",
    "decoration": "flat-brutalist",
    "vibe": "Flat brutalist on warm beige with electric blue and black borders",
    "h1_effect": "flat",
    "media_style": "brutal-offset"
}

# ---- site identity ----
SITE = {
    "slug": "07-chrome-liquid",
    "vercel_name": "abi-app-7",
    "logo": "site-07-mono.jpeg",
    "video": "urban_motion_graphic_new_york.mp4",
    "site_index": 6,
    "favicon": "site-07-mono-favicon.png",
    "og": "site-07-mono-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Flat-brutalist canvas: hard offset shadows, thick borders, blocky dividers.
# All colors via color-mix(); motion gated behind prefers-reduced-motion;
# a mobile override tames the brutal-offset media translate so it never
# pushes past the viewport edge at small widths.
SITE_CSS = (
    "/* ===== 07-chrome-liquid · LIGHT FLAT BRUTALIST + CHROME ===== */"
    # ---------------------------------------------------------------------------
    # Design language: warm beige paper, ink-black hard borders, electric-blue
    # accent, hard offset shadows (no blur), oversized numerals & uppercase
    # labels, structural grid lines, and a pure-CSS animated chrome/grid backdrop.
    # ---------------------------------------------------------------------------

    # -- contrast hardening: darker muted ink for small-text legibility on beige --
    ":root{--mut:#3f444c;--abi-paper:#ece9e3}"

    # -- 1) ANIMATED BACKGROUND: a slowly-scrolling structural grid + a single
    #       chrome diagonal sheen drifting across it. Pure CSS, gated by RM. --
    "body::before{content:'';position:fixed;inset:-2px;z-index:0;pointer-events:none;"
    "background-image:"
    "linear-gradient(color-mix(in srgb,var(--ink) 8%,transparent) 1.5px,transparent 1.5px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--ink) 8%,transparent) 1.5px,transparent 1.5px);"
    "background-size:48px 48px;background-position:0 0;opacity:.55}"
    "body::after{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;"
    "background:linear-gradient(115deg,transparent 38%,"
    "color-mix(in srgb,var(--accent) 9%,transparent) 47%,"
    "color-mix(in srgb,#ffffff 70%,transparent) 50%,"
    "color-mix(in srgb,var(--accent) 9%,transparent) 53%,transparent 62%);"
    "background-size:300% 300%;mix-blend-mode:multiply;opacity:.6}"
    "@media (prefers-reduced-motion:no-preference){"
    "body::before{animation:abiGridDrift 24s linear infinite}"
    "body::after{animation:abiChromeSheen 14s ease-in-out infinite}"
    "@keyframes abiGridDrift{to{background-position:48px 48px}}"
    "@keyframes abiChromeSheen{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}"
    "}"
    # keep the engine deco-flat subtle so the grid reads as the primary backdrop
    ".deco-flat{opacity:.6}"

    # -- 2) HEADER: turn the sticky header into a hard brutalist bar --
    ".site-header{background:color-mix(in srgb,var(--abi-paper) 92%,#fff);"
    "backdrop-filter:none;-webkit-backdrop-filter:none;border-bottom:3px solid var(--ink);"
    "box-shadow:0 4px 0 color-mix(in srgb,var(--ink) 14%,transparent)}"
    ".top-banner{border-bottom:3px solid var(--ink)}"
    ".primary-nav a{border-radius:0;font-weight:800;text-transform:uppercase;letter-spacing:.04em}"
    ".primary-nav a:hover,.primary-nav a.active{background:var(--accent);color:var(--bg)}"
    # logo chip: intentional white block with hard border + offset, not a floating box
    ".brand-mark.logo-light{background:#fff;border:2px solid var(--ink);border-radius:0;"
    "box-shadow:3px 3px 0 var(--accent);padding:3px 7px}"

    # -- 3) LANGUAGE TOGGLE: blocky, hard-edged, ink border + accent active --
    ".lang-toggle{border-radius:0;border:2px solid var(--ink);overflow:hidden}"
    ".lang-toggle button{font-weight:900;letter-spacing:.14em;transition:background .15s,color .15s}"
    ".lang-toggle button.active{background:var(--accent);color:#fff}"
    ".lang-toggle button+button{border-left:2px solid var(--ink)}"

    # -- 4) HERO: oversized flat headline, accent underscore slab, mono eyebrow --
    ".subpage-hero,.hero-home{border-bottom:3px solid var(--ink)}"
    ".subpage-hero h1,.hero-home h1{text-transform:uppercase;font-weight:400;"
    "letter-spacing:-.005em;text-shadow:4px 4px 0 color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".eyebrow{border:2px solid var(--ink);border-radius:0;background:var(--ink);color:#fff;"
    "font-weight:900;letter-spacing:.34em;box-shadow:3px 3px 0 var(--accent)}"
    ".hero-home .eyebrow{box-shadow:3px 3px 0 var(--accent)}"
    # accent slab under the H1
    ".subpage-hero .container::after,.hero-home .container::after{content:'';display:block;"
    "width:84px;height:8px;background:var(--accent);margin:18px auto 0}"

    # -- 5) SECTIONS: alternating paper tone + hard top rule = brutalist bands.
    #       Big ghost numerals stamped on the first three content sections. --
    "main section{border-top:3px solid var(--ink)}"
    "main section:first-of-type{border-top:0}"
    "main section:nth-of-type(even){background:color-mix(in srgb,#fff 60%,var(--abi-paper))}"
    "main section:nth-of-type(odd){background:color-mix(in srgb,var(--abi-paper) 94%,#fff)}"
    "main section .container{position:relative}"
    # stamped oversized section index numeral (decorative, behind content)
    "main section:nth-of-type(2) .container::before,"
    "main section:nth-of-type(3) .container::before,"
    "main section:nth-of-type(4) .container::before{position:absolute;top:-18px;right:6px;z-index:0;"
    "font-family:var(--font-head);font-size:clamp(4rem,16vw,9rem);line-height:.8;font-weight:900;"
    "color:transparent;-webkit-text-stroke:2px color-mix(in srgb,var(--ink) 12%,transparent);"
    "pointer-events:none;letter-spacing:-.04em}"
    "main section:nth-of-type(2) .container::before{content:'01'}"
    "main section:nth-of-type(3) .container::before{content:'02'}"
    "main section:nth-of-type(4) .container::before{content:'03'}"
    "section h2{text-transform:uppercase;font-weight:400}"

    # -- 6) CARDS: thick ink border + hard accent offset shadow (no blur) --
    ".card,.stat-card{background:#fff;border:2.5px solid var(--ink);border-radius:0;"
    "backdrop-filter:none;-webkit-backdrop-filter:none;"
    "box-shadow:7px 7px 0 var(--ink);transition:transform .18s,box-shadow .18s,border-color .18s}"
    ".card:hover,.stat-card:hover{border-color:var(--ink);"
    "box-shadow:11px 11px 0 var(--accent);transform:translate(-3px,-3px)}"
    "details.card{border-radius:0}"
    ".badge{border-radius:0;border:2px solid var(--ink);background:var(--accent);color:#fff;"
    "font-weight:900;box-shadow:2px 2px 0 var(--ink)}"
    ".price-tag{font-family:var(--font-head);font-size:1.9rem;letter-spacing:-.01em}"

    # -- 7) EYEBROW-ACC: offset accent tab block --
    ".eyebrow-acc{position:relative;padding-left:18px;letter-spacing:.26em}"
    ".eyebrow-acc::before{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);"
    "width:10px;height:18px;background:var(--accent);box-shadow:2px 2px 0 var(--ink)}"

    # -- 8) BUTTONS: hard slab, ink border, offset shadow, press-in on hover --
    ".btn{border-radius:0;text-transform:uppercase;font-weight:900;letter-spacing:.04em}"
    ".btn-primary{background:var(--accent);color:#fff;border:2.5px solid var(--ink);"
    "box-shadow:6px 6px 0 var(--ink)}"
    ".btn-primary:hover{filter:none;box-shadow:9px 9px 0 var(--ink);transform:translate(-3px,-3px)}"
    ".btn-primary:active{box-shadow:2px 2px 0 var(--ink);transform:translate(4px,4px)}"
    ".btn-ghost{border:2.5px solid var(--ink);color:var(--ink);background:#fff;"
    "box-shadow:6px 6px 0 var(--accent)}"
    ".btn-ghost:hover{background:var(--ink);color:#fff;box-shadow:9px 9px 0 var(--accent);"
    "transform:translate(-3px,-3px)}"
    ".cta-call{border-radius:0;border:2px solid currentColor;font-weight:900}"

    # -- 9) STATS BAND: oversized numerals, ink accent rail on the left --
    ".stats-band{border-top:3px solid var(--ink);border-bottom:3px solid var(--ink);"
    "background:var(--ink)}"
    ".stats-band .stat-card{background:#fff}"
    ".stat-card .count{font-size:clamp(2.6rem,9vw,4.4rem);font-weight:900;letter-spacing:-.03em;color:var(--ink)}"
    ".stat-card .count::after{content:'';display:block;width:38px;height:6px;background:var(--accent);margin:10px auto 0}"
    ".stat-card .label{letter-spacing:.16em;color:var(--ink)}"
    ".stat-card::before{width:6px;background:var(--accent)}"
    # the .row-stat mini-stats (used in body copy) get the same hard treatment
    ".row-stat .s{border:2px solid var(--ink);border-radius:0;background:#fff;box-shadow:4px 4px 0 var(--ink)}"
    ".row-stat .s b{font-size:clamp(1.6rem,5vw,2.3rem);color:var(--ink)}"

    # -- 10) SHARED COMPONENTS --
    # brand barber-pole (standalone): square it into a hard chrome rail
    ".barber-pole{border-radius:0;border:2px solid var(--ink);box-shadow:2px 2px 0 var(--accent)}"
    # next-class countdown: hard ticket block, oversized digits
    ".next-class{border:2.5px solid var(--ink);border-radius:0;background:#fff;"
    "backdrop-filter:none;-webkit-backdrop-filter:none;box-shadow:7px 7px 0 var(--accent)}"
    ".next-class .nc-label{letter-spacing:.26em}"
    ".next-class .nc-unit{border-radius:0;border:2px solid var(--ink);"
    "background:color-mix(in srgb,var(--accent) 10%,#fff)}"
    ".next-class .nc-unit b{font-size:clamp(1.4rem,4.5vw,2rem);color:var(--ink)}"
    # home contact box: hard split panel
    ".home-contact .hc-box{border:3px solid var(--ink);border-radius:0;background:#fff;"
    "backdrop-filter:none;-webkit-backdrop-filter:none;box-shadow:10px 10px 0 var(--accent)}"
    ".input{border:2px solid var(--ink);border-radius:0;background:#fff}"
    ".input:focus{outline:3px solid var(--accent);outline-offset:0;border-color:var(--ink)}"
    ".field-group label{letter-spacing:.14em}"
    ".radio-pill span,.hc-pill{border-radius:0;border:2px solid var(--ink);background:#fff;font-weight:800}"
    ".radio-pill input:checked+span{background:var(--accent);color:#fff;border-color:var(--ink)}"
    ".radio-pill:hover span,.hc-pill:hover{border-color:var(--ink);color:var(--accent);"
    "box-shadow:3px 3px 0 var(--accent)}"
    # campus split: hard-edged columns
    ".campus-split .campus-col{box-shadow:7px 7px 0 var(--ink)}"
    # instructor cards: hard photo frame
    ".ins-card .ins-photo{border-bottom:2.5px solid var(--ink)}"
    ".ins-card .ins-name{text-transform:uppercase;font-weight:400}"
    # partner cards: hard frame, ink rule under image
    ".partner-card .img-wrap{border-bottom:2.5px solid var(--ink)}"
    ".partner-card .partner-title{text-transform:uppercase;font-weight:400}"
    # gallery tiles: square hard frame
    ".gallery-tile{border:2px solid var(--ink);border-radius:0}"
    ".gallery-tile:hover{box-shadow:6px 6px 0 var(--accent)}"

    # -- 11) MEDIA BAND (brutal-offset): tighten heading, hard caption bar --
    ".media-band{border-top:3px solid var(--ink)}"
    ".media-band .m-head h2{text-transform:uppercase;font-weight:400}"
    ".m-tile .m-cap{background:var(--ink);color:#fff;left:0;right:auto;bottom:0;padding:8px 12px;"
    "text-shadow:none;font-weight:800;text-transform:uppercase;letter-spacing:.06em}"

    # -- 12) LISTS & DETAILS: hard accent markers --
    ".list-clean li::before{content:'';display:inline-block;width:9px;height:9px;"
    "background:var(--accent);margin-right:10px;vertical-align:middle}"
    "details.card summary::after{color:var(--accent)}"

    # -- 13) CTA BAND: full ink slab with reversed colors for a brutal stop block --
    ".cta-band{background:var(--ink);border-top:3px solid var(--ink);border-bottom:6px solid var(--accent)}"
    ".cta-band h2,.cta-band .quote{color:#fff}"
    ".cta-band .eyebrow-acc{color:#fff}"
    ".cta-band .lead{color:color-mix(in srgb,#fff 78%,var(--ink))}"
    ".cta-band .btn-ghost{background:transparent;color:#fff;border-color:#fff;box-shadow:6px 6px 0 var(--accent)}"
    ".cta-band .btn-ghost:hover{background:#fff;color:var(--ink)}"

    # -- 14) FOOTER: hard top rule, blocky social chips --
    ".site-footer{background:color-mix(in srgb,var(--abi-paper) 88%,#fff);border-top:6px solid var(--ink);"
    "color:var(--mut)}"
    ".footer-grid h4{letter-spacing:.16em}"
    ".social-row a{border-radius:0;border:2px solid var(--ink);font-weight:900}"
    ".social-row a:hover{background:var(--accent);border-color:var(--ink);color:#fff}"
    ".footer-logo{border:2px solid var(--ink);border-radius:0;background:#fff;padding:4px}"
    ".sticky-call a{border-radius:0;border:2px solid var(--ink)}"
    ".sticky-call a.call{background:#fff;color:var(--ink)}"
    ".sticky-call a.apply{background:var(--accent);color:#fff}"

    # -- 15) MOBILE: tame hard-offset shadows so nothing pushes past the edge.
    #        PRESERVES the engine's brutal-offset media mobile override. --
    "@media (max-width:600px){"
    ".card,.stat-card{box-shadow:4px 4px 0 var(--ink)}"
    ".card:hover,.stat-card:hover{box-shadow:5px 5px 0 var(--accent);transform:translate(-2px,-2px)}"
    ".btn-primary{box-shadow:4px 4px 0 var(--ink)}"
    ".btn-ghost{box-shadow:4px 4px 0 var(--accent)}"
    ".next-class{box-shadow:5px 5px 0 var(--accent)}"
    ".home-contact .hc-box{box-shadow:6px 6px 0 var(--accent)}"
    ".campus-split .campus-col{box-shadow:4px 4px 0 var(--ink)}"
    ".ms-brutal-offset .m-tile{transform:none;box-shadow:-5px 5px 0 var(--accent)}"
    ".ms-brutal-offset .m-tile.shown{transform:none}"
    ".ms-brutal-offset .m-tile:hover{box-shadow:-5px 5px 0 var(--accent);transform:none}"
    "main section .container::before{font-size:clamp(3rem,18vw,5rem);top:-8px;opacity:.7}"
    "}"

    # -- 16) REDUCED MOTION: kill translate nudges + background animation --
    "@media (prefers-reduced-motion:reduce){"
    ".card:hover,.stat-card:hover,.btn-primary:hover,.btn-ghost:hover{transform:none}"
    "body::before,body::after{animation:none}"
    "}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 07-chrome-liquid.")
