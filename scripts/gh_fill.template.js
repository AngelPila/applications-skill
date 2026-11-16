// Greenhouse form filler TEMPLATE.
// 1) Run gh_inspect.js and note combobox indexes / field ids.
// 2) Copy this file to a temp path, edit ANSWERS below (values come from the applicant profile), run:
//    browser_run_code_unsafe { filename: "<temp>/gh_fill.js" }
// 3) It NEVER clicks Submit. Legal consents are deliberately not handled here: tick them with
//    individual browser_click calls only after the applicant authorizes it.
async (page) => {
  const ANSWERS = {
    text: {
      // '#first_name': 'Given',
      // '#last_name': 'Family',
      // '#email': 'name@example.com',
      // '#phone': '600000000',
      // '#question_123456': 'Free-text answer',
    },
    files: {
      // '#resume': '/abs/path/upload/CV.pdf',
      // '#cover_letter': '/abs/path/upload/Cover.pdf',
    },
    // [comboboxIndex, searchTextOrNull, regexSourceForOption]
    combos: [
      // [0, 'Spain', 'Spain'],            // phone country
      // [1, 'City', 'City'],                  // Location (City) geocoder
      // [2, 'University name', '^Other$'],     // School
      // [6, null, '^Yes$'],                   // sponsorship
    ],
  };

  const log = [];
  for (const [sel, val] of Object.entries(ANSWERS.text)) {
    await page.locator(sel).fill(val);
    log.push(`text ${sel}`);
  }
  for (const [sel, path] of Object.entries(ANSWERS.files)) {
    await page.locator(sel).setInputFiles(path);
    log.push(`file ${sel}`);
  }
  for (const [i, search, reSrc] of ANSWERS.combos) {
    const box = page.getByRole('combobox').nth(i);
    await box.click();
    if (search) {
      await box.fill('');
      await box.pressSequentially(search, { delay: 40 });
      await page.waitForTimeout(1000);
    }
    const opt = page.getByRole('option').filter({ hasText: new RegExp(reSrc) }).first();
    if (!(await opt.count())) {
      const seen = (await page.getByRole('option').allTextContents()).slice(0, 8).join(' | ');
      await page.keyboard.press('Escape');
      log.push(`combo ${i} MISS (saw: ${seen})`);
      continue;
    }
    const t = (await opt.innerText()).replace(/\s+/g, ' ');
    await opt.click();
    await page.waitForTimeout(250);
    log.push(`combo ${i} -> ${t.slice(0, 80)}`);
  }
  const empty = await page.locator('input:visible, textarea:visible').evaluateAll(es =>
    es.filter(e => e.getAttribute('role') !== 'combobox' && (e.required || e.getAttribute('aria-required') === 'true') && !e.value)
      .map(e => e.id || e.name));
  log.push(`EMPTY REQUIRED TEXT: ${empty.join(', ') || 'none'}`);
  return log.join('\n');
}
