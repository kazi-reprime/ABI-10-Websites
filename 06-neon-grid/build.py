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
    "/* ===== unique polish for 06-neon-grid (magenta particle-network) ===== */"
    # --- ANIMATED BACKGROUND: perspective grid floor + drifting node-network field.
    #     Overrides the engine's static .deco-grid with a layered, motion-gated scene.
    #     Layer A (this element): a deep field of glowing nodes (radial-gradient dots) that
    #     slowly drifts; Layer B (::before): a 3D perspective grid floor anchored to the bottom;
    #     Layer C (::after): connecting "network" scan-lines that sweep diagonally. ---
    # Clip the layered scene: base .deco-grid is position:fixed;inset:0 in the engine but has
    # NO overflow:hidden, while our ::before floor uses left:-25%/right:-25% + a 3D rotateX tilt
    # that can extend past the viewport edges -> horizontal scroll on mobile. Contain it here.
    ".deco-grid{overflow:hidden;max-width:100vw}"
    ".deco-grid{background-image:"
    "radial-gradient(circle at 12% 22%,color-mix(in srgb,var(--accent) 60%,transparent) 0,transparent 1.4px),"
    "radial-gradient(circle at 78% 16%,color-mix(in srgb,var(--accent2) 55%,transparent) 0,transparent 1.4px),"
    "radial-gradient(circle at 33% 64%,color-mix(in srgb,var(--accent3) 55%,transparent) 0,transparent 1.4px),"
    "radial-gradient(circle at 88% 72%,color-mix(in srgb,var(--accent) 55%,transparent) 0,transparent 1.4px),"
    "radial-gradient(circle at 56% 40%,color-mix(in srgb,var(--accent2) 45%,transparent) 0,transparent 1.2px),"
    "linear-gradient(color-mix(in srgb,var(--accent) 6%,transparent) 1px,transparent 1px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--accent) 6%,transparent) 1px,transparent 1px);"
    "background-size:340px 340px,340px 340px,420px 420px,420px 420px,300px 300px,68px 68px,68px 68px;"
    "-webkit-mask-image:radial-gradient(ellipse 90% 80% at center,black 0,transparent 78%);"
    "mask-image:radial-gradient(ellipse 90% 80% at center,black 0,transparent 78%)}"
    # Layer B — 3D perspective grid FLOOR (bottom of viewport), the signature neon-grid plane.
    ".deco-grid::before{content:'';position:absolute;left:-25%;right:-25%;bottom:0;height:48vh;"
    "background-image:linear-gradient(color-mix(in srgb,var(--accent) 26%,transparent) 1.5px,transparent 1.5px),"
    "linear-gradient(90deg,color-mix(in srgb,var(--accent2) 22%,transparent) 1.5px,transparent 1.5px);"
    "background-size:58px 58px;transform:perspective(420px) rotateX(68deg);transform-origin:bottom center;"
    "-webkit-mask-image:linear-gradient(180deg,transparent 0,black 55%,black 100%);"
    "mask-image:linear-gradient(180deg,transparent 0,black 55%,black 100%);opacity:.55}"
    # Layer C — diagonal network scan ("data flowing between nodes").
    ".deco-grid::after{content:'';position:absolute;inset:0;"
    "background:linear-gradient(115deg,transparent 0,color-mix(in srgb,var(--accent) 8%,transparent) 48%,"
    "color-mix(in srgb,var(--accent2) 9%,transparent) 52%,transparent 100%);"
    "background-size:300% 300%;mix-blend-mode:screen;opacity:.7}"
    "@media (prefers-reduced-motion:no-preference){"
    ".deco-grid{animation:ng-nodes 26s linear infinite}"
    ".deco-grid::before{animation:ng-floor 7s linear infinite}"
    ".deco-grid::after{animation:ng-scan 14s ease-in-out infinite}"
    "@keyframes ng-nodes{from{background-position:0 0,0 0,0 0,0 0,0 0,0 0,0 0}"
    "to{background-position:340px 200px,-300px 260px,360px -240px,-380px 180px,220px 280px,0 0,0 0}}"
    "@keyframes ng-floor{from{background-position:0 0}to{background-position:0 58px}}"
    "@keyframes ng-scan{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}}"
    # --- magenta-glitch bilingual toggle (seed, enhanced) ---
    ".lang-toggle{border-color:var(--accent)}"
    ".lang-toggle button.active{background:var(--accent);color:var(--bg);"
    "box-shadow:2px 0 0 var(--accent2),-2px 0 0 var(--accent3),0 0 18px color-mix(in srgb,var(--accent) 55%,transparent)}"
    "@media (prefers-reduced-motion:no-preference){"
    ".lang-toggle button.active{animation:ng-glitch 3.4s steps(1) infinite}"
    "@keyframes ng-glitch{0%,92%,100%{box-shadow:2px 0 0 var(--accent2),-2px 0 0 var(--accent3),0 0 18px color-mix(in srgb,var(--accent) 55%,transparent)}"
    "94%{box-shadow:-3px 0 0 var(--accent2),3px 0 0 var(--accent3),0 0 22px color-mix(in srgb,var(--accent) 70%,transparent)}"
    "96%{box-shadow:3px 0 0 var(--accent2),-3px 0 0 var(--accent3),0 0 14px color-mix(in srgb,var(--accent) 50%,transparent)}}}"
    # --- GLITCH-FLICKER hero headline: chromatic-aberration node text, motion-gated ---
    ".hero-home h1,.subpage-hero h1{position:relative}"
    "@media (prefers-reduced-motion:no-preference){.hero-home h1{animation:ng-flicker 7s steps(1) infinite}"
    "@keyframes ng-flicker{0%,90%,100%{text-shadow:0 0 20px color-mix(in srgb,var(--accent) 40%,transparent)}"
    "92%{text-shadow:-2px 0 0 var(--accent2),2px 0 0 var(--accent),0 0 28px color-mix(in srgb,var(--accent) 60%,transparent)}"
    "94%{text-shadow:2px 0 0 var(--accent3),-2px 0 0 var(--accent2),0 0 16px color-mix(in srgb,var(--accent) 50%,transparent)}}}"
    # --- 3D TILT cards: nodes that lift toward the viewer on hover (network feel) ---
    ".card,.stat-card{transform-style:preserve-3d}"
    "@media (hover:hover){"
    ".card:hover{transform:perspective(700px) rotateX(4deg) rotateY(-4deg) translateY(-5px);"
    "box-shadow:0 22px 50px rgba(0,0,0,.5),0 0 0 1px color-mix(in srgb,var(--accent) 50%,transparent),"
    "0 0 30px color-mix(in srgb,var(--accent) 24%,transparent)}"
    ".stat-card:hover{transform:perspective(700px) rotateX(5deg) translateY(-5px);"
    "box-shadow:0 0 28px color-mix(in srgb,var(--accent) 24%,transparent)}"
    ".btn-primary:hover{box-shadow:0 0 24px color-mix(in srgb,var(--accent) 55%,transparent)}"
    ".btn-ghost:hover{box-shadow:0 0 20px color-mix(in srgb,var(--accent) 45%,transparent)}"
    ".partner-card:hover,.ins-card:hover{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 40%,transparent),"
    "0 18px 44px rgba(0,0,0,.5)}}"
    # --- card corner NODE: a glowing connection point on every card/stat tile ---
    ".card,.stat-card{position:relative}"
    ".card::after,.stat-card::after{content:'';position:absolute;top:-3px;left:-3px;width:7px;height:7px;"
    "border-radius:50%;background:var(--accent);pointer-events:none;"
    "box-shadow:0 0 10px color-mix(in srgb,var(--accent) 85%,transparent);opacity:.0;transition:opacity .3s}"
    "@media (hover:hover){.card:hover::after,.stat-card:hover::after{opacity:1}}"
    # --- neon network section dividers: rule with a centered + two satellite nodes ---
    "section + section{position:relative}"
    "section + section::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);"
    "width:min(880px,86%);height:1px;pointer-events:none;"
    "background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 60%,transparent) 22%,"
    "color-mix(in srgb,var(--accent2) 60%,transparent) 78%,transparent)}"
    "section + section::after{content:'';position:absolute;top:0;left:50%;width:6px;height:6px;"
    "transform:translate(-50%,-50%) rotate(45deg);pointer-events:none;background:var(--accent);"
    "box-shadow:0 0 12px color-mix(in srgb,var(--accent) 80%,transparent),"
    "-110px 0 0 -1px color-mix(in srgb,var(--accent2) 70%,transparent),"
    "110px 0 0 -1px color-mix(in srgb,var(--accent3) 70%,transparent)}"
    # --- eyebrow gets a faint neon ring to tie into the grid mood ---
    ".eyebrow{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 16%,transparent),"
    "0 0 16px color-mix(in srgb,var(--accent) 12%,transparent)}"
    # --- next-class node-unit + home-contact + campus-split network accents ---
    ".next-class{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 22%,transparent),"
    "0 0 30px color-mix(in srgb,var(--accent) 12%,transparent)}"
    ".next-class .nc-unit{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 25%,transparent)}"
    ".home-contact .hc-box{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 20%,transparent),"
    "0 0 40px color-mix(in srgb,var(--accent) 10%,transparent)}"
    ".campus-split .campus-col .campus-progs li::before{color:var(--accent2)}"
    # --- grid-tilt media: keep the 3D node feel but clamp it on small screens so tilted tiles
    #     never push past the viewport; flatten perspective under ~640px ---
    ".ms-grid-tilt .m-tile{box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 18%,transparent)}"
    "@media (max-width:640px){.ms-grid-tilt .m-grid{perspective:none}"
    ".ms-grid-tilt .m-tile{transform:translateY(22px)}"
    ".ms-grid-tilt .m-tile:hover{transform:translateY(-3px)}"
    # disable the heaviest bg layer cost on very small screens (perf), keep nodes
    ".deco-grid::before{opacity:.38;height:38vh}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 06-neon-grid.")
