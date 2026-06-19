#!/usr/bin/env python3
"""
Polish pass for ABI site 06-neon-grid (Theme: Particle Network / Glitch, magenta #ff2bd6).

Idempotently injects two <style> blocks before </head> in all 11 pages:

  1) #abi-toggle-custom  — a UNIQUE EN/ES language toggle styled as a magenta
     particle-grid switch with an RGB-split glitch active state. Only restyles
     .lang-toggle, .lang-toggle button, .lang-toggle button.active. No markup/JS changes.

  2) #abi-fix-custom — fixes a real CSS bug: the build emitted invalid color values
     `var(--accent)4d` (border-color) and `var(--accent)40` (hover box-shadow) on
     .m-tile / .m-tile:hover. Appending a raw hex-alpha suffix to a var() output is
     invalid CSS, so those declarations are silently dropped and the media-band tile
     border + hover glow never render. We re-declare them with valid color-mix() values
     keyed to the magenta theme accent.

Run from inside 06-neon-grid/:  python3 _polish.py
Safe to run repeatedly: each block is keyed by id and replaced (not duplicated).
"""

import re
import sys
from pathlib import Path

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

MAGENTA = "#ff2bd6"

# ---------------------------------------------------------------------------
# 1) Unique magenta particle-grid / glitch language toggle
# ---------------------------------------------------------------------------
# Distinct from a plain pill: square-cornered "grid module" with a fine
# magenta grid texture, scan-line sheen, and an active button that triggers a
# layered cyan/magenta RGB-split glitch (text-shadow split + clip jitter).
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* ABI 06-neon-grid — magenta particle-grid / glitch language toggle */
.lang-toggle{
  position:relative;
  display:inline-flex;align-items:stretch;height:38px;
  padding:3px;gap:3px;
  border-radius:6px;                 /* squared module, not a pill */
  border:1px solid rgba(255,43,214,.55);
  background:
    linear-gradient(rgba(255,43,214,.12),rgba(255,43,214,.04)),
    repeating-linear-gradient(0deg,rgba(255,43,214,.16) 0 1px,transparent 1px 7px),
    repeating-linear-gradient(90deg,rgba(255,43,214,.16) 0 1px,transparent 1px 7px),
    rgba(8,4,12,.55);
  box-shadow:0 0 0 1px rgba(0,0,0,.35) inset,0 6px 18px rgba(255,43,214,.18);
  overflow:hidden;
}
.lang-toggle::after{ /* moving scan sheen */
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(120deg,transparent 40%,rgba(255,43,214,.22) 50%,transparent 60%);
  background-size:220% 100%;
  animation:abiGridScan 5.5s linear infinite;mix-blend-mode:screen;
}
.lang-toggle button{
  position:relative;z-index:1;
  background:transparent;border:0;
  color:#cdb9d6;
  padding:0 14px;min-width:44px;
  border-radius:4px;
  cursor:pointer;font-weight:900;letter-spacing:.16em;
  font-family:inherit;font-size:.78rem;
  transition:color .18s ease,background .18s ease,text-shadow .18s ease;
}
.lang-toggle button:hover{ color:#fff; }
.lang-toggle button.active{
  color:#fff;
  background:
    linear-gradient(rgba(255,43,214,.30),rgba(255,43,214,.10)),
    repeating-linear-gradient(90deg,rgba(255,255,255,.10) 0 1px,transparent 1px 5px);
  box-shadow:0 0 0 1px rgba(255,43,214,.85),0 0 14px rgba(255,43,214,.6);
  /* cyan/magenta RGB split */
  text-shadow:-1.4px 0 rgba(0,240,255,.9),1.4px 0 rgba(255,43,214,.95);
  animation:abiGlitchSplit 2.4s steps(2,end) infinite;
}
@keyframes abiGridScan{ 0%{background-position:220% 0} 100%{background-position:-120% 0} }
@keyframes abiGlitchSplit{
  0%,86%,100%{ text-shadow:-1.4px 0 rgba(0,240,255,.9),1.4px 0 rgba(255,43,214,.95); transform:translateX(0); }
  88%{ text-shadow:-3px 0 rgba(0,240,255,1),3px 0 rgba(255,43,214,1); transform:translateX(-.6px); }
  90%{ text-shadow:2px 0 rgba(0,240,255,1),-2px 0 rgba(255,43,214,1); transform:translateX(.6px); }
  92%{ text-shadow:-1.4px 0 rgba(0,240,255,.9),1.4px 0 rgba(255,43,214,.95); transform:translateX(0); }
}
@media (prefers-reduced-motion:reduce){
  .lang-toggle::after{animation:none}
  .lang-toggle button.active{animation:none}
}
</style>"""

# ---------------------------------------------------------------------------
# 2) Layout/visual bug fix: invalid var(--accent)<hex> color values on .m-tile
# ---------------------------------------------------------------------------
# Re-declare with valid color-mix() so the media-band tile border + hover glow
# actually render. Keyed to the magenta theme accent.
FIX_STYLE = """<style id="abi-fix-custom">
/* ABI 06-neon-grid — fix invalid var(--accent)<hex> media-band tile colors */
.media-band .m-tile{
  border-color:color-mix(in srgb, %(m)s 32%%, transparent);
}
.media-band .m-tile:hover{
  box-shadow:0 22px 50px color-mix(in srgb, %(m)s 38%%, transparent);
}
</style>""" % {"m": MAGENTA}


def upsert_block(html: str, block_id: str, block_html: str) -> str:
    """Replace an existing <style id=block_id>...</style> or insert before </head>."""
    pattern = re.compile(
        r'<style id="%s">.*?</style>' % re.escape(block_id), re.DOTALL
    )
    if pattern.search(html):
        return pattern.sub(lambda _: block_html, html, count=1)
    # insert before the first </head>
    idx = html.lower().find("</head>")
    if idx == -1:
        raise ValueError("no </head> found")
    return html[:idx] + block_html + "\n" + html[idx:]


def main() -> int:
    base = Path(__file__).resolve().parent
    changed = 0
    for name in PAGES:
        p = base / name
        if not p.exists():
            print("SKIP (missing): %s" % name)
            continue
        html = p.read_text(encoding="utf-8")
        new = upsert_block(html, "abi-toggle-custom", TOGGLE_STYLE)
        new = upsert_block(new, "abi-fix-custom", FIX_STYLE)
        if new != html:
            p.write_text(new, encoding="utf-8")
            changed += 1
            print("updated: %s" % name)
        else:
            print("unchanged: %s" % name)
    print("\nDone. %d/%d files written." % (changed, len(PAGES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
