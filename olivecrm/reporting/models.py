from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard: {self.name}"

class DashboardWidget(models.Model):
    WIDGET_TYPES = [
        ('funnel', 'Sales Funnel'),
        ('chart', 'Chart'),
        ('kpi', 'KPI Card'),
        ('list', 'Recent Records'),
        ('calendar', 'Calendar'),
    ]
    
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    title = models.CharField(max_length=100)
    
    # Configuration (stored as JSON)
    config = models.JSONField(default=dict)  # Data source, filters, chart type
    
    # Layout
    row = models.IntegerField()
    col = models.IntegerField()
    width = models.IntegerField(default=4)  # Bootstrap grid columns (1-12)
    height = models.IntegerField(default=1)  # Custom height units
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
