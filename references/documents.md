# Documents

## CV

- Keep an editable source. Supported patterns:
  - **Europass:** Europass PDFs embed their XML (`pdfdetach -list cv.pdf` → `attachment.xml`). Extract it with `scripts/europass_xml.py extract`, edit (or use `add-award`), upload the XML at the Europass CV editor ("Start by uploading a Europass CV" → standard builder → Save → Download).
  - LaTeX / HTML / docx: edit the source and re-export.
- After regenerating: `scripts/pdf_text_diff.sh old.pdf new.pdf` – the diff must show only intended changes. Move the old PDF to `archive/` with a date suffix; copy the new one into `upload/`.
- Most forms want one CV in English; some programs mandate a format (e.g. Europass).

## Transcripts

- Always upload the latest official transcript. Note its issue date and validity.
- If a program accepts an **unofficial** translation: write the courses to a CSV (`year,term,code,course,theory_h,practice_h,independent_h,total_h,grade,attempts`) and run `scripts/transcript_translation.py`. Include: institution, student name and student number (not the national ID), program, grading scale with bands, cumulative average, totals, verification code/URL of the original, and the line "Translation prepared by the applicant."
- If a program requires an **official/certified** translation, tell the applicant early (it can take days): ask the registrar for an English version or use a certified translator.
- Some forms take one file only: merge original + translation (`pdfunite original.pdf translation.pdf merged.pdf`). Merging may invalidate the original's digital signature; keep separate files whenever two uploads are possible.

## Letters, statements, essays

- Source in Markdown in `docs/`; render with `scripts/md_to_pdf.py` (A4, serif, auto-shrinks to the page limit).
- First block = header lines (name, program, target), then paragraphs separated by a blank line.
- Respect limits: "ideally one page", word counts (count with `wc -w` or the script output).
- Reuse: keep a master motivation letter per theme and adapt the opening and the "why this place/lab" paragraph.
- Save every text you wrote for a form in `docs/<org>_<role>.md` so the applicant can review it later.

## Other documents

- Enrollment certificate, language certificate, passport scan: list them in the profile; check expiry dates vs. program dates.
- References: collect name/title/email/relationship in the profile; the applicant requests the letters. Many portals email the referee a link after you enter their address: confirm with the applicant before entering referee emails.
