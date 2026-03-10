from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Contact, Company
from .forms import ContactForm, CompanyForm
from olivecrm.core.utils import ExportCSVView

@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contacts:contact_list')

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'contacts/company_list.html', {'companies': companies})

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contacts/company_form.html'
    success_url = reverse_lazy('contacts:company_list')

class ContactExportView(ExportCSVView):
    model = Contact
    filename = "contacts.csv"
