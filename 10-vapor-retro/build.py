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
    "logo_dark_bg": False,
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
    "logo": "site-10-crest.jpeg",
    "video": "letter_i_transforms_barber_pole.mp4",
    "site_index": 9,
    "favicon": "site-10-crest-favicon.png",
    "og": "site-10-crest-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# Appended after the engine CSS, so these rules win on specificity-tie.
# All color blends use color-mix(); motion is gated behind prefers-reduced-motion.
SITE_CSS = (
    "/* ===== 10-vapor-retro :: SYNTHWAVE-SUN motif (sun + grid horizon + VHS) ===== */"

    # ============================================================
    # BACKGROUND: rebuild the deco into a full retro-sunset scene.
    # Sky gradient + glowing perspective grid (engine ::before) + an 80s neon SUN
    # with horizontal slits (the signature of this site) + drifting VHS scanlines.
    # Pure CSS; every moving layer is killed under prefers-reduced-motion.
    # ============================================================

    # Sunset sky wash behind everything (sits inside the fixed deco layer).
    ".deco-vapor{background:"
    "radial-gradient(120% 80% at 50% 78%,color-mix(in srgb,var(--accent) 28%,transparent) 0,transparent 55%),"
    "linear-gradient(180deg,var(--bg) 0,color-mix(in srgb,var(--accent3) 8%,var(--bg2)) 46%,"
    "color-mix(in srgb,var(--accent) 22%,var(--bg)) 100%)}"

    # Brighten + animate the engine's perspective grid into a glowing scrolling floor.
    ".deco-vapor::before{height:60%;background-image:"
    "linear-gradient(color-mix(in srgb,var(--accent2) 55%,transparent) 1.5px,transparent 1.5px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--accent) 60%,transparent) 1.5px,transparent 1.5px);"
    "background-size:46px 46px;filter:drop-shadow(0 0 4px color-mix(in srgb,var(--accent2) 70%,transparent));"
    "animation:vrGrid 5s linear infinite}"
    "@keyframes vrGrid{from{background-position:0 0,0 0}to{background-position:0 46px,0 0}}"

    # THE SUN: turn the engine's .vsun into a hot magenta->amber disc with horizontal slits.
    # The slits are a repeating-linear-gradient mask that thickens toward the bottom (classic).
    ".deco-vapor .vsun{width:clamp(220px,42vw,340px);height:clamp(220px,42vw,340px);"
    "transform:translate(-50%,-58%);opacity:.9;filter:none;"
    "background:linear-gradient(180deg,var(--accent3) 0,var(--accent) 52%,"
    "color-mix(in srgb,var(--accent) 70%,var(--accent2)) 100%);"
    "-webkit-mask-image:linear-gradient(180deg,#000 0,#000 38%,transparent 38%,#000 46%,"
    "transparent 50%,#000 58%,transparent 64%,#000 74%,transparent 80%,#000 92%,transparent 95%);"
    "mask-image:linear-gradient(180deg,#000 0,#000 38%,transparent 38%,#000 46%,"
    "transparent 50%,#000 58%,transparent 64%,#000 74%,transparent 80%,#000 92%,transparent 95%);"
    "box-shadow:0 0 120px 30px color-mix(in srgb,var(--accent) 55%,transparent);"
    "animation:vrSun 6s ease-in-out infinite}"
    "@keyframes vrSun{0%,100%{filter:saturate(1)}50%{filter:saturate(1.25) brightness(1.08)}}"

    # VHS scanlines: a faint horizontal raster drifting up over the whole deco layer.
    ".deco-vapor::after{content:'';position:absolute;inset:0;pointer-events:none;"
    "background:repeating-linear-gradient(0deg,color-mix(in srgb,#000 22%,transparent) 0 1px,"
    "transparent 1px 3px);mix-blend-mode:multiply;opacity:.5;animation:vrScan 9s linear infinite}"
    "@keyframes vrScan{from{background-position:0 0}to{background-position:0 -120px}}"

    "@media (prefers-reduced-motion:reduce){"
    ".deco-vapor::before,.deco-vapor .vsun,.deco-vapor::after{animation:none}}"

    # ============================================================
    # HERO: chrome/neon display type + chromatic-aberration eyebrow.
    # ============================================================
    # Override the engine's flat hfx-vapor with a magenta->cyan chrome gradient fill,
    # backed by a soft neon bloom so the headline reads like a lit sign.
    ".hfx-vapor h1{background:linear-gradient(170deg,#fff 0,var(--accent3) 26%,var(--accent) 58%,"
    "var(--accent2) 100%);-webkit-background-clip:text;background-clip:text;"
    "-webkit-text-fill-color:transparent;color:transparent;text-shadow:none;"
    "filter:drop-shadow(0 2px 0 color-mix(in srgb,var(--accent) 60%,transparent))"
    " drop-shadow(0 0 26px color-mix(in srgb,var(--accent2) 35%,transparent))}"
    # Retro chrome eyebrow pill on the hero.
    ".hero-home .eyebrow,.subpage-hero .eyebrow{background:color-mix(in srgb,var(--accent) 14%,transparent);"
    "border-color:color-mix(in srgb,var(--accent2) 45%,transparent);color:var(--accent2);"
    "text-shadow:0 0 10px color-mix(in srgb,var(--accent2) 55%,transparent)}"

    # --- Synthwave gradient language toggle (chrome/neon pill, >=44px tap target) ---
    ".lang-toggle{border:0;background:linear-gradient(90deg,var(--accent),var(--accent2));"
    "padding:2px;border-radius:999px;box-shadow:0 0 14px color-mix(in srgb,var(--accent) 45%,transparent)}"
    ".lang-toggle button{border-radius:999px;min-height:34px;padding:8px 16px;font-weight:800;"
    "letter-spacing:.06em}"
    ".lang-toggle button.active{background:var(--bg);color:var(--accent2);"
    "text-shadow:0 0 8px color-mix(in srgb,var(--accent2) 60%,transparent)}"
    "@media (max-width:1180px){.lang-toggle button{min-height:44px;padding:11px 18px}}"

    # --- Neon horizon divider under every section heading + hero h1 ---
    "section>.container>h2::after,.subpage-hero h1::after{content:'';display:block;"
    "width:clamp(60px,18vw,120px);height:3px;margin:14px auto 0;border-radius:3px;"
    "background:linear-gradient(90deg,var(--accent),var(--accent2));"
    "box-shadow:0 0 12px color-mix(in srgb,var(--accent) 60%,transparent)}"
    ".subpage-hero h1::after{margin-left:auto;margin-right:auto}"

    # ============================================================
    # LOGO FRAME: intentional retro panel for the vintage crest.
    # Magenta->cyan gradient border, scanline-free white plate, neon glow.
    # ============================================================
    ".brand-mark.logo-light{background:#fff;padding:3px 8px;border:0;"
    "box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 70%,transparent),"
    "0 0 0 4px color-mix(in srgb,var(--accent2) 60%,transparent),"
    "0 0 18px color-mix(in srgb,var(--accent) 45%,transparent)}"

    # ============================================================
    # CARDS: glass tiles with a magenta->cyan top edge that lights on hover.
    # ============================================================
    ".card{position:relative;background:color-mix(in srgb,var(--bg2) 70%,transparent);"
    "border-color:color-mix(in srgb,var(--accent) 28%,transparent)}"
    ".card::before{content:'';position:absolute;left:0;right:0;top:0;height:2px;"
    "border-radius:var(--card-r) var(--card-r) 0 0;"
    "background:linear-gradient(90deg,var(--accent),var(--accent2));opacity:.6;transition:opacity .3s}"
    ".card:hover{border-color:var(--accent2);"
    "box-shadow:0 16px 44px color-mix(in srgb,var(--accent) 30%,transparent),"
    "0 0 0 1px color-mix(in srgb,var(--accent2) 35%,transparent)}"
    ".card:hover::before{opacity:1}"

    # ============================================================
    # BUTTONS: neon-sign primary; cyan ghost secondary.
    # ============================================================
    ".btn-primary{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent2) 40%,transparent),"
    "0 10px 30px color-mix(in srgb,var(--accent) 40%,transparent)}"
    ".btn-primary:hover{box-shadow:0 0 0 1px var(--accent2),"
    "0 0 26px color-mix(in srgb,var(--accent) 55%,transparent)}"

    # ============================================================
    # STATS BAND: retro scoreboard — cyan glowing counters on a grid strip.
    # ============================================================
    ".stats-band{background:linear-gradient(180deg,transparent,"
    "color-mix(in srgb,var(--accent) 10%,transparent))}"
    ".stat-card{background:color-mix(in srgb,var(--bg) 70%,transparent);"
    "border-color:color-mix(in srgb,var(--accent2) 30%,transparent)}"
    ".stat-card::before{background:linear-gradient(180deg,var(--accent),var(--accent2));"
    "box-shadow:0 0 10px color-mix(in srgb,var(--accent2) 70%,transparent)}"
    ".stat-card .count{color:var(--accent2);"
    "text-shadow:0 0 18px color-mix(in srgb,var(--accent2) 50%,transparent)}"

    # ============================================================
    # NEXT-CLASS countdown: glowing retro flip-units.
    # ============================================================
    ".next-class{border-color:color-mix(in srgb,var(--accent2) 40%,transparent);"
    "box-shadow:0 0 24px color-mix(in srgb,var(--accent) 25%,transparent)}"
    ".next-class .nc-unit{background:color-mix(in srgb,var(--accent) 16%,transparent);"
    "box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent2) 30%,transparent)}"
    ".next-class .nc-unit b{text-shadow:0 0 14px color-mix(in srgb,var(--accent) 55%,transparent)}"

    # ============================================================
    # HOME CONTACT .hc-box: retro panel with a neon gradient frame.
    # ============================================================
    ".home-contact .hc-box{border-color:color-mix(in srgb,var(--accent) 35%,transparent);"
    "box-shadow:0 0 0 1px color-mix(in srgb,var(--accent2) 22%,transparent),"
    "0 18px 50px color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".hc-pill:hover,.radio-pill:hover span{border-color:var(--accent2);color:var(--accent2)}"

    # ============================================================
    # CAMPUS-SPLIT: glowing divider between the two campuses.
    # ============================================================
    ".campus-split{position:relative}"
    ".campus-split::after{content:'';position:absolute;left:50%;top:8%;bottom:8%;width:2px;"
    "transform:translateX(-50%);background:linear-gradient(180deg,transparent,var(--accent),"
    "var(--accent2),transparent);box-shadow:0 0 14px color-mix(in srgb,var(--accent) 55%,transparent)}"
    "@media (max-width:760px){.campus-split::after{display:none}}"

    # ============================================================
    # INSTRUCTORS: photo gets a magenta duotone-ish wash that clears on hover.
    # ============================================================
    ".ins-card{border-color:color-mix(in srgb,var(--accent) 26%,transparent)}"
    ".ins-card .ins-photo{position:relative}"
    ".ins-card .ins-photo::after{content:'';position:absolute;inset:0;pointer-events:none;"
    "background:linear-gradient(180deg,color-mix(in srgb,var(--accent2) 18%,transparent),"
    "color-mix(in srgb,var(--accent) 30%,transparent));mix-blend-mode:overlay;"
    "opacity:.7;transition:opacity .4s}"
    ".ins-card:hover .ins-photo::after{opacity:0}"
    ".ins-card .ins-tags{color:var(--accent2)}"

    # ============================================================
    # PARTNER CARDS: neon name plate + magenta location label.
    # ============================================================
    ".partner-card{border-color:color-mix(in srgb,var(--accent2) 28%,transparent)}"
    ".partner-card:hover{box-shadow:0 16px 40px color-mix(in srgb,var(--accent) 26%,transparent)}"
    ".partner-card .img-wrap .partner-name{text-shadow:0 0 16px "
    "color-mix(in srgb,var(--accent2) 70%,transparent),0 2px 8px rgba(0,0,0,.6)}"

    # ============================================================
    # MEDIA BAND: tint heading to cyan to tie into the VHS look.
    # ============================================================
    ".media-band .m-head .eyb{color:var(--accent2);"
    "text-shadow:0 0 10px color-mix(in srgb,var(--accent2) 50%,transparent)}"

    # ============================================================
    # SECTION RHYTHM: alternate sections get a faint scanline tint so the
    # page reads as bands of retro signal (nth-of-type, per brief).
    # ============================================================
    "main section:nth-of-type(even){background:linear-gradient(180deg,transparent,"
    "color-mix(in srgb,var(--accent) 6%,transparent),transparent)}"

    # ===== MOBILE / RESPONSIVENESS FIXES =====

    # NOTE: the engine now fixes two issues globally, so the local patches that used
    # to live here have been REMOVED to avoid double-up:
    #   * sticky-call bar: engine's page-in is opacity-only (no transform persists on
    #     <body>), so position:fixed children anchor to the viewport correctly.
    #   * nav drawer gap: engine anchors .primary-nav at top:100% (max-width:1280px).
    # Only the two genuinely vapor-specific fixes below remain.

    # FIX A (vhs-flip media projection): rotateX(-25deg) projects tiles a few px past
    # their container. Body overflow-x:hidden already prevents scroll, but clip the
    # media band so the projection never grazes the viewport edge on small screens.
    "@media (max-width:760px){.media-band{overflow-x:clip}"
    ".ms-vhs-flip .m-grid{overflow:visible}}"

    # FIX B (vapor chrome H1 on mobile): the H1 is now a magenta->cyan chrome gradient
    # fill (set above). At narrow widths long words can overrun the container, so allow
    # breaking and soften the drop-shadow bloom so it stays crisp at 360px.
    "@media (max-width:600px){"
    ".hfx-vapor h1{overflow-wrap:break-word;"
    "filter:drop-shadow(0 1px 0 color-mix(in srgb,var(--accent) 60%,transparent))}}"
    "@media (max-width:380px){.hfx-vapor h1{hyphens:auto}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 10-vapor-retro.")
