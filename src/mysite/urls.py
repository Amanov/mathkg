"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#here for downlaoding files from media file
from django.conf import settings
from django.conf.urls.static import static

from mysite import download_file

# Accessing folders in media




#
from personal.views import (
    home_screen_view,
    #more views
    four_basic_operations_view,
    directed_numbers_view,
    all_operations_view,
    onedigitarithmetics_view,
    success_view,
    )

from account.views import (
    registration_view,
    registerSchool_view,
    logout_view,
    login_view,
    account_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('home/', home_screen_view, name='home'), #root
    path('register/', registration_view, name='register'),
    path('registerSchool/', registerSchool_view, name='registerSchool'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),



    path('', include('django.contrib.auth.urls')),



    #REST FRAMEWORK URLS

    path('api/account',include('account.api.urls','account_api')),

    #link paths to the sandar pages
    path('SuccessMessage/', success_view, name='SuccessMessage'),

    path('four_basic_operations/',four_basic_operations_view, name='four_basic_operations'),
    path('directed_numbers/',directed_numbers_view, name='directed_numbers'),
    path('all_operations',all_operations_view, name='all_operations'),
    #link paths to the decimals pages
    path('onedigitarithmetics/',onedigitarithmetics_view, name='onedigitarithmetics'),

    # here i am trying to add other urls to go a link
    path('download/<str:file_name>/', download_file, name='download_file'),
    # path('four-operations/', views.four_operations, name='four_operations'),

    #password recovering
    #path('account/', include('django.contrib.auth.urls')), it will give an error interfere with to others
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),

    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/',auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # trying to link html file
    #  path('operations/',operations_view,name='fourOperation.html'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# form mysite view
