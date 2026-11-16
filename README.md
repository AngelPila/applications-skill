# applications – a Claude Code skill for internship, job and research-program applications

A person-agnostic skill that helps anyone apply to many opportunities without retyping their data and without misrepresenting themselves.

**What it does**

- Finds opportunities and checks eligibility on the **official** pages (work authorization, sponsorship, enrollment, graduation window, GPA, deadlines, one-application rules).
- Keeps a tracker (active, upcoming, excluded with reasons).
- Prepares documents: CV regeneration (Europass XML supported), unofficial transcript translations, one-page motivation/cover letters, short essays in the applicant's voice.
- Fills web forms with the Playwright MCP (Greenhouse, Lever, Workable, custom portals) from a single `profile.yml`.
- **Stops before Submit.** The applicant reviews, solves captchas and clicks Submit; the skill then confirms the submission went through.

**Principles:** truth only (honest sponsorship/work-authorization answers, real GPA and scale), no invented facts in essays, consents only with explicit permission, personal identifiers only in official forms.

## Install

```bash
git clone https://github.com/<you>/applications-skill ~/.claude/skills/applications
```

Requirements: Claude Code with the Playwright MCP; `python3`; Chrome/Chromium (PDF rendering); poppler-utils (`pdftotext`, `pdfinfo`, `pdfdetach`, `pdfunite`).

## Use

1. Ask Claude: "set up my applications workspace". It copies `templates/profile.example.yml` and `templates/tracker.example.md` into `~/applications/`.
2. Fill `profile.yml` once (leave unknowns empty).
3. Then: "find internships I'm eligible for", "apply to <URL>", "prepare a one-page motivation letter for <program>", "translate my transcript".

## Layout

```
SKILL.md                     workflow and rules (what Claude reads)
templates/                   profile and tracker templates
references/                  eligibility filters, per-platform playbooks, documents, writing, gotchas
scripts/                     Playwright inspectors/filler, transcript translation, letter→PDF, Europass helpers
```

## License

MIT
