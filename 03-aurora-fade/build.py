#!/usr/bin/env python3
"""Standalone build file for Aurora Fade (03-aurora-fade).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 03-aurora-fade/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for 03-aurora-fade ----
TOKENS = {
    "slug": "03-aurora-fade",
    "logo_dark_bg": False,
    "bg": "#f4f1ff",
    "bg2": "rgba(255,255,255,.55)",
    "ink": "#1a1430",
    "mut": "#6b6385",
    # accent darkened from #7c5cff -> #6536e6 so accent-as-text (eyebrow, price, nav links,
    # list markers, form labels) and bg-text-on-accent-fill (buttons, badges, sticky bar)
    # both reach WCAG AA: 5.85:1 on the lavender bg (was 3.91:1, failing). Keeps violet identity.
    "accent": "#6536e6",
    "accent2": "#ff6fd8",
    "accent3": "#3ad0ff",
    "line": "rgba(101,54,230,.20)",
    "glass": "rgba(255,255,255,.55)",
    "body_font": "'Trebuchet MS','Segoe UI',sans-serif",
    "heading_font": "Georgia,'Times New Roman',serif",
    "heading_ls": "-.01em",
    "heading_lh": "1.02",
    "card_radius": "24px",
    "button_radius": "46px",
    "button_shape": "pill",
    "ribbon_bg": "rgba(255,255,255,.7)",
    # ribbon text on the near-white banner: #6536e6 = ~6.2:1 (was #7c5cff at 4.22:1)
    "ribbon_color": "#6536e6",
    "ribbon_text": "American Barber Institute · Where craft becomes career · Next start: First Monday",
    "decoration": "holographic",
    "vibe": "Holographic light theme with iridescent gradients on lavender",
    "h1_effect": "holo-gradient",
    "media_style": "holo-float"
}

# ---- site identity ----
SITE = {
    "slug": "03-aurora-fade",
    "vercel_name": "abi-app-3",
    "logo": "site-03-aurora.jpeg",
    "video": "animated_logo_transition_america-_2.mp4",
    "site_index": 2,
    "favicon": "site-03-aurora-favicon.png",
    "og": "site-03-aurora-og.png"
}

# ---- per-site unique polish (engine appends this last; overrides the engine) ----
# Airy holographic LIGHT theme. Every override below is contrast-checked against the
# lavender bg (#f4f1ff). Iridescent gradients use color-mix(), never var(--x)NN. All
# motion is wrapped in prefers-reduced-motion:no-preference.
SITE_CSS = r"""
/* ===== unique polish for 03-aurora-fade (holographic light) ===== */

/* --- CONTRAST FIX: footer ---
   The engine hardcodes .site-footer background:rgba(0,0,0,.4), which on this light page
   composites to a muddy grey (~#929199) where --mut footer links land at only 1.80:1 and
   accent at 1.39:1 (broken-looking + failing AA). Repaint it as a soft lavender glass panel:
   --mut 4.67:1, --ink 14.8:1, --accent 5.9:1 — all pass, and it stays on-theme/airy. */
.site-footer{
  background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 3%,var(--bg)),color-mix(in srgb,var(--accent) 7%,var(--bg)));
  color:var(--mut);
  border-top:1px solid color-mix(in srgb,var(--accent) 26%,transparent);
}
/* iridescent hairline above the footer */
.site-footer::before{
  content:"";position:absolute;left:0;right:0;top:-1px;height:2px;pointer-events:none;
  background:linear-gradient(90deg,
    color-mix(in srgb,var(--accent) 75%,transparent),
    color-mix(in srgb,var(--accent2) 60%,transparent),
    color-mix(in srgb,var(--accent3) 55%,transparent),
    color-mix(in srgb,var(--accent) 75%,transparent));
  background-size:200% 100%;
}
@media (prefers-reduced-motion:no-preference){
  .site-footer::before{animation:af-shimmer 9s linear infinite}
}

/* --- CONTRAST FIX: holo-gradient H1 ---
   The engine's .hfx-holo h1 sweeps accent->accent2(#ff6fd8,2.2:1)->accent3(#3ad0ff,1.6:1),
   which washes out on a light bg. Re-stop the gradient with darkened iridescent hues
   (violet #6536e6=5.85:1, magenta #c026a8=4.62:1, teal #1786b3=3.70:1) so every part of the
   heading stays legible as large text. A faint text-shadow guards the lightest stop. */
.hfx-holo h1{
  background:linear-gradient(95deg,#6536e6 0%,#8a2fce 28%,#c026a8 52%,#1786b3 78%,#6536e6 100%);
  background-size:280% 100%;
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;
  text-shadow:0 1px 18px color-mix(in srgb,var(--accent) 22%,transparent);
}
@media (prefers-reduced-motion:reduce){
  .hfx-holo h1{animation:none;background-position:0 0}
}

/* --- iridescent EN/ES toggle (unique signature, elegant + light) --- */
.lang-toggle{
  border:0;padding:2px;border-radius:999px;
  background:linear-gradient(120deg,var(--accent),var(--accent2),var(--accent3),var(--accent));
  background-size:240% 100%;
  box-shadow:0 4px 16px color-mix(in srgb,var(--accent) 22%,transparent);
}
.lang-toggle button{border-radius:999px;color:#fff;transition:color .2s,background .2s}
.lang-toggle button.active{
  background:var(--bg);
  color:var(--accent);            /* 5.85:1 on the light pill */
  box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 30%,transparent);
}
@media (prefers-reduced-motion:no-preference){
  .lang-toggle{animation:af-shimmer 7s linear infinite}
}

/* --- gentle holographic accents (cards + media), kept soft on light --- */
.card,.stat-card{
  border-color:color-mix(in srgb,var(--accent) 16%,transparent);
}
.card::before{
  content:"";position:absolute;left:0;right:0;top:0;height:2px;border-radius:var(--card-r) var(--card-r) 0 0;
  background:linear-gradient(90deg,
    color-mix(in srgb,var(--accent) 70%,transparent),
    color-mix(in srgb,var(--accent2) 55%,transparent),
    color-mix(in srgb,var(--accent3) 50%,transparent));
  opacity:0;transition:opacity .3s;pointer-events:none;
}
.card:hover::before{opacity:1}
/* iridescent underline under section eyebrows */
.eyebrow-acc::after,.media-band .m-head .eyb::after{
  content:"";display:block;width:34px;height:2px;margin-top:6px;border-radius:2px;
  background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3));
}
/* primary button: soft iridescent lift on hover (text stays --bg on --accent = 5.85:1) */
.btn-primary{box-shadow:0 6px 20px color-mix(in srgb,var(--accent) 26%,transparent)}
.btn-primary:hover{box-shadow:0 10px 30px color-mix(in srgb,var(--accent) 38%,transparent)}

@keyframes af-shimmer{0%{background-position:0 0}100%{background-position:200% 0}}
"""

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built 03-aurora-fade.")
