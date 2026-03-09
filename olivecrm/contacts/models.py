from django.db import models
from django.contrib.auth.models import User
from wagtail.fields import RichTextField
from olivecrm.core.models import TimeStampedModel

LEAD_STATUS_CHOICES = [
    ('cold', 'Cold'),
    ('warm', 'Warm'),
    ('hot', 'Hot'),
    ('customer', 'Customer'),
    ('inactive', 'Inactive'),
]

class Company(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='companies/', blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    employee_count = models.IntegerField(null=True, blank=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Address
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Relationships
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    domain = models.CharField(max_length=100, unique=True)  # For company auto-discovery
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(TimeStampedModel):
    # Basic Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='contacts/', blank=True)
    
    # Contact Details
    emails = models.JSONField(default=list)  # [{'type': 'work', 'email': '...', 'primary': True}]
    phones = models.JSONField(default=list)  # [{'type': 'mobile', 'number': '...'}]
    social_media = models.JSONField(default=dict)  # {'linkedin': 'url', 'twitter': 'handle'}
    
    # Relationships
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    contact_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_contacts')
    
    # Sales Intelligence
    lead_status = models.CharField(max_length=50, choices=LEAD_STATUS_CHOICES, default='cold')
    lead_score = models.IntegerField(default=0)  # Auto-calculated by AI
    source = models.CharField(max_length=100, blank=True)  # Where did they come from?
    
    # Timestamps inherited from TimeStampedModel
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            # models.Index(fields=['email']), # emails is JSONField, indexing it directly might be tricky depending on DB
            models.Index(fields=['lead_score']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interaction(models.Model):
    INTERACTION_TYPES = [
        ('email', 'Email'),
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('chat', 'Chat'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    content = RichTextField()  # Wagtail Rich Text
    datetime = models.DateTimeField(auto_now_add=True)
    
    # Relationships
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Metadata
    attachments = models.JSONField(default=list)  # Store file paths/URLs
    is_private = models.BooleanField(default=False)  # Only visible to owner/manager

    def __str__(self):
        return f"{self.type} - {self.subject}"
