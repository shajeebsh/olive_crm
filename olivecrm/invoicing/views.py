from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Invoice
from .forms import InvoiceForm
from olivecrm.core.utils import ExportCSVView

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoicing/invoice_list.html', {'invoices': invoices})

class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoicing/invoice_form.html'
    success_url = reverse_lazy('invoicing:invoice_list')

class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoicing/invoice_detail.html'

class InvoiceExportView(ExportCSVView):
    model = Invoice
    filename = "invoices.csv"
