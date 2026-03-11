from decimal import Decimal
from django.db import models
from django.conf import settings
from olivecrm.contacts.models import Contact, Company
from olivecrm.core.models import TimeStampedModel

class Invoice(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('overdue', 'Overdue'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    number = models.CharField(max_length=50, unique=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='invoices')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    issue_date = models.DateField()
    due_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    currency = models.CharField(max_length=10, default='USD')
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)

    def __str__(self):
        return f"Invoice {self.number} - {self.contact}"

    def update_totals(self):
        self.subtotal = sum(item.total for item in self.line_items.all())
        # Simplified tax calculation (e.g., 10%)
        self.tax_total = self.subtotal * Decimal('0.1') 
        self.total_amount = self.subtotal + self.tax_total
        self.save()

class LineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items')
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.invoice.update_totals()

class Payment(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)  # Stripe, Bank Transfer, PayPal
    transaction_id = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.invoice.amount_paid += self.amount
        if self.invoice.amount_paid >= self.invoice.total_amount:
            self.invoice.status = 'paid'
        self.invoice.save()
