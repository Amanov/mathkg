from .models import Resource, ResourceDownload

@admin.register(ResourceDownload)
class ResourceDownloadAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'ip_address', 'downloaded_at')
    list_filter = ('downloaded_at', 'resource__category')
    search_fields = ('resource__title', 'user__username', 'ip_address')
    readonly_fields = ('resource', 'user', 'ip_address', 'downloaded_at', 'user_agent')
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation