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
    "logo": "abi_monogram_with_accent.jpeg",
    "video": "futuristic_abi_animation_barber_-.mp4",
    "site_index": 3
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Tactical HUD signature touches. All translucency uses color-mix(...) (NEVER var(--x)NN
# hex-alpha — that was a prior regression). Pseudo-elements .card::before/::after,
# .stat-card::after, .eyebrow-acc::before are confirmed unused by the engine.
SITE_CSS = (
    "/* ===== 04-midnight-hud :: tactical HUD polish ===== */"
    # -- lang toggle: mono + AA-compliant 44px tap target (engine omits min-height) --
    ".lang-toggle{border-radius:4px;font-family:ui-monospace,Menlo,monospace}"
    ".lang-toggle button{min-height:44px;display:inline-flex;align-items:center;justify-content:center}"
    ".lang-toggle button.active{background:color-mix(in srgb,var(--accent) 22%,transparent);color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}"
    # -- signature 1: reticle corner brackets on cards (cyan L-brackets, top-left + bottom-right) --
    ".card{position:relative}"
    ".card::before{content:'';position:absolute;inset:7px;pointer-events:none;z-index:1;border:0 solid color-mix(in srgb,var(--accent2) 38%,transparent);"
    "clip-path:polygon(0 0,18px 0,18px 1.5px,1.5px 1.5px,1.5px 18px,0 18px,0 100%,100% 100%,100% calc(100% - 18px),calc(100% - 1.5px) calc(100% - 18px),calc(100% - 1.5px) calc(100% - 1.5px),calc(100% - 18px) calc(100% - 1.5px),calc(100% - 18px) 100%,0 100%);"
    "border-width:1.5px;opacity:.55;transition:opacity .3s,border-color .3s}"
    ".card:hover::before{opacity:1;border-color:color-mix(in srgb,var(--accent) 70%,transparent)}"
    # -- signature 2: stat labels as monospace terminal readout (cyan, 12:1 on glass) --
    ".stat-card .label{font-family:ui-monospace,Menlo,monospace;color:var(--accent2);letter-spacing:.16em;font-weight:700}"
    ".stat-card .count{text-shadow:0 0 18px color-mix(in srgb,var(--accent) 30%,transparent)}"
    # -- signature 2b: faint scanline wash inside stat cards (screen-blend, non-interactive) --
    ".stat-card::after{content:'';position:absolute;inset:0;pointer-events:none;z-index:0;"
    "background:repeating-linear-gradient(0deg,transparent 0 3px,color-mix(in srgb,var(--accent2) 6%,transparent) 3px 4px);mix-blend-mode:screen;opacity:.7}"
    ".stat-card>*{position:relative;z-index:1}"
    # -- signature 3: terminal '//' prefix on accent eyebrows + mono instrument price readout --
    ".eyebrow-acc::before{content:'// ';color:color-mix(in srgb,var(--accent2) 80%,transparent);font-family:ui-monospace,Menlo,monospace;font-weight:900}"
    ".price-tag{font-family:ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;letter-spacing:-.01em}"
    # -- respect reduced motion: freeze the bracket transition --
    "@media (prefers-reduced-motion:reduce){.card::before{transition:none}}"
    # -- mobile: lighten bracket inset so it never crowds tight cards --
    "@media (max-width:480px){.card::before{inset:5px}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 04-midnight-hud.")
