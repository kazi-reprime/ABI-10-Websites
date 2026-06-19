#!/usr/bin/env python3
"""
ABI 10-vapor-retro polish: inject two idempotent <style> blocks before </head>
on all 11 pages.

  1. <style id="abi-toggle-custom">  - unique synthwave EN/ES toggle skin
  2. <style id="abi-fix-custom">      - mobile nav offset layout fix

Idempotent: re-running replaces the existing blocks (matched by id) rather than
appending duplicates. Only restyles .lang-toggle / .lang-toggle button /
.lang-toggle button.active and adds a scoped layout fix. No markup/JS changes.

Edits ONLY files inside 10-vapor-retro/. Does NOT run the central build.
"""
import os
import re

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 1) Unique synthwave / vaporwave EN-ES toggle.
#    Chrome-gradient retro housing, magenta+cyan dual glow, sunset-gradient
#    active state with a moving scanline sheen. Distinct from a plain pill.
# ---------------------------------------------------------------------------
TOGGLE_CSS = """<style id="abi-toggle-custom">
/* === ABI synthwave EN/ES toggle (10-vapor-retro) === */
.lang-toggle{
  position:relative;display:inline-flex;align-items:stretch;height:38px;
  padding:2px;border-radius:11px;overflow:hidden;
  border:1px solid rgba(255,255,255,.55);
  background:
    linear-gradient(180deg,#fff6ff 0%,#d9b8ee 24%,#7a4fa3 52%,#2a0f44 53%,#5a2e84 80%,#c79bff 100%);
  box-shadow:
    0 0 0 1px rgba(41,241,255,.35),
    0 0 14px rgba(255,77,141,.55),
    0 0 22px rgba(41,241,255,.30),
    inset 0 1px 1px rgba(255,255,255,.8),
    inset 0 -2px 4px rgba(0,0,0,.45);
}
.lang-toggle::after{ /* glassy top sheen */
  content:"";position:absolute;left:0;right:0;top:0;height:46%;
  background:linear-gradient(180deg,rgba(255,255,255,.55),transparent);
  pointer-events:none;border-radius:10px 10px 0 0;
}
.lang-toggle button{
  position:relative;z-index:1;background:transparent;border:0;
  display:inline-flex;align-items:center;justify-content:center;
  min-width:46px;padding:0 15px;cursor:pointer;border-radius:9px;
  font-family:inherit;font-weight:900;font-size:.74rem;letter-spacing:.18em;
  color:#2a0f44;text-shadow:0 1px 0 rgba(255,255,255,.65);
  transition:color .22s ease, text-shadow .22s ease, transform .12s ease;
}
.lang-toggle button:hover{ color:#150522; }
.lang-toggle button:active{ transform:translateY(1px); }
.lang-toggle button:focus-visible{
  outline:2px solid #29f1ff;outline-offset:2px;
}
.lang-toggle button.active{
  color:#fff;
  text-shadow:0 0 6px rgba(255,255,255,.85),0 1px 2px rgba(0,0,0,.55);
  background:
    linear-gradient(180deg,#ffe14d 0%,#ff9e5e 42%,#ff4d8d 82%,#b3247f 100%);
  box-shadow:
    0 0 10px rgba(255,77,141,.85),
    0 0 18px rgba(255,158,94,.55),
    inset 0 1px 1px rgba(255,255,255,.85),
    inset 0 -2px 4px rgba(0,0,0,.40);
}
.lang-toggle button.active::before{ /* sunset scanline shimmer */
  content:"";position:absolute;inset:0;border-radius:9px;pointer-events:none;
  background:repeating-linear-gradient(0deg,rgba(0,0,0,.16) 0 2px,transparent 2px 4px);
  mix-blend-mode:overlay;
}
@media (prefers-reduced-motion:no-preference){
  .lang-toggle button.active{ animation:abiTogPulse 2.4s ease-in-out infinite; }
  @keyframes abiTogPulse{
    0%,100%{ box-shadow:0 0 10px rgba(255,77,141,.85),0 0 18px rgba(255,158,94,.55),inset 0 1px 1px rgba(255,255,255,.85),inset 0 -2px 4px rgba(0,0,0,.40); }
    50%{ box-shadow:0 0 16px rgba(255,77,141,1),0 0 26px rgba(41,241,255,.45),inset 0 1px 1px rgba(255,255,255,.9),inset 0 -2px 4px rgba(0,0,0,.40); }
  }
}
</style>"""

# ---------------------------------------------------------------------------
# 2) Layout fix: the mobile slide-down nav was anchored with hardcoded top
#    offsets (inset:134px / 124px / 116px) that assume a single-row top-banner.
#    On narrow screens the magenta .top-banner wraps its two phone CTAs + the
#    language toggle onto 2-3 rows, so the banner is taller than the guessed
#    offset and the opened nav overlaps the header (or floats with a gap).
#    Fix: anchor the nav to the actual bottom of the (sticky) header instead of
#    a magic pixel value. Scoped to <=1100px so desktop layout is untouched.
# ---------------------------------------------------------------------------
FIX_CSS = """<style id="abi-fix-custom">
/* === ABI mobile-nav offset fix (10-vapor-retro) === */
@media (max-width:1100px){
  .site-header{ position:sticky; }              /* ensure positioned ancestor */
  .primary-nav{
    position:absolute;                          /* was: fixed + magic px top */
    top:100%; left:0; right:0; inset:auto 0 auto 0;
    max-height:calc(100vh - 100%);
  }
}
</style>"""


def upsert_block(html, block, block_id):
    """Replace an existing <style id=...>...</style> with block, else insert
    before </head>. Returns (new_html, action)."""
    pattern = re.compile(
        r'[ \t]*<style id="%s">.*?</style>\n?' % re.escape(block_id),
        re.DOTALL,
    )
    if pattern.search(html):
        return pattern.sub(block + "\n", html, count=1), "replaced"
    # insert before first </head>
    idx = html.lower().find("</head>")
    if idx == -1:
        return html, "no-head"
    return html[:idx] + block + "\n" + html[idx:], "inserted"


def main():
    for name in PAGES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            print("SKIP (missing): %s" % name)
            continue
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        orig = html
        html, a1 = upsert_block(html, TOGGLE_CSS, "abi-toggle-custom")
        html, a2 = upsert_block(html, FIX_CSS, "abi-fix-custom")
        if html != orig:
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            print("OK   %-18s toggle=%s fix=%s" % (name, a1, a2))
        else:
            print("NOOP %-18s toggle=%s fix=%s" % (name, a1, a2))


if __name__ == "__main__":
    main()
