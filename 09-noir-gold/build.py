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
    "/* === 09-noir-gold: cinematic noir + gold === */"

    # ---- Bodoni heading wrap safety net (engine only sets overflow-wrap on <p>) ----
    "h1,h2,h3,h4{overflow-wrap:break-word;word-wrap:break-word;hyphens:auto}"

    # ---- Refined gold lang-toggle (AA: near-black ink on gold = 9.46:1) ----
    ".lang-toggle{height:34px;border-width:1px;letter-spacing:.2em}"
    ".lang-toggle button.active{background:var(--accent);color:#0a0908}"

    # ============================================================
    #  A. CINEMATIC ATMOSPHERE — three fixed full-screen layers stacked under
    #     content (z below .container/section z:2). Order: vignette → film grain.
    #     The engine's deco-spotlight (z:1, cursor-tracked) already provides the
    #     moving gold spotlight; we deepen the room around it.
    # ============================================================
    #     Both attach to the engine's always-present, fixed, full-screen cursor-tracked
    #     .deco-spotlight element (z:1, pointer-events:none) via its pseudo-elements —
    #     no new markup needed (build.py only edits CSS/tokens).
    # A1. Theatre vignette — a deep darkened frame so the centre reads "lit on stage".
    ".deco-spotlight::before{content:'';position:fixed;inset:0;z-index:1;pointer-events:none;"
    "background:radial-gradient(120% 90% at 50% 38%,transparent 40%,color-mix(in srgb,var(--bg) 72%,#000) 100%)}"
    # A2. Film grain — tileable SVG noise via data URI (self-contained), faint, animated drift.
    ".deco-spotlight::after{content:'';position:fixed;inset:-120px;z-index:1;pointer-events:none;opacity:.05;mix-blend-mode:overlay;"
    "background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\");"
    "background-size:160px 160px}"
    "@media (prefers-reduced-motion:no-preference){.deco-spotlight::after{animation:noirGrain 1.1s steps(4) infinite}}"
    "@keyframes noirGrain{0%{transform:translate(0,0)}25%{transform:translate(-30px,12px)}"
    "50%{transform:translate(18px,-22px)}75%{transform:translate(-12px,26px)}100%{transform:translate(0,0)}}"

    # ============================================================
    #  B. LETTERBOX — fixed film mattes top & bottom with a gold hairline. Slim
    #     (clamped) so content is never obscured; above atmosphere, below content.
    # ============================================================
    "body::before,body::after{content:'';position:fixed;left:0;right:0;height:clamp(14px,2.2vh,30px);"
    "z-index:20;pointer-events:none}"
    "body::before{top:0;border-bottom:1px solid color-mix(in srgb,var(--accent) 30%,transparent);"
    "background:linear-gradient(180deg,var(--bg),color-mix(in srgb,var(--bg) 0%,transparent))}"
    "body::after{bottom:0;border-top:1px solid color-mix(in srgb,var(--accent) 30%,transparent);"
    "background:linear-gradient(0deg,var(--bg),color-mix(in srgb,var(--bg) 0%,transparent))}"
    # drop on mobile so the sticky call bar + safe-areas stay clear
    "@media (max-width:980px){body::before,body::after{display:none}}"

    # ============================================================
    #  C. HERO — a single spotlit frame: gold eyebrow capsule glows, the gold-sheen
    #     h1 (engine hfx-gold) sits over a soft pool of light, thin gold rules below.
    # ============================================================
    ".hero-home,.subpage-hero{isolation:isolate}"
    ".hero-home::before,.subpage-hero::before{content:'';position:absolute;left:50%;top:34%;translate:-50% -50%;"
    "width:min(120%,1100px);height:min(90%,540px);z-index:-1;pointer-events:none;"
    "background:radial-gradient(closest-side,color-mix(in srgb,var(--accent) 14%,transparent),transparent 72%);"
    "filter:blur(8px)}"
    # mobile: clip the wider-than-viewport hero glow so it can never extend the scroll width
    "@media (max-width:980px){.hero-home,.subpage-hero{overflow:hidden}"
    ".hero-home::before,.subpage-hero::before{width:100%}}"
    ".hero-home .eyebrow,.subpage-hero .eyebrow{background:color-mix(in srgb,var(--accent) 8%,transparent);"
    "box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 22%,transparent),"
    "0 0 26px color-mix(in srgb,var(--accent) 18%,transparent)}"
    ".hero-home h1,.subpage-hero h1{text-shadow:0 2px 30px color-mix(in srgb,var(--accent) 22%,transparent)}"
    # a centred hairline beneath the hero sub — a closing gold cut
    ".hero-home .sub::after,.subpage-hero .sub::after{content:'';display:block;width:64px;height:1px;margin:22px auto 0;"
    "background:linear-gradient(90deg,transparent,var(--accent),transparent)}"

    # ============================================================
    #  D. SECTION RHYTHM — alternating "scenes". Even sections sit in a darker pit
    #     with a top + bottom gold hairline, like cuts between film reels.
    # ============================================================
    "main section:nth-of-type(even){background:linear-gradient(180deg,"
    "color-mix(in srgb,#000 26%,transparent),transparent 14%,transparent 86%,color-mix(in srgb,#000 26%,transparent))}"
    "main section:nth-of-type(even)::before,main section:nth-of-type(even)::after{content:'';position:absolute;"
    "left:0;right:0;height:1px;pointer-events:none;"
    "background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 34%,transparent),transparent)}"
    "main section:nth-of-type(even)::before{top:0}main section:nth-of-type(even)::after{bottom:0}"
    # section h2 — small gold serif over-rule, cinematic chapter mark
    "main section>.container>h2:first-child::before,.cta-band h2::before{content:'';display:block;width:38px;height:2px;"
    "margin:0 0 16px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent))}"
    ".center h2::before,.cta-band h2::before{margin-left:auto;margin-right:auto;"
    "background:linear-gradient(90deg,transparent,var(--accent),transparent)}"

    # ---- Gold serif eyebrow rule — luxe hairline trailing each accent eyebrow ----
    ".eyebrow-acc{position:relative}"
    ".eyebrow-acc::after{content:'';display:inline-block;vertical-align:middle;width:clamp(22px,4vw,46px);"
    "height:1px;margin-left:12px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent))}"
    ".center .eyebrow-acc::after,.m-head .eyb::after{display:none}"

    # ============================================================
    #  E. CARDS — dramatic high-contrast: deep shadow, warm corner key-light that
    #     blooms on hover, and a gold rim that ignites. Excludes image partner cards.
    # ============================================================
    ".card{box-shadow:0 18px 44px -18px #000,inset 0 1px 0 color-mix(in srgb,var(--accent) 9%,transparent)}"
    ".card:hover{box-shadow:0 26px 60px -16px #000,0 0 0 1px color-mix(in srgb,var(--accent) 40%,transparent)}"
    ".card:not(.partner-card){position:relative}"
    ".card:not(.partner-card)::after{content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:0;"
    "background:radial-gradient(120% 90% at 85% 0%,color-mix(in srgb,var(--accent) 11%,transparent),transparent 55%);"
    "opacity:.6;transition:opacity .45s}"
    ".card:not(.partner-card):hover::after{opacity:1}"
    ".card:not(.partner-card)>*{position:relative;z-index:1}"
    # details FAQ cards share the noir card frame already; warm the open one
    "details.card[open]{border-color:color-mix(in srgb,var(--accent) 42%,transparent)}"

    # ============================================================
    #  F. BUTTONS — the primary is a cast-gold plate with a sheen sweep on hover;
    #     the ghost fills with a warm gold wash. Sharp corners suit the noir frame.
    # ============================================================
    ".btn-primary{position:relative;overflow:hidden;background:linear-gradient(180deg,var(--accent2),var(--accent) 55%,var(--accent3));"
    "color:#0a0908;box-shadow:0 12px 30px -10px color-mix(in srgb,var(--accent) 60%,#000)}"
    ".btn-primary::after{content:'';position:absolute;inset:0;transform:translateX(-130%);"
    "background:linear-gradient(105deg,transparent 30%,color-mix(in srgb,#fff 60%,transparent) 50%,transparent 70%);"
    "transition:transform .6s}"
    ".btn-primary:hover::after{transform:translateX(130%)}"
    ".btn-ghost{border-color:color-mix(in srgb,var(--accent) 60%,transparent)}"
    "@media (prefers-reduced-motion:reduce){.btn-primary::after{display:none}}"

    # ============================================================
    #  G. STATS BAND — counters in a darker pit; the accent rail and number glow
    #     like marquee bulbs, with a faint gold underglow under the band.
    # ============================================================
    ".stats-band{background:linear-gradient(180deg,color-mix(in srgb,#000 30%,transparent),transparent)}"
    ".stat-card{box-shadow:0 16px 40px -20px #000}"
    ".stat-card .count{text-shadow:0 0 26px color-mix(in srgb,var(--accent) 32%,transparent)}"
    ".stat-card::before{width:2px;box-shadow:0 0 14px color-mix(in srgb,var(--accent) 60%,transparent)}"

    # ============================================================
    #  H. SHARED COMPONENTS — cinematic gold treatment.
    # ============================================================
    # H1. next-class countdown — a marquee plate; units glow, label spaced like a sign.
    ".next-class{box-shadow:0 18px 44px -20px #000,inset 0 0 0 1px color-mix(in srgb,var(--accent) 14%,transparent)}"
    ".next-class .nc-unit{box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 18%,transparent)}"
    ".next-class .nc-unit b{text-shadow:0 0 16px color-mix(in srgb,var(--accent) 34%,transparent)}"
    # H2. home contact box — a lit set; gold rim, deep cast shadow.
    ".home-contact .hc-box{box-shadow:0 30px 70px -30px #000,inset 0 1px 0 color-mix(in srgb,var(--accent) 10%,transparent)}"
    # H3. campus split — each campus column reads as its own framed scene.
    ".campus-split .campus-col{position:relative;padding-left:18px}"
    ".campus-split .campus-col::before{content:'';position:absolute;left:0;top:4px;bottom:4px;width:2px;"
    "background:linear-gradient(180deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent));border-radius:2px}"
    # H4. instructor cards — portrait under a noir top-light; photo desaturates to b/w,
    #     warming to full colour on hover (vintage-cinema reveal).
    ".ins-card .ins-photo{position:relative}"
    ".ins-card .ins-photo img{filter:grayscale(.55) contrast(1.06) brightness(.92);transition:transform .6s,filter .6s}"
    ".ins-card:hover .ins-photo img{filter:none}"
    ".ins-card .ins-photo::after{content:'';position:absolute;inset:0;pointer-events:none;"
    "background:linear-gradient(180deg,transparent 55%,color-mix(in srgb,var(--bg) 78%,transparent))}"
    "@media (prefers-reduced-motion:reduce){.ins-card .ins-photo img{transition:none}}"
    # H5. partner cards — gold name plate already over image; add a cast shadow + rim ignite.
    ".partner-card:hover{box-shadow:0 24px 56px -20px #000,0 0 0 1px color-mix(in srgb,var(--accent) 38%,transparent)}"
    # H6. media band (spotlight-cine) — caption in gold; tile rim warms on hover.
    ".media-band .m-tile:hover{border-color:color-mix(in srgb,var(--accent) 45%,transparent)}"

    # ============================================================
    #  I. ELEGANT SLOW REVEALS — the engine reveals sections/cards (revealUp). Slow
    #     and soften it here for a vintage, deliberate fade-in feel.
    # ============================================================
    "@media (prefers-reduced-motion:no-preference){"
    ".reveal{animation-duration:.9s;animation-timing-function:cubic-bezier(.16,.84,.3,1)}"
    "}"

    # keep all motion polish honest under reduced-motion
    "@media (prefers-reduced-motion:reduce){.card::after,.card,.stat-card,.ins-card .ins-photo img{transition:none}}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 09-noir-gold.")
