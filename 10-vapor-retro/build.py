#!/usr/bin/env python3
"""Standalone build file for Vapor Retro (10-vapor-retro).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 10-vapor-retro/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 10-vapor-retro ----
TOKENS = {
    "slug": "10-vapor-retro",
    "bg": "#150522",
    "bg2": "#1a0530",
    "ink": "#fdeaff",
    "mut": "#e7c9f5",
    "accent": "#ff4d8d",
    "accent2": "#29f1ff",
    "accent3": "#ffe14d",
    "line": "rgba(255,77,141,.3)",
    "glass": "rgba(21,5,34,.6)",
    "body_font": "'Space Grotesk',sans-serif",
    "heading_font": "'Bungee',sans-serif",
    "heading_ls": ".02em",
    "heading_lh": "1.04",
    "card_radius": "14px",
    "button_radius": "30px",
    "button_shape": "pill",
    "ribbon_bg": "#ff4d8d",
    "ribbon_color": "#150522",
    "ribbon_text": "AMERICAN BARBER INSTITUTE · OLD-SCHOOL SOUL · NEW-WAVE CUTS · MANHATTAN + BRONX",
    "decoration": "vapor-grid",
    "vibe": "Synthwave/vaporwave with magenta+cyan neon and 3D grid sun",
    "h1_effect": "vapor-shadow",
    "media_style": "vhs-flip"
}

# ---- site identity ----
SITE = {
    "slug": "10-vapor-retro",
    "vercel_name": "abi-app-10",
    "logo": "futuristic_wordmark_logo_america-.jpeg",
    "video": "letter_i_transforms_barber_pole.mp4",
    "site_index": 9
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Appended after the engine CSS, so these rules win on specificity-tie.
# All color blends use color-mix(); motion is gated behind prefers-reduced-motion.
SITE_CSS = (
    "/* ===== 10-vapor-retro :: synthwave polish + mobile fixes ===== */"

    # --- Synthwave gradient language toggle (seed, enhanced) ---
    # Chrome/neon pill with a >=44px tap target and a glowing active state.
    ".lang-toggle{border:0;background:linear-gradient(90deg,var(--accent),var(--accent2));"
    "padding:2px;border-radius:999px;box-shadow:0 0 14px color-mix(in srgb,var(--accent) 45%,transparent)}"
    ".lang-toggle button{border-radius:999px;min-height:34px;padding:8px 16px;font-weight:800;"
    "letter-spacing:.06em}"
    ".lang-toggle button.active{background:var(--bg);color:var(--accent2);"
    "text-shadow:0 0 8px color-mix(in srgb,var(--accent2) 60%,transparent)}"
    # Bigger tap target on touch screens without distorting the desktop pill.
    "@media (max-width:1180px){.lang-toggle button{min-height:44px;padding:11px 18px}}"

    # --- Neon grid divider: a retro horizon line under every section heading ---
    "section>.container>h2::after,.subpage-hero h1::after{content:'';display:block;"
    "width:clamp(60px,18vw,120px);height:3px;margin:14px auto 0;border-radius:3px;"
    "background:linear-gradient(90deg,var(--accent),var(--accent2));"
    "box-shadow:0 0 12px color-mix(in srgb,var(--accent) 60%,transparent)}"
    ".subpage-hero h1::after{margin-left:auto;margin-right:auto}"

    # --- Retro sun glow: warm the fixed vapor-grid sun a touch more ---
    ".deco-vapor .vsun{box-shadow:0 0 90px color-mix(in srgb,var(--accent) 50%,transparent)}"

    # --- Chrome/gradient accent on the primary button label for extra neon pop ---
    ".btn-primary{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent2) 40%,transparent),"
    "0 10px 30px color-mix(in srgb,var(--accent) 35%,transparent)}"

    # ===== MOBILE / RESPONSIVENESS FIXES =====

    # FIX 1 (sticky-call bar): the engine's body{animation:pageIn ... both} leaves a
    # residual identity transform on <body>, which turns <body> into the containing
    # block for position:fixed children -> the sticky call bar drops to page bottom.
    # Override with an opacity-only page-in so no transform persists on <body>.
    "@media (prefers-reduced-motion:no-preference){"
    "body.hfx-vapor{animation:vaporIn .42s cubic-bezier(.2,.8,.2,1) both}"
    "@keyframes vaporIn{from{opacity:0}to{opacity:1}}}"
    # Belt-and-suspenders: guarantee no transform lingers on <body>.
    "body.hfx-vapor{transform:none}"

    # FIX 2 (nav drawer gap): <header> has backdrop-filter, making it the containing
    # block for its position:fixed .primary-nav child. The engine's --nav-top
    # (a viewport coordinate) then mis-anchors the drawer by the top-banner height.
    # Anchor the drawer flush to the header's own bottom edge instead.
    "@media (max-width:1180px){"
    ".site-header .primary-nav{top:calc(100% + 1px);max-height:calc(100dvh - 100%);"
    "max-height:calc(100svh - 100%)}}"

    # FIX 3 (vhs-flip media projection): rotateX(-25deg) projects tiles a few px past
    # their container. Body overflow-x:hidden already prevents scroll, but clip the
    # media band so the projection never grazes the viewport edge on small screens.
    "@media (max-width:760px){.media-band{overflow-x:clip}"
    ".ms-vhs-flip .m-grid{overflow:visible}}"

    # FIX 4 (vapor-shadow H1 legibility): the 3px/-2px double offset reads as a heavy
    # ghost at mobile heading sizes. Tighten offsets progressively so the H1 stays
    # crisp and inside its container at 360px (contrast itself already passes AA).
    "@media (max-width:600px){"
    ".hfx-vapor h1{text-shadow:2px 2px 0 var(--accent2),-1px -1px 0 var(--accent)}}"
    "@media (max-width:380px){"
    ".hfx-vapor h1{text-shadow:1.5px 1.5px 0 var(--accent2),-1px -1px 0 var(--accent);"
    "overflow-wrap:break-word}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 10-vapor-retro.")
