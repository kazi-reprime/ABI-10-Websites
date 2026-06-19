# ABI 10 Websites — Design-Fixes Audit

**Date:** 2026-06-19
**Scope:** All 10 sites (`01-neon-blade` … `10-vapor-retro`), all 11 pages each.
**Method:** Central fixes in `_build/build.py` + `_content/`, regenerated, then 10 per-site agents (one per website) audited every page and applied per-site polish.

---

## 0. v7 — Per-site rebuild, content reconciliation & mobile fixes (latest)

**Scope:** All 10 sites rebuilt on a new architecture; content reconciled to the authoritative reference; mobile responsiveness fixed at the root; 10 parallel agents (one per site) verified + polished.

### 0.1 Architecture — every site now has its own Python build file
- Split the single monolithic `build.py` into: a shared engine `_build/abi_engine.py` + **one `<slug>/build.py` per site** (inline `TOKENS` + `SITE` + `SITE_CSS`). Each site is independently buildable (`python3 <slug>/build.py`) and independently customizable. Old monolith archived at `_archive/build-v5.py`.

### 0.2 Root-cause fix for "still not mobile responsive"
- **Root cause:** the home `index.html` was scraped third-party HTML (classes `.wrap/.hero/.neon-sign/.ticker`, `.btn-pri`) surgically patched — it never used the responsive system the sub-pages used. **Fix:** home is now generated from the same mobile-first template as every page. Legacy scraped classes: **0** across all 10 homes.
- **Engine bug (found by parallel agents 01 & 10, fixed centrally):** `.site-header`'s `backdrop-filter` makes it the containing block for the `position:fixed` nav drawer, so the JS-measured `--nav-top` mis-anchored the drawer ~135px below the header. Fixed by anchoring the drawer to `top:100%` (the header's own bottom edge) — robust to the top-banner wrapping.
- **Engine bug (agent 10):** `body{animation:pageIn … both}` left a residual `translateY(0)` transform, making `body` the containing block for the fixed sticky call bar → bar pushed off-screen. Fixed: page-in is now opacity-only.
- **Heading overflow (agent 09):** wrap rule was on `<p>` only → added `overflow-wrap:break-word` to `h1–h4`.
- **brutal-offset media overflow ~4px at 360px (agent 07):** added a ≤600px clamp in the engine.
- Mobile system: hamburger ≤1180px (no 11-item clip), drawer scroll-locks the body, tap targets, `clamp()` typography, `overflow-x:hidden`, `100dvh`, `env(safe-area-inset-*)`.

### 0.3 Content reconciled to the authoritative source ("content is king")
- **Programs 5→4** to match the reference exactly: 500-Hr Master Barber (Manhattan) $5,600 · 500-Hr Master Barber — Bronx $5,600 (was wrongly "540-Hr") · 50-Hr Refresher $1,500 · **3-Hr Contagious Diseases $100** (was "Call for pricing"; dropped the duplicate Bronx-contagious entry).
- **"Why Choose ABI" 12→6** exact source cards (NY State Licensed; Hands-On from the First Few Weeks; Flexible Schedules; Job Placement Office; Financial Assistance Available; Monthly Start Dates).
- **Job Placement** rebuilt to source: stats 90%+/500+/30yrs/Free, the 6 source offerings, Jerrick M. quote, Browse-jobs + Own-a-shop cards.
- **Banner** = "Start Your Barber Journey Today for Only $150 per Week*". **Footer** rebuilt to source (Links/Locations/Contact incl. Bronx (718) 676-0640 + admission@abi.edu/hours, "© 2026 American Barber Institute (ABI)…", GI Bill® trademark note).
- **Removed invented extras** not in source (e.g. the fabricated career-earnings table). **Kept Partners + Instructors** per instruction. Resources aligned to source (ACCES-VR, GI Bill® & VA, NY State Board, Tools & Supplies).
- **Light-theme footer contrast (agent 03):** engine footer bg was hardcoded `rgba(0,0,0,.4)` (muddy on light themes) → now `color-mix(var(--bg) 86%,#000)`.

### 0.4 Per-site agent verification
10 parallel agents each built their site, verified responsiveness (live browser where the shared preview was available, rigorous static audit otherwise), graded WCAG AA contrast (site 03 light theme needed the most fixes — accent darkened to pass AA; site 02 banner red darkened to 4.94:1), and added theme-matched polish in their own `SITE_CSS`. Fleet re-verify after the central engine fixes: **11 pages each · 1 header/1 footer · 0 invalid `var()` CSS · drawer + opacity-page-in + theme footer present on all 10.**

---

## 1. Issues found and fixed (v5/v6 — earlier)

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
