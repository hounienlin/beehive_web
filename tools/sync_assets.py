#!/usr/bin/env python3
"""Re-copy and downscale screenshots, mascot art and the app icon from the app repo.

Usage:
    python3 tools/sync_assets.py /path/to/beehive            # app repo root
    python3 tools/sync_assets.py /path/to/beehive --icon icon-A2.png

What it does (all outputs go into ./assets/img/ of this site repo):
  screenshots/<locale>/NN-name.webp   600 px wide, from docs/appstore/final/<locale>/iphone-6.9/*.png
  mascot/<name>.webp                  360 px, from ios/BeeHive/Resources/Assets.xcassets/Mascot/*/*@3x.png
  icon/favicon-32.png, favicon-192.png, apple-touch-icon.png (180), og-icon.png (512)
                                      from docs/appstore/icon/<icon file> (default icon-C2.png)

Needs Pillow (python3 -m pip install Pillow). Only reads from the app repo; never writes there.
After running, check `git status` and update alt text in the HTML if the screenshot set changed.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: python3 -m pip install Pillow")

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img"
LOCALES = ("zh-Hant", "en-US")
SHOT_WIDTH = 600
MASCOT_SIZE = 360


def downscale_width(src: Path, dst: Path, width: int) -> None:
    im = Image.open(src)
    if im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=82, method=6)


def sync_screenshots(app: Path) -> int:
    n = 0
    for loc in LOCALES:
        src_dir = app / "docs" / "appstore" / "final" / loc / "iphone-6.9"
        dst_dir = OUT / "screenshots" / loc
        if not src_dir.is_dir():
            print(f"  ! missing {src_dir}")
            continue
        if dst_dir.exists():
            shutil.rmtree(dst_dir)
        for src in sorted(src_dir.glob("*.png")):
            downscale_width(src, dst_dir / (src.stem + ".webp"), SHOT_WIDTH)
            n += 1
    return n


def sync_mascots(app: Path) -> int:
    n = 0
    base = app / "ios" / "BeeHive" / "Resources" / "Assets.xcassets" / "Mascot"
    for src in sorted(base.glob("*/*@3x.png")):
        name = src.name.replace("@3x.png", "")
        im = Image.open(src).convert("RGBA")
        im.thumbnail((MASCOT_SIZE, MASCOT_SIZE), Image.LANCZOS)
        dst = OUT / "mascot" / f"{name}.webp"
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=88, method=6)
        n += 1
    return n


def sync_icon(app: Path, icon_name: str) -> int:
    src = app / "docs" / "appstore" / "icon" / icon_name
    if not src.is_file():
        print(f"  ! missing {src}")
        return 0
    im = Image.open(src).convert("RGB")
    targets = {
        "favicon-32.png": 32,
        "favicon-192.png": 192,
        "apple-touch-icon.png": 180,
        "og-icon.png": 512,
    }
    for name, size in targets.items():
        dst = OUT / "icon" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.resize((size, size), Image.LANCZOS).save(dst, "PNG", optimize=True)
    return len(targets)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("app_repo", type=Path, help="path to the BeeHive app repo root")
    ap.add_argument("--icon", default="icon-C2.png", help="file name in docs/appstore/icon/ (default icon-C2.png)")
    args = ap.parse_args()
    app = args.app_repo.expanduser().resolve()
    if not (app / "docs" / "appstore").is_dir():
        sys.exit(f"Not an app repo (no docs/appstore): {app}")
    print(f"screenshots: {sync_screenshots(app)}")
    print(f"mascots:     {sync_mascots(app)}")
    print(f"icons:       {sync_icon(app, args.icon)}")


if __name__ == "__main__":
    main()
