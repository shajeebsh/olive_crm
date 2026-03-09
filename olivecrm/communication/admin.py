from django.contrib import admin
from .models import EmailAccount, WhatsAppMessage

@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'user', 'last_synced', 'is_active')

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ('contact', 'direction', 'status', 'sent_at')
    list_filter = ('direction', 'status')
