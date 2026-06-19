# ABI 10 Websites — Design-Fixes Audit

**Date:** 2026-06-19
**Scope:** All 10 sites (`01-neon-blade` … `10-vapor-retro`), all 11 pages each.
**Method:** Central fixes in `_build/build.py` + `_content/`, regenerated, then 10 per-site agents (one per website) audited every page and applied per-site polish.

---

## 1. Issues found and fixed

### 1.1 Duplicate menu bar (and footer) on every home page — FIXED
- **Symptom (user-reported, with screenshots):** two identical nav rows stacked on each site's home page; the footer was likewise doubled.
- **Root cause:** `add_v5_chrome()` was **not idempotent**. `build.py` had been run more than once; each run injected another `<header class="site-header">` / `<footer class="site-footer">` and re-appended `lang-en` to the body class. Result on every `index.html`: **2 headers, 3 footers, `<body class="lang-en lang-en lang-en">`**. Sub-pages were unaffected (they are rendered fresh from a template each build).
- **Fix:** rewrote `add_v5_chrome()` to be idempotent — it now strips **all** prior chrome (sentinel-wrapped regions + any `<header>`/`<footer>`/sticky-bar/bg-video/media-band) before injecting exactly one of each, and normalizes the body class to a single `lang-en`. The 10 home pages were restored from the last clean pre-corruption commit (`4ef6cf9`, v4) and rebuilt once.
- **Verified:** every `index.html` now has exactly **1 header, 1 footer**, no duplicated body class. Re-running the build no longer stacks anything.

### 1.2 Desktop nav clipping at 1101–1280px — FIXED (per-site)
- **Found by agents** on several sites: the inline nav carries 11 links with `overflow:hidden`, but the mobile hamburger only engages at ≤1100px — so on mid-desktop widths the trailing links (Resources/FAQ/Contact) were silently clipped.
- **Fix:** each affected site got an idempotent `<style id="abi-fix-custom">` block (tighter padding / horizontal-scroll / `overflow:visible`) so all 11 links stay reachable.

### 1.3 Invalid CSS in media-style hover/border tints — FIXED (central + in-place)
- **Found by agents (04, 06):** the new media-style CSS used `var(--accent)66` — appending a hex-alpha to a `var()` output is invalid CSS, so browsers silently dropped those declarations (subtle border/glow tints didn't render). 8 of 10 styles were affected.
- **Fix:** converted every `var(--x)HH` to valid `color-mix(in srgb, var(--x) N%, transparent)` — both at the source (`build.py`) and in-place across all 68 affected generated HTML files. **0 invalid occurrences remain.**

### 1.4 Light-theme contrast (03-aurora-fade) — FIXED
- Nav hover/active used a near-white tint invisible on the light header. Replaced with a visible violet tint + accent underline (per-site override).

---

## 2. Content changes

### 2.1 Haircuts page restored
- Re-added a full **Haircuts** page to all 10 sites (scraped from the reference `…/haircuts`): intro, "How It Works" (3 steps), full styles list, a media showcase, "Visit Us" + booking line `(856) 316-1551`, the student-supervision disclaimer, and a "Become a Barber" CTA. Added to nav, footer, and `sitemap.xml`.

### 2.2 "$3 haircut" de-emphasized everywhere
- Per instruction ("the $3 is not important, the page is"), the explicit `$3` price was removed from the testimonial, the FAQ answer, the clinic block, and the scraped home content. The negative-lookahead scrub protects legitimate amounts (`$300`, `$500`, `$5,600`, `$35,000`). **0 `$3` haircut references remain** across all generated HTML.

### 2.3 Tuition pricing verified exact (no change needed)
Re-scraped the live reference site and confirmed our pricing matches exactly:
| Schedule | Total | Plan |
|---|---|---|
| Full-Time Morning (Mon–Fri 8–2) | **$5,600** | $500 down + 17 × $300 |
| Full-Time Afternoon (Mon–Fri 2–8) | **$4,600** | $500 down + 16 × $250 + $100 |
| Weekend (Sat–Sun 9–7) | **$4,600** | $550 down + 27 × $150 |

---

## 3. Media distribution (photos + videos on every page)

- Imported **35 barbershop videos + 39 photos** (web-safe filenames) into `assets/showcase/`, bundled per site.
- A **media showcase band** is rendered on **every page** (11 × 10 = 110 pages), interleaving lazy-loaded videos (play-on-scroll, `preload="none"`) and photos with generic, real captions (never labeled "AI").
- A deterministic rotation gives each site/page a **different** mix so no two pages look identical.

### 3.1 Per-site signature animation (10 distinct treatments)
| # | Site | `media_style` | Reveal signature |
|---|------|---------------|------------------|
| 1 | neon-blade | `neon-scan` | neon-skew + scanline + chromatic hover |
| 2 | chrome-culture | `metal-slab` | metal slab slide-in + shine sweep |
| 3 | aurora-fade | `holo-float` | iridescent border + gentle float |
| 4 | midnight-hud | `hud-reticle` | targeting-reticle frame |
| 5 | barber-prime | `gold-curtain` | gold-curtain wipe + slow zoom |
| 6 | neon-grid | `grid-tilt` | 3D perspective tilt-in |
| 7 | chrome-liquid | `brutal-offset` | brutalist offset-block snap |
| 8 | holographic | `glass-rotate` | 3D rotate-in glass + sheen |
| 9 | noir-gold | `spotlight-cine` | cinematic brightness/Ken-Burns |
| 10 | vapor-retro | `vhs-flip` | VHS scanline + retro flip |

### 3.2 Per-site unique EN/ES toggle
Each of the 10 sites received a **distinct, theme-matched language toggle** (neon segmented switch, chrome slab, iridescent gradient, HUD terminal module, gold serif rule, magenta glitch, brutalist block, frosted glass, noir letterbox, synthwave chrome) — injected on all 11 pages, restyling only `.lang-toggle*` so the toggle still works.

---

## 4. Verification (all 10 sites)

`index.html`: 1 header, 1 footer, single body class · 11 pages each · media band on all 11 · unique toggle on all 11 · **0** invalid `var()` CSS · **0** `$3` haircut refs · pricing exact · haircuts page + nav link present · contact form present.

---

## 5. Gap analysis vs reference site
The reference nav also lists pages we do not currently have as standalone pages: *How to Get Started, Skills & Techniques, Virtual Tour, Class Schedule, Blog*. Their content is largely covered within our existing pages (programs/about/resources). **Haircuts was the key missing page and is now restored.** Adding the others is optional and not yet requested.

---

## 6. Not done (not requested / not possible here)
- **Real-device + headless-browser screenshots:** the `ecc:playwright` MCP bridge extension is not connected in this environment, so pixel-level visual QA could not be captured. Structural QA was exhaustive; recommend a spot-check of the deployed URLs on a phone.
- **Redeploy to Vercel:** pending (see below). Sites are corrected locally but the live `abi-app-N.vercel.app` URLs still serve the old build until redeployed.
- Lighthouse scores, form backend, analytics, custom domains — unchanged from prior scope.

---

## 7. Build/maintenance notes
- `_build/build.py` is now **idempotent** — safe to re-run.
- The per-site agent polish (`<style id="abi-toggle-custom">` / `abi-fix-custom`, written by each site's `_polish.py`) lives **only in the generated HTML**. A full `build.py` rerun regenerates HTML from scratch and would drop those injections; re-run each site's `_polish.py` afterward (idempotent) to reapply.
- New one-shot importer: `_build/import_media.py` (sanitizes + copies the barbershop media into `assets/showcase/`).
