// Generic form inspector for any ATS / custom portal (Lever, Workable, tfaforms, university portals…).
// Run with Playwright MCP: browser_run_code_unsafe { filename: "<path>/generic_inspect.js" }
// Read-only. Prints every visible input/select/textarea with its question text, required flag and options.
async (page) => {
  return await page.evaluate(() => {
    const question = (e) => {
      if (e.labels && e.labels[0]) return e.labels[0].innerText;
      let c = e;
      for (let i = 0; i < 6 && c; i++) {
        c = c.parentElement;
        const l = c && c.querySelector('label, legend, .application-label, .text, [class*=label], [class*=question]');
        if (l && l.innerText.trim()) return l.innerText;
      }
      return e.getAttribute('aria-label') || e.placeholder || e.name || e.id || '';
    };
    const els = [...document.querySelectorAll('input, select, textarea')]
      .filter(e => e.type !== 'hidden' && (e.offsetParent || ['file', 'radio', 'checkbox'].includes(e.type)));
    const seenGroups = new Set();
    const out = [];
    for (const e of els) {
      const q = question(e).replace(/\s+/g, ' ').trim().slice(0, 200);
      const req = e.required || e.getAttribute('aria-required') === 'true' || /\*|✱/.test(q);
      if (e.type === 'radio' || e.type === 'checkbox') {
        const key = e.name || q;
        if (seenGroups.has(key)) continue;
        seenGroups.add(key);
        const group = [...document.querySelectorAll(`input[name="${CSS.escape(e.name)}"]`)];
        const opts = group.map(g => (g.labels && g.labels[0] ? g.labels[0].innerText : g.value).trim()).join(' | ');
        let container = e;
        for (let i = 0; i < 6 && container; i++) container = container.parentElement;
        const ctx = container ? container.innerText.replace(/\s+/g, ' ').slice(0, 220) : q;
        out.push(`${e.type.toUpperCase()} name=${e.name} req=${req} :: ${ctx} => ${opts.slice(0, 400)}`);
      } else if (e.tagName === 'SELECT') {
        const opts = [...e.options].map(o => o.text.trim());
        out.push(`SELECT name=${e.name} id=${e.id} req=${req} :: ${q} => ${opts.slice(0, 25).join(' | ')}${opts.length > 25 ? ` …(${opts.length})` : ''}`);
      } else {
        out.push(`${e.tagName}/${e.type} name=${e.name} id=${e.id} req=${req} :: ${q}${e.value ? ` [value: ${e.value.slice(0, 40)}]` : ''}`);
      }
    }
    const buttons = [...document.querySelectorAll('button, input[type=submit]')]
      .filter(b => b.offsetParent).map(b => (b.innerText || b.value || b.getAttribute('aria-label') || '').trim()).filter(Boolean);
    out.push('BUTTONS: ' + [...new Set(buttons)].slice(0, 30).join(' | '));
    return out.join('\n');
  });
}
