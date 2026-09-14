from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from config import download_file

from apps.resources.models import Resource

from apps.resources.views import dashboard_view
from apps.resources.views import analytics_dashboard_view
from apps.resources.views import big4_view
from apps.resources.views import topic_view



# from apps.resources.views import (
#     home_screen_view,
#     # #sandar korinushu
#     # four_basic_operations_view,
#     # directed_numbers_view,
#     # all_operations_view,
#     koshuu_1_digit_view,
#     #bir orunduu sandar
#     onedigitarithmetics_view,

#     dashboard_view,
#     four_basic_operations_view,
#     all_operations_view,
#     koshuu_1_digit_view,
#     directed_numbers_view,

#     #iygilik message
#     success_view,

#     #resursttar bazadagy
#     resources_view,

#     #kochurup aluulardy koruu uchun
#     download_resource_view,
# )

from apps.resources.views import (
    home_screen_view,
    success_view,
    dashboard_view,
    analytics_dashboard_view,
    resources_view,

    download_resource_view,
    


    # sandar
    directed_numbers_view,
    four_basic_operations_view,
    all_operations_view,
    koshuu_1_digit_view,
    big4_view,

    # onduktar
    onedigitarithmetics_view,
)

from apps.account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('home/', home_screen_view, name='home'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('account/', account_view, name='account'),
    # Success message
    path('SuccessMessage/', success_view, name='SuccessMessage'),

    #sandar
    
    path('four_basic_operations/', four_basic_operations_view, name='four_basic_operations'),

    path('directed_numbers/', directed_numbers_view, name='directed_numbers'),

    
    path('all_operations/', all_operations_view, name='all_operations'),
    path('koshuu-1-digit/', koshuu_1_digit_view, name='koshuu_1_digit'),

    path('templates/interactive/big4/', big4_view, name='big4'),

    # for dynamic resources
    path(
    "topic/<slug:topic_slug>/<slug:subtopic_slug>/",
    topic_view,
    name="topic_page",),

    path('resources/', include('apps.resources.urls')),


    


    
    
    path('', home_screen_view),
    path('dashboard/', dashboard_view),
    path('analytics/', analytics_dashboard_view),

    #onduktar
    path('onedigitarithmetics/', onedigitarithmetics_view, name='onedigitarithmetics'),



    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('analytics/', analytics_dashboard_view, name='analytics_dashboard'), 

    # Resources
    path('resources/download/<int:pk>/', download_resource_view, name='download_resource'),

    path('resources/', resources_view, name='resources'),

    # Old download (keep until you remove it from templates)
    path('download/<str:file_name>/', download_file, name='download_file'),

    # Password management
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# In your main urls.py, add temporarily:
from django.http import JsonResponse
from apps.resources.models import MenuItem
from django.conf import settings

# def debug_menu(request):
#     # Check 1: What context processors are registered?
#     cps = settings.TEMPLATES[0]['OPTIONS']['context_processors']
    
#     # Check 2: What does the DB actually have?
#     roots = MenuItem.objects.filter(parent__isnull=True).prefetch_related(
#         'children', 'children__children'
#     )
#     menu_data = []
#     for r in roots:
#         children = []
#         for c in r.children.all():
#             children.append({
#                 'title': c.title,
#                 'grandchildren': list(c.children.values_list('title', flat=True))
#             })
#         menu_data.append({'title': r.title, 'children': children})

#     # Check 3: Does the context processor function actually work?
#     from apps.resources.views.context_processors import menu_items
#     cp_result = menu_items(request)

#     return JsonResponse({
#     '1_context_processors_in_settings': cps,
#     '2_db_menu_structure': menu_data,
#     '3_context_processor_output_count': len(cp_result.get('menu_items', [])),
#     '4_context_processor_keys': list(cp_result.keys()),
# }, json_dumps_params={'indent': 2})  # ← fix here

# urlpatterns = [
#     # ... your existing urls ...
#     path('debug/', debug_menu),   # ← add this line
# ]