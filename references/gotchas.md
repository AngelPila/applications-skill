# Gotchas and fixes

| Symptom | Cause | Fix |
|---|---|---|
| "Application submit failed / Something went wrong", network shows `net::ERR_UPLOAD_FILE_CHANGED` | The file was overwritten on disk after the form selected it. | Re-select the file from a copy that will not change (`upload/`). Never overwrite files in `upload/` while forms are open; write a new file name instead. |
| Lever: "There was an error verifying your application. Please try again." (POST `/apply` → 400 right after hCaptcha) | hCaptcha token rejected (solved too long before submitting, expired, or flagged). The page reloads with fields kept but the **résumé file dropped**. | Re-upload the résumé (`setInputFiles`), check that the parser did not overwrite fields, verify required fields, then the applicant clicks Submit and solves the captcha immediately (do not leave the captcha open for minutes). |
| Auto-parsed experience shows dates one month early | Résumé parser timezone bug. | Edit each card; some portals require re-selecting company and position before "Save/Change" enables. |
| Greenhouse dropdown "No options" after typing | Text was appended to a previous value. | `fill('')`, click, then `pressSequentially`. |
| Option not found in a long school list | Name differs (long official name, accents, acronym). | Try full name without accents, acronym, city, country; then "Other". |
| A script clicked Submit | Locator matched by position or a generic name ("Select an option" button lists shift; `following::button[1]` hit Submit). | Validate the button text before clicking; prefer refs from a fresh snapshot; check the URL/state right after. If the form blocked it for missing fields, nothing was sent. |
| Europass "Save" step stays disabled; console shows HTTP 500 | Award/certificate with a year-only date, or a stale draft. | Put the year in the title instead of a date; open the editor in a new isolated browser context; choose "Continue" (discard draft). |
| Europass download button greyed out after clicking | PDF generated server-side; download event missed. | Read the `office/download/pdf/<id>` request in network logs and fetch it as a blob, then trigger a download from the page. |
| Navigation blocked by a modal state | `beforeunload` dialog. | `browser_handle_dialog accept=true`. |
| Click intercepted by an overlay | Cookie banner or loading overlay. | Dismiss the banner; wait for the overlay to detach. |
| `check()` "did not change its state" | Custom radio implementation. | `page.evaluate` → set `checked=true`, dispatch `change` and `click`. |
| Permission classifier blocks a script | Script ticks legal consents. | Use individual `browser_click` calls after the applicant explicitly authorizes. |
| Playwright "browser already in use" | Another session holds the browser profile. | Ask the applicant to close the other session. |
| Snapshot file write denied | Snapshot path outside allowed roots. | Save snapshots under the home directory or the Playwright output dir. |
| Merged transcript PDF warns about xref / fields | Digitally signed original. | Expected; signature is not valid in the merged copy. Prefer separate uploads. |
| Optional `file` uploads with `browser_file_upload` fail ("no modal state") | No file chooser open. | Use `locator.setInputFiles()` inside `browser_run_code_unsafe`. |
