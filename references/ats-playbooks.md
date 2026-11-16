# Filling forms by platform (Playwright MCP)

General loop for every platform:
1. `browser_tabs action=new url=…` – one tab per application so finished forms stay open for the applicant.
2. Dismiss cookie banners (prefer "reject non-essential").
3. Inspect (`scripts/gh_inspect.js` or `scripts/generic_inspect.js` via `browser_run_code_unsafe` with `filename`).
4. Map fields → profile values; list the mapping.
5. Fill; upload from `upload/`.
6. Verify (empty required fields, screenshot).
7. Hand over. Do not click Submit.

## Greenhouse (job-boards.greenhouse.io, job-boards.eu.greenhouse.io, embedded iframes)

- Company pages often embed the form in an iframe: read `iframe.src` (`…/embed/job_app?for=<board>&token=<job id>`) and navigate to it directly.
- Text fields: `#first_name`, `#last_name`, `#email`, `#phone`, `#preferred_name`, `#question_<id>`.
- Files: `#resume`, `#cover_letter`, `#question_<id>` (custom uploads such as transcripts). Use `locator.setInputFiles(path)`.
- Dropdowns are react-select comboboxes (`role=combobox`). To select: click it, `pressSequentially(text)` to filter, wait ~1 s, click the `role=option` whose text matches. `fill()` alone does not select.
- The phone "Country" combobox lists entries like "Spain +34".
- "Location (City)" is a geocoder: type the city and pick the first matching option.
- School dropdowns have ~5,000 entries: search by full name, acronym and country; fall back to "Other" (and a free-text field if one appears).
- Education block: Degree, Discipline, start/end month (comboboxes) + year (text inputs `#start-year--0`, `#end-year--0`).
- Consent dropdowns ("Privacy Statement", "Interview Conduct Policy", "Terms and Conditions") have a single "I agree" option: tick only with the applicant's explicit OK; use `browser_click` on the combobox then the option.
- Combobox indexes shift when conditional questions appear: re-inspect after answering questions that reveal others.

## Lever (jobs.lever.co/<company>/<id>/apply)

- Plain HTML. Inputs by `name`: `name`, `email`, `phone`, `location`, `org`, `urls[LinkedIn]`, `urls[GitHub]`, `urls[Portfolio]`, `resume` (file), `comments`.
- Custom questions: `cards[<uuid>][fieldN]` (radio, checkbox, select, textarea). Read each card's container text to get the question.
- Some radios ignore `check()`: set `checked=true` and dispatch `change` via `page.evaluate`.
- Uploading the résumé triggers a parser that may overwrite name/location: upload first, then fill fields.

## Workable (apply.workable.com)

- Multi-step form; résumé parser fills fields. Re-check every auto-filled value, especially dates.

## Custom portals seen in practice

| Portal pattern | Notes |
|---|---|
| Company-built forms (e.g. trading firms) | Custom dropdowns made of `<button>Select an option</button>` + list items + a search box. Click the button by its *label's* sibling, choose the `listitem`, verify. Hidden radios: click `label[for=id]`. |
| Résumé auto-parse + experience cards (e.g. fintech portals) | After upload a modal "Uploading resume / importing" blocks clicks: wait for it to detach. Parsed dates can be off by one month; editing a card may require re-selecting company and position. |
| University portals with e-mail magic links | The applicant requests the link (captcha), then pastes it to you; open it in the automated browser. |
| SiROP / research portals | Account registration by the applicant; documents as PDF only; check each document rule (e.g. Europass CV, official transcript). |
| FormAssembly / tfaforms (fellowships) | Multi-page; eligibility checkboxes are attestations: tick only what is true. Code-sample and essay questions need the applicant's input. |
| Europass CV editor | Upload Europass XML (or PDF+XML), "standard builder", template step, Save → Download. See gotchas. |

## Verification snippets

Empty required fields (generic):
```js
() => [...document.querySelectorAll('[required]')]
  .filter(e => (e.type==='radio'||e.type==='checkbox') ? !document.querySelector(`[name="${e.name}"]:checked`) : !e.value)
  .map(e => e.name || e.id)
```

Confirm a submission after the applicant clicks Submit: `browser_network_requests` filtered by the platform's application endpoint; look for 2xx (e.g. `POST …/record-application => 204`).
