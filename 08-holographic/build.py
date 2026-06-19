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
    "logo_dark_bg": False,
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
    "logo": "site-08-abimono.jpeg",
    "video": "abstract_animation_for_american_-.mp4",
    "site_index": 7,
    "favicon": "site-08-abimono-favicon.png",
    "og": "site-08-abimono-og.png"
}

# ---- per-site unique polish (engine appends this last; overrides engine for THIS site only) ----
# ICED HOLOGRAM: deep iridescent base, frosted glass cards with prismatic edge gradients,
# floating holo rings, conic rainbow-sheen accents, 3D rotate-on-hover glass tiles.
# All translucency via color-mix(); every animation gated behind prefers-reduced-motion.
SITE_CSS = (
    "/* ===== unique polish for 08-holographic (iced hologram glass) ===== */"

    # ===== UNIQUE PURE-CSS ANIMATED BACKGROUND =====
    # Layer A: prismatic conic-gradient mesh that slowly hue-drifts (distinct from 03-aurora's
    # soft light wash — this is darker, glassier, ring-based). Layer B: floating holo rings.
    # Both sit at z-index 0 behind the engine's deco-orbs; non-interactive.
    "body::before{content:'';position:fixed;inset:-20%;z-index:0;pointer-events:none;"
    "background:"
    "conic-gradient(from 0deg at 22% 28%,color-mix(in srgb,var(--accent2) 26%,transparent),"
    "color-mix(in srgb,var(--accent) 22%,transparent),color-mix(in srgb,var(--accent3) 24%,transparent),"
    "color-mix(in srgb,var(--accent2) 26%,transparent)),"
    "conic-gradient(from 180deg at 80% 75%,color-mix(in srgb,var(--accent3) 22%,transparent),"
    "color-mix(in srgb,var(--accent2) 20%,transparent),transparent 70%);"
    "filter:blur(70px) saturate(1.25);opacity:.6;"
    "-webkit-mask-image:radial-gradient(ellipse 75% 65% at 50% 35%,#000 0,transparent 100%);"
    "mask-image:radial-gradient(ellipse 75% 65% at 50% 35%,#000 0,transparent 100%);"
    "animation:holoMesh 30s ease-in-out infinite alternate}"
    "@keyframes holoMesh{0%{transform:scale(1) rotate(0deg)}100%{transform:scale(1.18) rotate(8deg)}}"
    # Layer B: floating concentric prismatic RINGS (the site's ring motif), drawn with
    # repeating radial-gradient as a pure-CSS second fixed layer — no extra DOM needed.
    "body::after{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;"
    "background:"
    "repeating-radial-gradient(circle at 16% 22%,transparent 0 46px,"
    "color-mix(in srgb,var(--accent2) 22%,transparent) 46px 48px,transparent 48px 92px),"
    "repeating-radial-gradient(circle at 86% 78%,transparent 0 40px,"
    "color-mix(in srgb,var(--accent3) 20%,transparent) 40px 42px,transparent 42px 80px);"
    "-webkit-mask-image:radial-gradient(circle at 16% 22%,#000 0,transparent 38%),"
    "radial-gradient(circle at 86% 78%,#000 0,transparent 34%);"
    "mask-image:radial-gradient(circle at 16% 22%,#000 0,transparent 38%),"
    "radial-gradient(circle at 86% 78%,#000 0,transparent 34%);"
    "opacity:.5;animation:holoRings 26s ease-in-out infinite alternate}"
    "@keyframes holoRings{0%{transform:translate(0,0)}100%{transform:translate(28px,-30px)}}"
    "@media (max-width:760px){body::after{opacity:.32}}"

    # ===== frosted, iridescent EN/ES toggle =====
    ".lang-toggle{position:relative;border-color:color-mix(in srgb,var(--accent) 55%,transparent);"
    "background:color-mix(in srgb,var(--accent) 9%,transparent);backdrop-filter:blur(8px) saturate(1.3);"
    "-webkit-backdrop-filter:blur(8px) saturate(1.3);"
    "box-shadow:0 2px 14px color-mix(in srgb,var(--accent) 22%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 18%,transparent)}"
    ".lang-toggle button{min-height:44px}"  # WCAG tap target (overrides engine's compact toggle for this site)
    ".lang-toggle button.active{background:linear-gradient(120deg,color-mix(in srgb,var(--accent) 34%,transparent),"
    "color-mix(in srgb,var(--accent2) 30%,transparent));color:var(--ink);"
    "text-shadow:0 0 10px color-mix(in srgb,var(--accent2) 45%,transparent)}"

    # ===== brand-mark: white logo framed as a frosted glass chip with prismatic edge =====
    ".brand-mark.logo-light{background:linear-gradient(145deg,#fff,color-mix(in srgb,#fff 90%,var(--accent2) 10%));"
    "border:1px solid color-mix(in srgb,var(--accent2) 35%,transparent);"
    "box-shadow:0 4px 16px color-mix(in srgb,var(--accent) 30%,transparent),"
    "0 0 0 1px color-mix(in srgb,#fff 50%,transparent),inset 0 1px 0 #fff}"
    # standalone spinning pole: glassy holo capsule beside the chip
    ".barber-pole{box-shadow:0 2px 10px color-mix(in srgb,var(--accent2) 40%,transparent),"
    "inset 0 0 0 1px color-mix(in srgb,#fff 22%,transparent)}"

    # ===== banner call CTAs: lift to 44px tap target on this site =====
    "@media (max-width:760px){.cta-call{min-height:44px}}"

    # ===== HERO: holographic eyebrow + glassy next-class plate =====
    ".hero-home,.subpage-hero{position:relative;z-index:2}"
    ".eyebrow{background:color-mix(in srgb,var(--accent2) 12%,transparent);"
    "border-color:color-mix(in srgb,var(--accent2) 45%,transparent);backdrop-filter:blur(6px);"
    "-webkit-backdrop-filter:blur(6px);"
    "box-shadow:0 0 22px color-mix(in srgb,var(--accent2) 25%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 18%,transparent)}"
    ".subpage-hero p.sub,.hero-home p.sub{text-shadow:0 1px 20px color-mix(in srgb,var(--accent) 18%,transparent)}"

    # ===== SECTIONS: alternating prismatic hairline dividers (nth-of-type) =====
    "main section:nth-of-type(odd)::before{content:'';position:absolute;left:0;right:0;top:0;height:1px;"
    "background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent2) 55%,transparent),"
    "color-mix(in srgb,var(--accent3) 45%,transparent),transparent);opacity:.55}"
    "main section:nth-of-type(even){background:linear-gradient(180deg,"
    "color-mix(in srgb,var(--accent) 5%,transparent),transparent 55%)}"

    # ===== CARD glassmorphism: prismatic edge + diagonal sheen + 3D lift =====
    ".card{position:relative;overflow:hidden;"
    "background:linear-gradient(160deg,color-mix(in srgb,#fff 8%,transparent),"
    "color-mix(in srgb,var(--accent) 6%,transparent));"
    "backdrop-filter:blur(14px) saturate(1.3);-webkit-backdrop-filter:blur(14px) saturate(1.3);"
    "box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 12%,transparent)}"
    ".card::before{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;z-index:0;"
    "background:linear-gradient(135deg,color-mix(in srgb,#fff 12%,transparent) 0%,transparent 36%,"
    "transparent 64%,color-mix(in srgb,var(--accent2) 13%,transparent) 100%);opacity:.85;transition:opacity .3s}"
    # prismatic conic edge ring revealed on hover
    ".card::after{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;z-index:0;padding:1px;"
    "background:conic-gradient(from 140deg,color-mix(in srgb,var(--accent2) 70%,transparent),"
    "color-mix(in srgb,var(--accent) 60%,transparent),color-mix(in srgb,var(--accent3) 65%,transparent),"
    "color-mix(in srgb,var(--accent2) 70%,transparent));"
    "-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);"
    "-webkit-mask-composite:xor;mask-composite:exclude;opacity:0;transition:opacity .35s}"
    ".card>*{position:relative;z-index:1}"
    ".card:hover{transform:translateY(-6px);border-color:color-mix(in srgb,var(--accent2) 60%,transparent);"
    "box-shadow:0 22px 52px color-mix(in srgb,var(--accent) 30%,transparent),"
    "inset 0 1px 0 color-mix(in srgb,#fff 16%,transparent)}"
    ".card:hover::before{opacity:1}"
    ".card:hover::after{opacity:.9}"
    # FAQ details: holo summary marker
    "details.card summary::after{color:var(--accent2);text-shadow:0 0 12px color-mix(in srgb,var(--accent2) 50%,transparent)}"

    # ===== BUTTONS: rainbow-sheen primary + glass ghost =====
    ".btn-primary{background-image:linear-gradient(120deg,var(--accent),var(--accent2),var(--accent3),var(--accent));"
    "background-size:280% 100%;color:var(--bg);animation:holoBtn 9s linear infinite;"
    "box-shadow:0 8px 26px color-mix(in srgb,var(--accent) 35%,transparent)}"
    "@keyframes holoBtn{0%{background-position:0% 50%}100%{background-position:280% 50%}}"
    ".btn-ghost{position:relative;border-color:color-mix(in srgb,var(--accent2) 60%,transparent);"
    "background:color-mix(in srgb,var(--accent2) 7%,transparent);backdrop-filter:blur(6px);"
    "-webkit-backdrop-filter:blur(6px)}"
    ".btn-ghost:hover{background:linear-gradient(120deg,color-mix(in srgb,var(--accent) 90%,transparent),"
    "color-mix(in srgb,var(--accent2) 90%,transparent));color:var(--bg);border-color:transparent}"

    # ===== STATS BAND: glassy plates with conic top sheen + holo count glow =====
    ".stats-band{position:relative}"
    ".stat-card{background:linear-gradient(160deg,color-mix(in srgb,#fff 7%,transparent),"
    "color-mix(in srgb,var(--accent) 6%,transparent));backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}"
    ".stat-card::before{background:linear-gradient(180deg,var(--accent2),var(--accent3));width:3px}"
    ".stat-card .count{background:linear-gradient(120deg,var(--accent2),var(--accent),var(--accent3));"
    "-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;"
    "filter:drop-shadow(0 0 14px color-mix(in srgb,var(--accent2) 40%,transparent))}"
    ".stat-card:hover{border-color:color-mix(in srgb,var(--accent2) 60%,transparent);"
    "box-shadow:0 18px 44px color-mix(in srgb,var(--accent) 26%,transparent)}"
    # row-stat (inline mini stats) get the glass treatment too
    ".row-stat .s b{background:linear-gradient(120deg,var(--accent2),var(--accent));"
    "-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}"

    # ===== NEXT-CLASS: holographic countdown plate, glowing nc-unit chips =====
    ".next-class{position:relative;overflow:hidden;border-color:color-mix(in srgb,var(--accent2) 40%,transparent);"
    "background:linear-gradient(160deg,color-mix(in srgb,#fff 8%,transparent),"
    "color-mix(in srgb,var(--accent) 7%,transparent));"
    "box-shadow:0 12px 36px color-mix(in srgb,var(--accent) 24%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 14%,transparent)}"
    ".next-class .nc-unit{background:linear-gradient(160deg,color-mix(in srgb,var(--accent2) 18%,transparent),"
    "color-mix(in srgb,var(--accent) 14%,transparent));"
    "box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent2) 28%,transparent)}"
    ".next-class .nc-unit b{color:var(--accent2);text-shadow:0 0 14px color-mix(in srgb,var(--accent2) 45%,transparent)}"

    # ===== HOME CONTACT: frosted hc-box with prismatic edge =====
    ".home-contact .hc-box{position:relative;overflow:hidden;"
    "background:linear-gradient(155deg,color-mix(in srgb,#fff 8%,transparent),"
    "color-mix(in srgb,var(--accent) 7%,transparent));"
    "border-color:color-mix(in srgb,var(--accent2) 32%,transparent);"
    "backdrop-filter:blur(16px) saturate(1.25);-webkit-backdrop-filter:blur(16px) saturate(1.25);"
    "box-shadow:0 18px 50px color-mix(in srgb,var(--accent) 24%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 14%,transparent)}"
    ".home-contact .hc-box::before{content:'';position:absolute;inset:0;pointer-events:none;border-radius:inherit;padding:1px;"
    "background:conic-gradient(from 120deg,color-mix(in srgb,var(--accent2) 55%,transparent),"
    "color-mix(in srgb,var(--accent3) 50%,transparent),color-mix(in srgb,var(--accent) 55%,transparent),"
    "color-mix(in srgb,var(--accent2) 55%,transparent));"
    "-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);"
    "-webkit-mask-composite:xor;mask-composite:exclude;opacity:.5}"
    ".input:focus{box-shadow:0 0 0 3px color-mix(in srgb,var(--accent2) 25%,transparent)}"

    # ===== CAMPUS SPLIT: holo bullet markers =====
    ".campus-split .campus-col .campus-progs li::before{color:var(--accent2);"
    "text-shadow:0 0 10px color-mix(in srgb,var(--accent2) 50%,transparent)}"

    # ===== INSTRUCTOR CARDS: prismatic photo sheen + holo tags =====
    ".ins-card .ins-photo{position:relative}"
    ".ins-card .ins-photo::after{content:'';position:absolute;inset:0;pointer-events:none;"
    "background:linear-gradient(150deg,color-mix(in srgb,var(--accent2) 22%,transparent),transparent 45%,"
    "color-mix(in srgb,var(--accent3) 20%,transparent));mix-blend-mode:screen;opacity:.45;transition:opacity .4s}"
    ".ins-card:hover .ins-photo::after{opacity:.8}"
    ".ins-card .ins-tags{color:var(--accent2)}"

    # ===== PARTNER CARDS: glass body + holo name plate =====
    ".partner-card .body{background:linear-gradient(160deg,color-mix(in srgb,#fff 6%,transparent),transparent)}"
    ".partner-card .partner-title{color:var(--ink)}"
    ".partner-card .locations{color:var(--accent2)}"
    ".partner-card:hover{box-shadow:0 22px 52px color-mix(in srgb,var(--accent) 28%,transparent)}"

    # ===== MEDIA BAND: holo eyebrow + ring focus on tiles (3D rotate handled by glass-rotate) =====
    ".media-band .m-head .eyb{color:var(--accent2);text-shadow:0 0 12px color-mix(in srgb,var(--accent2) 40%,transparent)}"
    ".m-tile{box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 10%,transparent)}"
    ".m-tile:hover{box-shadow:0 22px 54px color-mix(in srgb,var(--accent) 30%,transparent),"
    "0 0 0 1px color-mix(in srgb,var(--accent2) 45%,transparent)}"
    # MOBILE: flatten the glass-rotate 3D tiles (rotateY around left edge projects past the
    # viewport on narrow/single-column layouts). Kill perspective + all rotateY states and
    # clip the grid horizontally as a belt-and-suspenders guard against 3D overflow.
    "@media (max-width:760px){.media-band.ms-glass-rotate .m-grid{perspective:none;overflow-x:clip}"
    ".media-band.ms-glass-rotate .m-tile,"
    ".media-band.ms-glass-rotate .m-tile.shown,"
    ".media-band.ms-glass-rotate .m-tile:hover{transform:translateY(24px);transform-origin:center}"
    ".media-band.ms-glass-rotate .m-tile.shown{transform:none}}"

    # ===== reduced-motion: kill all custom motion (engine guards globally too) =====
    "@media (prefers-reduced-motion:reduce){.btn-primary{animation:none}"
    "body::before,body::after{animation:none}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 08-holographic.")
