from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Contact, Company

@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'contacts/company_list.html', {'companies': companies})
