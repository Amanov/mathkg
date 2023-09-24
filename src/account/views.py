
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from account.forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm
from django.core.mail import send_mail
from .models import Account
from django.contrib import messages

from .forms import RegistrationForm

# Create your views here.
#User registration
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            user = form.save()

            # Perform manual activation steps
            # For example, send an activation email
            activation_link = "https://mathkh.pythonanywhere.com/activate/?user_id={}".format(user.id)
            message = "Dear {},\n\nPlease click on the following link to activate your account: {}".format(
                user.username, activation_link)
            send_mail('Account Activation', message, 'noreply@yourwebsite.com', [user.email], fail_silently=False)

            # Display a success message to the user
            # Redirect to a thank you or activation pending page
            # ...

            # login(request, user)

            messages.success(request, "Registration is successful. Please for activation")
            # print("Success")
            return redirect('SuccessMessage')
    else:
        form = RegistrationForm()
        print("failure")

     # Render the registration form template
    context = {'form': form}
    return render(request, 'account/register.html', context)
#
#register success




#School  registration
def registerSchool_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Perform manual activation steps
            # For example, send an activation email
            activation_link = "https://yourwebsite.com/activate/?user_id={}".format(user.id)
            message = "Dear {},\n\nPlease click on the following link to activate your account: {}".format(
                user.username, activation_link)
            send_mail('Account Activation', message, 'noreply@yourwebsite.com', [user.email], fail_silently=False)

            # Display a success message to the user
            # Redirect to a thank you or activation pending page
            # ...
            messages.success(request, 'Registration is successful. Please wait for activation.')
            return redirect('SuccessMessage')
    else:
        form = RegistrationForm()

    # Render the registration form template
    context = {'form': form}
    return render(request, 'account/registerSchool.html', context)


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

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial ={
                "email":request.POST['email'],
                "username":request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form =AccountUpdateForm(
            initial={
                "email":request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form
    return render(request,'account/account.html',context)

from django.shortcuts import render, redirect
from django.contrib import messages

def activation_view(request):
    user_id = request.GET.get('user_id')
    try:
        user = Account.objects.get(id=user_id)
        user.is_active = True
        user.save()
        # Perform any additional actions after activation
        # For example, display an activation success message or redirect to a login page
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')  # Redirect to the login page after activation
    except Account.DoesNotExist:
        # Handle the case when the user is not found
        # For example, display an activation failure message or redirect to an error page
        messages.error(request, 'Invalid activation link.')
        return redirect('activation_failure')  # Redirect to the activation failure page
from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from account.forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm
from django.core.mail import send_mail
from .models import Account


# Create your views here.
#User registration
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Perform manual activation steps
            # For example, send an activation email
            activation_link = "https://http://mathkh.pythonanywhere.com/activate/?user_id={}".format(user.id)
            message = "Dear {},\n\nPlease click on the following link to activate your account: {}".format(
                user.username, activation_link)
            send_mail('Account Activation', message, 'noreply@yourwebsite.com', [user.email], fail_silently=False)

            # Display a success message to the user
            # Redirect to a thank you or activation pending page
            # ...
            messages.success(request, 'Registration is successful. Please wait for activation.')
            return redirect('home')
    else:
        form = RegistrationForm()

    # Render the registration form template
    context = {'form': form}
    return render(request, 'account/register.html', context)
#

#School  registration
def registerSchool_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Perform manual activation steps
            # For example, send an activation email
            activation_link = "https://yourwebsite.com/activate/?user_id={}".format(user.id)
            message = "Dear {},\n\nPlease click on the following link to activate your account: {}".format(
                user.username, activation_link)
            send_mail('Account Activation', message, 'noreply@yourwebsite.com', [user.email], fail_silently=False)

            # Display a success message to the user
            # Redirect to a thank you or activation pending page
            # ...
            messages.success(request, 'Registration is successful. Please wait for activation.')
            return redirect('home')
    else:
        form = RegistrationForm()

    # Render the registration form template
    context = {'form': form}
    return render(request, 'account/registerSchool.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')



#User Login

def login_view(request):

    context ={}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect("home")

    else:
        form =AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html',context)

#account update
def account_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial ={
                "email":request.POST['email'],
                "username":request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form =AccountUpdateForm(
            initial={
                "email":request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form
    return render(request,'account/account.html',context)

from django.shortcuts import render, redirect
from django.contrib import messages

def activation_view(request):
    user_id = request.GET.get('user_id')
    try:
        user = Account.objects.get(id=user_id)
        user.is_active = True
        user.save()
        # Perform any additional actions after activation
        # For example, display an activation success message or redirect to a login page
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')  # Redirect to the login page after activation
    except Account.DoesNotExist:
        # Handle the case when the user is not found
        # For example, display an activation failure message or redirect to an error page
        messages.error(request, 'Invalid activation link.')
        return redirect('activation_failure')  # Redirect to the activation failure page

