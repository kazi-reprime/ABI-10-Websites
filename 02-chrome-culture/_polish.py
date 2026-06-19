#!/usr/bin/env python3
"""
Polish injector for 02-chrome-culture (Liquid Metal . Brutalism, red/chrome).

Idempotently injects two <style> blocks before </head> in all 11 pages:
  1. id="abi-toggle-custom"  -> unique chrome-slab EN/ES toggle (heavy beveled
     metal switch, hard brutalist edges, red active accent). Restyles ONLY
     .lang-toggle / .lang-toggle button / .lang-toggle button.active.
  2. id="abi-fix-custom"     -> layout bug fix for the desktop primary-nav
     clipping band (1100px-1280px) where 11 nav items overflow:hidden and clip
     their text before the hamburger engages at <=1100px.

Safe to run repeatedly: each block is replaced (not duplicated) on every run.
Does NOT touch markup or JS. Edits ONLY files inside this folder.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

# --- Block 1: unique chrome-slab toggle -------------------------------------
# Brushed-metal body, hard 90-degree corners (brutalism), thick black border,
# divider seam between buttons, beveled inset metallic ACTIVE state with a red
# underline strike. Distinct from any rounded "pill".
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* ABI 02-chrome-culture - liquid-metal / brutalist chrome-slab language switch */
.lang-toggle{
  display:inline-flex;align-items:stretch;height:38px;
  border-radius:0 !important;            /* hard edges - brutalism */
  border:3px solid #07080a !important;
  overflow:hidden;
  background:
    linear-gradient(180deg,#e8e9ee 0%,#b9bcc4 18%,#80838c 50%,#aeb1b9 82%,#d6d8de 100%);
  box-shadow:
    0 0 0 1px rgba(255,255,255,.35) inset,
    0 6px 0 #050507,                       /* hard offset drop - brutalist slab */
    0 10px 22px rgba(0,0,0,.55);
  padding:0;
}
.lang-toggle button{
  position:relative;
  background:transparent;border:0;
  padding:0 16px;min-width:46px;cursor:pointer;
  color:#23252b;                           /* dark engraved label on chrome */
  font-weight:900;letter-spacing:.18em;
  font-family:'Arial Black','Helvetica Neue',inherit;
  font-size:.76rem;text-transform:uppercase;
  text-shadow:0 1px 0 rgba(255,255,255,.6);
  transition:color .15s ease, transform .05s ease;
}
.lang-toggle button + button{ border-left:3px solid #07080a; }  /* seam */
.lang-toggle button:hover{ color:#000; }
.lang-toggle button:active{ transform:translateY(1px); }
.lang-toggle button.active{
  /* pressed, beveled, energized metal cell with red brutalist strike */
  color:#fff;
  background:
    linear-gradient(180deg,#2a2c31 0%,#16171b 48%,#202227 100%);
  text-shadow:0 1px 2px rgba(0,0,0,.8);
  box-shadow:
    0 2px 0 rgba(255,255,255,.18) inset,
    0 -3px 0 #ff2e2e inset,                /* red accent strike - brutalism */
    0 3px 7px rgba(0,0,0,.6) inset;
}
@media (max-width:760px){ .lang-toggle{ height:36px; box-shadow:0 0 0 1px rgba(255,255,255,.35) inset,0 4px 0 #050507,0 8px 16px rgba(0,0,0,.5); } }
</style>"""

# --- Block 2: layout fix ----------------------------------------------------
# In 1100-1280px the desktop nav (11 items, flex-wrap:nowrap, overflow:hidden)
# clips link text. Tighten spacing/letterspacing in that band so all 11 items
# fit without being cut off. Pure additive CSS, no markup/JS change.
FIX_STYLE = """<style id="abi-fix-custom">
/* ABI 02-chrome-culture - prevent desktop nav text clipping in 1100-1280px band */
@media (min-width:1101px) and (max-width:1280px){
  .header-inner{ gap:10px; }
  .primary-nav{ gap:1px; }
  .primary-nav a{
    padding:8px 7px;
    font-size:.76rem;
    letter-spacing:0;
  }
}
@media (min-width:1101px) and (max-width:1180px){
  .primary-nav a{ padding:8px 5px; font-size:.73rem; }
}
</style>"""

INSERT = "\n" + TOGGLE_STYLE + "\n" + FIX_STYLE + "\n"

# Regexes to strip any previously-injected blocks (idempotency).
RE_TOGGLE = re.compile(
    r'\n?<style id="abi-toggle-custom">.*?</style>', re.DOTALL)
RE_FIX = re.compile(
    r'\n?<style id="abi-fix-custom">.*?</style>', re.DOTALL)


def polish(path):
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()
    original = html

    # Remove existing injected blocks so re-runs replace rather than duplicate.
    html = RE_TOGGLE.sub("", html)
    html = RE_FIX.sub("", html)

    if "</head>" not in html:
        return ("SKIP-no-head", path)

    # Inject once, immediately before the first </head>.
    html = html.replace("</head>", INSERT + "</head>", 1)

    if html == original:
        return ("UNCHANGED", path)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return ("OK", path)


def main():
    for name in PAGES:
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            print(f"MISSING  {name}")
            continue
        status, _ = polish(p)
        print(f"{status:9} {name}")


if __name__ == "__main__":
    main()
