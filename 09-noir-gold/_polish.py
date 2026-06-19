#!/usr/bin/env python3
"""
09-noir-gold polish: inject idempotent <style> blocks before </head> in all 11 pages.

Two blocks:
  1. #abi-toggle-custom  — unique cinematic noir+gold EN/ES toggle (letterbox/film-frame
     switch with a spotlight active state; NOT a plain pill). Restyles ONLY .lang-toggle,
     .lang-toggle button, .lang-toggle button.active. Markup/JS untouched.
  2. #abi-fix-custom     — layout fix: the desktop primary-nav has 11 links inside a flex
     bar with `overflow:hidden`, so on 1101-1280px widths the last links get silently
     clipped. This tightens spacing and removes the clip so every link stays reachable.

Idempotent: re-running replaces the existing blocks rather than duplicating them.
Run:  cd 09-noir-gold && python3 _polish.py
"""
import re
import pathlib

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* Cinematic Noir + Gold EN/ES toggle — film-frame / letterbox switch, not a pill */
.lang-toggle{
  display:inline-flex;align-items:stretch;height:38px;
  border-radius:2px;border:1px solid var(--accent,#caa15a);
  padding:2px;gap:2px;background:rgba(10,9,8,.72);overflow:hidden;
  box-shadow:0 0 0 1px rgba(0,0,0,.6),0 6px 18px rgba(0,0,0,.4),
             inset 0 0 0 1px rgba(202,161,90,.18);
  position:relative;
}
.lang-toggle::before,.lang-toggle::after{
  /* letterbox bars top & bottom for the cinematic frame feel */
  content:"";position:absolute;left:0;right:0;height:2px;
  background:rgba(0,0,0,.55);pointer-events:none;
}
.lang-toggle::before{top:0}
.lang-toggle::after{bottom:0}
.lang-toggle button{
  background:transparent;border:0;color:var(--accent,#caa15a);
  padding:0 16px;min-width:44px;cursor:pointer;border-radius:1px;
  font-family:'Bodoni Moda',serif;font-weight:700;font-style:italic;
  letter-spacing:.22em;font-size:.74rem;line-height:1;text-transform:uppercase;
  transition:color .25s ease,background .25s ease,text-shadow .25s ease;
}
.lang-toggle button:hover{color:#f3e3a0}
.lang-toggle button.active{
  /* spotlight-lit active frame */
  color:#0a0908;
  background:linear-gradient(180deg,#f3e3a0 0%,var(--accent,#caa15a) 55%,#8a6a18 100%);
  text-shadow:0 1px 0 rgba(243,227,160,.6);
  box-shadow:0 0 14px rgba(202,161,90,.55),inset 0 1px 0 rgba(255,255,255,.45);
}
.lang-toggle button:focus-visible{outline:1px solid #f3e3a0;outline-offset:2px}
</style>"""

FIX_STYLE = """<style id="abi-fix-custom">
/* Layout fix: 11-item desktop nav sat in a flex bar with overflow:hidden, so links
   past the visible width were silently clipped on 1101-1280px screens. Tighten the
   spacing and replace the clip with a safe shrink so all links stay reachable. */
@media (min-width:1101px){
  .primary-nav{overflow:visible;gap:2px;flex-wrap:nowrap}
  .primary-nav a{padding:8px 8px;font-size:.78rem;letter-spacing:.01em}
}
@media (min-width:1101px) and (max-width:1200px){
  .primary-nav a{padding:8px 6px;font-size:.74rem}
  .header-inner{gap:10px}
}
</style>"""

MARKER_RE = {
    "abi-toggle-custom": re.compile(
        r'<style id="abi-toggle-custom">.*?</style>', re.DOTALL),
    "abi-fix-custom": re.compile(
        r'<style id="abi-fix-custom">.*?</style>', re.DOTALL),
}


def upsert(html: str, block_id: str, block: str) -> str:
    """Replace an existing block by id, else insert it just before </head>."""
    pattern = MARKER_RE[block_id]
    if pattern.search(html):
        return pattern.sub(lambda _m: block, html, count=1)
    # insert before the first </head> (case-insensitive)
    idx = html.lower().find("</head>")
    if idx == -1:
        raise ValueError("no </head> found")
    return html[:idx] + block + html[idx:]


def main() -> None:
    here = pathlib.Path(__file__).resolve().parent
    for name in PAGES:
        path = here / name
        if not path.exists():
            print(f"SKIP (missing): {name}")
            continue
        html = path.read_text(encoding="utf-8")
        before = html
        html = upsert(html, "abi-toggle-custom", TOGGLE_STYLE)
        html = upsert(html, "abi-fix-custom", FIX_STYLE)
        if html != before:
            path.write_text(html, encoding="utf-8")
            print(f"updated: {name}")
        else:
            print(f"unchanged: {name}")


if __name__ == "__main__":
    main()
