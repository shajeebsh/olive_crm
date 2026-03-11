from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Contact, Company
from .forms import ContactForm, CompanyForm
from olivecrm.core.utils import ExportCSVView
from olivecrm.sales.models import Deal
from olivecrm.invoicing.models import Invoice

@login_required
def contact_list(request):
    query = request.GET.get('q')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(company__name__icontains=query)
        )
    
    deals = Deal.objects.filter(contact__in=contacts)
    metrics = {
        'total': contacts.count(),
        'total_deals': deals.count(),
        'total_deal_value': deals.aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    return render(request, 'contacts/contact_list.html', {'contacts': contacts, 'metrics': metrics})

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contacts:contact_list')

class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contacts:contact_list')

class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contacts:contact_list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("", status=200)
        return redirect(self.success_url)

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'

@login_required
def company_list(request):
    query = request.GET.get('q')
    companies = Company.objects.all()
    if query:
        companies = companies.filter(
            Q(name__icontains=query) | 
            Q(industry__icontains=query) | 
            Q(domain__icontains=query)
        )
    
    invoices = Invoice.objects.filter(company__in=companies)
    metrics = {
        'total': companies.count(),
        'total_contacts': Contact.objects.filter(company__in=companies).count(),
        'total_invoices': invoices.count(),
        'total_invoice_value': invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    return render(request, 'contacts/company_list.html', {'companies': companies, 'metrics': metrics})

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contacts/company_form.html'
    success_url = reverse_lazy('contacts:company_list')

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'contacts/company_form.html'
    success_url = reverse_lazy('contacts:company_list')

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('contacts:company_list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("", status=200)
        return redirect(self.success_url)

class ContactExportView(ExportCSVView):
    model = Contact
    filename = "contacts.csv"
