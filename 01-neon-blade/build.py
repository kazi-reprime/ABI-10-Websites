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
   01-neon-blade — unique polish + responsive fixes (SITE_CSS)
   ============================================================ */

/* --- FIX 1: mobile drawer anchoring (belt-and-suspenders) -----------------
   The engine already flips .primary-nav to a fixed drawer anchored at top:100%
   for max-width:1280px. .site-header has backdrop-filter, making it the
   containing block for the fixed drawer, so top:100% == the header's own bottom
   edge — correct and robust to the promo banner wrapping to multiple rows. We
   re-assert top:100% across the FULL engine drawer range so the anchoring holds
   even if upstream spacing changes. */
@media (max-width:1280px){
  .primary-nav{top:100%;max-height:calc(100dvh - 100%)}
}

/* --- FIX 2: desktop 12-item nav anti-clip (>=1281px) ----------------------
   At >=1281px the engine renders all 12 links inline (flex:1; flex-wrap:nowrap).
   On the narrowest desktop widths the rightmost links can crowd, so allow a
   graceful, scrollbar-less horizontal scroll as a safety net — no link is ever
   silently hidden. (Below 1281px the engine drawer takes over, so this never
   affects mobile.) */
@media (min-width:1281px){
  .primary-nav{overflow-x:auto;overflow-y:hidden;scrollbar-width:none;-ms-overflow-style:none}
  .primary-nav::-webkit-scrollbar{display:none}
}

/* --- POLISH 1: unique cyberpunk neon EN/ES segmented toggle ---------------
   Glowing neon-outlined switch, cyan default + magenta-tinted active glow,
   clipped corners. Restyles only .lang-toggle; no markup/JS changes. */
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

/* --- POLISH 2: neon hero underline ----------------------------------------
   A short animated cyan->magenta neon bar under the hero/subpage H1. */
.subpage-hero h1::after,.hero h1::after{
  content:"";display:block;width:clamp(64px,12vw,120px);height:3px;margin:18px auto 0;border-radius:3px;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  box-shadow:0 0 14px color-mix(in srgb,var(--accent) 70%,transparent),0 0 26px color-mix(in srgb,var(--accent2) 45%,transparent);
  background-size:200% 100%;animation:abiUnderline 5s ease-in-out infinite
}
@keyframes abiUnderline{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

/* --- POLISH 3: card hover neon glow + accent section divider --------------- */
.card:hover{
  border-color:color-mix(in srgb,var(--accent) 55%,transparent);
  box-shadow:0 0 22px color-mix(in srgb,var(--accent) 22%,transparent),0 16px 40px rgba(0,0,0,.45)
}
section + section{position:relative}
section + section::before{
  content:"";position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:min(120px,40%);height:1px;
  background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 60%,transparent),transparent)
}

/* --- respect reduced motion ----------------------------------------------- */
@media (prefers-reduced-motion:reduce){
  .lang-toggle button.active{animation:none}
  .subpage-hero h1::after,.hero h1::after{animation:none}
}
"""

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 01-neon-blade.")
