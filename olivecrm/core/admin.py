from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'object_type', 'object_id')
    list_filter = ('action', 'object_type', 'timestamp')
    readonly_fields = ('timestamp', 'user', 'action', 'object_type', 'object_id', 'changes')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
