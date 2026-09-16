from datetime import date
from logging import getLogger

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Account
from .forms import (
    RegistrationForm,
    AccountAuthenticationForm,
    AccountUpdateForm,
)

logger = getLogger(__name__)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

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

    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



#User Login
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
    }

    return render(request, 'account/account.html', context)


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


