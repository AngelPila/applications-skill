# Writing for the applicant

If the applicant has a personal voice skill, use it and ignore the style parts below.

## Process
1. Use only facts from the profile. Missing fact → `[brackets]` or ask. Never invent numbers.
2. Answer exactly what is asked, in the order asked. Respect the limit.
3. Pick 2–3 facts that answer the reader's question; do not list the whole CV.
4. Each claim carries its proof (event + number, project + what it does).
5. Things in progress are described as in progress or as a plan.
6. End with something concrete (what they would do/learn, what comes next), not a motivational line.

## Style
- Short, direct sentences; active voice; plain words a B2 English speaker would use.
- Explain technical work in one sentence: what goes in, what comes out, why it matters.
- Humble without apologising ("I want to learn how…" instead of "although I am only a student").

## Banned (AI tells)
- Em dashes (—). Use commas, periods or parentheses.
- "delve", "tapestry", "testament", "thrilled/honored to", "journey", "embark", "realm", "pivotal", "leverage" (non-technical), "showcase", "foster" (more than once), "in today's fast-paced world", "it's not just X, it's Y", chains of "furthermore/moreover".
- Automatic triads of adjectives or verbs.
- Generic closings ("I am confident I would be a great fit").

Check: `grep -nE "—|delve|tapestry|testament|thrilled|journey|embark|realm|pivotal|showcase" file.md`

## Common prompts and what they really ask
| Prompt | Answer with |
|---|---|
| Why us? | One specific thing about the team/product/lab + how it connects to one concrete thing the applicant did. |
| Hardest technical challenge | The problem, why it was hard (not just big), what changed in the approach, what was learned; no invented metrics. |
| Something not on your CV | One short true story from the profile's `not_on_cv`; ask if empty. |
| Diversity / perspective | Only what the applicant chose to share in `background_context`. |
| Code sample description | What it does, the applicant's part, one design decision, one thing learned. |
