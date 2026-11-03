import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import (
    Topic,
    Subtopic,
    SubSubtopic,
    Resource,
    ResourceDownload,
    SiteVisit,
    ButtonClick,
    SearchQuery,
    LoginEvent,
    MenuItem,
    NewsPost,
    PageFreeDownload,
    PageReaction,
    PageReactionCount,
    WrittenFeedback,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "title_ru", "slug")
    search_fields = ("title", "title_ru", "slug")
    prepopulated_fields = {"slug": ("title",)}


class SubSubtopicInline(admin.TabularInline):
    model = SubSubtopic
    extra = 1


@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "title_ru",
        "topic",
    )
    search_fields = ("title", "title_ru")

    list_filter = (
        "topic",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [SubSubtopicInline]


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
        "subtopic",
        "subsubtopic",
        "learning_goal",
        "activity_type",
        "difficulty",
        "category",
        "is_active",
        "download_count",
    )

    # Editable straight from the list: filter by Topic in the sidebar (below)
    # to narrow the rows down, then pick Subtopic/Sub-subtopic/Learning goal
    # from the dropdowns on each row and hit "Save" - no need to open every
    # Resource's own edit page one at a time.
    list_display_links = ("title",)

    list_editable = (
        "topic",
        "subtopic",
        "subsubtopic",
        "learning_goal",
    )

    list_filter = (
        "topic",
        "subtopic",
        "subsubtopic",
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


@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):

    list_display = (
        "resource",
        "user",
        "ip_address",
        "downloaded_at",
    )

    search_fields = (
        "resource__title",
        "user__username",
        "ip_address",
    )

    readonly_fields = (
        "resource",
        "user",
        "ip_address",
        "downloaded_at",
        "user_agent",
    )

    ordering = (
        "-downloaded_at",
    )

    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):

    list_display = (
        "path",
        "user",
        "ip_address",
        "visited_at",
    )

    list_filter = (
        "visited_at",
    )

    search_fields = (
        "path",
        "user__username",
        "ip_address",
        "session_key",
    )

    readonly_fields = (
        "session_key",
        "user",
        "ip_address",
        "path",
        "visited_at",
    )

    ordering = (
        "-visited_at",
    )

    date_hierarchy = "visited_at"

    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(ButtonClick)
class ButtonClickAdmin(admin.ModelAdmin):

    list_display = (
        "label",
        "path",
        "user",
        "ip_address",
        "clicked_at",
    )

    list_filter = (
        "clicked_at",
    )

    search_fields = (
        "label",
        "path",
        "user__username",
        "ip_address",
    )

    readonly_fields = (
        "label",
        "path",
        "session_key",
        "user",
        "ip_address",
        "clicked_at",
    )

    ordering = (
        "-clicked_at",
    )

    date_hierarchy = "clicked_at"

    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):

    list_display = (
        "query",
        "results_count",
        "user",
        "ip_address",
        "searched_at",
    )

    list_filter = (
        "searched_at",
    )

    search_fields = (
        "query",
        "user__username",
        "ip_address",
    )

    readonly_fields = (
        "query",
        "results_count",
        "session_key",
        "user",
        "ip_address",
        "searched_at",
    )

    ordering = (
        "-searched_at",
    )

    date_hierarchy = "searched_at"

    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "ip_address",
        "logged_in_at",
    )

    list_filter = (
        "logged_in_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "ip_address",
    )

    readonly_fields = (
        "user",
        "session_key",
        "ip_address",
        "logged_in_at",
    )

    ordering = (
        "-logged_in_at",
    )

    date_hierarchy = "logged_in_at"

    list_per_page = 50

    def has_add_permission(self, request):
        return False


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'parent',
        'order',
        'link_target',
    )

    list_filter = (
        'parent',
    )

    ordering = (
        'parent',
        'order'
    )

    fields = (
        'title',
        'parent',
        'order',
        'topic',
        'subtopic',
        'subsubtopic',
        'url_name',
    )

    @admin.display(description='Links to')
    def link_target(self, obj):
        if obj.subsubtopic_id or obj.subtopic_id or obj.topic_id:
            return obj.get_resolved_url() or '(broken topic link)'
        if obj.url_name:
            return obj.url_name
        return '—'


@admin.register(PageFreeDownload)
class PageFreeDownloadAdmin(admin.ModelAdmin):
    list_display = ('page_key', 'resource', 'pinned')
    list_editable = ('pinned',)
    search_fields = ('page_key', 'resource__title')
    autocomplete_fields = ('resource',)

    def save_model(self, request, obj, form, change):
        # Picking a different file in admin is an override. Pin it so the
        # next page visit does not replace that choice with a new random one.
        if 'resource' in form.changed_data and obj.resource_id:
            obj.pinned = True
        super().save_model(request, obj, form, change)


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date")
    list_editable = ("published_date",)
    search_fields = ("title", "body")
    ordering = ("-published_date",)


@admin.register(PageReaction)
class PageReactionAdmin(admin.ModelAdmin):
    list_display = ("face", "path", "material", "created_at")
    list_filter = ("face", "created_at")
    search_fields = ("path", "material")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 50
    readonly_fields = (
        "path",
        "face",
        "material",
        "topic",
        "subtopic",
        "subsubtopic",
        "visitor_key",
        "created_at",
    )

    def has_add_permission(self, request):
        return False


@admin.register(PageReactionCount)
class PageReactionCountAdmin(admin.ModelAdmin):
    """One row per page, sorted by most 🙁 first."""

    list_display = (
        "path",
        "material",
        "happy_count",
        "ok_count",
        "sad_count",
        "updated_at",
    )
    search_fields = ("path", "material")
    ordering = ("-sad_count", "-ok_count", "-happy_count", "path")
    list_per_page = 50
    readonly_fields = (
        "path",
        "material",
        "happy_count",
        "ok_count",
        "sad_count",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False


def export_feedback_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="feedback.csv"'
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow([
        "created_at",
        "type",
        "message",
        "name",
        "email",
        "about_page",
        "read",
        "show_on_site",
    ])
    for note in queryset.order_by("-created_at"):
        writer.writerow([
            note.created_at.isoformat(sep=" ", timespec="seconds"),
            note.get_kind_display(),
            note.message,
            note.name,
            note.email,
            note.about_page,
            "yes" if note.is_read else "no",
            "yes" if note.show_on_site else "no",
        ])
    return response


export_feedback_csv.short_description = "Export CSV"


@admin.action(description="Show on site")
def publish_feedback(modeladmin, request, queryset):
    queryset.update(show_on_site=True)


@admin.action(description="Hide on site")
def unpublish_feedback(modeladmin, request, queryset):
    queryset.update(show_on_site=False)


@admin.action(description="Mark as read")
def mark_feedback_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.register(WrittenFeedback)
class WrittenFeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "message_preview",
        "name",
        "email",
        "about_page",
        "is_read",
        "show_on_site",
        "created_at",
    )
    list_filter = ("kind", "is_read", "show_on_site", "created_at")
    list_editable = ("is_read", "show_on_site")
    search_fields = ("message", "name", "email", "about_page")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 50
    actions = (
        publish_feedback,
        unpublish_feedback,
        mark_feedback_read,
        export_feedback_csv,
    )

    @admin.display(description="Message")
    def message_preview(self, obj):
        text = " ".join(obj.message.split())
        if len(text) > 80:
            return text[:80] + "…"
        return text
