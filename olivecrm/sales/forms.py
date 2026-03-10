from django import forms
from .models import Deal, Task

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['name', 'amount', 'currency', 'pipeline', 'stage', 'stage_order', 'contact', 'company', 'expected_close_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'pipeline': forms.Select(attrs={'class': 'form-select'}),
            'stage': forms.TextInput(attrs={'class': 'form-control'}),
            'stage_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'expected_close_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'contact', 'deal']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'deal': forms.Select(attrs={'class': 'form-select'}),
        }
