#!/usr/bin/env python3
"""Automated, repeatable audit across every generated page of all 10 sites.

Checks structure, mobile-responsive signals, CSS validity, internal-link integrity,
content fidelity vs the authoritative source, bilingual coverage, and accessibility.
Exit code 0 = all green; 1 = failures (printed per page). Run as many times as you like:
    python3 _build/audit.py
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITES = [s["slug"] for s in json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]]
EXPECT_PAGES = {"index", "about", "programs", "resources", "faq", "job-placement",
                "haircuts", "gallery", "blog", "partners", "instructors", "contact"}
VALID_PATHS = {"/", "/about", "/programs", "/resources", "/faq", "/job-placement",
               "/haircuts", "/gallery", "/blog", "/partners", "/instructors", "/contact"}
LEGACY = ["class=\"wrap\"", "neon-sign", "class=\"ticker\"", "class=\"next-start\"", "btn-pri\"", "btn-gho\""]

fails = []   # (site, page, message)
def fail(site, page, msg): fails.append((site, page, msg))


def audit_page(site, path):
    page = path.stem
    html = path.read_text(encoding="utf-8", errors="replace")
    # structure
    if html.count("<header") != 1: fail(site, page, f"header count = {html.count('<header')}")
    if html.count("<footer") != 1: fail(site, page, f"footer count = {html.count('<footer')}")
    if "width=device-width" not in html: fail(site, page, "viewport meta missing width=device-width")
    if not re.search(r'<html lang="[a-z]{2}"', html): fail(site, page, "html lang attr missing")
    # CSS validity (invalid hex-alpha on var())
    bad = re.findall(r'var\(--[a-z0-9]+\)[0-9a-fA-F]{2}\b', html)
    if bad: fail(site, page, f"invalid var()HH CSS x{len(bad)}: {bad[0]}")
    # responsive signals
    if "overflow-x:hidden" not in html: fail(site, page, "body overflow-x:hidden missing")
    if "class=\"burger\"" not in html: fail(site, page, "hamburger missing")
    if "top:100%" not in html: fail(site, page, "mobile drawer anchor (top:100%) missing")
    if "@media (max-width:1280px)" not in html: fail(site, page, "responsive nav breakpoint missing")
    if "100dvh" not in html: fail(site, page, "100dvh (mobile viewport) missing")
    # legacy scraped markup must be gone
    for lg in LEGACY:
        if lg in html: fail(site, page, f"legacy scraped markup present: {lg}")
    # bilingual
    if "lang-en" not in html or "lang-es" not in html: fail(site, page, "bilingual spans missing")
    if "lang-toggle" not in html: fail(site, page, "EN/ES toggle missing")
    # media band on every page
    if "media-band" not in html: fail(site, page, "media band missing")
    # phones present + well-formed tel:
    if "tel:2122902289" not in html or "tel:2122900278" not in html: fail(site, page, "dual call numbers missing")
    # accessibility: every <img> has alt
    imgs_no_alt = [m for m in re.findall(r'<img\b[^>]*>', html) if "alt=" not in m]
    if imgs_no_alt: fail(site, page, f"{len(imgs_no_alt)} <img> without alt")
    # internal link integrity
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("tel:", "mailto:", "#", "https://", "http://", "//")):
            if "abi-app-" in href: fail(site, page, f"cross-site/self abi-app link: {href}")
            continue
        if href.startswith(("/assets/", "/blog/")) or href.endswith((".xml", ".txt")):
            continue
        if href not in VALID_PATHS:
            fail(site, page, f"unknown internal link: {href}")


def audit_site(site):
    d = ROOT / site
    have = {p.stem for p in d.glob("*.html")}
    missing = EXPECT_PAGES - have
    if missing: fail(site, "-", f"missing pages: {sorted(missing)}")
    for path in sorted(d.glob("*.html")) + sorted((d / "blog").glob("*.html")):
        audit_page(site, path)
    # content fidelity
    prog = (d / "programs.html").read_text(errors="replace") if (d / "programs.html").exists() else ""
    for price in ("$5,600", "$1,500", "$100"):
        if price not in prog: fail(site, "programs", f"price {price} missing")
    idx = (d / "index.html").read_text(errors="replace") if (d / "index.html").exists() else ""
    if "150 per Week" not in idx: fail(site, "index", "$150/week banner missing")
    blog = (d / "blog.html").read_text(errors="replace") if (d / "blog.html").exists() else ""
    if "Insights from the Chair" not in blog: fail(site, "blog", "blog headline missing")
    # forbidden stale content across all pages
    for path in sorted(d.glob("*.html")) + sorted((d / "blog").glob("*.html")):
        t = path.read_text(errors="replace")
        if "540-Hour" in t or "540 Hour" in t: fail(site, path.stem, "stale 540-Hour program")
        if "Call for pricing" in t: fail(site, path.stem, "stale 'Call for pricing'")
        if "abi-assets.vercel.app" in t: fail(site, path.stem, "stale asset host abi-assets")
        if "© 2026 American Barber Institute (ABI)" not in t: fail(site, path.stem, "footer copyright missing")


def main():
    for s in SITES:
        audit_site(s)
    total_pages = sum(len(list((ROOT / s).glob("*.html"))) + len(list((ROOT / s / "blog").glob("*.html"))) for s in SITES)
    print(f"Audited {len(SITES)} sites, {total_pages} pages.")
    if not fails:
        print("RESULT: ALL CHECKS PASS")
        return 0
    print(f"RESULT: {len(fails)} FAILURE(S):")
    for site, page, msg in fails:
        print(f"  [{site} / {page}] {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
