#!/usr/bin/env python3
"""
Polish script for 03-aurora-fade (Light Holographic Shader theme).

Idempotently injects two <style> blocks before </head> in all 11 pages:

  1. #abi-toggle-custom  — a UNIQUE iridescent, hue-shifting gradient-bordered
     EN/ES language toggle with a soft glassy active state. Matches the light
     holographic theme (violet #a285ff accent). Restyles ONLY:
       .lang-toggle, .lang-toggle button, .lang-toggle button.active
     Markup and JS are left untouched.

  2. #abi-fix-custom — layout/contrast fix. On this LIGHT theme the generated
     nav hover/active rule uses `background: rgba(255,255,255,.04)` (a
     near-invisible white-on-white tint, a dark-theme leftover). This block
     gives the active/hover nav item a visible, theme-appropriate violet tint
     so the current page is actually distinguishable.

Run from anywhere:  python3 03-aurora-fade/_polish.py
Re-running is safe: existing blocks are replaced, not duplicated.
"""

import os
import re

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

# 1) Unique iridescent hue-shifting toggle (light holographic theme).
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* === ABI Aurora Fade — unique iridescent EN/ES toggle (light holographic) === */
.lang-toggle{
  position:relative;
  display:inline-flex;align-items:stretch;
  height:38px;padding:2px;gap:2px;
  border:0;border-radius:999px;overflow:visible;
  background:
    linear-gradient(rgba(255,255,255,.78),rgba(255,255,255,.78)) padding-box,
    linear-gradient(90deg,#a285ff,#ff6fd8,#3ad0ff,#a285ff) border-box;
  background-size:auto, 300% 100%;
  border:2px solid transparent;
  animation:abiHoloBorder 8s linear infinite;
  box-shadow:0 6px 20px rgba(124,92,255,.22), inset 0 1px 0 rgba(255,255,255,.6);
  -webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);
}
.lang-toggle button{
  position:relative;z-index:1;
  background:transparent;border:0;border-radius:999px;
  color:#5a4bb3;
  padding:0 16px;min-width:46px;cursor:pointer;
  font-family:inherit;font-weight:900;letter-spacing:.14em;font-size:.78rem;
  transition:color .25s ease, transform .15s ease;
}
.lang-toggle button:hover{color:#1a1430;transform:translateY(-1px);}
.lang-toggle button.active{
  color:#1a1430;
  background:
    linear-gradient(135deg, rgba(162,133,255,.32), rgba(255,111,216,.26) 45%, rgba(58,208,255,.30));
  box-shadow:
    0 2px 10px rgba(124,92,255,.30),
    inset 0 1px 0 rgba(255,255,255,.75),
    inset 0 0 0 1px rgba(255,255,255,.45);
  -webkit-backdrop-filter:blur(6px) saturate(1.4);backdrop-filter:blur(6px) saturate(1.4);
}
@keyframes abiHoloBorder{from{background-position:0 0, 0% 50%}to{background-position:0 0, 300% 50%}}
@media (prefers-reduced-motion:reduce){.lang-toggle{animation:none;}}
</style>"""

# 2) Layout/contrast fix — visible nav active/hover state on the light theme.
FIX_STYLE = """<style id="abi-fix-custom">
/* === ABI Aurora Fade — layout/contrast fixes (light theme) === */
/* Generated rule used rgba(255,255,255,.04) (invisible white-on-white on a
   light header). Give the active/current nav item a real violet tint so the
   current page is distinguishable. */
.primary-nav a:hover,
.primary-nav a.active{
  background:rgba(124,92,255,.12);
  color:var(--accent);
}
.primary-nav a.active{box-shadow:inset 0 -2px 0 var(--accent);}
@media (max-width:1100px){
  /* In the mobile drawer, keep the active row readable too. */
  .primary-nav a.active{background:rgba(124,92,255,.14);box-shadow:none;}
}
</style>"""

HEAD_CLOSE_RE = re.compile(r"</head>", re.IGNORECASE)


def strip_block(html: str, block_id: str) -> str:
    """Remove an existing <style id="block_id">...</style> if present."""
    pattern = re.compile(
        r'[ \t]*<style id="' + re.escape(block_id) + r'">.*?</style>\n?',
        re.DOTALL | re.IGNORECASE,
    )
    return pattern.sub("", html)


def polish_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()

    original = html
    # Idempotent: remove any prior versions first.
    html = strip_block(html, "abi-toggle-custom")
    html = strip_block(html, "abi-fix-custom")

    if not HEAD_CLOSE_RE.search(html):
        return f"SKIP (no </head>): {os.path.basename(path)}"

    injection = TOGGLE_STYLE + "\n" + FIX_STYLE + "\n</head>"
    html = HEAD_CLOSE_RE.sub(lambda m: injection, html, count=1)

    if html == original:
        return f"UNCHANGED: {os.path.basename(path)}"

    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return f"OK: {os.path.basename(path)}"


def main() -> None:
    for page in PAGES:
        path = os.path.join(SITE_DIR, page)
        if not os.path.isfile(path):
            print(f"MISSING: {page}")
            continue
        print(polish_file(path))


if __name__ == "__main__":
    main()
