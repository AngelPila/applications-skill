#!/usr/bin/env python3
"""Build an UNOFFICIAL English translation of a transcript as HTML + PDF.

Usage:
  python3 transcript_translation.py courses.csv meta.json out_basename

courses.csv columns (header required):
  year,term,code,course,theory_h,practice_h,independent_h,total_h,grade,attempts
  (leave unknown columns empty; empty columns are dropped from the table)

meta.json keys (all optional except institution/student/program):
  institution, office, student, student_id, program, program_original,
  issued, valid_until, signed_by, grading_scale, cumulative_average,
  verification, totals (dict label->value), term_notes

Never put national ID numbers in meta.json.
PDF rendering uses a local Chrome/Chromium in headless mode.
"""
import csv
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

COLS = [
    ("year", "Year"), ("term", "Term"), ("code", "Code"), ("course", "Course"),
    ("theory_h", "Theory h"), ("practice_h", "Practice h"), ("independent_h", "Indep. h"),
    ("total_h", "Total h"), ("grade", "Grade"), ("attempts", "Times taken"),
]
NUMERIC = {"theory_h", "practice_h", "independent_h", "total_h", "attempts"}


def find_chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("No Chrome/Chromium found for PDF rendering (HTML was still written).")


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    csv_path, meta_path, out = sys.argv[1:]
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
    meta = json.load(open(meta_path, encoding="utf-8"))
    cols = [(k, h) for k, h in COLS if any((r.get(k) or "").strip() for r in rows)]
    e = html.escape

    def line(label, key):
        return f"<p><b>{label}:</b> {e(str(meta[key]))}</p>" if meta.get(key) else ""

    head = "".join([
        f"<p class='note'>Translation prepared by the applicant. The original document is attached."
        f"{' ' + e(meta['verification']) if meta.get('verification') else ''}</p>",
        line("Institution", "institution"), line("Office", "office"),
        f"<p><b>Student:</b> {e(meta.get('student', ''))}"
        f"{' – Student ID ' + e(meta['student_id']) if meta.get('student_id') else ''}</p>",
        f"<p><b>Program:</b> {e(meta.get('program', ''))}"
        f"{' (“' + e(meta['program_original']) + '”)' if meta.get('program_original') else ''}</p>",
        line("Issued", "issued"), line("Valid until", "valid_until"), line("Signed by", "signed_by"),
        line("Grading scale", "grading_scale"),
        f"<p><b>Cumulative average: {e(meta['cumulative_average'])}</b></p>" if meta.get("cumulative_average") else "",
    ])
    th = "".join(f"<th>{h}</th>" for _, h in cols)
    trs = "".join(
        "<tr>" + "".join(
            f"<td class='{'n' if k in NUMERIC else ''}'>{e((r.get(k) or '').strip())}</td>" for k, _ in cols
        ) + "</tr>" for r in rows
    )
    totals = meta.get("totals") or {}
    tot = "".join(f"<tr><td>{e(k)}:</td><td>&nbsp;{e(str(v))}</td></tr>" for k, v in totals.items())
    notes = f"<p class='note'>{e(meta['term_notes'])}</p>" if meta.get("term_notes") else ""
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Unofficial translation</title>
<style>@page {{ size: A4; margin: 16mm 14mm; }}
body {{ font-family: "DejaVu Sans", Arial, sans-serif; font-size: 9.5pt; color: #111; }}
h1 {{ font-size: 13pt; margin: 0 0 4px; }} p {{ margin: 3px 0; }} .note {{ font-style: italic; color: #444; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 8px; }}
th, td {{ border: 1px solid #999; padding: 3px 5px; text-align: left; }} th {{ background: #eee; }}
td.n {{ text-align: right; }} table.sum td {{ border: none; padding: 1px 0; }}</style></head><body>
<h1>Unofficial English translation – Academic transcript</h1>{head}
<table><tr>{th}</tr>{trs}</table>
{'<table class="sum" style="margin-top:10px;width:auto">' + tot + '</table>' if tot else ''}{notes}
</body></html>"""
    html_path = Path(out).with_suffix(".html")
    pdf_path = Path(out).with_suffix(".pdf")
    html_path.write_text(doc, encoding="utf-8")
    subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                    html_path.resolve().as_uri()], check=True, capture_output=True)
    print(f"{len(rows)} courses -> {pdf_path}")


if __name__ == "__main__":
    main()
