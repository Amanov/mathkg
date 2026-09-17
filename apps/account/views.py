from datetime import date
from logging import getLogger

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_ratelimit.decorators import ratelimit

from .models import Account, SubscriptionRequest
from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    AccountUpdateForm,
)

logger = getLogger(__name__)

# NOTE on key='ip': this uses django-ratelimit's default, which reads
# request.META['REMOTE_ADDR']. Whether that's the real client IP or
# Railway's proxy IP for every request depends on how Railway's edge
# sets REMOTE_ADDR - verify this isn't rate-limiting all users as one
# client (or, worse, trusting a spoofable header) once this is live.
#
# Also: with no CACHES setting configured, Django's implicit default is
# LocMemCache, which is per-process. Under gunicorn with more than one
# worker, each worker counts independently, so the effective limit is
# closer to (rate x worker count) than the configured rate. Fine as a
# first line of defense; move to a shared cache (Redis/Memcached) for
# an exact limit once this runs with multiple workers.


@ratelimit(key='ip', rate='10/h', method='POST', block=True)
def registration_view(request):
    # Carries the plan chosen in the subscribe modal through to here via
    # a query param on GET (?plan=6m) and a hidden field on the POSTed
    # form, since the modal opens before the user has an account to
    # attach a SubscriptionRequest to.
    valid_plans = dict(SubscriptionRequest.PLAN_CHOICES)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            plan = request.POST.get('plan')
            if plan in valid_plans:
                SubscriptionRequest.objects.create(user=user, plan=plan)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            activation_link = f"https://{domain}/activate/{uidb64}/{token}/"
            message = f"Dear {user.username},\n\nActivate: {activation_link}"

            try:
                send_mail(
                    'Account Activation',
                    message,
                    None,  # uses settings.DEFAULT_FROM_EMAIL
                    [user.email],
                    fail_silently=False
                )
            except Exception as e:
                logger.error(f"Failed to send activation email to {user.email}: {e}")

            messages.success(request, "Registration is successful. Please wait for activation.")
            return redirect('login')
    else:
        form = RegistrationForm()

    selected_plan = request.GET.get('plan')
    if selected_plan not in valid_plans:
        selected_plan = ''

    context = {
        'form': form,
        'selected_plan': selected_plan,
        'selected_plan_label': valid_plans.get(selected_plan, ''),
    }
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')



#User Login
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')  # Add a success message
                return redirect("home")
            else:
                messages.error(request, 'Invalid email or password.')  # Add an error message
    else:
        form = AccountAuthenticationForm()

    context = {'form': form}
    return render(request, 'account/login.html', context)


#account update
def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маалымат жаңыртылды.')
            return redirect('account')
    else:
        form = AccountUpdateForm(instance=user)

    today = date.today()

    # subscription end (hybrid) - single source of truth on the model,
    # shared with the download view's access check.
    subscription_end = user.subscription_end_date

    days_left = (subscription_end - today).days

    # status color
    if days_left > 7:
        status_color = "success"
    elif days_left > 0:
        status_color = "warning"
    else:
        status_color = "danger"

    context = {
        'account_form': form,
        'subscription_end': subscription_end,
        'days_left': days_left,
        'days_passed': abs(days_left),
        'status_color': status_color,
        'latest_subscription_request': user.subscription_requests.first(),
    }

    return render(request, 'account/account.html', context)


def subscribe_request_view(request):
    # Handles the subscribe modal's "continue" step for a user who
    # already has an account (e.g. opened from the account page) -
    # the modal sends brand-new visitors to registration instead, since
    # they don't have a user to attach a SubscriptionRequest to yet.
    if not request.user.is_authenticated:
        return redirect('login')

    plan = request.GET.get('plan')
    valid_plans = dict(SubscriptionRequest.PLAN_CHOICES)
    if plan in valid_plans:
        SubscriptionRequest.objects.create(user=request.user, plan=plan)
        messages.success(
            request,
            f"«{valid_plans[plan]}» планы катталды. Төлөм текшерилгенден кийин жазылууңуз активдештирилет.",
        )
    return redirect('account')


def activation_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        messages.success(request, 'Your account has been activated successfully.')
    else:
        messages.error(request, 'Invalid activation link.')

    return redirect('login')


@method_decorator(
    ratelimit(key='ip', rate='5/h', method='POST', block=True),
    name='dispatch',
)
class RateLimitedPasswordResetView(auth_views.PasswordResetView):
    """auth_views.PasswordResetView, rate-limited per IP.

    Otherwise identical - kept as a thin subclass purely so urls.py can
    rate-limit it the same way as login/registration, since a plain
    function decorator can't be applied to a class-based view's
    as_view() the same way.
    """


