from django.urls import path
from .views import (
    registration_view,
    registerSchool_view,
    login_view,
    logout_view,
    account_view,
    activation_view,
)

app_name = "account"

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('register-school/', registerSchool_view, name='register_school'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),
    path('activate/', activation_view, name='activate'),
    
]