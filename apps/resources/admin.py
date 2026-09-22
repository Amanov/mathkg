from django.contrib import admin

from .models import (
    Topic,
    Subtopic,
    SubSubtopic,
    Resource,
    ResourceDownload,
    SiteVisit,
    ButtonClick,
    LoginEvent,
    MenuItem,
    Question,
    Exam,
    ExamQuestion,
    ExamAttempt,
    ExamAnswer,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


class SubSubtopicInline(admin.TabularInline):
    model = SubSubtopic
    extra = 1


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


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "question_type", "topic", "subtopic", "subsubtopic", "marks", "created_by")
    list_filter = ("question_type", "topic", "subtopic", "subsubtopic")
    search_fields = ("text",)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "access_code", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "access_code")
    readonly_fields = ("access_code", "created_at")
    inlines = [ExamQuestionInline]


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ("student_name", "exam", "score", "started_at", "submitted_at")
    list_filter = ("exam",)
    search_fields = ("student_name",)
    readonly_fields = ("started_at",)


@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_choice", "is_correct")
    list_filter = ("is_correct",)
