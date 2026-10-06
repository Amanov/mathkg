# Per-plan download limits, pricing comparison page, footer link

Status: approved by user, ready for implementation plan.

## Goal

Gate how many resources of each category (presentation / teacher-led
activity / worksheet) a user can download per day, based on their
subscription tier:

- **Free trial (7 days, new signups only):** 1 presentation + 1 activity +
  1 worksheet per day — a "taste" of the materials.
- **3-month plan:** same as trial — 1 of each per day.
- **6-month plan:** 5 of each per day.
- **1-year plan:** unlimited.

Once the 7-day trial (or a paid plan) expires, the user is blocked from
downloading anything until they pay — this is already the site's existing
behavior (`Account.has_active_subscription` gates `download_resource_view`);
shortening the trial window is what makes it bite after 7 days instead of
365.

Also: surface these limits on the pricing UI, add a dedicated plan
comparison page, and link it from the footer.

## Current state (relevant pieces)

- `Resource.category` (`apps/resources/models.py`) already has exactly
  three choices: `presentation`, `worksheet`, `activity`. Labels are
  currently English (`'Presentation'`, `'Worksheet'`, `'Activity'`) even
  though the rest of the site is Kyrgyz.
- `ResourceDownload` (`apps/resources/models.py`) already logs every
  download: `user`, `resource`, `downloaded_at` (auto-now-add). No new
  tracking table is needed — daily counts can be queried from this.
- `Account.subscription_end` (`apps/account/models.py`) is a nullable
  date. `Account.subscription_end_date` is a property: the explicit date
  if set, else `date_joined + timedelta(days=365)` (the free trial).
  `Account.has_active_subscription` compares that date to today.
- `Account` has **no field recording which plan tier** (3m/6m/1y) a user
  is on — only the resulting end date. This needs to be added.
- `SubscriptionRequest` (`apps/account/models.py`) defines
  `PLAN_THREE_MONTHS`/`PLAN_SIX_MONTHS`/`PLAN_ONE_YEAR`,
  `PLAN_CHOICES`, `PLAN_MONTHS`, `PLAN_PRICE_SOM` as class attributes.
  `.activate()` sets `subscription_end`/`is_active` on the user and marks
  itself confirmed. It's idempotent and is the single path (besides the
  `repair_subscriptions` management command) that grants paid access.
- `download_resource_view` (`apps/resources/views/downloads.py`) already
  blocks the download entirely and redirects to `account` with a Kyrgyz
  error message when `has_active_subscription` is false.
- `pricing_cards.html` (`templates/partials/`) is the single source of
  truth for the 3 plan cards, shared (via `{% include %}` with a `mode`
  param) by the subscribe modal and the homepage preview.
- `subscribe.js` advances the modal from the plan-picker to the QR step
  only for `.subscribe-plan-card` elements **inside** `#subscribeModal`;
  cards rendered in `mode='preview'` elsewhere just open the modal fresh
  (`data-bs-toggle="modal"`) without pre-selecting a plan. This is
  existing, unchanged behavior the new pricing page will reuse as-is.
- `repair_subscriptions` management command already replays each
  account's confirmed `SubscriptionRequest` history to recompute
  `subscription_end`, dry-run by default, `--apply` to write. This is the
  natural place to also backfill the new plan-tracking field.
- Only two cross-app import directions exist today, both at the
  views/management-command layer (never model-to-model at module level):
  `apps/account/views.py` imports from `apps.resources.models`, and
  `apps/resources/tests.py` imports from `apps.account`. The new
  `Account.downloads_remaining_today()` method will do a local
  (function-body) import of `ResourceDownload` to stay consistent with
  that safe pattern and avoid any model-load-order risk.

## Data model changes

### `apps/account/models.py`

1. **Hoist plan constants to module level**, before `class Account`:
   ```python
   PLAN_THREE_MONTHS = '3m'
   PLAN_SIX_MONTHS = '6m'
   PLAN_ONE_YEAR = '1y'
   PLAN_CHOICES = [
       (PLAN_THREE_MONTHS, '3 ай - 1499 сом'),
       (PLAN_SIX_MONTHS, '6 ай - 2999 сом'),
       (PLAN_ONE_YEAR, '1 жыл - 4999 сом'),
   ]
   PLAN_MONTHS = {PLAN_THREE_MONTHS: 3, PLAN_SIX_MONTHS: 6, PLAN_ONE_YEAR: 12}
   PLAN_PRICE_SOM = {PLAN_THREE_MONTHS: 1499, PLAN_SIX_MONTHS: 2999, PLAN_ONE_YEAR: 4999}

   DAILY_DOWNLOAD_LIMITS = {
       None: {'presentation': 1, 'worksheet': 1, 'activity': 1},  # trial
       PLAN_THREE_MONTHS: {'presentation': 1, 'worksheet': 1, 'activity': 1},
       PLAN_SIX_MONTHS: {'presentation': 5, 'worksheet': 5, 'activity': 5},
       PLAN_ONE_YEAR: None,  # unlimited
   }
   ```
   `SubscriptionRequest` keeps its own `PLAN_THREE_MONTHS = PLAN_THREE_MONTHS`
   etc. class-attribute aliases pointing at the module constants, so every
   existing external reference (`SubscriptionRequest.PLAN_CHOICES`,
   `SubscriptionRequest.PLAN_MONTHS[...]` in `repair_subscriptions.py` and
   `apps/account/views.py`) keeps working unchanged.

2. **New fields on `Account`:**
   ```python
   current_plan = models.CharField(
       max_length=2, choices=PLAN_CHOICES, null=True, blank=True,
       help_text="Акыркы ырасталган төлөм планы. Акы төлөнбөгөн "
                  "аккаунттар үчүн бош (сыноо мөөнөтү).",
   )
   trial_days = models.PositiveIntegerField(
       default=7,
       help_text="Акысыз сыноо мөөнөтү (күн). Жаңы аккаунттар үчүн "
                  "демейки мааниси колдонулат; бул талаа кол менен "
                  "өзгөртүлбөсө, катталган күндөн тартып эсептелет.",
   )
   ```

3. **`subscription_end_date` property** changes its fallback from the
   hardcoded `timedelta(days=365)` to `timedelta(days=self.trial_days)`.

4. **New methods on `Account`:**
   ```python
   def daily_download_limit(self, category):
       """Per-day cap for this category under the account's current
       plan, or None for unlimited."""
       limits = DAILY_DOWNLOAD_LIMITS.get(self.current_plan, DAILY_DOWNLOAD_LIMITS[None])
       return limits[category] if limits else None

   def downloads_remaining_today(self, category):
       """None means unlimited. Otherwise the limit minus today's
       ResourceDownload count for this user+category."""
       limit = self.daily_download_limit(category)
       if limit is None:
           return None
       from apps.resources.models import ResourceDownload  # local: avoid
                                                             # cross-app
                                                             # model-level
                                                             # import
       used = ResourceDownload.objects.filter(
           user=self, resource__category=category,
           downloaded_at__date=timezone.now().date(),
       ).count()
       return max(0, limit - used)
   ```

5. **`SubscriptionRequest.activate()`** additionally sets
   `self.user.current_plan = self.plan` and includes it in the
   `update_fields` list alongside `subscription_end`/`is_active`.

### `apps/resources/models.py`

`Resource.CATEGORY_CHOICES` labels localized to Kyrgyz:
```python
CATEGORY_CHOICES = [
    ('presentation', 'Презентация'),
    ('worksheet', 'Иш барак'),
    ('activity', 'Мугалим жетектеген ишмердик'),
]
```
Codes (`'presentation'`/`'worksheet'`/`'activity'`) are unchanged — only
display labels change, so this is a no-op at the data level. Needed so
the new download-limit error message (which names the category) and the
existing `search_results.html` Материалдар section (which already calls
`resource.get_category_display`) both read in Kyrgyz instead of English.

## Enforcement: `download_resource_view`

In `apps/resources/views/downloads.py`, immediately after the existing
`has_active_subscription` check and before creating the
`ResourceDownload` row:

```python
remaining = request.user.downloads_remaining_today(resource.category)
if remaining is not None and remaining <= 0:
    messages.error(
        request,
        f"Бүгүнкү «{resource.get_category_display()}» жүктөп алуу "
        "чегине жеттиңиз. Эртең кайра аракет кылыңыз же планыңызды "
        "жаңыртыңыз."
    )
    return redirect('account')
```

Same shape as the existing inactive-subscription block right above it,
including the plain `redirect('account')` (no referer logic) — reads as
one family of access checks, not a bolted-on special case.

## UI changes

### `templates/partials/pricing_cards.html`

Add a small feature list to each plan card (new `<ul class="subscribe-plan-limits">`
under the existing name/price/note spans):
- 3 ай: "Күнүнө: 1 презентация, 1 ишмердик, 1 иш барак"
- 6 ай: "Күнүнө: 5 презентация, 5 ишмердик, 5 иш барак"
- 1 жыл: "Чексиз жүктөп алуу"

This is the single shared partial for both the subscribe modal and the
homepage preview, so one edit updates both.

New CSS in `static/css/subscribe.css` for `.subscribe-plan-limits` (small
muted list, consistent with the card's existing typography scale — no new
colors, reuse `--text-muted`/existing spacing tokens).

### New page: `/pricing/`

- `pricing_view` added to `apps/resources/views/pages.py` (next to
  `about_view`/`topics_tree_view` — same "simple static-ish page" family),
  exported from `apps/resources/views/__init__.py` alongside the other
  `pages` imports, and registered in `config/urls.py` as
  `path('pricing/', pricing_view, name='pricing')` (same import-list +
  path-list pattern already used for `search_suggest_view`).
- Template `templates/resources/pricing.html`, extends `base/base.html`.
  Content:
  1. A comparison table — rows: Баасы, Узактыгы, Презентация (күнүнө),
     Мугалим жетектеген ишмердик (күнүнө), Иш барак (күнүнө); columns:
     the 3 plans. "Чексиз" (unlimited) in the 1-year column's download
     rows.
  2. Below the table, `{% include 'partials/pricing_cards.html' with mode='preview' %}` —
     reuses the existing, already-wired pick-a-plan action instead of
     inventing new interaction code.
- New `static/css/pricing.css` for the comparison table, built from
  existing tokens (`--surface`, `--border-subtle`, `--color-navy`,
  `--radius-md`, etc.) — no new one-off colors, no gradients, per
  CLAUDE.md's design guidance. Responsive: table scrolls horizontally
  under the mobile breakpoint rather than squeezing columns unreadably
  thin (same pattern already used for wide tables elsewhere, if any
  precedent exists — otherwise a simple `overflow-x: auto` wrapper).

### Footer

`templates/snippets/footer.html`: add a "Баалар" item to the existing
Навигация `<ul class="footer-links">`, linking to `{% url 'pricing' %}`.
Placed first in that list (pricing is a primary nav concern, same
priority tier as "Сайттагы жаңылыктар").

## Migrations

Three migrations, in order:

1. **`apps/account/migrations/0011_...`** — adds `current_plan` and
   `trial_days` fields to `Account` (schema only, `trial_days` defaults
   to `7` for the column).
2. **`apps/account/migrations/0012_...`** (data migration) — sets
   `trial_days=365` on every `Account` row that exists at migration-run
   time (`Account.objects.update(trial_days=365)` inside a
   `RunPython`), so every account that already exists before this ships
   keeps its originally-granted 1-year trial window. Any account created
   *after* this migration runs gets the model's new default of `7`
   automatically — no cutover-date constant needed anywhere.
3. **`apps/resources/migrations/0023_...`** — label-only change for
   `Resource.category`'s choices (Kyrgyz labels). No data change.

## Backfill: `current_plan` for already-paying accounts

Extend the existing `repair_subscriptions` management command (which
already replays each account's confirmed `SubscriptionRequest` history
in order to recompute `subscription_end`) to also compare/set
`current_plan` to the **last** confirmed request's `plan` in that same
replayed chain, using the same dry-run-by-default / `--apply` convention
and the same per-account change log line. Without this, an account that
paid for a year *before* this feature shipped would read as
`current_plan=None` (trial-tier limit) until their next renewal —
wrongly restrictive for someone who already paid.

Run in production after deploying, per the project's established
"migrate then run the data-repair command" workflow
(`docs/deployment-notes.md`): `python manage.py migrate` then
`python manage.py repair_subscriptions --apply`.

## Testing

- `Account.downloads_remaining_today`: trial / 3m / 6m / 1y, at/under/over
  the limit, and that categories are tracked independently (maxing out
  presentations doesn't affect the worksheet count).
- `Account.subscription_end_date` / `has_active_subscription`: respects
  `trial_days` (not a hardcoded 365), and an explicit `subscription_end`
  still wins over the trial fallback.
- `download_resource_view`: a 3-month-plan user's 2nd same-day
  presentation download is blocked (redirect + error message) while a
  worksheet download the same day still succeeds; a 1-year-plan user's
  6th same-day presentation still succeeds (unlimited).
- `repair_subscriptions --apply`: backfills `current_plan` correctly
  from a multi-request confirmed history (last one wins).
- `pricing_view`: 200, renders all 3 plan names/prices/limits.
- Full existing test suite + `manage.py check` stay green.
- Visual (Playwright, light + dark mode, desktop + mobile): pricing cards
  with the new limit bullets, the new `/pricing/` comparison table, and
  the footer's new link.

## Rollout

Same established workflow as every other change this session: implement
and test on `claude/funny-goldberg-77684z`, add the Kyrgyz
`seed_launch_news` entry, cherry-pick to `main` (resolving the standard
`seed_launch_news.py` date-format conflict), push. After the next
production deploy: run `python manage.py migrate` then
`python manage.py repair_subscriptions --apply`.

## Explicitly out of scope (YAGNI for this change)

- No live "N of 5 remaining today" indicator on resource listing pages —
  only enforced + messaged at the moment of download. Can be added later
  if wanted.
- No admin-UI changes beyond what the new fields need by default (no new
  custom admin actions/filters for `current_plan`/`trial_days`).
- No change to how `SubscriptionRequest.activate()` stacks renewal
  periods — unrelated to this feature, already correct.
- No per-resource or per-topic override of the category limits — the
  three categories and their per-plan numbers are global.
