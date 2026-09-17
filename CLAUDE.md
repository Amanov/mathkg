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
