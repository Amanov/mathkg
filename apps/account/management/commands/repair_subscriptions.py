from datetime import timedelta

from django.core.management.base import BaseCommand

from apps.account.models import Account, SubscriptionRequest, add_months


class Command(BaseCommand):
    help = (
        "Finds accounts whose confirmed SubscriptionRequest history implies "
        "more paid access than their current subscription_end reflects - "
        "the symptom of confirming a request without activate() actually "
        "running (fixed in SubscriptionRequestAdmin.save_model, but "
        "requests confirmed before that fix may still be under-credited) - "
        "and tops them up to what they're owed. Never lowers anyone's "
        "subscription_end. Dry-run by default; pass --apply to write."
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

            # Replays every confirmed request in order, starting from the
            # same 1-year-trial baseline Account.subscription_end_date
            # falls back to when subscription_end is still null - i.e.
            # what the account would legitimately have ended up with if
            # every one of these had gone through activate() for real.
            simulated_end = account.date_joined.date() + timedelta(days=365)
            for req in confirmed:
                anchor = max(req.created_at.date(), simulated_end)
                simulated_end = add_months(anchor, SubscriptionRequest.PLAN_MONTHS[req.plan])

            actual_end = account.subscription_end
            under_credited = actual_end is None or simulated_end > actual_end

            if not under_credited:
                continue

            fixed += 1
            self.stdout.write(
                f"{account.email}: subscription_end {actual_end} -> {simulated_end} "
                f"({len(confirmed)} confirmed request(s))"
            )

            if apply_fix:
                account.subscription_end = simulated_end
                account.save(update_fields=['subscription_end'])
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
