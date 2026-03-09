from django.contrib import admin
from .models import Invoice, LineItem, Payment

class LineItemInline(admin.TabularInline):
    model = LineItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'contact', 'status', 'total_amount', 'amount_paid', 'issue_date')
    list_filter = ('status', 'issue_date')
    search_fields = ('number', 'contact__first_name', 'contact__last_name')
    inlines = [LineItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method')
