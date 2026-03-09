from django.contrib import admin
from .models import Company, Contact, Interaction

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'domain', 'created_at')
    search_fields = ('name', 'domain')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'lead_status', 'lead_score')
    list_filter = ('lead_status', 'company')
    search_fields = ('first_name', 'last_name')

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ('type', 'subject', 'contact', 'datetime')
    list_filter = ('type', 'datetime')
