from django.db import models
from django.contrib.auth.models import User

class Workflow(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Trigger Configuration
    TRIGGER_TYPES = [
        ('record_created', 'Record Created'),
        ('record_updated', 'Record Updated'),
        ('field_changed', 'Specific Field Changed'),
        ('date_reached', 'Date Field Reached'),
        ('incoming_email', 'Incoming Email'),
        ('form_submitted', 'Form Submitted'),
    ]
    
    trigger_type = models.CharField(max_length=50, choices=TRIGGER_TYPES)
    trigger_config = models.JSONField()  # e.g., {"object_type": "Contact", "field": "lead_status", "value": "hot"}
    
    # Conditions (JSON logic)
    conditions = models.JSONField(default=list)  # Additional filters
    
    # Actions
    actions = models.JSONField()  # List of actions to perform
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def check_conditions(self, context_object):
        """Placeholder for condition checking logic"""
        return True

    def execute_action(self, action, context_object):
        """Placeholder for action execution logic"""
        print(f"Executing action {action['type']} on {context_object}")

    def execute(self, context_object):
        """Execute workflow actions on the context object"""
        if self.check_conditions(context_object):
            for action in self.actions:
                self.execute_action(action, context_object)
