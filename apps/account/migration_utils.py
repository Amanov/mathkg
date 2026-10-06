"""Small, independently-importable helper functions used by data
migrations. Kept out of the migration files themselves so they can be
unit-tested directly against the real model classes, instead of only
through Django's migration machinery (whose historical models strip
everything but fields, and which Django's test runner only ever applies
once - before any test row exists - making the migration itself
untestable for "did it touch the right rows" in a normal TestCase)."""


def backfill_current_plan(Account):
    """For every account with at least one confirmed SubscriptionRequest
    but no current_plan set yet, sets current_plan to the plan of the
    latest confirmed request. Leaves accounts with no confirmed request,
    and accounts that already have a current_plan, untouched."""
    for account in Account.objects.filter(
        subscription_requests__status='confirmed',
        current_plan__isnull=True,
    ).distinct():
        latest = account.subscription_requests.filter(
            status='confirmed'
        ).order_by('created_at').last()
        if latest:
            account.current_plan = latest.plan
            account.save(update_fields=['current_plan'])
