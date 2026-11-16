// Greenhouse form inspector. Run with Playwright MCP: browser_run_code_unsafe { filename: "<path>/gh_inspect.js" }
// Lists text fields, file inputs, radios/checkboxes and every combobox with its options. Read-only (opens and closes dropdowns).
async (page) => {
  const out = [];
  const tbs = await page.locator('input[type=text],input[type=email],input[type=tel],input[type=url],input[type=number],textarea').evaluateAll(es => es.filter(e => e.offsetParent && e.getAttribute('role') !== 'combobox' && !e.closest('[aria-hidden=true]')).map(e => `TEXT #${e.id} req=${e.required||e.getAttribute('aria-required')} :: ${(e.labels?.[0]?.innerText||e.getAttribute('aria-label')||'').replace(/\s+/g,' ').slice(0,200)}`));
  out.push(...tbs);
  const files = await page.locator('input[type=file]').evaluateAll(es => es.map(e => { let c = e; for (let i=0;i<5;i++) c = c.parentElement||c; return `FILE #${e.id} :: ${(c.innerText||'').replace(/\s+/g,' ').slice(0,120)}`; }));
  out.push(...files);
  const checks = await page.locator('input[type=checkbox],input[type=radio]').evaluateAll(es => es.filter(e=>e.offsetParent||e.labels?.[0]?.offsetParent).map(e => `${e.type.toUpperCase()} #${e.id} name=${e.name} :: ${(e.labels?.[0]?.innerText||'').replace(/\s+/g,' ').slice(0,140)}`));
  out.push(...checks);
  const boxes = page.getByRole('combobox');
  const n = await boxes.count();
  for (let i = 0; i < n; i++) {
    const b = boxes.nth(i);
    const name = (await b.evaluate(e => e.labels?.[0]?.innerText || e.getAttribute('aria-label') || e.id)).replace(/\s+/g,' ').slice(0,220);
    if (/^Country\*?$/.test(name)) { out.push(`COMBO ${i} :: ${name} (phone)`); continue; }
    try { await b.click({ timeout: 2000 }); await page.waitForTimeout(250);
      const opts = (await page.getByRole('option').allTextContents()).filter(o => !/\+\d+$/.test(o));
      out.push(`COMBO ${i} :: ${name} => ${opts.slice(0, 20).join(' | ')}${opts.length>20?' …('+opts.length+')':''}`);
      await page.keyboard.press('Escape'); } catch (e) { out.push(`COMBO ${i} :: ${name} ERR`); }
  }
  return out.join('\n');
}
