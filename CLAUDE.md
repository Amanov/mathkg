# Design guidance for this project

When designing or redesigning any page or component in mathkg, avoid
generic "AI slop" UI patterns: gradient buttons with shine-sweep hover
effects, glassmorphism, emoji used as icons, purple-to-blue gradients as
a default accent, and unnecessary decorative flourishes that don't serve
the content.

Reference quality bar (not live-browsable — this sandbox's network policy
blocks fetching them directly, confirmed 2026-09; ask the user to paste a
screenshot of anything specific they want matched):

- **https://21st.dev** — modern React/Tailwind UI component patterns from
  real builders. Use as a mental model for what a well-built button, card,
  or form actually looks like versus a generic Bootstrap default.
- **https://pageflows.com** — screen-recorded UX flows from real,
  successful SaaS products. Reference for how multi-step flows (onboarding,
  checkout, settings) should actually sequence and feel.
- **https://fontsinuse.com** — archive of real-world professional
  typography. Reference for deliberate type pairing and hierarchy instead
  of default font-stack choices.

Keep new UI consistent with the site's existing design tokens rather than
introducing new one-off colors: see `--color-*`, `--radius-*`,
`--shadow-*`, `--transition-*` custom properties defined in
`static/css/main.css`. `static/css/auth.css`, `subscribe.css`, and
`account.css` show the established pattern (cards, consistent hover/focus
states, no gradients).

See `docs/deployment-notes.md` for infrastructure status and open
follow-ups (custom domain, persistent media storage, remaining QA items).

# News page maintenance

The site has a public changelog at `/news/`, backed by the `NewsPost`
model (`apps/resources/models.py`) and seeded via
`apps/resources/management/commands/seed_launch_news.py`'s `NEWS_ITEMS`
list. This is how the user (a non-technical site owner) tracks what
shipped and when, so it must stay current.

**Whenever a change ships to `main`** that a teacher/site-visitor would
notice or care about (a bug fix, a new feature, a UI change, new content),
add a corresponding entry to `NEWS_ITEMS` in the same commit:

- `published_date`: the date the change actually shipped (today's date,
  `'YYYY-MM-DD'` string, matching the existing entries' format).
- `title`: short, in Kyrgyz.
- `body`: 1-3 sentences, in Kyrgyz, written for a teacher/end-user (what
  changed and why it matters to them) — not a dev-facing commit-log
  description. Don't fabricate or oversell; describe only what's actually
  live.
- New entries go in the list (order doesn't matter — the page sorts by
  `published_date` descending). Follow the existing entries' tone/style.

Purely internal work a site visitor has no reason to know about (infra
config, refactors with no visible effect, deploy tooling) does not need a
news entry — use judgment.

Because `NEWS_ITEMS` is only a seed list, adding to it doesn't change the
live site by itself. After pushing, the new entry also needs to actually
be created in the production database: run
`python manage.py seed_launch_news` in production (see notes on running
management commands in production in `docs/deployment-notes.md`/session
history — the plain Railway "Shell" may not have the app's virtualenv
active; `source /opt/venv/bin/activate` first if `python` can't import
Django). It's idempotent, so re-running it is always safe.
