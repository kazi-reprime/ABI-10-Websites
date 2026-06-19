#!/usr/bin/env python3
"""
_polish.py — idempotent polish for 05-barber-prime (Black + Gold serif luxury).

Injects two <style> blocks immediately before </head> in all 11 pages:
  1. <style id="abi-toggle-custom"> — unique EN/ES luxury gold-rule serif toggle.
  2. <style id="abi-fix-custom">    — layout fixes (logo clamp sizing + brand/nav
     collision guard) scoped only to this site.

Safe to run repeatedly: existing blocks are replaced in place, never duplicated.
Only restyles .lang-toggle / .lang-toggle button / .lang-toggle button.active.
Does NOT touch markup or JS.
"""

import re
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

# ── 1. Unique luxury EN/ES toggle ────────────────────────────────────────────
# A thin gold-ruled serif toggle: square edges, hairline gold divider between
# the two options, refined letter-spacing, and an elegant solid-gold fill with
# dark serif lettering for the active language. Distinct from a plain pill.
TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* ABI 05-barber-prime — luxury gold-rule serif language toggle */
.lang-toggle{
  display:inline-flex;align-items:stretch;height:34px;
  border-radius:2px;overflow:hidden;
  border:1px solid var(--accent,#e8b54a);
  background:transparent;
  box-shadow:0 0 0 1px rgba(232,181,74,.12), inset 0 0 14px rgba(232,181,74,.05);
}
.lang-toggle button{
  position:relative;
  background:transparent;border:0;
  color:var(--accent,#e8b54a);
  font-family:'Times New Roman',Georgia,serif;
  font-weight:700;font-size:.74rem;
  letter-spacing:.22em;text-indent:.22em;
  text-transform:uppercase;
  padding:0 16px;min-width:46px;cursor:pointer;
  transition:background .25s ease,color .25s ease,letter-spacing .25s ease;
}
/* hairline gold divider between EN and ES */
.lang-toggle button + button{
  border-left:1px solid rgba(232,181,74,.42);
}
.lang-toggle button:hover{
  background:rgba(232,181,74,.10);
}
.lang-toggle button.active{
  background:var(--accent,#e8b54a);
  color:#0a0807;
  letter-spacing:.26em;text-indent:.26em;
}
.lang-toggle button.active:hover{
  background:var(--accent,#e8b54a);
}
@media (max-width:760px){ .lang-toggle{ height:32px; } }
</style>"""

# ── 2. Layout fixes (scoped, additive) ───────────────────────────────────────
# - Logo image sized via clamp() (was fixed 40px) so it scales fluidly and never
#   crowds the nav at intermediate widths.
# - Brand keeps a guaranteed min footprint and the centered nav gets a little
#   breathing room so the two never visually collide.
FIX_STYLE = """<style id="abi-fix-custom">
/* ABI 05-barber-prime — layout fixes (scoped to this site) */
.brand-logo img{
  width:clamp(34px,4.4vw,44px);
  height:clamp(34px,4.4vw,44px);
}
.header-inner{ gap:clamp(10px,2vw,18px); }
.primary-nav{ padding-inline:8px; }
@media (max-width:480px){
  .brand-logo img{ width:clamp(32px,9vw,38px);height:clamp(32px,9vw,38px); }
}
</style>"""

BLOCK_IDS = {
    "abi-toggle-custom": TOGGLE_STYLE,
    "abi-fix-custom": FIX_STYLE,
}


def upsert_block(html: str, block_id: str, block_html: str) -> str:
    """Replace an existing <style id=...> block or insert before </head>."""
    pattern = re.compile(
        r'<style id="' + re.escape(block_id) + r'">.*?</style>',
        re.DOTALL,
    )
    if pattern.search(html):
        return pattern.sub(lambda _m: block_html, html, count=1)
    # Insert before the first </head>
    idx = html.lower().find("</head>")
    if idx == -1:
        raise ValueError(f"no </head> found")
    return html[:idx] + block_html + "\n" + html[idx:]


def main() -> None:
    for name in PAGES:
        path = SITE_DIR / name
        if not path.exists():
            print(f"SKIP (missing): {name}")
            continue
        html = path.read_text(encoding="utf-8")
        original = html
        for block_id, block_html in BLOCK_IDS.items():
            html = upsert_block(html, block_id, block_html)
        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"updated: {name}")
        else:
            print(f"unchanged: {name}")


if __name__ == "__main__":
    main()
