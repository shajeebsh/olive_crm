from django import forms
from .models import Contact, Company

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'company', 'emails', 'lead_status', 'tags']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'emails': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '[{"email": "...", "primary": true}]'}),
            'lead_status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'comma, separated, tags'}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'domain', 'industry', 'address', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'domain': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
