from django.core.management.base import BaseCommand

from apps.account.models import Account, SubscriptionRequest, add_months


class Command(BaseCommand):
    help = (
        "Recomputes subscription_end for every account with a confirmed "
        "SubscriptionRequest, by replaying that history through the same "
        "rule activate() now uses (each plan grants exactly its own "
        "duration from whichever is later - today, or a still-active paid "
        "period - never stacked on top of the free signup trial), and "
        "corrects any account that doesn't match. This can move a date in "
        "either direction: it fixes both a confirmed request that never "
        "actually ran through activate() (subscription_end too low) and "
        "one that was activated under the old trial-stacking rule "
        "(subscription_end too high). It also activates (is_active=True) "
        "any account with a confirmed request that isn't already active - "
        "a verified payment is proof enough of a real user, so a confirmed "
        "request shouldn't leave login blocked on a separate, unrelated "
        "email-activation step. Dry-run by default; pass --apply to write. "
        "Ignores any admin adjustment to subscription_end that isn't "
        "backed by a SubscriptionRequest."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply', action='store_true',
            help='Write the fix. Without this flag, only a report is printed.',
        )

    def handle(self, *args, **options):
        apply_fix = options['apply']
        checked = 0
        fixed = 0

        accounts = Account.objects.filter(
            subscription_requests__status=SubscriptionRequest.STATUS_CONFIRMED,
        ).distinct()

        for account in accounts:
            checked += 1
            confirmed = list(
                account.subscription_requests
                .filter(status=SubscriptionRequest.STATUS_CONFIRMED)
                .order_by('created_at')
            )

            # Replays every confirmed request in order, mirroring
            # activate(): each one grants exactly its own duration from
            # whichever is later - the date it was actually confirmed
            # (activated_at, falling back to created_at for requests
            # confirmed before that field existed), or the point the
            # previous one in this chain left off - with no free-trial
            # baseline involved at all.
            simulated_end = None
            for req in confirmed:
                anchor = (req.activated_at or req.created_at).date()
                if simulated_end:
                    anchor = max(anchor, simulated_end)
                simulated_end = add_months(anchor, SubscriptionRequest.PLAN_MONTHS[req.plan])

            actual_end = account.subscription_end
            needs_date_fix = actual_end != simulated_end
            needs_activation = not account.is_active

            if not needs_date_fix and not needs_activation:
                continue

            fixed += 1
            changes = []
            if needs_date_fix:
                changes.append(f"subscription_end {actual_end} -> {simulated_end}")
            if needs_activation:
                changes.append("is_active False -> True")
            self.stdout.write(
                f"{account.email}: {'; '.join(changes)} "
                f"({len(confirmed)} confirmed request(s))"
            )

            if apply_fix:
                account.subscription_end = simulated_end
                account.is_active = True
                account.save(update_fields=['subscription_end', 'is_active'])
                for req in confirmed:
                    if req.activated_at is None:
                        req.activated_at = req.created_at
                        req.save(update_fields=['activated_at'])

        verb = "Fixed" if apply_fix else "Would fix"
        self.stdout.write(self.style.SUCCESS(
            f"{verb} {fixed} of {checked} account(s) with a confirmed subscription request."
        ))
        if not apply_fix and fixed:
            self.stdout.write("Re-run with --apply to write these changes.")
