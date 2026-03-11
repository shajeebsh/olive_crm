from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Deal, Task
from .forms import DealForm, TaskForm
from olivecrm.core.utils import ExportCSVView

@login_required
def deal_list(request):
    query = request.GET.get('q')
    deals = Deal.objects.all()
    if query:
        deals = deals.filter(
            Q(name__icontains=query) | 
            Q(stage__icontains=query)
        )
    return render(request, 'sales/deal_list.html', {'deals': deals})

class DealCreateView(LoginRequiredMixin, CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'sales/deal_form.html'
    success_url = reverse_lazy('sales:deal_list')

class DealUpdateView(LoginRequiredMixin, UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'sales/deal_form.html'
    success_url = reverse_lazy('sales:deal_list')

class DealDeleteView(LoginRequiredMixin, DeleteView):
    model = Deal
    success_url = reverse_lazy('sales:deal_list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("", status=200)
        return redirect(self.success_url)

class DealDetailView(LoginRequiredMixin, DetailView):
    model = Deal
    template_name = 'sales/deal_detail.html'

@login_required
def task_list(request):
    query = request.GET.get('q')
    tasks = Task.objects.all()
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    return render(request, 'sales/task_list.html', {'tasks': tasks})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'sales/task_form.html'
    success_url = reverse_lazy('sales:task_list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'sales/task_form.html'
    success_url = reverse_lazy('sales:task_list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('sales:task_list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        if request.headers.get('HX-Request'):
            return HttpResponse("", status=200)
        return redirect(self.success_url)

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
