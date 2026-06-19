#!/usr/bin/env python3
"""One-time bootstrap: emit a standalone per-site build file at <slug>/build.py for each site.

Each generated <slug>/build.py is self-contained for that ONE site:
  * its design TOKENS are baked in (edit them to re-theme just this site)
  * its SITE meta (slug, vercel_name, logo, video, site_index)
  * a SITE_CSS block — the per-site "canvas" for unique polish (seeded with a distinct
    language-toggle treatment so every site differs out of the gate)
It imports the shared engine (_build/abi_engine.py) for the responsive skeleton + content,
then calls abi_engine.build_site(). Run:  python3 <slug>/build.py

After this bootstrap, the <slug>/build.py files are canonical and hand-editable. Re-running
scaffold.py OVERWRITES them, so only re-run to reset a site to defaults.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]

# Per-site seed for the unique EN/ES language toggle (theme-aware via var()). Index-keyed.
TOGGLE_CSS = [
    # 0 neon-blade — neon segmented switch
    ".lang-toggle{border-color:var(--accent);box-shadow:0 0 12px color-mix(in srgb,var(--accent) 45%,transparent)}.lang-toggle button.active{background:var(--accent);color:var(--bg);text-shadow:none}",
    # 1 chrome-culture — metallic slab, sharp
    ".lang-toggle{border-radius:3px;border-width:2px}.lang-toggle button{font-style:italic}.lang-toggle button.active{background:linear-gradient(180deg,#fff,var(--mut));color:#111}",
    # 2 aurora-fade — iridescent gradient pill
    ".lang-toggle{border:0;background:linear-gradient(90deg,var(--accent),var(--accent2),var(--accent3));padding:2px}.lang-toggle button{border-radius:999px}.lang-toggle button.active{background:var(--bg);color:var(--accent)}",
    # 3 midnight-hud — terminal module with brackets
    ".lang-toggle{border-radius:4px;font-family:ui-monospace,Menlo,monospace}.lang-toggle button.active{background:color-mix(in srgb,var(--accent) 22%,transparent);color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}",
    # 4 barber-prime — gold serif underline
    ".lang-toggle{border-radius:0;border-width:0 0 2px 0;border-color:var(--accent)}.lang-toggle button.active{background:transparent;color:var(--accent);box-shadow:inset 0 -3px 0 var(--accent)}",
    # 5 neon-grid — magenta glitch offset
    ".lang-toggle{border-color:var(--accent)}.lang-toggle button.active{background:var(--accent);color:var(--bg);box-shadow:2px 0 0 var(--accent2),-2px 0 0 var(--accent3)}",
    # 6 chrome-liquid — brutalist hard block
    ".lang-toggle{border-radius:0;border-width:2px}.lang-toggle button{font-weight:900}.lang-toggle button.active{background:var(--accent);color:var(--bg)}",
    # 7 holographic — frosted glass
    ".lang-toggle{border-color:color-mix(in srgb,var(--accent) 50%,transparent);background:color-mix(in srgb,var(--accent) 8%,transparent);backdrop-filter:blur(6px)}.lang-toggle button.active{background:color-mix(in srgb,var(--accent) 30%,transparent);color:var(--ink)}",
    # 8 noir-gold — thin elegant letterbox
    ".lang-toggle{height:34px;border-width:1px;letter-spacing:.2em}.lang-toggle button.active{background:var(--accent);color:#111}",
    # 9 vapor-retro — synthwave gradient border
    ".lang-toggle{border:0;background:linear-gradient(90deg,var(--accent),var(--accent2));padding:2px}.lang-toggle button{border-radius:999px}.lang-toggle button.active{background:var(--bg);color:var(--accent2)}",
]

TEMPLATE = '''#!/usr/bin/env python3
"""Standalone build file for {name} ({slug}).

This site has its OWN build file. Run it to regenerate just this site's 11 pages:
    python3 {slug}/build.py

Customize THIS site only by editing:
  * TOKENS   — colors, fonts, radii, decoration, h1 effect, media animation
  * SITE_CSS — per-site unique CSS (your canvas; appended last, overrides the engine)
Content is shared from _content/content.json (the single source of truth) via the engine.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_build"))
import abi_engine

# ---- design tokens for {slug} ----
TOKENS = {tokens}

# ---- site identity ----
SITE = {site}

# ---- per-site unique polish (engine appends this last; safe to expand) ----
SITE_CSS = {site_css!r}

if __name__ == "__main__":
    abi_engine.build_site(TOKENS, SITE, SITE_CSS)
    print("Built {slug}.")
'''


def main():
    for idx, s in enumerate(SITES):
        slug = s["slug"]
        tokens = json.loads((ROOT / "_content" / "tokens" / f"{slug}.json").read_text())
        site = {"slug": slug, "vercel_name": s["vercel_name"], "logo": s["logo"], "video": s["video"], "site_index": idx}
        site_css = "/* unique polish for " + slug + " */ " + TOGGLE_CSS[idx % len(TOGGLE_CSS)]
        out = TEMPLATE.format(
            name=s["name"], slug=slug,
            tokens=json.dumps(tokens, ensure_ascii=False, indent=4),
            site=json.dumps(site, ensure_ascii=False, indent=4),
            site_css=site_css,
        )
        dest = ROOT / slug / "build.py"
        dest.write_text(out, encoding="utf-8")
        print(f"  wrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
