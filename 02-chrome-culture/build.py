#!/usr/bin/env python3
"""Standalone build file for Chrome Culture (02-chrome-culture).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 02-chrome-culture/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 02-chrome-culture ----
TOKENS = {
    "slug": "02-chrome-culture",
    "bg": "#0c0c0e",
    "bg2": "#141417",
    "ink": "#f4f5f7",
    "mut": "#9a9da6",
    "accent": "#ff2e2e",
    "accent2": "#c8ccd2",
    "accent3": "#e8eaee",
    "line": "rgba(255,255,255,.09)",
    "glass": "rgba(12,12,14,.7)",
    "body_font": "'Helvetica Neue',Arial,sans-serif",
    "heading_font": "'Arial Black','Helvetica Neue',sans-serif",
    "heading_ls": "-.03em",
    "heading_lh": ".92",
    "card_radius": "4px",
    "button_radius": "0",
    "button_shape": "clip-blade",
    # Ribbon red darkened from #ff2e2e to #e01010 so white-on-red hits WCAG AA
    # (4.94:1 vs 3.70:1) for the small EN/ES flag labels + promo line. Still a vivid brand red.
    "ribbon_bg": "#e01010",
    "ribbon_color": "#fff",
    "ribbon_text": "American Barber Institute · Cut sharp. Cut clean. Cut for good. · Manhattan + Bronx",
    "decoration": "chrome-brutalism",
    "vibe": "Industrial dark mode with aggressive red accents and chrome chrome",
    "h1_effect": "chrome",
    "media_style": "metal-slab"
}

# ---- site identity ----
SITE = {
    "slug": "02-chrome-culture",
    "vercel_name": "abi-app-2",
    "logo": "american_barber_institute_logo_2.jpeg",
    "video": "animated_logo_transition_america-.mp4",
    "site_index": 1
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Liquid-metal brutalism: metallic toggle + chrome shine on buttons + hard-edged
# offset shadows on cards + brushed-metal header bevel. All responsive, color-mix only,
# motion gated behind prefers-reduced-motion. Kept as a single valid Python string.
SITE_CSS = (
    "/* unique polish for 02-chrome-culture: liquid-metal brutalism */"

    # --- metallic EN/ES toggle (brutalist hard corners + chrome active state) ---
    ".lang-toggle{border-radius:2px;border-width:2px}"
    ".lang-toggle button{font-style:italic;letter-spacing:.16em}"
    ".lang-toggle button.active{background:linear-gradient(180deg,#fff,var(--mut));color:#111;text-shadow:0 1px 0 rgba(255,255,255,.6)}"

    # --- chrome shine sweep across primary buttons (signature touch #1) ---
    ".btn-primary{position:relative;overflow:hidden;isolation:isolate}"
    ".btn-primary::after{content:'';position:absolute;top:0;left:-130%;width:55%;height:100%;z-index:1;"
    "background:linear-gradient(100deg,transparent,color-mix(in srgb,#fff 70%,transparent),transparent);"
    "transform:skewX(-22deg);pointer-events:none}"
    "@media (prefers-reduced-motion:no-preference){"
    ".btn-primary::after{transition:left .6s cubic-bezier(.2,.8,.2,1)}"
    ".btn-primary:hover::after{left:140%}}"

    # --- hard-edged brutalist offset shadow on cards (signature touch #2) ---
    # Solid red offset shadow that snaps tighter on hover; squared corners for the brutalist read.
    ".card{border-radius:2px;border:2px solid var(--line);"
    "box-shadow:6px 6px 0 color-mix(in srgb,var(--accent) 26%,transparent)}"
    ".card:hover{box-shadow:3px 3px 0 var(--accent);border-color:var(--accent)}"
    "@media (prefers-reduced-motion:reduce){.card{transition:none}}"
    "@media (max-width:480px){.card{box-shadow:4px 4px 0 color-mix(in srgb,var(--accent) 26%,transparent)}}"

    # --- brushed-metal bevel on the sticky header + chrome eyebrow rule (signature touch #3) ---
    ".site-header{box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 14%,transparent),0 1px 0 var(--line)}"
    ".eyebrow-acc{position:relative;padding-bottom:6px}"
    ".eyebrow-acc::after{content:'';position:absolute;left:0;bottom:0;width:34px;height:2px;"
    "background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent3) 80%,transparent))}"
    ".eyebrow-acc.center::after{left:50%;transform:translateX(-50%)}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 02-chrome-culture.")
