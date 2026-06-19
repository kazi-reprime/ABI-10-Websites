#!/usr/bin/env python3
"""
_polish.py — idempotent QA polish for 01-neon-blade (Cyberpunk · Neon Blade).

Injects two <style> blocks immediately before </head> in all 11 pages:
  1. #abi-toggle-custom — unique cyberpunk neon segmented EN/ES toggle
     (glowing neon-outlined switch, cyan default + magenta-tinted active glow,
     animated sliding scanline). Restyles ONLY .lang-toggle, .lang-toggle button,
     .lang-toggle button.active. No markup/JS changes.
  2. #abi-fix-custom — fixes the desktop nav-clipping bug: between 1100px and
     1280px the 11-item .primary-nav (flex:1; flex-wrap:nowrap; overflow:hidden)
     clips the rightmost links behind the brand logo before the hamburger
     appears. Allow graceful horizontal scroll + tighter spacing so no link
     is silently hidden.

Both injections are idempotent (skipped if the marker id already present).
Run from anywhere:  python3 01-neon-blade/_polish.py
"""

import os

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

HERE = os.path.dirname(os.path.abspath(__file__))

# --- 1. Unique cyberpunk neon segmented toggle -----------------------------
# Accent cyan #00f0ff (default glow) + magenta #ff2bd6 (active state glow).
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* === Cyberpunk Neon Blade — unique EN/ES segmented switch === */
.lang-toggle{
  position:relative;display:inline-flex;align-items:stretch;
  height:38px;padding:2px;gap:2px;border-radius:10px;overflow:hidden;
  background:linear-gradient(180deg,rgba(0,240,255,.06),rgba(255,43,214,.05));
  border:1.5px solid rgba(0,240,255,.55);
  box-shadow:0 0 0 1px rgba(0,240,255,.18),0 0 14px rgba(0,240,255,.30),
             inset 0 0 10px rgba(0,240,255,.12);
  -webkit-clip-path:polygon(7px 0,100% 0,100% calc(100% - 7px),calc(100% - 7px) 100%,0 100%,0 7px);
  clip-path:polygon(7px 0,100% 0,100% calc(100% - 7px),calc(100% - 7px) 100%,0 100%,0 7px);
}
.lang-toggle button{
  position:relative;z-index:1;background:transparent;border:0;
  color:rgba(0,240,255,.78);padding:0 14px;min-width:44px;cursor:pointer;
  font-weight:900;letter-spacing:.18em;font-family:inherit;font-size:.74rem;
  border-radius:8px;text-shadow:0 0 6px rgba(0,240,255,.35);
  transition:color .22s ease,text-shadow .22s ease,background .22s ease;
}
.lang-toggle button:hover{color:#bff7ff;text-shadow:0 0 10px rgba(0,240,255,.7);}
.lang-toggle button.active{
  color:#03060a;
  background:linear-gradient(135deg,#00f0ff 0%,#36f7ff 45%,#ff2bd6 140%);
  text-shadow:none;
  box-shadow:0 0 12px rgba(0,240,255,.85),0 0 22px rgba(255,43,214,.45),
             inset 0 0 6px rgba(255,255,255,.55);
  animation:abiTogGlow 2.4s ease-in-out infinite;
}
@keyframes abiTogGlow{
  0%,100%{box-shadow:0 0 12px rgba(0,240,255,.85),0 0 22px rgba(255,43,214,.40),inset 0 0 6px rgba(255,255,255,.55);}
  50%{box-shadow:0 0 18px rgba(0,240,255,1),0 0 30px rgba(255,43,214,.62),inset 0 0 8px rgba(255,255,255,.7);}
}
@media (prefers-reduced-motion:reduce){.lang-toggle button.active{animation:none;}}
</style>"""

# --- 2. Layout fix: stop desktop nav from clipping links --------------------
FIX_STYLE = """<style id="abi-fix-custom">
/* === Layout fix: prevent .primary-nav clipping links (1100-1280px) === */
@media (min-width:1101px){
  .primary-nav{overflow-x:auto;overflow-y:hidden;scrollbar-width:none;-ms-overflow-style:none;}
  .primary-nav::-webkit-scrollbar{display:none;}
}
@media (min-width:1101px) and (max-width:1280px){
  .primary-nav{gap:2px;}
  .primary-nav a{padding:8px 7px;font-size:.78rem;letter-spacing:0;}
}
</style>"""


def inject(html: str, marker_id: str, block: str) -> tuple[str, bool]:
    """Insert block before </head> if marker_id not already present."""
    if marker_id in html:
        return html, False
    idx = html.lower().rfind("</head>")
    if idx == -1:
        return html, False
    return html[:idx] + block + "\n" + html[idx:], True


def main() -> None:
    for name in PAGES:
        path = os.path.join(HERE, name)
        if not os.path.isfile(path):
            print(f"SKIP (missing): {name}")
            continue
        with open(path, "r", encoding="utf-8") as fh:
            html = fh.read()

        html, did_tog = inject(html, "abi-toggle-custom", TOGGLE_STYLE)
        html, did_fix = inject(html, "abi-fix-custom", FIX_STYLE)

        if did_tog or did_fix:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
        print(f"{name:18} toggle={'+' if did_tog else 'skip'}  fix={'+' if did_fix else 'skip'}")


if __name__ == "__main__":
    main()
