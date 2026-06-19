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
    "logo_dark_bg": True,
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
    "logo": "site-02-chrome.jpeg",
    "video": "animated_logo_transition_america-.mp4",
    "site_index": 1,
    "favicon": "site-02-chrome-favicon.png",
    "og": "site-02-chrome-og.png"
}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
# LIQUID-METAL BRUTALISM for 02-chrome-culture.
# Red + brushed chrome on near-black. Hard 0-radius edges, riveted metal panels,
# solid offset block shadows, brushed-metal sweeps/shine, a scrolling steel marquee,
# heavy slab headings, and a pure-CSS animated brushed-metal background.
# All widths use clamp/%/max-width (no horizontal scroll); color-mix only (no var()NN);
# every animation gated behind prefers-reduced-motion. Mobile-nav drawer blocks preserved.
SITE_CSS = (
    "/* ===== 02-chrome-culture: liquid-metal brutalism ===== */"

    # --- pure-CSS animated brushed-metal background (signature backdrop) ---
    # Layered fine vertical brushing + a slow diagonal chrome sheen sweep + a faint
    # red horizon glow. Sits above the deco-chrome layer, below content (z-index 1).
    "body::before{content:'';position:fixed;inset:0;z-index:1;pointer-events:none;"
    "background:"
    "repeating-linear-gradient(90deg,rgba(255,255,255,.020) 0 1px,transparent 1px 3px),"
    "radial-gradient(120% 60% at 50% -10%,color-mix(in srgb,var(--accent) 12%,transparent) 0,transparent 60%),"
    "linear-gradient(180deg,color-mix(in srgb,#fff 4%,transparent),transparent 40%)}"
    "body::after{content:'';position:fixed;inset:-40% -10%;z-index:1;pointer-events:none;"
    "background:linear-gradient(115deg,transparent 38%,color-mix(in srgb,#fff 7%,transparent) 48%,"
    "color-mix(in srgb,var(--accent) 9%,transparent) 50%,color-mix(in srgb,#fff 7%,transparent) 52%,transparent 62%);"
    "background-size:300% 300%;mix-blend-mode:screen}"
    "@media (prefers-reduced-motion:no-preference){"
    "body::after{animation:chromeSweep 14s ease-in-out infinite}"
    "@keyframes chromeSweep{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}}"

    # --- scrolling steel marquee accent under the hero (signature touch) ---
    # Brutalist repeating tag rail. Pure CSS, duplicated content via ::before/::after so
    # the loop is seamless; disabled under reduced-motion (becomes a static rivet rail).
    ".subpage-hero{position:relative;overflow:hidden}"
    ".subpage-hero::after{content:'CUT SHARP \\00B7 CUT CLEAN \\00B7 CUT FOR GOOD \\00B7 MANHATTAN + BRONX \\00B7 ';"
    "position:absolute;left:0;right:0;bottom:0;white-space:nowrap;font-family:var(--font-head);"
    "font-weight:900;font-size:clamp(.7rem,2vw,1rem);letter-spacing:.18em;text-transform:uppercase;"
    "color:color-mix(in srgb,var(--accent) 70%,#fff);padding:7px 0;"
    "border-top:2px solid color-mix(in srgb,#fff 16%,transparent);"
    "border-bottom:2px solid color-mix(in srgb,#000 60%,transparent);"
    "background:linear-gradient(180deg,#26262b,#101013);"
    "box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 18%,transparent);"
    "text-shadow:0 1px 0 rgba(0,0,0,.6);will-change:transform}"
    "@media (prefers-reduced-motion:no-preference){"
    ".subpage-hero::after{animation:steelMarquee 18s linear infinite}"
    "@keyframes steelMarquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}}"
    "@media (max-width:480px){.subpage-hero::after{letter-spacing:.1em}}"

    # --- heavy slab eyebrow as a riveted red tab ---
    ".eyebrow{border-radius:0;border:2px solid color-mix(in srgb,var(--accent) 50%,transparent);"
    "background:color-mix(in srgb,var(--accent) 12%,transparent);font-weight:900;color:var(--accent3);"
    "box-shadow:3px 3px 0 color-mix(in srgb,var(--accent) 30%,transparent)}"

    # --- metallic EN/ES toggle (brutalist hard corners + chrome active state) ---
    ".lang-toggle{border-radius:0;border-width:2px}"
    ".lang-toggle button{font-style:italic;letter-spacing:.16em}"
    ".lang-toggle button.active{background:linear-gradient(180deg,#fff,var(--mut));color:#111;text-shadow:0 1px 0 rgba(255,255,255,.6)}"

    # --- buttons: 0-radius blades with chrome shine sweep + hard offset (signature #1) ---
    ".btn{border-radius:0;text-transform:uppercase;letter-spacing:.06em;font-weight:900}"
    ".btn-primary{position:relative;overflow:hidden;isolation:isolate;"
    "background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 92%,#fff),var(--accent));"
    "box-shadow:5px 5px 0 #000,inset 0 1px 0 color-mix(in srgb,#fff 40%,transparent)}"
    ".btn-primary:hover{transform:translate(2px,2px);box-shadow:2px 2px 0 #000,inset 0 1px 0 color-mix(in srgb,#fff 40%,transparent)}"
    ".btn-primary::after{content:'';position:absolute;top:0;left:-130%;width:55%;height:100%;z-index:1;"
    "background:linear-gradient(100deg,transparent,color-mix(in srgb,#fff 75%,transparent),transparent);"
    "transform:skewX(-22deg);pointer-events:none}"
    ".btn-ghost{position:relative;background:linear-gradient(180deg,#2a2a30,#141417);color:var(--accent3);"
    "border:2px solid color-mix(in srgb,#fff 22%,transparent);box-shadow:5px 5px 0 color-mix(in srgb,var(--accent) 34%,transparent)}"
    ".btn-ghost:hover{background:var(--accent);color:#111;border-color:var(--accent);transform:translate(2px,2px);"
    "box-shadow:2px 2px 0 color-mix(in srgb,var(--accent) 34%,transparent)}"
    "@media (prefers-reduced-motion:no-preference){"
    ".btn-primary::after{transition:left .6s cubic-bezier(.2,.8,.2,1)}"
    ".btn-primary:hover::after{left:140%}}"

    # --- riveted metal panel cards: hard offset block shadow + brushed sweep (signature #2) ---
    ".card{border-radius:0;border:2px solid color-mix(in srgb,#fff 14%,transparent);"
    "background:linear-gradient(180deg,color-mix(in srgb,#fff 4%,transparent),var(--glass));"
    "box-shadow:7px 7px 0 color-mix(in srgb,var(--accent) 26%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 12%,transparent);"
    "position:relative;overflow:hidden}"
    # corner rivets (two dots, top-left + bottom-right) — pure CSS, decorative
    ".card::before{content:'';position:absolute;top:8px;left:8px;width:6px;height:6px;border-radius:50%;z-index:3;"
    "background:radial-gradient(circle at 35% 30%,#fff,#6b6e76 55%,#1a1a1d);box-shadow:0 0 0 1px rgba(0,0,0,.4)}"
    # brushed-metal sheen that wipes across on hover
    ".card::after{content:'';position:absolute;top:0;left:-75%;width:50%;height:100%;z-index:2;pointer-events:none;"
    "background:linear-gradient(100deg,transparent,color-mix(in srgb,#fff 22%,transparent),transparent);transform:skewX(-18deg)}"
    ".card:hover{box-shadow:3px 3px 0 var(--accent),inset 0 1px 0 color-mix(in srgb,#fff 14%,transparent);"
    "border-color:var(--accent);transform:translate(2px,2px)}"
    "@media (prefers-reduced-motion:no-preference){.card::after{transition:left .6s cubic-bezier(.2,.8,.2,1)}.card:hover::after{left:130%}}"
    "@media (prefers-reduced-motion:reduce){.card{transition:none}}"
    "@media (max-width:480px){.card{box-shadow:4px 4px 0 color-mix(in srgb,var(--accent) 26%,transparent)}.card:hover{transform:none}}"

    # --- alternating section backgrounds + hard chrome dividers (brushed steel rhythm) ---
    "main section:nth-of-type(even){background:linear-gradient(180deg,color-mix(in srgb,#fff 3%,transparent),transparent)}"
    "main section:nth-of-type(odd){background:"
    "repeating-linear-gradient(90deg,color-mix(in srgb,#fff 2%,transparent) 0 1px,transparent 1px 4px)}"
    "main section+section{border-top:3px solid color-mix(in srgb,var(--accent) 40%,transparent);"
    "box-shadow:0 -2px 0 color-mix(in srgb,#000 60%,transparent)}"

    # --- brushed-metal bevel on the sticky header + chrome eyebrow rule (signature #3) ---
    ".site-header{box-shadow:inset 0 1px 0 color-mix(in srgb,#fff 18%,transparent),0 2px 0 #000}"
    ".eyebrow-acc{position:relative;padding-bottom:6px}"
    ".eyebrow-acc::after{content:'';position:absolute;left:0;bottom:0;width:40px;height:3px;"
    "background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent3) 80%,transparent))}"
    ".eyebrow-acc.center::after{left:50%;transform:translateX(-50%)}"

    # --- stats band: machined steel plates with red top-edge ---
    ".stat-card{border-radius:0;border:2px solid color-mix(in srgb,#fff 12%,transparent);"
    "background:linear-gradient(180deg,#23232a,#121215);box-shadow:5px 5px 0 color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".stat-card::before{width:100%;height:4px;bottom:auto;background:var(--accent);transform:scaleX(0);transform-origin:left}"
    ".stat-card.in::before,.stat-card:hover::before{transform:scaleX(1)}"
    ".stat-card:hover{transform:translate(2px,2px);box-shadow:2px 2px 0 color-mix(in srgb,var(--accent) 22%,transparent)}"

    # --- next-class countdown: bolted instrument panel ---
    ".next-class{border-radius:0;border:2px solid color-mix(in srgb,#fff 14%,transparent);"
    "background:linear-gradient(180deg,#23232a,#101013);box-shadow:6px 6px 0 #000}"
    ".next-class .nc-unit{border-radius:0;border:1px solid color-mix(in srgb,var(--accent) 30%,transparent);"
    "background:color-mix(in srgb,var(--accent) 10%,transparent)}"

    # --- home contact box: heavy bolted slab ---
    ".home-contact .hc-box{border-radius:0;border:2px solid color-mix(in srgb,#fff 14%,transparent);"
    "box-shadow:8px 8px 0 color-mix(in srgb,var(--accent) 24%,transparent)}"
    "@media (max-width:480px){.home-contact .hc-box{box-shadow:5px 5px 0 color-mix(in srgb,var(--accent) 24%,transparent)}}"

    # --- campus split + instructor + partner cards inherit the riveted panel look; sharpen edges ---
    ".campus-split .campus-col{box-shadow:7px 7px 0 color-mix(in srgb,var(--accent) 22%,transparent)}"
    ".ins-card .ins-photo,.partner-card .img-wrap{border-radius:0}"
    ".ins-card:hover{border-color:var(--accent)}"
    ".partner-card .locations{letter-spacing:.16em}"

    # --- media band metal-slab tiles already sweep; square them off + red rivet edge ---
    ".media-band .m-tile{border-radius:0;border-color:color-mix(in srgb,#fff 14%,transparent)}"
    ".media-band .m-tile:hover{box-shadow:6px 6px 0 var(--accent)}"

    # --- inputs: machined slots ---
    ".input{border-radius:0;border:2px solid color-mix(in srgb,#fff 12%,transparent);background:#0a0a0c}"
    ".radio-pill span,.hc-pill{border-radius:0}"

    # --- spinning header pole: square it slightly + steel collar to match the chrome logo ---
    ".barber-pole{border-radius:2px;box-shadow:0 2px 8px rgba(0,0,0,.5),inset 0 0 0 1px color-mix(in srgb,#fff 30%,transparent)}"
)

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 02-chrome-culture.")
