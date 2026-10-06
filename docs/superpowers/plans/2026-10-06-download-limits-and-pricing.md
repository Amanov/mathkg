# Download Limits & Pricing Comparison Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gate daily downloads per resource category by subscription tier (trial/3mo: 1 each, 6mo: 5 each, 1yr: unlimited), shorten the free trial to 7 days for new signups without affecting existing accounts, and add a pricing comparison page linked from the footer.

**Architecture:** All tier/limit logic lives as module-level constants and `Account` methods in `apps/account/models.py`, queried against the already-existing `ResourceDownload` log (no new tracking table). `download_resource_view` gains one more access check, in the same shape as its existing subscription-expiry check. A new `/pricing/` page and a small addition to the existing shared `pricing_cards.html` partial surface the limits in the UI.

**Tech Stack:** Django 4.2, Django TestCase, Bootstrap 5 templates, project CSS design tokens (no new framework).

**Spec:** `docs/superpowers/specs/2026-10-06-download-limits-and-pricing-design.md`

## Global Constraints

- Every user-facing string is Kyrgyz (site-wide convention; see CLAUDE.md).
- No new one-off CSS colors or gradients — reuse existing tokens (`--surface`, `--surface-alt`, `--border-subtle`, `--color-navy`, `--color-bootstrap-primary`, `--text-muted`, `--radius-sm`, `--radius-md`, `--transition-fast`).
- Exact values from the spec: trial = 7 days for new accounts, 365 days (grandfathered) for accounts existing before this ships; `DAILY_DOWNLOAD_LIMITS` = trial and 3-month → `{presentation: 1, worksheet: 1, activity: 1}`, 6-month → `{presentation: 5, worksheet: 5, activity: 5}`, 1-year → unlimited (`None`).
- `SubscriptionRequest.PLAN_CHOICES`, `.PLAN_MONTHS`, `.PLAN_PRICE_SOM`, `.PLAN_THREE_MONTHS`, `.PLAN_SIX_MONTHS`, `.PLAN_ONE_YEAR` must keep working exactly as before (other modules reference them as class attributes) even after the constants move to module level.
- `repair_subscriptions` keeps its existing dry-run-by-default / `--apply` convention; its output format (`"{verb} {fixed} of {checked} account(s)..."`) is unchanged, just extended with another kind of fix.
- Any code that needs both `Account` (app `account`) and `ResourceDownload` (app `resources`) in the same function must import the one it doesn't already have access to *inside that function body*, not at module level — there is no existing precedent in this codebase for a model-to-module-level cross-app import in either direction, and this plan should not become the first one.

## Review Focus

- A user who has never had a confirmed `SubscriptionRequest` (`current_plan` is `None`, pure trial) hitting the daily limit must get the trial-tier numbers (1/1/1), not a `KeyError` from a limits dict that only has plan codes as keys.
- A user whose access has actually expired (`has_active_subscription` is `False`) must be stopped by the *existing* expiry check before the new limit check ever runs, and must see the expiry message, not a "limit reached" message.
- The daily count must reset on a new calendar day — a download logged yesterday must not count against today's limit — and the boundary must be exact: the Nth allowed download today succeeds, the (N+1)th is blocked.
- `repair_subscriptions --apply`, run a second time right after a successful run, must report zero further fixes — the new `current_plan` backfill must not break the command's existing idempotency.
- Maxing out one category's daily limit (e.g. presentations) must not reduce what's left in another category (worksheets, activities) for the same user on the same day.

---

### Task 1: `Account` plan tier, trial length, and daily-limit lookup

**Files:**
- Modify: `apps/account/models.py:1-14` (imports), `:46-214` (constants hoist, new fields, property, new methods), `:270-271` (`activate()`)
- Create: `apps/account/migrations/0011_account_current_plan_trial_days.py`
- Test: `apps/account/tests.py`

**Interfaces:**
- Produces (module level, `apps/account/models.py`): `PLAN_THREE_MONTHS`, `PLAN_SIX_MONTHS`, `PLAN_ONE_YEAR` (str constants `'3m'`/`'6m'`/`'1y'`), `PLAN_CHOICES`, `PLAN_MONTHS`, `PLAN_PRICE_SOM` (same shapes as today, just hoisted), `DAILY_DOWNLOAD_LIMITS: dict[str | None, dict[str, int] | None]`.
- Produces (on `Account`): `current_plan` field (nullable `CharField`, values from `PLAN_CHOICES` or `None`), `trial_days` field (`PositiveIntegerField`, default `7`), `daily_download_limit(self, category: str) -> int | None`, `downloads_remaining_today(self, category: str) -> int | None` (`None` = unlimited).
- Consumes: `apps.resources.models.ResourceDownload` (imported inside `downloads_remaining_today`'s body only — see Global Constraints).

- [ ] **Step 1: Write the failing tests**

Add to `apps/account/tests.py` (extend the imports at the top: add `SubscriptionRequest` to the existing `from .models import Account, School` line; add `from datetime import timedelta`; add `from django.utils import timezone`; add `import tempfile`; add `from django.core.files.uploadedfile import SimpleUploadedFile`; add `from django.test import override_settings`; add `from apps.resources.models import Resource, ResourceDownload`):

```python
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DownloadLimitTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='limits@example.com', username='limitsuser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

    def _make_resource(self, category, title='R'):
        return Resource.objects.create(
            title=title, category=category, is_active=True,
            file=SimpleUploadedFile(f'{title}.txt', b'data'),
        )

    def test_trial_user_has_3month_tier_limits(self):
        self.assertEqual(self.user.daily_download_limit('presentation'), 1)
        self.assertEqual(self.user.daily_download_limit('worksheet'), 1)
        self.assertEqual(self.user.daily_download_limit('activity'), 1)

    def test_three_month_plan_has_same_limits_as_trial(self):
        self.user.current_plan = SubscriptionRequest.PLAN_THREE_MONTHS
        self.assertEqual(self.user.daily_download_limit('presentation'), 1)

    def test_six_month_plan_allows_five_per_category(self):
        self.user.current_plan = SubscriptionRequest.PLAN_SIX_MONTHS
        self.assertEqual(self.user.daily_download_limit('presentation'), 5)
        self.assertEqual(self.user.daily_download_limit('worksheet'), 5)
        self.assertEqual(self.user.daily_download_limit('activity'), 5)

    def test_one_year_plan_is_unlimited(self):
        self.user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        self.assertIsNone(self.user.daily_download_limit('presentation'))
        self.assertIsNone(self.user.downloads_remaining_today('presentation'))

    def test_downloads_remaining_today_counts_todays_downloads(self):
        resource = self._make_resource('worksheet')
        ResourceDownload.objects.create(resource=resource, user=self.user)
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 0)

    def test_categories_are_tracked_independently(self):
        presentation = self._make_resource('presentation', 'P')
        ResourceDownload.objects.create(resource=presentation, user=self.user)
        self.assertEqual(self.user.downloads_remaining_today('presentation'), 0)
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 1)

    def test_yesterdays_download_does_not_count_against_todays_limit(self):
        resource = self._make_resource('worksheet')
        download = ResourceDownload.objects.create(resource=resource, user=self.user)
        ResourceDownload.objects.filter(pk=download.pk).update(
            downloaded_at=timezone.now() - timedelta(days=1)
        )
        self.assertEqual(self.user.downloads_remaining_today('worksheet'), 1)

    def test_trial_days_defaults_to_seven_for_new_accounts(self):
        self.assertEqual(self.user.trial_days, 7)

    def test_subscription_end_date_uses_trial_days(self):
        self.user.trial_days = 30
        expected = self.user.date_joined.date() + timedelta(days=30)
        self.assertEqual(self.user.subscription_end_date, expected)

    def test_explicit_subscription_end_overrides_trial(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.assertEqual(self.user.subscription_end_date, self.user.subscription_end)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python manage.py test apps.account.tests.DownloadLimitTests -v 2`
Expected: FAIL / ERROR — `current_plan`, `trial_days`, `daily_download_limit`, `downloads_remaining_today` don't exist yet.

- [ ] **Step 3: Hoist the plan constants to module level**

In `apps/account/models.py`, move what is currently `SubscriptionRequest`'s class-body block (today at lines 200-214: `PLAN_THREE_MONTHS`/`PLAN_SIX_MONTHS`/`PLAN_ONE_YEAR`/`PLAN_CHOICES`/`PLAN_MONTHS`/`PLAN_PRICE_SOM`, with their existing comment) to module level, placed after the imports and before `class Account(AbstractBaseUser):`. Keep the exact same names, values, and the existing comment. Immediately after `PLAN_PRICE_SOM`, add:

```python
DAILY_DOWNLOAD_LIMITS = {
    None: {'presentation': 1, 'worksheet': 1, 'activity': 1},  # trial
    PLAN_THREE_MONTHS: {'presentation': 1, 'worksheet': 1, 'activity': 1},
    PLAN_SIX_MONTHS: {'presentation': 5, 'worksheet': 5, 'activity': 5},
    PLAN_ONE_YEAR: None,  # unlimited
}
```

Then, where `SubscriptionRequest`'s class body used to define these, replace with aliases so every existing `SubscriptionRequest.PLAN_*` reference elsewhere in the codebase (`repair_subscriptions.py`, `apps/account/views.py`) keeps working unchanged:

```python
class SubscriptionRequest(models.Model):
    PLAN_THREE_MONTHS = PLAN_THREE_MONTHS
    PLAN_SIX_MONTHS = PLAN_SIX_MONTHS
    PLAN_ONE_YEAR = PLAN_ONE_YEAR
    PLAN_CHOICES = PLAN_CHOICES
    PLAN_MONTHS = PLAN_MONTHS
    PLAN_PRICE_SOM = PLAN_PRICE_SOM
    ...
```

- [ ] **Step 4: Add the two new `Account` fields**

Immediately after the existing `subscription_end = models.DateField(null=True, blank=True)` field:

```python
    current_plan = models.CharField(
        max_length=2, choices=PLAN_CHOICES, null=True, blank=True,
        help_text="Акыркы ырасталган төлөм планы. Акы төлөнбөгөн "
                   "аккаунттар үчүн бош (сыноо мөөнөтү).",
    )
    trial_days = models.PositiveIntegerField(
        default=7,
        help_text="Акысыз сыноо мөөнөтү (күн). Катталган күндөн тартып "
                   "эсептелет (subscription_end коюлбаса).",
    )
```

- [ ] **Step 5: Update `subscription_end_date` to use `trial_days`**

Change the fallback from `timedelta(days=365)` to `timedelta(days=self.trial_days)`. Keep the rest of the property (and its docstring/comment, updated to say "the account's own trial length" instead of "1 year") unchanged.

- [ ] **Step 6: Add `daily_download_limit` and `downloads_remaining_today` to `Account`**

Place them directly after the existing `has_active_subscription` property:

```python
    def daily_download_limit(self, category):
        limits = DAILY_DOWNLOAD_LIMITS.get(self.current_plan, DAILY_DOWNLOAD_LIMITS[None])
        return limits[category] if limits else None

    def downloads_remaining_today(self, category):
        limit = self.daily_download_limit(category)
        if limit is None:
            return None
        from apps.resources.models import ResourceDownload
        used = ResourceDownload.objects.filter(
            user=self, resource__category=category,
            downloaded_at__date=timezone.now().date(),
        ).count()
        return max(0, limit - used)
```

- [ ] **Step 7: Make `activate()` set `current_plan`**

In `SubscriptionRequest.activate()`, change the final `self.user.save(update_fields=['subscription_end', 'is_active'])` to also set and save `current_plan`:

```python
        self.user.current_plan = self.plan
        self.user.save(update_fields=['subscription_end', 'is_active', 'current_plan'])
```
(Set `current_plan` on the line before this save call, same place `subscription_end`/`is_active` are already being set a few lines above.)

- [ ] **Step 8: Generate and inspect the migration**

Run: `python manage.py makemigrations account`
Expected: creates `apps/account/migrations/0011_account_current_plan_trial_days.py` (or similar auto-generated name — rename the file to that if Django picks a generic name) adding both fields. Confirm it has no `RunPython` — schema only.

- [ ] **Step 9: Run tests to verify they pass**

Run: `python manage.py test apps.account.tests.DownloadLimitTests -v 2`
Expected: PASS (all cases from Step 1).

- [ ] **Step 10: Run the full account test suite to check nothing else broke**

Run: `python manage.py test apps.account -v 2`
Expected: PASS (existing `RegistrationAndActivationTests`, `LoginTests`, etc. all still pass — confirms the `PLAN_*` alias hoist didn't break anything).

- [ ] **Step 11: Commit**

```bash
git add apps/account/models.py apps/account/migrations/0011_*.py apps/account/tests.py
git commit -m "Add Account.current_plan/trial_days and per-category daily download limits"
```

---

### Task 2: Grandfather existing accounts' trial length

**Files:**
- Create: `apps/account/migrations/0012_backfill_trial_days.py`

**Interfaces:**
- Consumes: `Account.trial_days` (from Task 1).
- Produces: every `Account` row that exists at the moment this migration runs ends up with `trial_days=365`; any row created afterward keeps the model's default of `7` (nothing to produce for later tasks — this is a one-time data fix, not an API).

This step is a plain one-time `UPDATE` with no conditional logic, and — because Django's test runner applies every migration once before any test touches the database — there is no "before" state left to assert against in a normal `TestCase` (the backfill runs during test-DB setup, before any row exists, so it always affects zero rows in tests). Correctness here rests on the migration being this exact, obviously-correct one-liner, not on a test; the full test suite passing (Step 3 below) proves the migration at least runs cleanly as part of the normal migration chain.

- [ ] **Step 1: Write the data migration**

```bash
python manage.py makemigrations account --empty --name backfill_trial_days
```

Edit the generated file to:

```python
from django.db import migrations


def backfill_trial_days(apps, schema_editor):
    Account = apps.get_model('account', 'Account')
    Account.objects.update(trial_days=365)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_account_current_plan_trial_days'),  # exact name from Task 1, Step 8
    ]

    operations = [
        migrations.RunPython(backfill_trial_days, migrations.RunPython.noop),
    ]
```

- [ ] **Step 2: Run the migration**

Run: `python manage.py migrate account`
Expected: `Applying account.0012_backfill_trial_days... OK`

- [ ] **Step 3: Run the full test suite**

Run: `python manage.py test`
Expected: PASS — confirms the migration chain (0001 through 0012) applies cleanly when Django builds the test database.

- [ ] **Step 4: Commit**

```bash
git add apps/account/migrations/0012_backfill_trial_days.py
git commit -m "Grandfather existing accounts to the old 365-day trial window"
```

---

### Task 3: Backfill `current_plan` for already-paying accounts

**Files:**
- Modify: `apps/account/management/commands/repair_subscriptions.py:7-96`
- Test: `apps/account/tests.py`

**Interfaces:**
- Consumes: `Account.current_plan` (Task 1), `SubscriptionRequest.PLAN_*` (Task 1, unchanged aliases).
- Produces: nothing new consumed downstream — this is the production backfill tool, run once after deploy per the spec's Rollout section (outside this plan).

- [ ] **Step 1: Write the failing tests**

Add to `apps/account/tests.py` (add `from io import StringIO` and `from django.core.management import call_command` to the imports):

```python
class RepairSubscriptionsBackfillsCurrentPlanTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='backfill@example.com', username='backfilluser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        # .activate() is what realistically sets subscription_end/is_active
        # (and, after Task 1, current_plan) from a confirmed request. Null
        # current_plan back out afterward to simulate a payment that was
        # confirmed *before* current_plan existed as a field - exactly the
        # account repair_subscriptions needs to backfill.
        self.request = SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_ONE_YEAR,
            status=SubscriptionRequest.STATUS_PENDING,
        )
        self.request.activate()
        self.user.current_plan = None
        self.user.save(update_fields=['current_plan'])

    def test_dry_run_does_not_write(self):
        call_command('repair_subscriptions', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertIsNone(self.user.current_plan)

    def test_apply_backfills_current_plan_from_last_confirmed_request(self):
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_ONE_YEAR)

    def test_apply_uses_the_latest_of_multiple_confirmed_requests(self):
        SubscriptionRequest.objects.create(
            user=self.user, plan=SubscriptionRequest.PLAN_THREE_MONTHS,
            status=SubscriptionRequest.STATUS_CONFIRMED,
            activated_at=timezone.now(),
        )
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        self.user.refresh_from_db()
        self.assertEqual(self.user.current_plan, SubscriptionRequest.PLAN_THREE_MONTHS)

    def test_rerunning_apply_is_idempotent(self):
        call_command('repair_subscriptions', '--apply', stdout=StringIO())
        second_run_output = StringIO()
        call_command('repair_subscriptions', '--apply', stdout=second_run_output)
        self.assertIn('Fixed 0 of', second_run_output.getvalue())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python manage.py test apps.account.tests.RepairSubscriptionsBackfillsCurrentPlanTests -v 2`
Expected: FAIL on `test_apply_backfills_current_plan_from_last_confirmed_request` and `test_apply_uses_the_latest_of_multiple_confirmed_requests` (current_plan stays `None` after `--apply`, since the command doesn't touch it yet). `test_rerunning_apply_is_idempotent` passes vacuously today — fine, it's pinned so it can't regress once Step 3 lands.

- [ ] **Step 3: Extend the command to also backfill `current_plan`**

In `apps/account/management/commands/repair_subscriptions.py`, inside the per-account loop (after the existing `simulated_end` computation, before `actual_end = account.subscription_end`):

```python
            simulated_plan = confirmed[-1].plan if confirmed else None
```

Change the "needs fix" check from:
```python
            needs_date_fix = actual_end != simulated_end
            needs_activation = not account.is_active

            if not needs_date_fix and not needs_activation:
                continue
```
to also check the plan (this is the exact scenario the tests exercise: date and activation already correct, only `current_plan` is stale):
```python
            needs_date_fix = actual_end != simulated_end
            needs_activation = not account.is_active
            needs_plan_fix = account.current_plan != simulated_plan

            if not needs_date_fix and not needs_activation and not needs_plan_fix:
                continue
```

Add to the `changes` log list, alongside the existing two `changes.append(...)` calls:
```python
            if needs_plan_fix:
                changes.append(f"current_plan {account.current_plan} -> {simulated_plan}")
```

In the `if apply_fix:` block, set the field and extend `update_fields`:
```python
                account.current_plan = simulated_plan
                account.save(update_fields=['subscription_end', 'is_active', 'current_plan'])
```

Update the command's `help` string to mention this (append a sentence noting it also backfills `current_plan` from the last confirmed request, for accounts that paid before that field existed).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python manage.py test apps.account.tests.RepairSubscriptionsBackfillsCurrentPlanTests -v 2`
Expected: PASS.

- [ ] **Step 5: Run the full account test suite**

Run: `python manage.py test apps.account -v 2`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/account/management/commands/repair_subscriptions.py apps/account/tests.py
git commit -m "Backfill current_plan in repair_subscriptions for pre-existing paid accounts"
```

---

### Task 4: Localize `Resource.CATEGORY_CHOICES` to Kyrgyz

**Files:**
- Modify: `apps/resources/models.py:124-128`
- Create: `apps/resources/migrations/0023_alter_resource_category_choices.py`
- Test: `apps/resources/tests.py`

**Interfaces:**
- Produces: `Resource(category='presentation').get_category_display() == 'Презентация'`, `'worksheet' -> 'Иш барак'`, `'activity' -> 'Мугалим жетектеген ишмердик'`. Stored codes (`'presentation'`/`'worksheet'`/`'activity'`) are unchanged — Task 5's enforcement code and Task 1's `DAILY_DOWNLOAD_LIMITS` keys keep using these same codes.

- [ ] **Step 1: Write the failing test**

Add to `apps/resources/tests.py` (add `from .models import Resource` to the existing `from .models import Exam, ExamQuestion, NewsPost, Question` import line):

```python
class ResourceCategoryLabelTests(TestCase):
    def test_category_labels_are_kyrgyz(self):
        self.assertEqual(Resource(category='presentation').get_category_display(), 'Презентация')
        self.assertEqual(Resource(category='worksheet').get_category_display(), 'Иш барак')
        self.assertEqual(Resource(category='activity').get_category_display(), 'Мугалим жетектеген ишмердик')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python manage.py test apps.resources.tests.ResourceCategoryLabelTests -v 2`
Expected: FAIL — current labels are `'Presentation'`/`'Worksheet'`/`'Activity'`.

- [ ] **Step 3: Change `CATEGORY_CHOICES`**

```python
    CATEGORY_CHOICES = [
        ('presentation', 'Презентация'),
        ('worksheet', 'Иш барак'),
        ('activity', 'Мугалим жетектеген ишмердик'),
    ]
```

- [ ] **Step 4: Generate the migration**

Run: `python manage.py makemigrations resources`
Expected: creates a label-only `AlterField` migration for `Resource.category` (next number after `0022_merge_...`, i.e. `0023_...`). No data change.

- [ ] **Step 5: Run test to verify it passes**

Run: `python manage.py test apps.resources.tests.ResourceCategoryLabelTests -v 2`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/resources/models.py apps/resources/migrations/0023_*.py apps/resources/tests.py
git commit -m "Localize Resource category labels to Kyrgyz"
```

---

### Task 5: Enforce the daily download limit

**Files:**
- Modify: `apps/resources/views/downloads.py` (full file, 57 lines)
- Test: `apps/resources/tests.py`

**Interfaces:**
- Consumes: `request.user.downloads_remaining_today(category)` (Task 1), `resource.get_category_display()` (Task 4).
- Produces: nothing downstream consumes this directly; it's the enforcement point itself.

- [ ] **Step 1: Write the failing tests**

Add to `apps/resources/tests.py` (add `import tempfile`; `from django.test import override_settings`; `from django.core.files.uploadedfile import SimpleUploadedFile`; `from apps.account.models import SubscriptionRequest` alongside the existing `from apps.account.models import Account`; `from .models import ResourceDownload` alongside the existing model imports):

```python
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DownloadLimitEnforcementTests(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            email='dl@example.com', username='dluser', password='SuperSecret123!'
        )
        self.user.is_active = True
        self.user.current_plan = SubscriptionRequest.PLAN_THREE_MONTHS
        self.user.save(update_fields=['is_active', 'current_plan'])
        self.client.login(email='dl@example.com', password='SuperSecret123!')

    def _make_resource(self, category, title='R'):
        return Resource.objects.create(
            title=title, category=category, is_active=True,
            file=SimpleUploadedFile(f'{title}.txt', b'data'),
        )

    def test_second_same_day_download_in_same_category_is_blocked(self):
        first = self._make_resource('presentation', 'First')
        second = self._make_resource('presentation', 'Second')
        self.client.get(reverse('download_resource', args=[first.pk]))
        resp = self.client.get(reverse('download_resource', args=[second.pk]), follow=True)
        self.assertContains(resp, 'чегине жеттиңиз')
        self.assertEqual(ResourceDownload.objects.filter(resource=second).count(), 0)

    def test_different_category_is_unaffected_by_other_categorys_limit(self):
        presentation = self._make_resource('presentation', 'P')
        worksheet = self._make_resource('worksheet', 'W')
        self.client.get(reverse('download_resource', args=[presentation.pk]))
        resp = self.client.get(reverse('download_resource', args=[worksheet.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_one_year_plan_has_no_limit(self):
        self.user.current_plan = SubscriptionRequest.PLAN_ONE_YEAR
        self.user.save(update_fields=['current_plan'])
        for i in range(6):
            r = self._make_resource('presentation', f'P{i}')
            resp = self.client.get(reverse('download_resource', args=[r.pk]))
            self.assertEqual(resp.status_code, 200)

    def test_expired_subscription_blocks_before_the_limit_check_runs(self):
        self.user.subscription_end = timezone.now().date() - timedelta(days=1)
        self.user.save(update_fields=['subscription_end'])
        resource = self._make_resource('presentation', 'P')
        resp = self.client.get(reverse('download_resource', args=[resource.pk]), follow=True)
        self.assertContains(resp, 'мөөнөтү бүткөн')
        self.assertNotContains(resp, 'чегине жеттиңиз')
```

This last test needs `timezone` and `timedelta` imported in `apps/resources/tests.py` too — add `from datetime import date, timedelta` (extending the existing `from datetime import date` line) and `from django.utils import timezone`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python manage.py test apps.resources.tests.DownloadLimitEnforcementTests -v 2`
Expected: FAIL on `test_second_same_day_download_in_same_category_is_blocked` and `test_one_year_plan_has_no_limit`'s later iterations (no limit is enforced yet, so the "blocked" test's second download wrongly succeeds — actually check: without enforcement, the "blocked" test will fail because the second download is NOT blocked). `test_expired_subscription_blocks_before_the_limit_check_runs` already passes today (the expiry check already exists) — fine, it's pinned here so Step 3 can't accidentally reorder the two checks.

- [ ] **Step 3: Add the enforcement check**

In `download_resource_view`, between fetching `resource` and creating the `ResourceDownload` row:

```python
    resource = get_object_or_404(
        Resource,
        pk=pk,
        is_active=True
    )

    remaining = request.user.downloads_remaining_today(resource.category)
    if remaining is not None and remaining <= 0:
        messages.error(
            request,
            f"Бүгүнкү «{resource.get_category_display()}» жүктөп алуу "
            "чегине жеттиңиз. Эртең кайра аракет кылыңыз же планыңызды "
            "жаңыртыңыз."
        )
        return redirect('account')

    ResourceDownload.objects.create(
        ...
```
(leave the existing `ResourceDownload.objects.create(...)` call and everything after it unchanged — only the new block above is inserted).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python manage.py test apps.resources.tests.DownloadLimitEnforcementTests -v 2`
Expected: PASS.

- [ ] **Step 5: Run the full resources test suite**

Run: `python manage.py test apps.resources -v 2`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add apps/resources/views/downloads.py apps/resources/tests.py
git commit -m "Enforce per-category daily download limits in download_resource_view"
```

---

### Task 6: Surface the limits on the existing plan cards

**Files:**
- Modify: `templates/partials/pricing_cards.html` (full file, 42 lines)
- Modify: `static/css/subscribe.css`
- Test: `apps/resources/tests.py`

**Interfaces:**
- Consumes: nothing from earlier tasks (static Kyrgyz copy — the numbers are the same ones in `DAILY_DOWNLOAD_LIMITS`, written here as plain text, same way the card's price is already hardcoded text rather than pulled from `PLAN_PRICE_SOM`).
- Produces: nothing consumed downstream.

- [ ] **Step 1: Write the failing test**

Add to the `PagesTests` class in `apps/resources/tests.py`:

```python
    def test_homepage_shows_plan_download_limits(self):
        resp = self.client.get(reverse('home'))
        self.assertContains(resp, 'Күнүнө: 1 презентация, 1 ишмердик, 1 иш барак')
        self.assertContains(resp, 'Күнүнө: 5 презентация, 5 ишмердик, 5 иш барак')
        self.assertContains(resp, 'Чексиз жүктөп алуу')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python manage.py test apps.resources.tests.PagesTests.test_homepage_shows_plan_download_limits -v 2`
Expected: FAIL — the strings aren't in the page yet.

- [ ] **Step 3: Add the limits line to each card**

In `templates/partials/pricing_cards.html`, inside each of the 3 `<button class="subscribe-plan-card...">` elements, add a `<p class="subscribe-plan-limits">` between the existing `<span class="subscribe-plan-price">` and `<span class="subscribe-plan-note">`:

- 3 ай card: `<p class="subscribe-plan-limits">Күнүнө: 1 презентация, 1 ишмердик, 1 иш барак</p>`
- 6 ай card: `<p class="subscribe-plan-limits">Күнүнө: 5 презентация, 5 ишмердик, 5 иш барак</p>`
- 1 жыл card: `<p class="subscribe-plan-limits">Чексиз жүктөп алуу</p>`

- [ ] **Step 4: Add the CSS**

In `static/css/subscribe.css`, after the existing `.subscribe-plan-note` rule:

```css
.subscribe-plan-limits {
    font-size: 0.85rem;
    color: var(--text-muted);
    text-align: center;
    margin: 4px 0 0;
    line-height: 1.4;
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python manage.py test apps.resources.tests.PagesTests.test_homepage_shows_plan_download_limits -v 2`
Expected: PASS.

- [ ] **Step 6: Run the full resources test suite**

Run: `python manage.py test apps.resources -v 2`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add templates/partials/pricing_cards.html static/css/subscribe.css apps/resources/tests.py
git commit -m "Show per-plan daily download limits on the subscribe cards"
```

---

### Task 7: `/pricing/` comparison page and footer link

**Files:**
- Modify: `apps/resources/views/pages.py` (add `pricing_view`)
- Modify: `apps/resources/views/__init__.py:50-52`
- Modify: `config/urls.py:49-54` (import list) and `:1443-1445` (path list)
- Create: `templates/resources/pricing.html`
- Create: `static/css/pricing.css`
- Modify: `templates/snippets/footer.html` (Навигация `<ul class="footer-links">`)
- Test: `apps/resources/tests.py`

**Interfaces:**
- Consumes: `SubscriptionRequest.PLAN_THREE_MONTHS/.PLAN_SIX_MONTHS/.PLAN_ONE_YEAR/.PLAN_MONTHS/.PLAN_PRICE_SOM` and `DAILY_DOWNLOAD_LIMITS` (Task 1, both importable from `apps.account.models`), `partials/pricing_cards.html` with `mode='preview'` (existing, unchanged).
- Produces: URL name `'pricing'`.

- [ ] **Step 1: Write the failing tests**

Add to `apps/resources/tests.py`:

```python
class PricingPageTests(TestCase):
    def test_pricing_page_loads_and_shows_all_plans(self):
        resp = self.client.get(reverse('pricing'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '3 ай')
        self.assertContains(resp, '6 ай')
        self.assertContains(resp, '1 жыл')
        self.assertContains(resp, '1499 сом')
        self.assertContains(resp, '2999 сом')
        self.assertContains(resp, '4999 сом')
        self.assertContains(resp, 'Чексиз')

    def test_footer_links_to_pricing_page(self):
        resp = self.client.get(reverse('about'))
        self.assertContains(resp, reverse('pricing'))
        self.assertContains(resp, 'Баалар')
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python manage.py test apps.resources.tests.PricingPageTests -v 2`
Expected: FAIL — `reverse('pricing')` raises `NoReverseMatch` (URL doesn't exist yet).

- [ ] **Step 3: Add `pricing_view`**

In `apps/resources/views/pages.py`, add (near `about_view`/`topics_tree_view`; add `from apps.account.models import SubscriptionRequest, DAILY_DOWNLOAD_LIMITS` to the top of the file):

```python
def pricing_view(request):
    plan_names = {
        SubscriptionRequest.PLAN_THREE_MONTHS: '3 ай',
        SubscriptionRequest.PLAN_SIX_MONTHS: '6 ай',
        SubscriptionRequest.PLAN_ONE_YEAR: '1 жыл',
    }
    unlimited_display = {'presentation': 'Чексиз', 'worksheet': 'Чексиз', 'activity': 'Чексиз'}
    plans = []
    for code, name in plan_names.items():
        limits = DAILY_DOWNLOAD_LIMITS[code]
        plans.append({
            'code': code,
            'name': name,
            'price_som': SubscriptionRequest.PLAN_PRICE_SOM[code],
            'months': SubscriptionRequest.PLAN_MONTHS[code],
            'limits': limits or unlimited_display,
        })
    return render(request, 'resources/pricing.html', {
        'plans': plans,
        'featured_code': SubscriptionRequest.PLAN_ONE_YEAR,
    })
```

- [ ] **Step 4: Wire the URL**

In `apps/resources/views/__init__.py`, change:
```python
from .pages import (
    news_list_view, about_view, topics_tree_view, search_view, search_suggest_view,
)
```
to:
```python
from .pages import (
    news_list_view, about_view, topics_tree_view, search_view, search_suggest_view,
    pricing_view,
)
```

In `config/urls.py`, add `pricing_view,` to the `# pages` import block (after `search_suggest_view,`), and add this line after `path('topics/', topics_tree_view, name='topics_tree'),`:
```python
    path('pricing/', pricing_view, name='pricing'),
```

- [ ] **Step 5: Create the template**

`templates/resources/pricing.html`:

```django
{% extends 'base/base.html' %}
{% load static %}

{% block title %}Баалар{% endblock %}

{% block extra_head %}
<link rel="stylesheet" href="{% static 'css/pricing.css' %}">
{% endblock %}

{% block content %}
<div class="container py-5 pricing-page">
    <div class="text-center mb-5">
        <h1 class="display-6 fw-bold">Баалар</h1>
        <p class="text-muted">Өзүңүзгө ылайыктуу планды тандаңыз</p>
    </div>

    <div class="pricing-table-wrap">
        <table class="pricing-table">
            <thead>
                <tr>
                    <th></th>
                    {% for plan in plans %}
                    <th class="{% if plan.code == featured_code %}pricing-featured{% endif %}">{{ plan.name }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th>Баасы</th>
                    {% for plan in plans %}<td>{{ plan.price_som }} сом</td>{% endfor %}
                </tr>
                <tr>
                    <th>Узактыгы</th>
                    {% for plan in plans %}<td>{{ plan.months }} ай</td>{% endfor %}
                </tr>
                <tr>
                    <th>Презентация (күнүнө)</th>
                    {% for plan in plans %}<td>{{ plan.limits.presentation }}</td>{% endfor %}
                </tr>
                <tr>
                    <th>Мугалим жетектеген ишмердик (күнүнө)</th>
                    {% for plan in plans %}<td>{{ plan.limits.activity }}</td>{% endfor %}
                </tr>
                <tr>
                    <th>Иш барак (күнүнө)</th>
                    {% for plan in plans %}<td>{{ plan.limits.worksheet }}</td>{% endfor %}
                </tr>
            </tbody>
        </table>
    </div>

    <div class="pricing-cta mt-5">
        {% include 'partials/pricing_cards.html' with mode='preview' %}
    </div>
</div>
{% endblock %}
```

- [ ] **Step 6: Create the CSS**

`static/css/pricing.css`:

```css
/* /pricing/ - plan comparison table. Built from the same tokens as the
   rest of the site - no new one-off colors or gradients. */

.pricing-table-wrap {
    overflow-x: auto;
}

.pricing-table {
    width: 100%;
    min-width: 560px;
    border-collapse: collapse;
}

.pricing-table th,
.pricing-table td {
    padding: 14px 18px;
    text-align: center;
    border-bottom: 1px solid var(--border-subtle);
}

.pricing-table thead th {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-navy);
    background: var(--surface-alt);
}

.pricing-table thead th.pricing-featured {
    color: var(--color-bootstrap-primary);
}

.pricing-table tbody th {
    text-align: left;
    font-weight: 600;
    color: var(--text);
    background: var(--surface-alt);
}

.pricing-table tbody td {
    color: var(--text);
}

.pricing-cta {
    max-width: 900px;
    margin: 0 auto;
}
```

- [ ] **Step 7: Add the footer link**

In `templates/snippets/footer.html`, add as the first `<li>` inside the Навигация `<ul class="footer-links">` (before the existing "Сайттагы жаңылыктар" item):

```html
          <li>
            <a href="{% url 'pricing' %}">
              <i class="fa-solid fa-chevron-right"></i>
              Баалар
            </a>
          </li>
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `python manage.py test apps.resources.tests.PricingPageTests -v 2`
Expected: PASS.

- [ ] **Step 9: Run the full resources test suite and `manage.py check`**

Run: `python manage.py test apps.resources -v 2` then `python manage.py check`
Expected: both clean.

- [ ] **Step 10: Commit**

```bash
git add apps/resources/views/pages.py apps/resources/views/__init__.py config/urls.py \
        templates/resources/pricing.html static/css/pricing.css templates/snippets/footer.html \
        apps/resources/tests.py
git commit -m "Add /pricing/ plan comparison page, link it from the footer"
```

---

### Task 8: News entry and final verification

**Files:**
- Modify: `apps/resources/management/commands/seed_launch_news.py`

- [ ] **Step 1: Add the Kyrgyz news entry**

Add a new entry at the top of `NEWS_ITEMS` (string `'published_date'` format, matching this branch's existing convention — this gets converted to a `date()` object during the cherry-pick-to-`main` step, per this project's established workflow):

```python
    {
        'published_date': '<today's date, YYYY-MM-DD>',
        'title': 'Жазылуу боюнча жүктөп алуу чектери жана Баалар барагы',
        'body': (
            'Эми ар бир жазылуу планы күнүнө белгилүү санда '
            'презентация, мугалим жетектеген ишмердик жана иш барак '
            'жүктөп алууга мүмкүндүк берет: 3 айлык жана акысыз сыноо '
            'планы - ар бирден 1, 6 айлык - ар бирден 5, ал эми 1 '
            'жылдык план - чексиз. Акысыз сыноо мөөнөтү жаңы '
            'колдонуучулар үчүн 7 күнгө чейин кыскарды. Пландарды '
            'салыштырган жаңы "Баалар" барагы кошулду - шилтемесин '
            'баракчанын төмөнкү бөлүгүнөн табасыз.'
        ),
    },
```

- [ ] **Step 2: Run the full test suite**

Run: `python manage.py test -v 2`
Expected: PASS — every test from Tasks 1-7 plus the pre-existing suite.

- [ ] **Step 3: Run `manage.py check`**

Run: `python manage.py check`
Expected: `System check identified no issues (0 silenced).`

- [ ] **Step 4: Manual/visual check**

Start the dev server and, in both light and dark mode (desktop and mobile widths): confirm the subscribe modal and homepage preview show the new limit text on all 3 cards; confirm `/pricing/` renders the comparison table and the same plan cards below it; confirm the footer's "Баалар" link navigates to `/pricing/`.

- [ ] **Step 5: Commit**

```bash
git add apps/resources/management/commands/seed_launch_news.py
git commit -m "Add news entry for download limits and the new pricing page"
```

---

## After this plan

Shipping to `main` (cherry-pick per this project's established per-commit workflow, resolving the standard `seed_launch_news.py` date-format conflict, excluding any dev-only exam-feature content that doesn't belong on `main`) and the production rollout (`migrate` then `repair_subscriptions --apply`) happen afterward, outside this plan, the same way every other change in this session has shipped.
