# American Barber Institute — Ten Website Concepts

Ten complete, self-contained website concepts for the **American Barber Institute (ABI)**, New York's only dedicated barber school. One repository, ten deployable sites, plus a landing page that links to all of them.

Every concept is built from the **real ABI content** (scraped from the live site): programs and pricing, schedules, the 3-step enrollment, why-choose-us, career earnings, real student reviews, FAQ, partners, tuition plans, and both campuses. Each site is **visually and editorially unique** — its own logo treatment, color system, typography, 3D/motion signature, hero copy, and calls to action.

## Live structure

```
/                     → landing page (links to all ten, with desktop + mobile preview)
/01-neon-blade/       → Concept 1  · Cyberpunk · WebGL particle field
/02-chrome-culture/   → Concept 2  · Liquid-metal brutalism
/03-aurora-fade/      → Concept 3  · Light holographic shader
/04-midnight-hud/     → Concept 4  · Tactical sci-fi interface
/05-barber-prime/     → Concept 5  · Black / gold / 3D pole
/06-neon-grid/        → Concept 6  · Particle network · glitch
/07-chrome-liquid/    → Concept 7  · Brutalist · chrome orb
/08-holographic/      → Concept 8  · Iridescent glass · ring
/09-noir-gold/        → Concept 9  · Cinematic luxe · spotlight
/10-vapor-retro/      → Concept 10 · Synthwave · 3D grid sun
/assets/img/          → shared real photography (bundled, not hotlinked)
```

Each `*/index.html` is a single self-contained file (logo embedded as a data URI; photos referenced from `/assets/img/`). No build step, no dependencies — open any `index.html` in a browser.

## Deploy on GitHub Pages

1. Create a new repository on GitHub and push this folder (see commands below).
2. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, branch **`main`**, folder **`/ (root)`**, then **Save**.
3. After a minute your sites are live:
   - Landing: `https://<you>.github.io/<repo>/`
   - Each concept: `https://<you>.github.io/<repo>/06-neon-grid/` (etc.)

The included `.nojekyll` file tells GitHub Pages to serve the folders as-is.

## Push commands

```bash
cd abi-ten
git init
git add .
git commit -m "ABI: ten website concepts"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

## Deploy on Vercel / Netlify (alternative)

Drag the folder into Netlify Drop, or run `vercel` from inside it. It's a static site — no framework config needed. Each concept folder is independently routable.

## Notes for production

- **Images** are bundled in `/assets/img/` (copied from the live site). Replace with final-resolution originals when available.
- **Fonts** load from Google Fonts; self-host for production performance.
- **Lead form** is represented by the call-to-action buttons (tel: links). Wire these to the real enrollment form / CRM.
- Content is accurate as of the latest scrape; confirm tuition and start dates before publishing.

© 2026 American Barber Institute (ABI). Licensed by the NY State Department of Education.
*GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs.
