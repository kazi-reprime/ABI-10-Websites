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
    "logo": "luxury_logo_american_barber_inst-.jpeg",
    "video": "gold_abi_monogram_in_dark.mp4",
    "site_index": 4
}

# ---- per-site unique polish (engine appends this last; overrides the engine) ----
# Luxe black + gold serif identity. All accent text already clears WCAG AA on the
# near-black surfaces (#e8b54a => 10.6:1), so polish is purely decorative.
# Rules: color-mix() only (never var(--x)NN), responsive, reduced-motion respected.
SITE_CSS = (
    "/* ===== unique polish for 05-barber-prime — luxe black/gold serif ===== */"

    # 1) EN/ES toggle: squared gold-underline tabs (seed, refined).
    ".lang-toggle{border-radius:0;border-width:0 0 2px 0;border-color:var(--accent)}"
    ".lang-toggle button{transition:color .25s,box-shadow .25s}"
    ".lang-toggle button.active{background:transparent;color:var(--accent);box-shadow:inset 0 -3px 0 var(--accent)}"

    # 2) Thin gold rule under section + media headings — an engraved luxury divider.
    "section>.container>h2,.media-band .m-head h2{position:relative;padding-bottom:.42em}"
    "section>.container>h2::after,.media-band .m-head h2::after{content:'';position:absolute;"
    "left:0;bottom:0;width:54px;height:2px;"
    "background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 12%,transparent))}"
    ".media-band .m-head h2::after{left:50%;transform:translateX(-50%);"
    "background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 12%,transparent),"
    "var(--accent),color-mix(in srgb,var(--accent) 12%,transparent))}"

    # 3) Gold-sheen sweep on the primary button (matches the h1 gold-sheen motif).
    ".btn-primary{position:relative;overflow:hidden;"
    "box-shadow:0 6px 20px color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".btn-primary::after{content:'';position:absolute;top:0;left:-130%;width:60%;height:100%;"
    "background:linear-gradient(100deg,transparent,color-mix(in srgb,#ffffff 55%,transparent),transparent);"
    "transform:skewX(-18deg);pointer-events:none}"
    "@media (prefers-reduced-motion:no-preference){"
    ".btn-primary::after{transition:left .6s cubic-bezier(.7,0,.2,1)}"
    ".btn-primary:hover::after{left:130%}}"

    # 4) Elegant gold corner-bracket on cards — a quiet bespoke frame, fades in on hover.
    ".card,.stat-card{position:relative}"
    ".card::after,.stat-card::after{content:'';position:absolute;top:8px;right:8px;width:14px;height:14px;"
    "border-top:1.5px solid color-mix(in srgb,var(--accent) 70%,transparent);"
    "border-right:1.5px solid color-mix(in srgb,var(--accent) 70%,transparent);"
    "opacity:0;transition:opacity .3s;pointer-events:none}"
    ".card:hover::after,.stat-card:hover::after{opacity:1}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 05-barber-prime.")
