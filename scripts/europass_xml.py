#!/usr/bin/env python3
"""Helpers for Europass CVs.

  extract  <europass.pdf> <out.xml>            Extract the XML embedded in a Europass PDF (needs poppler's pdfdetach).
  add-award <in.xml> <out.xml> --title T --org O --desc D [--date YYYY-MM]
                                               Insert an award at the top of Honours/Certifications.
                                               Europass rejects year-only dates: use YYYY-MM or put the year in --title.
  validate <file.xml>                          Check the XML is well formed.

After editing, upload the XML at the Europass CV editor
("Start by uploading a Europass CV" -> standard builder -> Save -> Download).
"""
import argparse
import html
import re
import subprocess
import sys
import xml.dom.minidom


def extract(pdf, out):
    listing = subprocess.run(["pdfdetach", "-list", pdf], capture_output=True, text=True).stdout
    m = re.search(r"^(\d+):\s+(\S+\.xml)", listing, re.M)
    if not m:
        sys.exit("No embedded XML found: this PDF was not exported by Europass (or the attachment was stripped).")
    subprocess.run(["pdfdetach", "-save", m.group(1), "-o", out, pdf], check=True)
    print(f"extracted {m.group(2)} -> {out}")


def add_award(src, out, title, org, desc, date):
    s = open(src, encoding="utf-8").read()
    if date and not re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", date):
        sys.exit("--date must be YYYY-MM or YYYY-MM-DD (Europass fails on year-only dates).")
    e = html.escape
    date_xml = (f"\n                <eures:FirstIssuedDate>\n                    <hr:FormattedDateTime>{date}"
                f"</hr:FormattedDateTime>\n                </eures:FirstIssuedDate>") if date else ""
    block = (f"            <Certification>\n                <hr:CertificationName>{e(title)}</hr:CertificationName>{date_xml}\n"
             f"                <eures:IssuingAuthority>\n                    <oa:Name>{e(org)}</oa:Name>\n"
             f"                </eures:IssuingAuthority>\n"
             f"                <oa:Description>&lt;p&gt;{e(e(desc))}&lt;/p&gt;</oa:Description>\n"
             f"            </Certification>\n")
    anchor = re.search(r"<Certifications>\s*\n", s)
    if not anchor:
        sys.exit("No <Certifications> section found; add one award in the Europass editor first.")
    s = s[:anchor.end()] + block + s[anchor.end():]
    xml.dom.minidom.parseString(s.encode())
    open(out, "w", encoding="utf-8").write(s)
    print(f"added '{title}' -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("extract"); p.add_argument("pdf"); p.add_argument("out")
    p = sp.add_parser("add-award"); p.add_argument("src"); p.add_argument("out")
    p.add_argument("--title", required=True); p.add_argument("--org", required=True)
    p.add_argument("--desc", required=True); p.add_argument("--date")
    p = sp.add_parser("validate"); p.add_argument("xml")
    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.pdf, a.out)
    elif a.cmd == "add-award":
        add_award(a.src, a.out, a.title, a.org, a.desc, a.date)
    else:
        xml.dom.minidom.parse(a.xml)
        print("well formed")


if __name__ == "__main__":
    main()
