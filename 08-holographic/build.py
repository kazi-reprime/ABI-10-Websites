#!/usr/bin/env python3
"""Standalone build file for Holographic (08-holographic).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 08-holographic/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 08-holographic ----
TOKENS = {
    "slug": "08-holographic",
    "bg": "#0c0b1a",
    "bg2": "rgba(255,255,255,.055)",
    "ink": "#ecebff",
    "mut": "#bfbce8",
    "accent": "#a78bfa",
    "accent2": "#22d3ee",
    "accent3": "#f472d0",
    "line": "rgba(167,139,250,.28)",
    "glass": "rgba(255,255,255,.06)",
    "body_font": "'Sora',sans-serif",
    "heading_font": "'Syne',sans-serif",
    "heading_ls": ".02em",
    "heading_lh": "1.04",
    "card_radius": "18px",
    "button_radius": "46px",
    "button_shape": "pill",
    "ribbon_bg": "linear-gradient(90deg,#a78bfa,#22d3ee,#f472d0,#a78bfa)",
    "ribbon_color": "#0c0b1a",
    "ribbon_text": "American Barber Institute · Iridescent craft. Inspired careers. · Next start: First Monday",
    "decoration": "aurora-orbs",
    "vibe": "Holographic glassmorphism with aurora orbs and gradient text",
    "h1_effect": "holo-gradient",
    "media_style": "glass-rotate"
}

# ---- site identity ----
SITE = {
    "slug": "08-holographic",
    "vercel_name": "abi-app-8",
    "logo": "abi_crest_logo_design.jpeg",
    "video": "abstract_animation_for_american_-.mp4",
    "site_index": 7
}

# ---- per-site unique polish (engine appends this last; overrides engine for THIS site only) ----
# Iridescent-glass theme: frosted toggle + aurora sheen on cards + soft holo glow.
# All translucency via color-mix(); animations guarded by prefers-reduced-motion.
SITE_CSS = (
    "/* ===== unique polish for 08-holographic (iridescent glass) ===== */"
    # --- frosted, iridescent EN/ES toggle ---
    ".lang-toggle{position:relative;border-color:color-mix(in srgb,var(--accent) 55%,transparent);"
    "background:color-mix(in srgb,var(--accent) 9%,transparent);backdrop-filter:blur(8px) saturate(1.3);"
    "-webkit-backdrop-filter:blur(8px) saturate(1.3);"
    "box-shadow:0 2px 14px color-mix(in srgb,var(--accent) 22%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 18%,transparent)}"
    ".lang-toggle button{min-height:44px}"  # WCAG tap target (overrides engine's compact toggle for this site)
    ".lang-toggle button.active{background:linear-gradient(120deg,color-mix(in srgb,var(--accent) 34%,transparent),"
    "color-mix(in srgb,var(--accent2) 30%,transparent));color:var(--ink);"
    "text-shadow:0 0 10px color-mix(in srgb,var(--accent2) 45%,transparent)}"
    # --- banner call CTAs: lift to 44px tap target on this site ---
    "@media (max-width:760px){.cta-call{min-height:44px}}"
    # --- card glassmorphism sheen: subtle iridescent diagonal highlight ---
    ".card{position:relative;overflow:hidden}"
    ".card::before{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;z-index:0;"
    "background:linear-gradient(135deg,color-mix(in srgb,#fff 9%,transparent) 0%,transparent 36%,"
    "transparent 64%,color-mix(in srgb,var(--accent2) 11%,transparent) 100%);opacity:.85;"
    "transition:opacity .3s}"
    ".card>*{position:relative;z-index:1}"
    # --- iridescent border + soft holo glow on hover ---
    ".card:hover{border-color:color-mix(in srgb,var(--accent2) 60%,transparent);"
    "box-shadow:0 18px 46px color-mix(in srgb,var(--accent) 26%,transparent),"
    "0 0 0 1px color-mix(in srgb,var(--accent2) 30%,transparent),"
    "inset 0 1px 0 color-mix(in srgb,#fff 14%,transparent)}"
    ".card:hover::before{opacity:1}"
    # --- gentle aurora shimmer on the primary button ---
    ".btn-primary{background-image:linear-gradient(120deg,var(--accent),var(--accent2),var(--accent3),var(--accent));"
    "background-size:280% 100%;animation:holoBtn 9s linear infinite}"
    "@keyframes holoBtn{0%{background-position:0% 50%}100%{background-position:280% 50%}}"
    # --- reduced-motion: stop the shimmer (belt-and-suspenders; engine also guards globally) ---
    "@media (prefers-reduced-motion:reduce){.btn-primary{animation:none}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 08-holographic.")
