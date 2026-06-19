#!/usr/bin/env python3
"""Convenience: run every per-site build (each site still owns its <slug>/build.py)."""
import subprocess, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SITES = json.loads((ROOT / "_content" / "sites.json").read_text())["sites"]
for s in SITES:
    subprocess.run([sys.executable, str(ROOT / s["slug"] / "build.py")], check=True)
print("All 10 sites built.")
