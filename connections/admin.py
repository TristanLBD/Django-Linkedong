from django.contrib import admin
from .models import Connection

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'from_user__email', 'to_user__username', 'to_user__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Utilisateurs', {
            'fields': ('from_user', 'to_user')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('from_user', 'to_user')

admin.site.register(Connection, ConnectionAdmin)
