from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Deal, Task
from .forms import DealForm, TaskForm
from olivecrm.core.utils import ExportCSVView

@login_required
def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'sales/deal_list.html', {'deals': deals})

class DealCreateView(CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'sales/deal_form.html'
    success_url = reverse_lazy('sales:deal_list')

class DealDetailView(DetailView):
    model = Deal
    template_name = 'sales/deal_detail.html'

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'sales/task_list.html', {'tasks': tasks})

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'sales/task_form.html'
    success_url = reverse_lazy('sales:task_list')

class DealExportView(ExportCSVView):
    model = Deal
    filename = "deals.csv"
