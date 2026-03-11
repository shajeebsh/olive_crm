from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice
from .forms import InvoiceForm
from olivecrm.core.utils import ExportCSVView

@login_required
def invoice_list(request):
    query = request.GET.get('q')
    invoices = Invoice.objects.all()
    if query:
        invoices = invoices.filter(
            Q(number__icontains=query)
        )
    return render(request, 'invoicing/invoice_list.html', {'invoices': invoices})

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoicing/invoice_form.html'
    success_url = reverse_lazy('invoicing:list')

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoicing/invoice_form.html'
    success_url = reverse_lazy('invoicing:list')

class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoicing:list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("", status=200)
        return redirect(self.success_url)

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoicing/invoice_detail.html'

class InvoiceExportView(ExportCSVView):
    model = Invoice
    filename = "invoices.csv"

@login_required
def mark_invoice_sent(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'sent'
    invoice.save()
    return redirect('invoicing:detail', pk=pk)

@login_required
def mark_invoice_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'paid'
    invoice.save()
    return redirect('invoicing:detail', pk=pk)
