#!/usr/bin/env python3
"""Standalone build file for Noir Gold (09-noir-gold).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 09-noir-gold/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 09-noir-gold ----
TOKENS = {
    "slug": "09-noir-gold",
    "logo_dark_bg": True,
    "bg": "#0a0908",
    "bg2": "#0f0d0a",
    "ink": "#f3ede0",
    "mut": "#cdc3ad",
    "accent": "#d4af37",
    "accent2": "#f3e3a0",
    "accent3": "#a07f23",
    "line": "rgba(212,175,55,.26)",
    "glass": "rgba(10,9,8,.7)",
    "body_font": "'Jost',sans-serif",
    "heading_font": "'Bodoni Moda',serif",
    "heading_ls": "-.01em",
    "heading_lh": "1.04",
    "card_radius": "2px",
    "button_radius": "2px",
    "button_shape": "sharp",
    "ribbon_bg": "#d4af37",
    "ribbon_color": "#0a0908",
    "ribbon_text": "American Barber Institute · Cinematic craft. Confident cuts. · 48 W 39th & 121 Westchester Sq",
    "decoration": "noir-spotlight",
    "vibe": "Cinematic noir + gold luxe with Bodoni serif headlines",
    "h1_effect": "gold-sheen",
    "media_style": "spotlight-cine"
}

# ---- site identity ----
SITE = {
    "slug": "09-noir-gold",
    "vercel_name": "abi-app-9",
    "logo": "site-09-waxseal.jpeg",
    "video": "luxury_logo_animation_abi_monogram.mp4",
    "site_index": 8,
    "favicon": "site-09-waxseal-favicon.png",
    "og": "site-09-waxseal-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Cinematic noir + gold, Bodoni serif luxe. Touches:
#   1. Film letterbox bars (top/bottom) with thin gold hairlines — desktop only, fixed,
#      pointer-events:none, slim enough never to cover content. Hidden ≤980px so the
#      mobile sticky call bar + content keep full height.
#   2. Gold serif eyebrow rule — an elegant centered/leading gold hairline accent.
#   3. Cinematic vignette on cards — a soft inner corner-light that warms on hover.
#   4. Heading wrap safety net (Bodoni long words never overflow at 360px).
#   5. Refined gold lang-toggle, AA-contrast active state via near-black ink.
# All colors via color-mix(); prefers-reduced-motion respected; valid single Python string.
SITE_CSS = (
    "/* === 09-noir-gold unique polish === */"

    # 4. Bodoni heading wrap safety net (engine only sets overflow-wrap on <p>)
    "h1,h2,h3,h4{overflow-wrap:break-word;word-wrap:break-word;hyphens:auto}"

    # 5. Refined gold lang-toggle (AA: near-black ink on gold = 9.46:1)
    ".lang-toggle{height:34px;border-width:1px;letter-spacing:.2em}"
    ".lang-toggle button.active{background:var(--accent);color:#0a0908}"

    # 1. Cinematic letterbox bars — fixed film mattes top & bottom with a gold hairline.
    #    Slim (clamped) so content is never obscured; sit above decoration, below content.
    "body::before,body::after{content:'';position:fixed;left:0;right:0;height:clamp(14px,2.2vh,30px);"
    "z-index:20;pointer-events:none;background:linear-gradient(var(--bg),color-mix(in srgb,var(--bg) 86%,transparent));}"
    "body::before{top:0;border-bottom:1px solid color-mix(in srgb,var(--accent) 30%,transparent);"
    "background:linear-gradient(180deg,var(--bg),color-mix(in srgb,var(--bg) 0%,transparent));}"
    "body::after{bottom:0;border-top:1px solid color-mix(in srgb,var(--accent) 30%,transparent);"
    "background:linear-gradient(0deg,var(--bg),color-mix(in srgb,var(--bg) 0%,transparent));}"
    # letterbox only on larger viewports; drop on mobile so the sticky bar + safe-areas are clear
    "@media (max-width:980px){body::before,body::after{display:none}}"

    # 2. Gold serif eyebrow rule — a luxe hairline trailing each accent eyebrow
    ".eyebrow-acc{position:relative}"
    ".eyebrow-acc::after{content:'';display:inline-block;vertical-align:middle;width:clamp(22px,4vw,46px);"
    "height:1px;margin-left:12px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent))}"
    ".center .eyebrow-acc::after,.m-head .eyb::after{display:none}"

    # 3. Cinematic vignette on cards — soft warm corner light, intensifies on hover (no jank).
    #    Scoped to exclude .partner-card (image cards with their own gradient overlay).
    ".card:not(.partner-card){position:relative}"
    ".card:not(.partner-card)::after{content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:0;"
    "background:radial-gradient(120% 90% at 85% 0%,color-mix(in srgb,var(--accent) 9%,transparent),transparent 55%);"
    "opacity:.7;transition:opacity .4s}"
    ".card:not(.partner-card):hover::after{opacity:1}"
    ".card:not(.partner-card)>*{position:relative;z-index:1}"

    # keep all motion polish honest under reduced-motion
    "@media (prefers-reduced-motion:reduce){.card::after{transition:none}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 09-noir-gold.")
