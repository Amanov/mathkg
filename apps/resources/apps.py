from django.apps import AppConfig


# class ResourcesConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'apps.personal'

class ResourcesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.resources'
    label = 'personal'

    def ready(self):
        # Public pages, emails, and the admin chrome share one site name.
        from django.contrib import admin
        admin.site.site_header = 'MathKG'
        admin.site.site_title = 'MathKG'