from django.db import models
from olivecrm.core.models import TimeStampedModel

class Partner(TimeStampedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage 0-100")
    status = models.CharField(max_length=20, default='active')  # active, inactive
    
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
