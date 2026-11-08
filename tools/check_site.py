#!/usr/bin/env python3
"""Static checks for the site. Run from anywhere: python3 tools/check_site.py

1. Every internal href/src resolves to a file (and #fragment to an id on that page).
2. Nothing is loaded from another origin (src=, <link href=> to http/https/protocol-relative URLs).
3. Banned marketing words never appear in visible text or comments.
4. The only email address anywhere is the approved contact address.
Exit code 0 = all good, 1 = problems found.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
BASE = "/beehive_web/"  # GitHub Pages project path, used by 404.html
ALLOWED_EMAIL = "hounienlin@gmail.com"
BANNED = [
    r"spelling[\s\-]*bee",       # trademark; the 7-letter game is Hive Challenge / 蜂巢挑戰
    r"官方", r"\bofficial\b", r"題庫", r"指定字表", r"歷屆",
    r"全年級", r"\bK[–-]12\b", r"all grades",
    r"\bAI\b", r"人工智慧", r"保證", r"\bbest\b", r"#1", r"No\.1",
    r"立即購買", r"限時", r"馬上解鎖",
    r"\[聯絡信箱\]", r"\[contact email\]", r"\[開發者名稱\]", r"\[developer name\]",
]


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str, str]] = []  # (tag, attr, value)
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a and a["id"]:
            self.ids.add(a["id"])
        for attr in ("href", "src"):
            if a.get(attr):
                self.refs.append((tag, attr, a[attr]))


def parse(path: Path) -> Collector:
    c = Collector()
    c.feed(path.read_text(encoding="utf-8"))
    return c


def resolve(page: Path, url: str) -> Path:
    path = unquote(urlsplit(url).path)
    if path.startswith(BASE):
        target = ROOT / path[len(BASE):]
    elif path.startswith("/"):
        target = ROOT / path.lstrip("/")
    elif path == "":
        target = page
    else:
        target = (page.parent / path).resolve()
    if target.is_dir() or str(path).endswith("/"):
        target = target / "index.html"
    return target


def main() -> int:
    pages = sorted(p for p in ROOT.rglob("*.html") if "tools" not in p.parts)
    parsed = {p: parse(p) for p in pages}
    problems: list[str] = []
    checked = 0

    for page, c in parsed.items():
        rel = page.relative_to(ROOT)
        for tag, attr, url in c.refs:
            parts = urlsplit(url)
            if parts.scheme in ("mailto", "tel"):
                continue
            if parts.scheme in ("http", "https") or url.startswith("//"):
                # absolute links are fine for <a>, canonical/alternate/og; never as loaded resources
                if attr == "src" or (tag == "link" and "stylesheet" in url) or tag in ("script", "img"):
                    problems.append(f"{rel}: third-party resource {url}")
                continue
            if url == "#":
                continue  # App Store placeholder button (TODO)
            checked += 1
            target = resolve(page, url)
            if not target.exists():
                problems.append(f"{rel}: broken {attr}={url}")
                continue
            if parts.fragment and target.suffix == ".html":
                ids = parsed.get(target.resolve(), None) or parse(target)
                if parts.fragment not in ids.ids:
                    problems.append(f"{rel}: missing anchor {url}")

    for page in pages:
        text = page.read_text(encoding="utf-8")
        rel = page.relative_to(ROOT)
        for pat in BANNED:
            for m in re.finditer(pat, text, flags=re.IGNORECASE):
                problems.append(f"{rel}: banned term {m.group(0)!r}")
        for m in re.finditer(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
            if m.group(0) != ALLOWED_EMAIL:
                problems.append(f"{rel}: unexpected email {m.group(0)}")
        if re.search(r"<link[^>]+href=\"(https?:)?//(?!hounienlin\.github\.io)", text):
            problems.append(f"{rel}: <link> to another origin")
        if "<script" in text and "src=" in text.split("<script", 1)[1].split(">", 1)[0]:
            problems.append(f"{rel}: external script")

    print(f"pages: {len(pages)}, internal refs checked: {checked}")
    for p in problems:
        print("  ✗", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
