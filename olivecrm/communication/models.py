from django.db import models
from django.contrib.auth.models import User
from olivecrm.contacts.models import Contact

class EmailAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_address = models.EmailField()
    imap_server = models.CharField(max_length=200)
    imap_port = models.IntegerField(default=993)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)  # Should be encrypted in production
    
    last_synced = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email_address

class WhatsAppMessage(models.Model):
    DIRECTION_CHOICES = [('inbound', 'Inbound'), ('outbound', 'Outbound')]
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=100, unique=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    content = models.TextField()
    media_url = models.URLField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, default='sent')  # sent, delivered, read
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.direction} - {self.contact}"
