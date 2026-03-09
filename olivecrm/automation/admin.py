from django.contrib import admin
from .models import Workflow

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'trigger_type', 'is_active', 'created_at')
    list_filter = ('trigger_type', 'is_active')
