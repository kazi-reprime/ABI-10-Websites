#!/usr/bin/env python3
"""
Polish script for 04-midnight-hud (Tactical Sci-Fi Interface / amber-cyan HUD).

Injects, idempotently, before </head> on all 11 pages:
  1) <style id="abi-toggle-custom"> — a unique tactical-HUD EN/ES toggle:
     bracketed/cornered terminal switch, monospace label, scan-line active state.
     Only restyles .lang-toggle / .lang-toggle button / .lang-toggle button.active.
  2) <style id="abi-fix-custom"> — layout/theme fix:
     repairs the invalid CSS `border:1px solid var(--accent)66` used by the
     signature .ms-hud-reticle .m-tile::before bracket frame. Browsers drop the
     whole invalid declaration, so the HUD reticle border never renders. We
     restate the rule with a valid rgba() amber so the signature frame shows.

Run from anywhere:  python3 04-midnight-hud/_polish.py
Idempotent: re-running replaces the existing blocks rather than duplicating.
Edits ONLY files inside 04-midnight-hud/.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

# --- 1) Unique tactical-HUD EN/ES toggle -----------------------------------
# Lives in an amber top-banner (#ffb238 bg, #040810 ink). Reads as a cornered
# terminal module: monospace, square HUD corner brackets, a hairline divider,
# and a cyan scan-line wash on the active segment.
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* === Tactical HUD language switch (04-midnight-hud) === */
.lang-toggle{
  position:relative;display:inline-flex;align-items:stretch;height:34px;
  padding:0;border:1.5px solid #040810;border-radius:2px;overflow:visible;
  background:rgba(4,8,16,.06);
  font-family:ui-monospace,'SF Mono',Menlo,'Courier New',monospace;
  box-shadow:inset 0 0 0 1px rgba(4,8,16,.18);
}
/* HUD corner brackets */
.lang-toggle::before,.lang-toggle::after{
  content:"";position:absolute;width:8px;height:8px;pointer-events:none;
  border:1.5px solid #040810;
}
.lang-toggle::before{top:-3px;left:-3px;border-right:0;border-bottom:0;}
.lang-toggle::after{bottom:-3px;right:-3px;border-left:0;border-top:0;}
.lang-toggle button{
  position:relative;background:transparent;border:0;color:#040810;
  padding:0 14px;min-width:46px;cursor:pointer;
  font-family:inherit;font-weight:800;font-size:.72rem;letter-spacing:.22em;
  text-transform:uppercase;line-height:1;overflow:hidden;
  transition:color .18s ease,background .18s ease;
}
/* hairline divider between segments */
.lang-toggle button+button{box-shadow:inset 1.5px 0 0 rgba(4,8,16,.35);}
.lang-toggle button::before{
  content:"";position:absolute;left:5px;top:50%;width:3px;height:3px;
  transform:translateY(-50%);background:rgba(4,8,16,.45);
  clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%);opacity:0;transition:opacity .18s;
}
.lang-toggle button:hover{background:rgba(4,8,16,.1);}
.lang-toggle button:hover::before{opacity:1;}
/* active = inverted terminal cell with cyan scan-lines */
.lang-toggle button.active{
  color:#dffaff;background:#040810;
  background-image:repeating-linear-gradient(
    0deg,rgba(70,230,255,.55) 0,rgba(70,230,255,.55) 1px,
    transparent 1px,transparent 4px);
  text-shadow:0 0 6px rgba(70,230,255,.85);
}
.lang-toggle button.active::before{
  opacity:1;background:#46e6ff;
  box-shadow:0 0 5px rgba(70,230,255,.9);
}
.lang-toggle button.active::after{
  content:"";position:absolute;left:0;right:0;bottom:0;height:1.5px;
  background:#46e6ff;box-shadow:0 0 6px rgba(70,230,255,.9);
}
@media (prefers-reduced-motion:reduce){
  .lang-toggle button{transition:none;}
}
</style>"""

# --- 2) Layout / theme fix --------------------------------------------------
# Repairs the broken signature reticle frame border. `var(--accent)66` is not a
# valid color token, so the entire `border` declaration is dropped by the
# parser and the HUD bracket frame on every media tile renders borderless.
# Restate with the intended ~40% amber. !important + same specificity ensures
# this (placed last in <head>... but inline page styles are also in <head>);
# we raise specificity via .ms-hud-reticle .m-tile::before to win the cascade.
FIX_STYLE = """<style id="abi-fix-custom">
/* === Fix: invalid `var(--accent)66` broke the HUD reticle bracket frame === */
.ms-hud-reticle .m-tile::before{
  border:1px solid rgba(255,178,56,.4) !important;
}
/* Safety: keep desktop nav from clipping if items run long (>1100px) */
@media (min-width:1101px){
  .primary-nav{overflow:visible;flex-wrap:wrap;}
}
</style>"""

START = "<!-- abi-polish:start -->"
END = "<!-- abi-polish:end -->"
BLOCK = f"{START}\n{TOGGLE_STYLE}\n{FIX_STYLE}\n{END}"

# Match a previously-injected block (idempotent re-run) OR loose individual styles.
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
LOOSE_TOGGLE_RE = re.compile(r'<style id="abi-toggle-custom">.*?</style>', re.S)
LOOSE_FIX_RE = re.compile(r'<style id="abi-fix-custom">.*?</style>', re.S)


def polish(path):
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()
    original = html

    # Remove any prior injected block / loose styles for clean idempotent re-run.
    html = BLOCK_RE.sub("", html)
    html = LOOSE_TOGGLE_RE.sub("", html)
    html = LOOSE_FIX_RE.sub("", html)

    if "</head>" not in html:
        return path, "SKIP (no </head>)"

    html = html.replace("</head>", BLOCK + "\n</head>", 1)

    if html == original:
        return path, "unchanged"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path, "polished"


def main():
    results = []
    for name in PAGES:
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            results.append((name, "MISSING"))
            continue
        _, status = polish(p)
        results.append((name, status))
    width = max(len(n) for n, _ in results)
    for name, status in results:
        print(f"  {name:<{width}}  {status}")


if __name__ == "__main__":
    main()
