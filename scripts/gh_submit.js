// Click the single "Submit application" button on a Greenhouse/Lever form and report the result.
// Use ONLY after the applicant explicitly asked to submit this form.
async (page) => {
  const btn = page.getByRole('button', { name: /^Submit application$/i });
  const n = await btn.count();
  if (n !== 1) return `ABORT: found ${n} submit buttons`;
  await btn.click();
  await page.waitForTimeout(8000);
  const errs = (await page.locator('[class*=error]:visible, [role=alert]:visible').allInnerTexts()).filter(t => t.trim());
  const captcha = await page.locator('iframe[src*=captcha]').evaluateAll(fs => fs.filter(f => f.getBoundingClientRect().height > 100).length);
  const body = (await page.locator('body').innerText()).replace(/\s+/g, ' ').slice(0, 220);
  return `URL: ${page.url()}\nCAPTCHA VISIBLE: ${captcha}\nERRORS: ${errs.join(' | ').slice(0, 300) || 'none'}\nPAGE: ${body}`;
}
