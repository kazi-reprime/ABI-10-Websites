#!/usr/bin/env python3
"""Standalone build file for Neon Grid (06-neon-grid).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 06-neon-grid/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 06-neon-grid ----
# Magenta-forward identity (#ff2bd6 primary) on a deep-navy dark base, with cyan as the
# secondary so the grid keeps its neon duotone but reads distinctly from the cyan-led 01-neon-blade.
# Contrast (WCAG AA, vs #05060a bg): magenta 6.33 (normal text + UI pass), ink 18.4, mut 9.6.
# Button text uses var(--bg) on magenta => 6.33 (pass). Translucent colors stay in --line/--glass
# as plain rgba (valid CSS); SITE_CSS uses color-mix(...) exclusively — never var(--accent)NN.
TOKENS = {
    "slug": "06-neon-grid",
    "logo_dark_bg": True,
    "bg": "#05060a",
    "bg2": "rgba(13,18,28,.6)",
    "ink": "#e8f6ff",
    "mut": "#a9c0d0",
    "accent": "#ff2bd6",
    "accent2": "#00f0ff",
    "accent3": "#7b5cff",
    "line": "rgba(255,43,214,.20)",
    "glass": "rgba(5,6,10,.6)",
    "body_font": "'Space Grotesk',sans-serif",
    "heading_font": "'Orbitron',sans-serif",
    "heading_ls": ".02em",
    "heading_lh": "1.04",
    "card_radius": "14px",
    "button_radius": "40px",
    "button_shape": "pill",
    "ribbon_bg": "#ff2bd6",
    "ribbon_color": "#04060c",
    "ribbon_text": "American Barber Institute · Particle-network barbering education · Next: First Monday",
    "decoration": "particle-network",
    "vibe": "Neon grid: magenta particle-network on deep navy, cyan accents",
    "h1_effect": "neon-shadow",
    "media_style": "grid-tilt"
}

# ---- site identity ----
SITE = {
    "slug": "06-neon-grid",
    "vercel_name": "abi-app-6",
    "logo": "site-06-chrome2.jpeg",
    "video": "futuristic_animation_for_abi.mp4",
    "site_index": 5,
    "favicon": "site-06-chrome2-favicon.png",
    "og": "site-06-chrome2-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Neon-grid theme touches. RULES (per brief / prior regression):
#   * ONLY color-mix(in srgb, var(--token) N%, transparent) for translucency — NEVER var(--accent)NN.
#   * Responsive: no fixed widths that can overflow; section dividers are full-bleed via the
#     container's own padding box; media perspective stays inside the engine's .m-grid.
#   * prefers-reduced-motion: reduce disables the animated glitch + scanline sweep.
SITE_CSS = (
    "/* ===== unique polish for 06-neon-grid (magenta neon grid) ===== */"
    # --- magenta-glitch bilingual toggle (seed, enhanced) ---
    ".lang-toggle{border-color:var(--accent)}"
    ".lang-toggle button.active{background:var(--accent);color:var(--bg);"
    "box-shadow:2px 0 0 var(--accent2),-2px 0 0 var(--accent3),0 0 18px color-mix(in srgb,var(--accent) 55%,transparent)}"
    "@media (prefers-reduced-motion:no-preference){"
    ".lang-toggle button.active{animation:ng-glitch 3.4s steps(1) infinite}"
    "@keyframes ng-glitch{0%,92%,100%{box-shadow:2px 0 0 var(--accent2),-2px 0 0 var(--accent3),0 0 18px color-mix(in srgb,var(--accent) 55%,transparent)}"
    "94%{box-shadow:-3px 0 0 var(--accent2),3px 0 0 var(--accent3),0 0 22px color-mix(in srgb,var(--accent) 70%,transparent)}"
    "96%{box-shadow:3px 0 0 var(--accent2),-3px 0 0 var(--accent3),0 0 14px color-mix(in srgb,var(--accent) 50%,transparent)}}}"
    # --- neon grid-line section dividers: thin magenta->cyan rule with a centered node glow ---
    "section + section{position:relative}"
    "section + section::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);"
    "width:min(880px,86%);height:1px;pointer-events:none;"
    "background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 60%,transparent) 22%,"
    "color-mix(in srgb,var(--accent2) 60%,transparent) 78%,transparent)}"
    "section + section::after{content:'';position:absolute;top:0;left:50%;width:6px;height:6px;"
    "transform:translate(-50%,-50%) rotate(45deg);pointer-events:none;background:var(--accent);"
    "box-shadow:0 0 12px color-mix(in srgb,var(--accent) 80%,transparent)}"
    # --- neon glow on interactive hover (cards, ghost buttons, stat cards) ---
    "@media (hover:hover){"
    ".card:hover{box-shadow:0 16px 40px rgba(0,0,0,.45),0 0 0 1px color-mix(in srgb,var(--accent) 45%,transparent),"
    "0 0 28px color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".stat-card:hover{box-shadow:0 0 26px color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".btn-primary:hover{box-shadow:0 0 24px color-mix(in srgb,var(--accent) 55%,transparent)}"
    ".btn-ghost:hover{box-shadow:0 0 20px color-mix(in srgb,var(--accent) 45%,transparent)}}"
    # --- eyebrow gets a faint neon ring to tie into the grid mood ---
    ".eyebrow{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 16%,transparent),"
    "0 0 16px color-mix(in srgb,var(--accent) 12%,transparent)}"
    # --- grid-tilt media: keep the 3D node feel but clamp it on small screens so tilted tiles
    #     never push past the viewport; flatten perspective under ~640px ---
    ".ms-grid-tilt .m-tile{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 18%,transparent)}"
    "@media (max-width:640px){.ms-grid-tilt .m-grid{perspective:none}"
    ".ms-grid-tilt .m-tile{transform:translateY(22px)}"
    ".ms-grid-tilt .m-tile:hover{transform:translateY(-3px)}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 06-neon-grid.")
