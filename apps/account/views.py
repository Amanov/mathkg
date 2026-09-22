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
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit

from apps.resources.models import Exam, LoginEvent, Question, ResourceDownload

from .models import Account, School, SubscriptionRequest
from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    AccountUpdateForm,
)

logger = getLogger(__name__)


def get_client_ip(request):
    # Railway terminates TLS and proxies every request to this app, so
    # REMOTE_ADDR is always Railway's edge IP, never the visitor's -
    # django-ratelimit's built-in key='ip' would key every single
    # visitor's rate limit off that one shared address, meaning one
    # person mistyping their password could lock out everyone else
    # trying to log in. Railway is the only hop in front of this app
    # (same trust assumption production.py already makes for
    # X-Forwarded-Proto), so the first X-Forwarded-For value is the
    # real client IP.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def ratelimit_key(group, request):
    return get_client_ip(request)


# NOTE: with no CACHES setting configured, Django's implicit default is
# LocMemCache, which is per-process. Under gunicorn with more than one
# worker, each worker counts independently, so the effective limit is
# closer to (rate x worker count) than the configured rate. Fine as a
# first line of defense while this runs on a single worker; move to a
# shared cache (Redis/Memcached) if that ever changes.


@ratelimit(key=ratelimit_key, rate='10/h', method='POST', block=True)
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

            messages.success(
                request,
                "Каттоо ийгиликтүү аяктады!\n"
                "Аккаунтуңузду активдештирүү үчүн электрондук почтаңызга жиберилген "
                "шилтемени басыңыз, андан кийин кызматты пайдаланып, сабактардан "
                "ырахат ала аласыз.\n"
                "QR код аркылуу төлөм жасаган болсоңуз, төлөм текшерилгенден кийин "
                "жазылууңуз өзү активдештирилет - кошумча аракет талап кылынбайт.\n"
                "Кирүү менен көйгөй чыкса, бизге жазыңыз: mathematicskgz@gmail.com",
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    # A failed validation (mismatched passwords, a weak password, an
    # email already in use...) re-renders this same view as a POST, on
    # which request.GET is empty - reading only that would silently drop
    # the plan on the very first retry, and with it the hidden field
    # that would have carried it into the next submission too. Reading
    # whichever of GET/POST this request actually is keeps the plan
    # alive across that retry, all the way to a successful submission.
    plan_source = request.POST if request.method == 'POST' else request.GET
    selected_plan = plan_source.get('plan')
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
@ratelimit(key=ratelimit_key, rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                if not request.session.session_key:
                    request.session.save()
                LoginEvent.objects.create(
                    user=user,
                    session_key=request.session.session_key or '',
                    ip_address=get_client_ip(request),
                )
                messages.success(request, 'Кирүү ийгиликтүү аяктады!')
                return redirect("home")
            else:
                messages.error(request, 'Электрондук почта же сырсөз туура эмес.')
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


@require_POST
def subscribe_request_view(request):
    # Handles the subscribe modal's "continue" step for a user who
    # already has an account (e.g. opened from the account page) -
    # the modal sends brand-new visitors to registration instead, since
    # they don't have a user to attach a SubscriptionRequest to yet.
    #
    # Must be POST, not a plain link: this creates a database row, and a
    # GET request that does that is both unprotected by Django's CSRF
    # middleware (which only covers unsafe methods) and non-idempotent -
    # a page refresh, a browser's link-prefetch, or someone replaying the
    # URL would silently create another pending request. Two pending
    # requests for one real payment is a real billing bug: whoever
    # confirms them in admin has no way to tell they're duplicates, and
    # confirming both extends the subscription twice for money paid once.
    if not request.user.is_authenticated:
        return redirect('login')

    if SubscriptionRequest.objects.filter(
        user=request.user, status=SubscriptionRequest.STATUS_PENDING,
    ).exists():
        messages.info(
            request,
            "Сизде мурунтан эле каралып жаткан суранычыңыз бар. Төлөм текшерилгенде сизге кабарлайбыз.",
        )
        return redirect('account')

    plan = request.POST.get('plan')
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


def school_dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_school_admin or not request.user.school_id:
        return redirect('account')

    school = request.user.school

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_teacher':
            email = request.POST.get('email', '').strip().lower()
            try:
                teacher = Account.objects.get(email=email)
            except Account.DoesNotExist:
                messages.error(request, f"'{email}' дареги менен катталган колдонуучу табылган жок.")
            else:
                if teacher.school_id and teacher.school_id != school.id:
                    messages.error(request, f"{teacher.email} мурунтан эле башка мектепке таандык.")
                else:
                    teacher.school = school
                    teacher.save(update_fields=['school'])
                    messages.success(request, f"{teacher.email} мектепке кошулду.")

        elif action == 'remove_teacher':
            teacher_id = request.POST.get('teacher_id')
            Account.objects.filter(id=teacher_id, school=school).update(school=None)
            messages.success(request, "Мугалим мектептен алынды.")

        return redirect('school_dashboard')

    teachers = [
        {
            'account': teacher,
            'downloads': ResourceDownload.objects.filter(user=teacher).count(),
            'logins': LoginEvent.objects.filter(user=teacher).count(),
            'exams_created': Exam.objects.filter(created_by=teacher).count(),
            'questions_created': Question.objects.filter(created_by=teacher).count(),
        }
        for teacher in school.teachers.all()
    ]

    return render(request, 'account/school_dashboard.html', {
        'school': school,
        'teachers': teachers,
    })


@method_decorator(
    ratelimit(key=ratelimit_key, rate='5/h', method='POST', block=True),
    name='dispatch',
)
class RateLimitedPasswordResetView(auth_views.PasswordResetView):
    """auth_views.PasswordResetView, rate-limited per IP.

    Otherwise identical - kept as a thin subclass purely so urls.py can
    rate-limit it the same way as login/registration, since a plain
    function decorator can't be applied to a class-based view's
    as_view() the same way.
    """


