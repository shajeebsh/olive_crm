from django.contrib import admin
from .models import MailingList, EmailCampaign

@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_public', 'created_at')
    search_fields = ('name',)

# EmailCampaign is usually managed via Wagtail Admin as a snippet, 
# but we can register it here too for standard Django Admin access.
@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'target_list', 'scheduled_time', 'sent_at')
    list_filter = ('sent_at', 'scheduled_time')
