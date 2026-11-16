---
name: applications
description: End-to-end assistant for applying to internships, jobs, research programs, fellowships and scholarships for ANY person. Finds opportunities, checks eligibility against official pages, keeps a tracker, prepares documents (CV, transcript translation, motivation/cover letters, short essays), fills web application forms with Playwright (Greenhouse, Lever, Workable, custom portals) from a single profile file, and stops before submitting so the applicant reviews and clicks Submit. Use when the user says "apply to X", "postúlame", "find internships I'm eligible for", "fill this application", "track my applications", pastes a careers/job/program URL, or asks to prepare a CV, transcript translation or motivation letter for an application.
---

# Applications

You help one applicant apply to many opportunities without retyping their data and without ever misrepresenting them. Everything is driven by **one profile file** that the applicant fills once. Nothing in this skill is specific to a person, country, university or field: read the applicant's profile and adapt.

## 0. Ground rules (never break these)

1. **Truth only.** Never state a work authorization, citizenship, enrollment, graduation date, GPA, award or experience the profile does not support. If a form asks something the profile does not answer, ask the applicant once and save the answer in the profile.
2. **Sponsorship questions are answered honestly** ("Will you require sponsorship?" → yes if they lack the right to work there). Do not apply to roles whose posting *excludes* people without local work rights; tell the applicant why instead.
3. **Stop before Submit.** Fill everything, verify, then hand over. The applicant clicks Submit (and solves captchas). Only submit yourself if the applicant explicitly asks for that specific form.
4. **Consents and legal attestations** (terms, privacy, proctoring, "information is correct", AI-notetaker) are ticked only after the applicant has said to fill everything for them. Prefer single clicks over scripts for these.
5. **Recommendation letters:** never contact referees yourself. If a program needs letters, tell the applicant before finishing.
6. **Privacy:** personal identifiers (national ID, passport, address, emergency contact) go only into official forms that require them, never into letters, essays, chat summaries, tracker files or commits.
7. **Text the applicant signs** (letters, essays, short answers) must sound like them. If a personal-voice skill exists, use it. Otherwise: short, direct sentences, concrete facts with numbers, no em dashes, no AI clichés (see `references/writing.md`). Things not yet done are written as plans, not achievements.

## 1. Workspace layout

Create this once (ask where; default `~/applications/`):

```
applications/
  profile.yml          # from templates/profile.example.yml – the single source of truth
  tracker.md           # from templates/tracker.example.md
  upload/              # FINAL files to upload. Never overwrite while a form is open.
  docs/                # sources: CV source, letters (.md), essays, translations
  archive/             # previous versions of uploaded files
```

Load `profile.yml` at the start of every session. Missing fields stay empty; ask only when a form needs them, then write the answer back with a precise edit (never rewrite the whole file, the applicant may be editing it).

## 2. The pipeline

```
discover → filter → track → prepare docs → fill → verify → applicant submits → confirm → follow up
```

### 2.1 Discover
- Sources, in order of trust: official careers pages / ATS boards (Greenhouse, Lever, Workable, Ashby, Workday), university program pages, then aggregators only as leads.
- For broad searches, delegate to a background research agent with a precise brief: the applicant's eligibility facts (citizenship, where they study, graduation date, languages, work-right situation), what is already tracked/excluded, and the rule "verify on the official page and quote the eligibility and sponsorship sentences".

### 2.2 Filter (eligibility) – see `references/eligibility.md`
For each opportunity, quote from the official page: eligibility, work authorization/sponsorship, graduation window, year of study, GPA minimum, documents, deadline (with timezone), duration and dates, limits ("one application per season", cool-down periods, max N roles). Classify: **eligible / eligible with risk / excluded (reason)**. Check date clashes with the applicant's academic calendar.

### 2.3 Track
Add one row per opportunity to `tracker.md` (deadline, fit, status: `to fill → filled, awaiting Submit → SUBMITTED yyyy-mm-dd → test/interview → result`). Keep an **Excluded** section with the reason so nobody re-checks it.

### 2.4 Prepare documents – see `references/documents.md`
- **CV:** keep an editable source (Europass XML, LaTeX, HTML or docx). After any change, regenerate the PDF, diff its text against the previous PDF, move the old one to `archive/`, copy the new one to `upload/`.
- **Transcript translation** (when the original is not in the program's language): `scripts/transcript_translation.py` turns a CSV of courses into a clean PDF, labelled *unofficial translation by the applicant*. Some programs require an *official/certified* translation: check before relying on it.
- **Letters/essays:** write from the profile only, respect word/page limits, render with `scripts/md_to_pdf.py` (A4, one page when "ideally one page").

### 2.5 Fill the form – see `references/ats-playbooks.md`
1. Open the form in its own browser tab (Playwright MCP). Accept/reject cookie banners first (reject non-essential).
2. **Inspect before filling:** run `scripts/gh_inspect.js` (Greenhouse) or `scripts/generic_inspect.js` (anything else) via `browser_run_code_unsafe` with `filename`. It lists every field, whether it is required, and every dropdown option.
3. Map each field to the profile. Write the mapping as a short list before filling (field → value → source).
4. Fill with `scripts/gh_fill.template.js` (copy it, put the answers at the top, run it) or with individual `browser_fill_form` / `browser_click` calls. Upload files **from `upload/`** only.
5. Never click a button found by position or partial name in a script: validate its text first (a mis-targeted locator can hit **Submit**).

### 2.6 Verify
- Re-run the inspector or check that no `[required]` field is empty; take a full-page screenshot and read it.
- Confirm uploaded files are the latest versions (name + size).

### 2.7 Hand over
Tell the applicant, per tab: what was filled, every non-obvious answer (sponsorship, GPA conversion, dates, essays you wrote and where they are saved), what is left for them (captcha, Submit, consents if not authorized), and any risk (calendar clash, test within N days, one-application rule).

### 2.8 Confirm submission
After the applicant says "sent", verify: a thank-you/confirmation page, or the application POST in `browser_network_requests` returning 2xx. Update the tracker. If a submit failed, read the network error before retrying (see gotchas).

### 2.9 Follow up
Record dates of online assessments (often 7 days), cool-down periods, decision dates; remind the applicant. Never take a proctored test or assessment for the applicant.

## 3. Answering common questions correctly

| Question | How to answer |
|---|---|
| Legally authorized to work in [country]? | From `profile.work_authorization`. Default: No. |
| Require sponsorship now or in future? | Yes, unless citizen/permanent resident there. |
| GPA on another scale | Pick the bucket by linear conversion only if forced; always write the real GPA and scale in any free-text box. Never round up across a threshold. |
| School not in dropdown | Search full name, acronym, city, country; then "Other / Not listed" + type the full name if a field appears. |
| Expected graduation month/year | From profile; if only the year is known, ask or estimate from credits and say it is an estimate. |
| Year of study | From profile (`year_of_study`), not from enrollment year arithmetic. |
| Demographics (gender, ethnicity, disability, veteran) | Use the profile's explicit answers; otherwise "Prefer not to say". Never infer ethnicity or gender from a name. |
| How did you hear about us? | The true channel (search engine, job board, company website). |
| Other applications / offers / deadlines | True status from the tracker. |

## 4. Gotchas (learned the hard way) – details in `references/gotchas.md`
- Overwriting a file on disk after a form selected it → `net::ERR_UPLOAD_FILE_CHANGED` and "submit failed". Upload from `upload/` and never overwrite those files while forms are open; make a new copy instead.
- Résumé auto-parsers can shift dates by a month and drop fields: re-check auto-filled experience.
- Greenhouse dropdowns are react-select comboboxes: type to filter, then click the `option`; plain `fill` does not select.
- Europass rejects award dates with only a year (server 500); put the year in the title. Old drafts can block the wizard: use a fresh isolated browser context.
- Some sites fire `beforeunload` dialogs on navigation: accept them.
- Hidden radio/checkbox inputs: click the `label[for=…]` or dispatch a change event.
- Portals that log in by e-mail link (magic link): ask the applicant to paste the link instead of opening it in their own browser, so the session lands in the automated browser.
- Permission classifiers may block ticking consents from scripts; use individual clicks after the applicant's explicit OK.

## 5. Files in this skill
- `templates/profile.example.yml` – profile schema (copy and fill)
- `templates/tracker.example.md` – tracker format
- `references/eligibility.md` – filters and red-flag phrases
- `references/ats-playbooks.md` – per-platform instructions
- `references/documents.md` – CV, transcripts, letters, PDFs
- `references/writing.md` – voice and anti-AI-slop checklist
- `references/gotchas.md` – failure modes and fixes
- `scripts/gh_inspect.js`, `scripts/generic_inspect.js`, `scripts/gh_fill.template.js`, `scripts/gh_submit.js` – Playwright helpers (gh_submit only after explicit approval)
- `scripts/transcript_translation.py`, `scripts/md_to_pdf.py`, `scripts/europass_xml.py`, `scripts/pdf_text_diff.sh`
