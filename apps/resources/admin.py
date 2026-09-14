from django.contrib import admin
from django.contrib import messages

# from .models import Topic, Resource, ResourceDownload

from .models import (
    Topic,
    Subtopic,
    Resource,
    ResourceDownload,
)
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
    )

    list_filter = (
        "topic",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

# apps/resources/admin.py — add this
from .models import SubSubtopic

class SubSubtopicInline(admin.TabularInline):
    model = SubSubtopic
    extra = 1

# update your SubtopicAdmin to include the inline
class SubtopicAdmin(admin.ModelAdmin):
    inlines = [SubSubtopicInline]
    
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
        "subtopic",
        "learning_goal",
        "activity_type",
        "difficulty",
        "category",
        "is_active",
        "download_count",
    )

    list_filter = (
        "topic",
        "subtopic",
        "learning_goal",
        "activity_type",
        "difficulty",
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )

    readonly_fields = (
        "download_count",
        "created_at",
    )



# @admin.register(ResourceDownload)
# class ResourceDownloadAdmin(admin.ModelAdmin):


#     list_display = (
#         "resource",
#         "user",
#         "ip_address",
#         "downloaded_at",
#     )

#     search_fields = (
#         "resource__title",
#         "user__username",
#         "ip_address",
#     )

#     readonly_fields = (
#         "resource",
#         "user",
#         "ip_address",
#         "downloaded_at",
#         "user_agent",
#     )

#     ordering = (
#         "-downloaded_at",
#     )

#     list_per_page = 50

@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ("resource",)

def has_add_permission(self, request):
    return False

# for data driven menu 
from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'parent',
        'order'
    )

    list_filter = (
        'parent',
    )

    ordering = (
        'parent',
        'order'
    )
