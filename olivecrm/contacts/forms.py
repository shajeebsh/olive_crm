from django import forms
from .models import Contact, Company

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'title', 'company', 'emails', 'lead_status']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'emails': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '[{"email": "...", "primary": true}]'}),
            'lead_status': forms.Select(attrs={'class': 'form-select'}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'domain', 'industry', 'website', 'employee_count', 'annual_revenue', 'billing_address', 'shipping_address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'domain': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'employee_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'annual_revenue': forms.NumberInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
