from django.contrib import admin
from .models import Partner

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'commission_rate', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'email')
