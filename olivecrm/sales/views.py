from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import Deal, Task
from .forms import DealForm, TaskForm
from olivecrm.core.utils import ExportCSVView

@login_required
def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'sales/deal_list.html', {'deals': deals})

class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'sales/deal_form.html'
    success_url = reverse_lazy('sales:deal_list')

class DealDetailView(LoginRequiredMixin, DetailView):
    model = Deal
    template_name = 'sales/deal_detail.html'

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'sales/task_list.html', {'tasks': tasks})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'sales/task_form.html'
    success_url = reverse_lazy('sales:task_list')

class PipelineKanbanView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/pipeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Deal
        # Predefined stages for the Kanban board
        stages = [
            {'name': 'Lead', 'deals': Deal.objects.filter(stage='Lead')},
            {'name': 'Qualified', 'deals': Deal.objects.filter(stage='Qualified')},
            {'name': 'Proposal', 'deals': Deal.objects.filter(stage='Proposal')},
            {'name': 'Negotiation', 'deals': Deal.objects.filter(stage='Negotiation')},
            {'name': 'Closed Won', 'deals': Deal.objects.filter(stage='Closed Won')},
        ]
        context['stages'] = stages
        return context

class DealExportView(ExportCSVView):
    model = Deal
    filename = "deals.csv"
