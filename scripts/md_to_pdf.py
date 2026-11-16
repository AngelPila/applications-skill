#!/usr/bin/env python3
"""Render a letter/essay written in simple Markdown-ish text to an A4 PDF.

Usage:
  python3 md_to_pdf.py letter.md out.pdf [--max-pages N] [--font serif|sans]

Format of letter.md:
  - First block (until the first blank line) = header lines (name, program, target).
  - Then paragraphs separated by blank lines. Single newlines inside a paragraph become <br>.
  - Lines starting with "## " are rendered as small headings (for multi-answer documents).

The script shrinks font size and margins step by step until the PDF fits --max-pages (default 1).
Also prints the word count and warns about em dashes.
"""
import argparse
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

STEPS = [(10.5, 1.4, 20), (10.0, 1.32, 16), (9.5, 1.28, 14), (9.0, 1.25, 12)]


def chrome():
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(n):
            return shutil.which(n)
    sys.exit("No Chrome/Chromium found.")


def pages(pdf):
    try:
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        return int([l for l in out.splitlines() if l.startswith("Pages:")][0].split()[1])
    except Exception:
        return 0


def build(text, size, lh, margin, family):
    blocks = [b for b in text.strip().split("\n\n") if b.strip()]
    e = html.escape
    parts = ['<div class="h">' + "<br>".join(e(l) for l in blocks[0].splitlines()) + "</div>"]
    for b in blocks[1:]:
        if b.startswith("## "):
            parts.append(f"<h2>{e(b[3:].strip())}</h2>")
        else:
            parts.append("<p>" + "<br>".join(e(l) for l in b.splitlines()) + "</p>")
    font = '"DejaVu Serif", Georgia, serif' if family == "serif" else '"DejaVu Sans", Arial, sans-serif'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: {margin}mm {margin + 3}mm; }}
body {{ font-family: {font}; font-size: {size}pt; line-height: {lh}; color: #111; }}
.h {{ margin-bottom: 12px; }} p {{ margin: 0 0 7px; }} h2 {{ font-size: {size + 1}pt; margin: 12px 0 4px; }}
</style></head><body>{''.join(parts)}</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--max-pages", type=int, default=1)
    ap.add_argument("--font", choices=["serif", "sans"], default="serif")
    a = ap.parse_args()
    text = Path(a.src).read_text(encoding="utf-8")
    words = len(text.split())
    if "—" in text:
        print("WARNING: em dash found; replace it before sending.")
    with tempfile.TemporaryDirectory() as td:
        for size, lh, margin in STEPS:
            h = Path(td) / "doc.html"
            h.write_text(build(text, size, lh, margin, a.font), encoding="utf-8")
            subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                            "--no-pdf-header-footer", f"--print-to-pdf={a.out}", h.as_uri()],
                           check=True, capture_output=True)
            n = pages(a.out)
            if n and n <= a.max_pages:
                print(f"{a.out}: {n} page(s), {size}pt, {words} words")
                return
    print(f"{a.out}: still {pages(a.out)} pages at the smallest size; shorten the text ({words} words).")


if __name__ == "__main__":
    main()
