# account/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

from .forms import RegistrationForm


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send activation email
            activation_link = f"https://mathkh.pythonanywhere.com/activate/?user_id={user.id}"
            
            email_message = (
                f"Dear {user.username},\n\n"
                f"Please click the link below to activate your account:\n\n"
                f"{activation_link}\n\n"
                "Best regards,\nMathematika Okutabyz Team"
            )

            try:
                send_mail(
                    subject='Account Activation',
                    message=email_message,
                    from_email='noreply@mathkh.pythonanywhere.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception:
                messages.warning(request, "Каттоо ийгиликтүү өттү, бирок email жөнөтүлбөдү.")

            # ← THIS IS THE KEY CHANGE
            messages.success(request, 
                'Сиз ийгиликтүү катталдыңыз! Администратор аккаунтуңузду активдештиргенден кийин кабар аласыз.'
            )
            
            return redirect('home')          # Changed from 'SuccessMessage'

    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def registerSchool_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            activation_link = f"https://mathkh.pythonanywhere.com/activate/?user_id={user.id}"
            
            email_message = (
                f"Dear {user.username},\n\n"
                f"Please click the link below to activate your account:\n\n"
                f"{activation_link}\n\n"
                "Best regards,\nMathematika Okutabyz Team"
            )

            try:
                send_mail('Account Activation', email_message, 
                          'noreply@mathkh.pythonanywhere.com', [user.email])
            except Exception:
                messages.warning(request, "Каттоо ийгиликтүү өттү, бирок email жөнөтүлбөдү.")

            messages.success(request, 
                'Сиз ийгиликтүү катталдыңыз! Администратор аккаунтуңузду активдештирүүсүн күтүңүз.'
            )
            
            return redirect('home')

    else:
        form = RegistrationForm()

    return render(request, 'account/registerSchool.html', {'form': form})