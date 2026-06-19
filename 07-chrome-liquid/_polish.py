#!/usr/bin/env python3
"""
Polish script for 07-chrome-liquid (Brutalist · Chrome Orb, blue/beige flat brutalist).

Idempotently injects two <style> blocks before </head> in all 11 pages:
  1. <style id="abi-toggle-custom">  — unique flat-brutalist EN/ES toggle
  2. <style id="abi-fix-custom">      — minor layout safety fixes

Restyles ONLY .lang-toggle / .lang-toggle button / .lang-toggle button.active.
Does NOT alter markup or JS. Safe to run multiple times.

Run:  cd 07-chrome-liquid && python3 _polish.py
"""
import re
import pathlib

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

HERE = pathlib.Path(__file__).resolve().parent

# ── 1. UNIQUE TOGGLE: hard-edged offset-shadow block switch ──────────────────
# Flat brutalist: zero radius, heavy 2px ink border, a real "hard shadow"
# offset block (3px, no blur). Active button = solid blue slab that visually
# presses into the shadow (offset collapses) — distinct from a pill.
TOGGLE_CSS = """<style id="abi-toggle-custom">
/* ABI 07-chrome-liquid — flat brutalist EN/ES toggle (hard offset-shadow block switch) */
.lang-toggle{
  display:inline-flex; align-items:stretch; height:36px;
  border:2px solid #0a0a0a; border-radius:0; overflow:visible;
  background:#ece9e3;
  box-shadow:3px 3px 0 0 #0a0a0a;      /* hard, blur-free brutalist drop */
  padding:0;
}
.lang-toggle button{
  position:relative;
  background:transparent; color:#0a0a0a;
  border:0; border-radius:0;
  padding:0 16px; min-width:46px;
  font-family:inherit; font-weight:900; font-size:.78rem; letter-spacing:.16em;
  text-transform:uppercase; cursor:pointer;
  transition:background .12s linear, color .12s linear;
}
/* hard divider slab between the two options */
.lang-toggle button + button{ border-left:2px solid #0a0a0a; }
.lang-toggle button:hover{ background:#dad6cd; }
.lang-toggle button.active{
  background:#1a3cff; color:#ece9e3;   /* solid blocky active slab */
  box-shadow:inset 0 0 0 2px #0a0a0a;  /* crisp inner edge, no rounding */
}
.lang-toggle button.active:hover{ background:#1a3cff; }
.lang-toggle button:focus-visible{ outline:3px solid #1a3cff; outline-offset:2px; }
</style>"""

# ── 2. LAYOUT FIX BLOCK ──────────────────────────────────────────────────────
# Defensive, idempotent. Keeps the brutalist toggle from being squashed when the
# top-banner wraps tightly on very narrow phones, and guarantees the hard shadow
# is never clipped by the banner edge.
FIX_CSS = """<style id="abi-fix-custom">
/* ABI 07-chrome-liquid — minor layout safety fixes */
.top-banner{ row-gap:8px; }
.lang-toggle{ flex:0 0 auto; }                 /* never let the switch collapse */
@media (max-width:480px){
  .lang-toggle{ height:34px; box-shadow:2px 2px 0 0 #0a0a0a; }
  .lang-toggle button{ padding:0 12px; min-width:42px; letter-spacing:.12em; }
}
</style>"""

BLOCKS = [
    ('id="abi-toggle-custom"', TOGGLE_CSS),
    ('id="abi-fix-custom"', FIX_CSS),
]


def polish(path: pathlib.Path) -> str:
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html:
        return f"SKIP (no </head>): {path.name}"

    to_inject = []
    for marker, block in BLOCKS:
        if marker in html:
            continue  # already present — idempotent
        to_inject.append(block)

    if not to_inject:
        return f"unchanged (already injected): {path.name}"

    payload = "\n".join(to_inject) + "\n</head>"
    # Replace only the first </head>.
    new_html = html.replace("</head>", payload, 1)
    path.write_text(new_html, encoding="utf-8")
    return f"injected {len(to_inject)} block(s): {path.name}"


def main():
    for name in PAGES:
        p = HERE / name
        if not p.exists():
            print(f"MISSING: {name}")
            continue
        print(polish(p))


if __name__ == "__main__":
    main()
