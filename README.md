# American Barber Institute — Ten Websites

**10 unique website concepts for ABI (American Barber Institute), New York's only dedicated barber school.** One brand, ten production-ready deployments, mobile-first, SEO-optimized.

## Live URLs

| # | Concept | Theme | URL |
|---|---------|-------|-----|
| 01 | Neon Blade | Cyberpunk · WebGL particle field | https://abi-app-1.vercel.app |
| 02 | Chrome Culture | Liquid-metal brutalism | https://abi-app-2.vercel.app |
| 03 | Aurora Fade | Light holographic shader | https://abi-app-3.vercel.app |
| 04 | Midnight HUD | Tactical sci-fi interface | https://abi-app-4.vercel.app |
| 05 | Barber Prime | Black / gold / 3D barber pole | https://abi-app-5.vercel.app |
| 06 | Neon Grid | Particle network · glitch | https://abi-app-6.vercel.app |
| 07 | Chrome Liquid | Brutalist · chrome orb | https://abi-app-7.vercel.app |
| 08 | Holographic | Iridescent glass · ring | https://abi-app-8.vercel.app |
| 09 | Noir Gold | Cinematic luxe · spotlight | https://abi-app-9.vercel.app |
| 10 | Vapor Retro | Synthwave · 3D grid sun | https://abi-app-10.vercel.app |

**Master hub:** https://abi-ten.vercel.app  
**Asset CDN:** https://abi-assets.vercel.app

## Architecture

- **11 Vercel projects:** 10 site projects + 1 asset CDN.
- **One shared CDN** (`abi-assets.vercel.app`) hosts all logos, gallery photography, and background videos. The 10 site deployments reference assets via absolute URLs — each site deploy is ~300KB–1MB (HTML only).
- **Pattern:** `abi-app-N.vercel.app` — change N from 1 to 10 for the ten sites.

## What's in each site

- **Home (`/`)** — full hero, programs, careers, reviews, tuition, FAQ, locations.
- **Programs (`/programs`)** — every program + 3 schedules + tuition plans.
- **Gallery (`/gallery`)** — 30+ photos from the clinic floor.
- **FAQ (`/faq`)** — 15 questions with full answers + FAQPage JSON-LD.
- **Contact (`/contact`)** — both campuses + admissions form.

## Mobile + SEO

- Mobile-first responsive (360px → 1440px+), iOS / Android / tablet / desktop.
- Hamburger nav with 44px touch targets.
- `<meta>` description, OpenGraph, Twitter cards, canonical.
- JSON-LD: EducationalOrganization + FAQPage.
- `sitemap.xml` and `robots.txt` per site.
- Vercel `cleanUrls` (`.html` extension stripped).

## Repo layout

```
/                       — landing index.html (preview hub)
/01-neon-blade …/10-…/  — 10 site folders (each: index + 4 subpages + sitemap + robots + vercel.json)
/assets/                — source-of-truth for img + logos + videos (mirrored on abi-assets.vercel.app)
/landing/               — master hub (abi-ten.vercel.app)
/_content/              — content.json (single source of truth) + sites.json
/_build/                — Python builder (build.py) + PPT generator (make_pptx.py)
/_deploy/               — deploy manifest + PPT deck + audit script
```

## Rebuild

```bash
python3 _build/build.py        # rebuilds 10 sites from _content/*.json
python3 _build/make_pptx.py    # rebuilds ABI-Ten-Websites.pptx
```

## Deploy

Each site folder is a Vercel project. Re-deploying a site:

```bash
cd 03-aurora-fade
vercel deploy --prod --yes --scope mkknights-projects
```

© 2026 American Barber Institute (ABI). Licensed by NY State Dept. of Education. GI Bill® accepted.
