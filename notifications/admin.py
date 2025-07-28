from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'from_user', 'notification_type', 'is_read', 'created_at', 'message_preview')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('to_user__username', 'from_user__username', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_read',)
    
    fieldsets = (
        ('Utilisateurs', {
            'fields': ('to_user', 'from_user')
        }),
        ('Notification', {
            'fields': ('notification_type', 'message', 'is_read')
        }),
        ('Références', {
            'fields': ('post', 'comment'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('to_user', 'from_user', 'post', 'comment')

admin.site.register(Notification, NotificationAdmin)
