from django.db import models
from django.contrib.auth.models import User
from olivecrm.contacts.models import Contact, Company

class Pipeline(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Sales Process", "Recruitment"
    stages = models.JSONField(default=list)  # [{'name': 'Lead', 'order': 1, 'probability': 10}, ...]
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Deal(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    
    # Pipeline Tracking
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT)
    stage = models.CharField(max_length=100)  # Current stage name
    stage_order = models.IntegerField()  # Denormalized for sorting
    probability = models.IntegerField(default=0)  # 0-100
    
    # Dates
    expected_close_date = models.DateField(null=True, blank=True)
    actual_close_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Relationships
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    deal_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='deals')
    
    # Additional
    products = models.JSONField(default=list)  # Simplified line items
    notes = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated
    
    class Meta:
        indexes = [
            models.Index(fields=['stage', 'expected_close_date']),
        ]

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Relationships
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Reminder
    reminder_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['due_date', '-priority']

    def __str__(self):
        return self.title
