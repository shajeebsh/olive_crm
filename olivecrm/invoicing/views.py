from django.db.models import Q, Sum
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
    
    # Calculate metrics
    metrics = {
        'total': {
            'count': invoices.count(),
            'amount': invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        },
        'paid': {
            'count': invoices.filter(status='paid').count(),
            'amount': invoices.filter(status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        },
        'overdue': {
            'count': invoices.filter(status='overdue').count(),
            'amount': invoices.filter(status='overdue').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        },
        'cancelled': {
            'count': invoices.filter(status='cancelled').count(),
            'amount': invoices.filter(status='cancelled').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        }
    }
    
    return render(request, 'invoicing/invoice_list.html', {'invoices': invoices, 'metrics': metrics})

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
