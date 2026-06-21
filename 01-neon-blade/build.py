#!/usr/bin/env python3
"""Standalone build file for Neon Blade (01-neon-blade).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 01-neon-blade/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 01-neon-blade ----
TOKENS = {
    "slug": "01-neon-blade",
    "logo_dark_bg": True,
    "bg": "#05060a",
    "bg2": "#0a0d18",
    "ink": "#e9ecff",
    "mut": "#8b91b8",
    "accent": "#00f0ff",
    "accent2": "#ff2bd6",
    "accent3": "#7b5cff",
    "line": "rgba(123,92,255,.18)",
    "glass": "rgba(18,22,40,.55)",
    "body_font": "'Segoe UI',system-ui,sans-serif",
    "heading_font": "'Arial Black','Segoe UI',sans-serif",
    "heading_ls": "-.02em",
    "heading_lh": "1",
    "card_radius": "14px",
    "button_radius": "46px",
    "button_shape": "pill",
    "ribbon_bg": "linear-gradient(90deg,#ff2bd6,#7b5cff,#00f0ff)",
    "ribbon_color": "#04060c",
    "ribbon_text": "American Barber Institute · Manhattan + Bronx · Next class: First Monday of every month · GI Bill® accepted · 30+ years",
    "decoration": "neon-glow",
    "vibe": "Cyberpunk neon with cyan/magenta glow on deep black",
    "h1_effect": "glow",
    "media_style": "neon-scan"
}

# ---- site identity ----
SITE = {
    "slug": "01-neon-blade",
    "vercel_name": "abi-app-1",
    "logo": "site-01-neon.jpeg",
    "video": "cyberpunk_neon_animation_abi_mon-.mp4",
    "site_index": 0,
    "favicon": "site-01-neon-favicon.png",
    "og": "site-01-neon-og.png"
}

# ---- per-site unique polish (engine appends this last; SITE_CSS wins the cascade) ----
# Everything below is consolidated into the engine's single <style> block. It folds in
# the former _polish.py patches (unique neon EN/ES toggle + desktop nav-clip fix), the
# mobile drawer containing-block fix, and the signature cyberpunk polish. Translucent
# accent colors use color-mix(in srgb, var(--accent) N%, transparent) — never var(--x)NN.
SITE_CSS = r"""
/* ============================================================
   01-neon-blade — CYBERPUNK NEON signature look (SITE_CSS)
   Cyan #00f0ff + magenta #ff2bd6 on near-black. Glitch/scanline
   overlays, neon-outlined glowing clipped cards, diagonal section
   skews, animated cyan->magenta underlines + grid scanlines, and
   RGB-split image hover. Appended last; wins the cascade.
   ============================================================ */

/* --- FIX 1: mobile drawer anchoring (belt-and-suspenders) -----------------
   The engine already flips .primary-nav to a fixed drawer anchored at top:100%
   for max-width:1280px. .site-header has backdrop-filter, making it the
   containing block for the fixed drawer, so top:100% == the header's own bottom
   edge — correct and robust to the promo banner wrapping to multiple rows. We
   re-assert top:100% across the FULL engine drawer range so the anchoring holds
   even if upstream spacing changes. */
@media (max-width:1280px){
  .primary-nav{top:100%;max-height:calc(100dvh - var(--nav-top, 116px))}
}

/* (removed the desktop nav horizontal-scroll clip — it could hide Contact; the engine
   nav now fits all items, so no clipping safety net is needed.) */

/* ============================================================
   SIGNATURE BACKGROUND — animated neon grid + drifting scanline
   Two fixed pseudo-elements on <body>, GPU-light (transform/opacity
   only), layered above the engine deco (z-index:1) but behind all
   content (sections are z-index:2). Gated behind no-preference.
   ============================================================ */
body::before{
  content:"";position:fixed;inset:-2px;z-index:1;pointer-events:none;
  background-image:
    linear-gradient(color-mix(in srgb,var(--accent) 9%,transparent) 1px,transparent 1px),
    linear-gradient(90deg,color-mix(in srgb,var(--accent2) 7%,transparent) 1px,transparent 1px);
  background-size:46px 46px,46px 46px;
  -webkit-mask-image:radial-gradient(ellipse 90% 80% at 50% 35%,#000 0,transparent 75%);
  mask-image:radial-gradient(ellipse 90% 80% at 50% 35%,#000 0,transparent 75%);
  opacity:.5
}
body::after{
  content:"";position:fixed;left:0;right:0;top:0;height:34vh;z-index:1;pointer-events:none;
  background:linear-gradient(180deg,transparent,color-mix(in srgb,var(--accent) 14%,transparent) 48%,transparent);
  mix-blend-mode:screen;opacity:.5;transform:translateY(-40vh)
}
@media (prefers-reduced-motion:no-preference){
  body::before{animation:abiGridDrift 24s linear infinite}
  body::after{animation:abiScanSweep 7.5s linear infinite}
}
@keyframes abiGridDrift{to{background-position:46px 46px,-46px -46px}}
@keyframes abiScanSweep{0%{transform:translateY(-40vh)}100%{transform:translateY(140vh)}}

/* ============================================================
   HERO — glitch headline + animated neon underline
   ============================================================ */
.subpage-hero h1,.hero-home h1{position:relative;isolation:isolate}
.subpage-hero h1::after,.hero-home h1::after{
  content:"";display:block;width:clamp(72px,13vw,140px);height:3px;margin:18px auto 0;border-radius:3px;
  background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent));
  box-shadow:0 0 14px color-mix(in srgb,var(--accent) 75%,transparent),0 0 28px color-mix(in srgb,var(--accent2) 50%,transparent);
  background-size:200% 100%;animation:abiUnderline 5s ease-in-out infinite
}
@keyframes abiUnderline{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.eyebrow{
  position:relative;border-color:color-mix(in srgb,var(--accent) 50%,transparent);
  background:color-mix(in srgb,var(--accent) 8%,transparent);
  box-shadow:0 0 12px color-mix(in srgb,var(--accent) 22%,transparent),inset 0 0 8px color-mix(in srgb,var(--accent) 10%,transparent);
  text-shadow:0 0 8px color-mix(in srgb,var(--accent) 55%,transparent)
}
@media (prefers-reduced-motion:no-preference){
  .hero-home h1{animation:abiGlitch 6.5s steps(1) infinite}
  @keyframes abiGlitch{
    0%,93%,100%{text-shadow:0 0 24px color-mix(in srgb,var(--accent) 42%,transparent),0 0 48px color-mix(in srgb,var(--accent) 22%,transparent)}
    94%{text-shadow:-3px 0 var(--accent2),3px 0 var(--accent)}
    95%{text-shadow:3px 0 var(--accent2),-3px 0 var(--accent);transform:translateX(1px)}
    96%{text-shadow:-2px 0 var(--accent),2px 0 var(--accent2)}
    97%{text-shadow:0 0 24px color-mix(in srgb,var(--accent) 42%,transparent)}
  }
}

/* ============================================================
   SECTIONS — alternating diagonal-skew neon dividers
   Uses main section:nth-of-type(n) for distinct alternating
   treatments. Odd sections get a top cyan skewed hairline; even
   sections get a tinted skewed slab + magenta hairline.
   ============================================================ */
main section{position:relative}
main section:nth-of-type(even)::before{
  content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(100deg,color-mix(in srgb,var(--accent) 5%,transparent),transparent 40%,color-mix(in srgb,var(--accent2) 5%,transparent));
  transform:skewY(-1.6deg);transform-origin:left;
  border-top:1px solid color-mix(in srgb,var(--accent2) 30%,transparent);
  border-bottom:1px solid color-mix(in srgb,var(--accent) 24%,transparent)
}
main section:nth-of-type(odd) + section::after,
main section:nth-of-type(n+2)::after{
  content:"";position:absolute;top:0;left:50%;transform:translateX(-50%) skewX(-24deg);
  width:min(160px,46%);height:2px;border-radius:2px;
  background:linear-gradient(90deg,transparent,var(--accent),var(--accent2),transparent);
  box-shadow:0 0 12px color-mix(in srgb,var(--accent) 60%,transparent)
}
.eyebrow-acc{text-shadow:0 0 10px color-mix(in srgb,var(--accent) 45%,transparent)}

/* ============================================================
   CARDS — neon-outlined glowing panels w/ clipped corner
   ============================================================ */
.card{
  position:relative;
  border-color:color-mix(in srgb,var(--accent) 22%,transparent);
  background:linear-gradient(160deg,color-mix(in srgb,var(--accent) 5%,transparent),var(--glass) 60%);
  -webkit-clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px));
  clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px))
}
.card::after{
  content:"";position:absolute;top:0;right:0;width:14px;height:14px;pointer-events:none;
  background:linear-gradient(225deg,var(--accent2),transparent);opacity:.85
}
.card:hover{
  border-color:var(--accent);
  box-shadow:0 0 22px color-mix(in srgb,var(--accent) 30%,transparent),
             0 0 44px color-mix(in srgb,var(--accent2) 16%,transparent),
             0 16px 40px rgba(0,0,0,.5)
}
.eyebrow-acc.eyebrow-acc{display:block}

/* ============================================================
   BUTTONS — neon pill w/ scan-sweep + glow
   ============================================================ */
.btn-primary{
  background:linear-gradient(120deg,var(--accent),color-mix(in srgb,var(--accent) 70%,var(--accent2)));
  position:relative;overflow:hidden;
  box-shadow:0 0 16px color-mix(in srgb,var(--accent) 40%,transparent)
}
.btn-primary::before{
  content:"";position:absolute;top:0;left:-120%;width:55%;height:100%;
  background:linear-gradient(100deg,transparent,color-mix(in srgb,#fff 70%,transparent),transparent);
  transform:skewX(-20deg);transition:left .6s ease
}
.btn-primary:hover::before{left:160%}
.btn-primary:hover{box-shadow:0 0 26px var(--accent),0 0 46px color-mix(in srgb,var(--accent2) 40%,transparent),0 14px 28px rgba(0,0,0,.4)}
.btn-ghost{
  border-color:var(--accent);color:var(--accent);
  box-shadow:inset 0 0 12px color-mix(in srgb,var(--accent) 14%,transparent),0 0 10px color-mix(in srgb,var(--accent) 18%,transparent);
  text-shadow:0 0 8px color-mix(in srgb,var(--accent) 50%,transparent)
}
.btn-ghost:hover{
  background:var(--accent);color:var(--bg);text-shadow:none;
  box-shadow:0 0 24px var(--accent),0 0 44px color-mix(in srgb,var(--accent2) 35%,transparent)
}

/* ============================================================
   STATS BAND — neon HUD tiles, magenta count glow
   ============================================================ */
.stat-card{
  border-color:color-mix(in srgb,var(--accent) 26%,transparent);
  background:linear-gradient(160deg,color-mix(in srgb,var(--accent2) 5%,transparent),var(--glass) 55%)
}
.stat-card::before{background:linear-gradient(180deg,var(--accent),var(--accent2));box-shadow:0 0 14px var(--accent)}
.stat-card:hover{border-color:var(--accent);box-shadow:0 0 26px color-mix(in srgb,var(--accent) 24%,transparent),0 14px 36px rgba(0,0,0,.45)}
.stat-card .count{text-shadow:0 0 18px color-mix(in srgb,var(--accent) 55%,transparent),0 0 36px color-mix(in srgb,var(--accent2) 30%,transparent)}
.row-stat .s b{text-shadow:0 0 14px color-mix(in srgb,var(--accent) 45%,transparent)}

/* ============================================================
   BRAND MARK + BARBER POLE — neon-framed, glowing pole
   ============================================================ */
.brand-mark.logo-dark{
  box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 30%,transparent),0 0 16px color-mix(in srgb,var(--accent) 20%,transparent);
  background:color-mix(in srgb,var(--accent) 5%,transparent)
}
.barber-pole{
  border-color:color-mix(in srgb,var(--accent) 60%,transparent);
  box-shadow:0 0 12px color-mix(in srgb,var(--accent) 55%,transparent),0 0 22px color-mix(in srgb,var(--accent2) 28%,transparent),inset 0 0 0 1px rgba(255,255,255,.2)
}

/* ============================================================
   EN/ES TOGGLE — neon-outlined clipped segmented switch
   ============================================================ */
.lang-toggle{
  position:relative;display:inline-flex;align-items:stretch;
  height:44px;min-height:44px;padding:2px;gap:2px;border-radius:10px;overflow:hidden;
  background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 7%,transparent),color-mix(in srgb,var(--accent2) 6%,transparent));
  border:1.5px solid color-mix(in srgb,var(--accent) 55%,transparent);
  box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 18%,transparent),
             0 0 14px color-mix(in srgb,var(--accent) 30%,transparent),
             inset 0 0 10px color-mix(in srgb,var(--accent) 12%,transparent);
  -webkit-clip-path:polygon(7px 0,100% 0,100% calc(100% - 7px),calc(100% - 7px) 100%,0 100%,0 7px);
  clip-path:polygon(7px 0,100% 0,100% calc(100% - 7px),calc(100% - 7px) 100%,0 100%,0 7px)
}
.lang-toggle button{
  position:relative;z-index:1;background:transparent;border:0;
  color:color-mix(in srgb,var(--accent) 78%,var(--ink));
  padding:0 14px;min-width:44px;min-height:40px;cursor:pointer;
  font-weight:900;letter-spacing:.18em;font-family:inherit;font-size:.74rem;
  border-radius:8px;text-shadow:0 0 6px color-mix(in srgb,var(--accent) 35%,transparent);
  transition:color .22s ease,text-shadow .22s ease,background .22s ease
}
.lang-toggle button:hover{color:var(--ink);text-shadow:0 0 10px color-mix(in srgb,var(--accent) 70%,transparent)}
.lang-toggle button.active{
  color:var(--bg);
  background:linear-gradient(135deg,var(--accent) 0%,color-mix(in srgb,var(--accent) 80%,#fff) 45%,var(--accent2) 140%);
  text-shadow:none;
  box-shadow:0 0 12px color-mix(in srgb,var(--accent) 85%,transparent),
             0 0 22px color-mix(in srgb,var(--accent2) 45%,transparent),
             inset 0 0 6px color-mix(in srgb,#fff 55%,transparent);
  animation:abiTogGlow 2.4s ease-in-out infinite
}
@keyframes abiTogGlow{
  0%,100%{box-shadow:0 0 12px color-mix(in srgb,var(--accent) 85%,transparent),0 0 22px color-mix(in srgb,var(--accent2) 40%,transparent),inset 0 0 6px color-mix(in srgb,#fff 55%,transparent)}
  50%{box-shadow:0 0 18px var(--accent),0 0 30px color-mix(in srgb,var(--accent2) 62%,transparent),inset 0 0 8px color-mix(in srgb,#fff 70%,transparent)}
}

/* ============================================================
   NEXT-CLASS COUNTDOWN — HUD console w/ clipped corners
   ============================================================ */
.next-class{
  position:relative;border-color:color-mix(in srgb,var(--accent) 40%,transparent);
  background:linear-gradient(160deg,color-mix(in srgb,var(--accent) 7%,transparent),var(--glass) 60%);
  box-shadow:0 0 20px color-mix(in srgb,var(--accent) 18%,transparent),inset 0 0 14px color-mix(in srgb,var(--accent) 8%,transparent);
  -webkit-clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px);
  clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px)
}
.next-class .nc-unit{
  background:color-mix(in srgb,var(--accent) 12%,transparent);
  border:1px solid color-mix(in srgb,var(--accent) 30%,transparent)
}
.next-class .nc-unit b{text-shadow:0 0 12px color-mix(in srgb,var(--accent) 60%,transparent)}
.next-class .nc-date{text-shadow:0 0 10px color-mix(in srgb,var(--accent) 30%,transparent)}

/* ============================================================
   HOME CONTACT BOX — neon-edged console
   ============================================================ */
.home-contact .hc-box{
  border-color:color-mix(in srgb,var(--accent) 30%,transparent);
  background:linear-gradient(160deg,color-mix(in srgb,var(--accent2) 5%,transparent),var(--glass) 55%);
  box-shadow:0 0 30px color-mix(in srgb,var(--accent) 12%,transparent),inset 0 0 1px color-mix(in srgb,var(--accent) 40%,transparent)
}
.input:focus{box-shadow:0 0 14px color-mix(in srgb,var(--accent) 35%,transparent)}

/* ============================================================
   CAMPUS SPLIT — Manhattan/Bronx neon list markers
   ============================================================ */
.campus-split .campus-col{
  border-color:color-mix(in srgb,var(--accent) 28%,transparent)
}
.campus-split .campus-col .campus-progs li::before{
  color:var(--accent);text-shadow:0 0 8px color-mix(in srgb,var(--accent) 60%,transparent)
}
.campus-split h2 .nowrap-fit{text-shadow:0 0 16px color-mix(in srgb,var(--accent) 40%,transparent)}

/* ============================================================
   INSTRUCTOR CARDS — RGB-split photo hover + neon scan
   ============================================================ */
.ins-card .ins-photo{position:relative;overflow:hidden}
.ins-card .ins-photo::after{
  content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
  background:repeating-linear-gradient(0deg,transparent 0 2px,color-mix(in srgb,#000 12%,transparent) 2px 3px);
  opacity:.4;mix-blend-mode:overlay
}
.ins-card:hover .ins-photo img{
  filter:saturate(1.25) contrast(1.05)
       drop-shadow(2px 0 0 color-mix(in srgb,var(--accent2) 75%,transparent))
       drop-shadow(-2px 0 0 color-mix(in srgb,var(--accent) 75%,transparent))
}
.ins-card .ins-name{text-shadow:0 0 12px color-mix(in srgb,var(--accent) 30%,transparent)}

/* ============================================================
   PARTNER CARDS — neon underline name + glow on hover
   ============================================================ */
.partner-card{border-color:color-mix(in srgb,var(--accent) 22%,transparent)}
.partner-card .partner-title{
  position:relative;display:inline-block;padding-bottom:4px
}
.partner-card .partner-title::after{
  content:"";position:absolute;left:0;bottom:0;width:0;height:2px;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  box-shadow:0 0 8px var(--accent);transition:width .4s ease
}
.partner-card:hover .partner-title::after{width:100%}
.partner-card .locations{text-shadow:0 0 8px color-mix(in srgb,var(--accent) 40%,transparent)}

/* ============================================================
   MEDIA BAND — augments the engine ms-neon-scan style
   (chromatic-split + neon corner ticks on hover)
   ============================================================ */
.ms-neon-scan .m-tile{
  border-color:color-mix(in srgb,var(--accent) 45%,transparent)
}
.ms-neon-scan .m-tile:hover .m-media{
  filter:saturate(1.35) contrast(1.08)
       drop-shadow(2px 0 0 color-mix(in srgb,var(--accent2) 60%,transparent))
       drop-shadow(-2px 0 0 color-mix(in srgb,var(--accent) 60%,transparent))
}
.media-band .m-head h2{text-shadow:0 0 18px color-mix(in srgb,var(--accent) 30%,transparent)}

/* ============================================================
   DETAILS / FAQ — neon marker glow
   ============================================================ */
details.card summary::after{text-shadow:0 0 10px color-mix(in srgb,var(--accent) 60%,transparent)}

/* ============================================================
   FOOTER — neon top edge
   ============================================================ */
.site-footer{border-top:1px solid color-mix(in srgb,var(--accent) 28%,transparent);box-shadow:0 -1px 22px color-mix(in srgb,var(--accent) 10%,transparent) inset}
.footer-logo{box-shadow:0 0 16px color-mix(in srgb,var(--accent) 18%,transparent)}

/* ============================================================
   RESPECT REDUCED MOTION
   ============================================================ */
@media (prefers-reduced-motion:reduce){
  body::before,body::after{animation:none}
  .lang-toggle button.active{animation:none}
  .subpage-hero h1::after,.hero-home h1::after{animation:none}
}
"""

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 01-neon-blade.")
