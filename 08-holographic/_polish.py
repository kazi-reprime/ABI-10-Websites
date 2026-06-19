#!/usr/bin/env python3
"""
Polish pass for the 08-holographic ABI site (Iridescent Glass theme).

Idempotently injects two <style> blocks before </head> on all 11 pages:

  1. id="abi-toggle-custom" — a UNIQUE frosted-glass holographic capsule
     restyle of the EN/ES language toggle (.lang-toggle). Distinct from a
     plain pill: layered conic + linear holographic sheen, frosted glass,
     and a glowing iridescent ring on the active button. Markup/JS untouched.

  2. id="abi-fix-custom" — layout fix for the desktop nav (1101-1280px band)
     where 11 nav links + brand + two phone CTAs + toggle overflow the
     centered .primary-nav (flex:1; overflow:hidden) and the trailing links
     (FAQ / Contact) get silently clipped. We tighten nav spacing and swap
     the hard clip for graceful horizontal scroll so no link disappears.

Re-running is safe: each block is replaced if already present (matched by id),
otherwise inserted immediately before </head>. Edits ONLY 08-holographic/.
"""

import re
import sys
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent

PAGES = [
    "index.html", "about.html", "programs.html", "instructors.html",
    "gallery.html", "partners.html", "haircuts.html", "job-placement.html",
    "resources.html", "faq.html", "contact.html",
]

# --- Theme tokens (from this site's inline CSS) -----------------------------
# --bg:#0c0b1a  --accent:#a78bfa (purple)  --accent2:#22d3ee (cyan)
# brief primary accent: #7ce8ff (ring/glow cyan)

TOGGLE_STYLE = """<style id="abi-toggle-custom">
/* ===== Iridescent Glass language toggle — frosted holographic capsule ===== */
.lang-toggle{
  position:relative;
  display:inline-flex;
  align-items:stretch;
  height:38px;
  padding:3px;
  gap:2px;
  border-radius:999px;
  overflow:hidden;
  isolation:isolate;
  border:1px solid rgba(124,232,255,.40);
  background:
    linear-gradient(135deg, rgba(255,255,255,.10), rgba(255,255,255,.02)),
    rgba(12,11,26,.55);
  backdrop-filter:blur(12px) saturate(1.4);
  -webkit-backdrop-filter:blur(12px) saturate(1.4);
  box-shadow:
    0 6px 22px rgba(8,6,24,.45),
    inset 0 1px 0 rgba(255,255,255,.22);
}
/* holographic sheen — slow drifting aurora behind the buttons */
.lang-toggle::before{
  content:"";
  position:absolute; inset:-40%;
  z-index:0; pointer-events:none;
  background:
    conic-gradient(from 0deg,
      rgba(124,232,255,.35), rgba(167,139,250,.30),
      rgba(34,211,238,.28),  rgba(124,232,255,.35));
  filter:blur(10px);
  opacity:.55;
  animation:abiHoloSpin 9s linear infinite;
}
/* thin top-edge light streak */
.lang-toggle::after{
  content:"";
  position:absolute; left:6%; right:6%; top:0; height:42%;
  z-index:1; pointer-events:none;
  border-radius:999px;
  background:linear-gradient(180deg, rgba(255,255,255,.30), transparent);
  opacity:.6;
}
@keyframes abiHoloSpin{ to{ transform:rotate(1turn); } }

.lang-toggle button{
  position:relative;
  z-index:2;
  background:transparent;
  border:0;
  color:rgba(255,255,255,.82);
  padding:0 16px;
  min-width:46px;
  cursor:pointer;
  font-family:inherit;
  font-weight:900;
  font-size:.74rem;
  letter-spacing:.16em;
  border-radius:999px;
  transition:color .25s ease, transform .15s ease, text-shadow .25s ease;
}
.lang-toggle button:hover{ color:#fff; transform:translateY(-1px); }
.lang-toggle button:focus-visible{
  outline:2px solid #7ce8ff;
  outline-offset:2px;
}

/* active = glowing iridescent ring + frosted fill */
.lang-toggle button.active{
  color:#06121a;
  text-shadow:0 1px 0 rgba(255,255,255,.35);
  background:
    linear-gradient(135deg, #7ce8ff 0%, #a78bfa 55%, #22d3ee 100%);
  box-shadow:
    0 0 0 1.5px rgba(124,232,255,.85),
    0 0 14px rgba(124,232,255,.55),
    0 0 26px rgba(167,139,250,.40),
    inset 0 1px 0 rgba(255,255,255,.55);
}
@media (prefers-reduced-motion: reduce){
  .lang-toggle::before{ animation:none; }
}
</style>"""

FIX_STYLE = """<style id="abi-fix-custom">
/* ===== Layout fix: desktop nav clipping (1101-1280px) =====
   Above the 1100px hamburger breakpoint the inline .primary-nav holds all
   11 links inside flex:1 + overflow:hidden, alongside the brand and two
   phone CTAs + toggle. On narrower desktops the row overflows and the last
   links (FAQ / Contact) are silently clipped. Tighten spacing and allow
   graceful horizontal scroll so every link stays reachable. */
@media (min-width:1101px) and (max-width:1280px){
  .primary-nav{
    overflow-x:auto;
    overflow-y:hidden;
    scrollbar-width:none;
    -ms-overflow-style:none;
    justify-content:flex-start;
    -webkit-mask-image:linear-gradient(90deg,#000 92%,transparent);
    mask-image:linear-gradient(90deg,#000 92%,transparent);
  }
  .primary-nav::-webkit-scrollbar{ display:none; }
  .primary-nav a{
    padding:8px 7px;
    font-size:.78rem;
    letter-spacing:0;
  }
}
</style>"""

START_RE = lambda sid: re.compile(
    r'<style id="' + re.escape(sid) + r'">.*?</style>\s*', re.DOTALL
)


def upsert_block(html: str, style_id: str, block: str) -> str:
    """Replace an existing <style id=...> block, or insert before </head>."""
    pattern = START_RE(style_id)
    if pattern.search(html):
        return pattern.sub(block + "\n", html, count=1)
    # insert before the first </head>
    idx = html.lower().find("</head>")
    if idx == -1:
        raise ValueError("no </head> found")
    return html[:idx] + block + "\n" + html[idx:]


def process(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    before = html
    html = upsert_block(html, "abi-toggle-custom", TOGGLE_STYLE)
    html = upsert_block(html, "abi-fix-custom", FIX_STYLE)
    if html != before:
        path.write_text(html, encoding="utf-8")
        return "updated"
    return "unchanged"


def main() -> int:
    rc = 0
    for name in PAGES:
        p = SITE_DIR / name
        if not p.exists():
            print(f"MISSING {name}")
            rc = 1
            continue
        status = process(p)
        # verify exactly one of each block now present
        h = p.read_text(encoding="utf-8")
        t = h.count('id="abi-toggle-custom"')
        f = h.count('id="abi-fix-custom"')
        flag = "" if (t == 1 and f == 1) else "  <-- CHECK"
        print(f"{name:20} {status:9} toggle={t} fix={f}{flag}")
        if t != 1 or f != 1:
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
