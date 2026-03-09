from django.contrib import admin
from .models import Pipeline, Deal, Task

@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_default')

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'pipeline', 'stage', 'amount', 'deal_owner')
    list_filter = ('pipeline', 'stage')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'priority', 'status')
    list_filter = ('priority', 'status', 'due_date')
    search_fields = ('title',)
