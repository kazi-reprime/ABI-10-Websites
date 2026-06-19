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
    "logo": "logo_for_american_barber_institute_2.jpeg",
    "video": "urban_motion_graphic_new_york.mp4",
    "site_index": 6
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Flat-brutalist canvas: hard offset shadows, thick borders, blocky dividers.
# All colors via color-mix(); motion gated behind prefers-reduced-motion;
# a mobile override tames the brutal-offset media translate so it never
# pushes past the viewport edge at small widths.
SITE_CSS = (
    "/* ===== 07-chrome-liquid · flat brutalist polish ===== */"
    # -- blocky language toggle (seeded) --
    ".lang-toggle{border-radius:0;border-width:2px}"
    ".lang-toggle button{font-weight:900;transition:background .15s,color .15s}"
    ".lang-toggle button.active{background:var(--accent);color:var(--bg)}"

    # -- 1) hard offset shadow + thick ink border on cards (brutalist signature) --
    ".card,.stat-card{border:2px solid var(--ink);box-shadow:6px 6px 0 color-mix(in srgb,var(--ink) 88%,transparent)}"
    ".card:hover,.stat-card:hover{border-color:var(--accent);box-shadow:8px 8px 0 var(--accent);transform:translate(-2px,-2px)}"

    # -- 2) blocky section dividers: thick top rule + offset accent tab on h2 eyebrows --
    ".eyebrow-acc{position:relative;padding-left:16px}"
    ".eyebrow-acc::before{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);width:8px;height:18px;background:var(--accent)}"
    ".eyebrow-acc.center{padding-left:0}.eyebrow-acc.center::before{display:none}"

    # -- 3) brutalist primary button: hard offset, no soft glow --
    ".btn-primary{border:2px solid var(--ink);box-shadow:5px 5px 0 var(--ink)}"
    ".btn-primary:hover{filter:none;box-shadow:7px 7px 0 var(--ink);transform:translate(-2px,-2px)}"
    ".btn-ghost{border-width:2px;font-weight:900}"

    # -- contrast hardening: drop muted text a touch darker for small-size margin --
    ":root{--mut:#4f535b}"

    # -- mobile overflow guard for brutal-offset media (translate+shadow) --
    "@media (max-width:600px){"
    ".ms-brutal-offset .m-tile{transform:none;box-shadow:-6px 6px 0 var(--accent)}"
    ".ms-brutal-offset .m-tile.shown{transform:none}"
    ".ms-brutal-offset .m-tile:hover{box-shadow:-6px 6px 0 var(--accent);transform:none}"
    ".card,.stat-card{box-shadow:4px 4px 0 color-mix(in srgb,var(--ink) 88%,transparent)}"
    ".btn-primary{box-shadow:4px 4px 0 var(--ink)}"
    "}"

    # -- respect reduced-motion: kill the translate nudge on hover --
    "@media (prefers-reduced-motion:reduce){"
    ".card:hover,.stat-card:hover,.btn-primary:hover{transform:none}"
    "}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 07-chrome-liquid.")
