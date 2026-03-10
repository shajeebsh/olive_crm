from django import forms
from .models import Invoice, LineItem, Payment

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'contact', 'company', 'issue_date', 'due_date', 'status', 'currency', 'notes', 'terms']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
