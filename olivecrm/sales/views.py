from django.db.models import Q, Sum
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
    
    # Calculate metrics
    metrics = {
        'total': {
            'count': deals.count(),
            'amount': deals.aggregate(Sum('amount'))['amount__sum'] or 0
        },
        'won': {
            'count': deals.filter(stage='Closed Won').count(),
            'amount': deals.filter(stage='Closed Won').aggregate(Sum('amount'))['amount__sum'] or 0
        },
        'lost': {
            'count': deals.filter(stage='Closed Lost').count(),
            'amount': deals.filter(stage='Closed Lost').aggregate(Sum('amount'))['amount__sum'] or 0
        },
        'pending': {
            'count': deals.exclude(stage__in=['Closed Won', 'Closed Lost']).count(),
            'amount': deals.exclude(stage__in=['Closed Won', 'Closed Lost']).aggregate(Sum('amount'))['amount__sum'] or 0
        }
    }
    
    return render(request, 'sales/deal_list.html', {'deals': deals, 'metrics': metrics})

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
        from django.contrib.auth.models import User

        # Read filter params
        request = self.request
        owner_id = request.GET.get('owner')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        # Base queryset with filters applied
        def filtered_deals(stage_name):
            qs = Deal.objects.filter(stage=stage_name)
            if owner_id:
                qs = qs.filter(deal_owner__id=owner_id)
            if date_from:
                qs = qs.filter(expected_close_date__gte=date_from)
            if date_to:
                qs = qs.filter(expected_close_date__lte=date_to)
            return qs

        stage_names = ['Lead', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
        stages = [{'name': s, 'deals': filtered_deals(s)} for s in stage_names]

        # Pass filter state back to template
        owners = User.objects.filter(deals__isnull=False).distinct()
        context['stages'] = stages
        context['owners'] = owners
        context['filter'] = {
            'owner': owner_id,
            'date_from': date_from or '',
            'date_to': date_to or '',
        }
        return context

class DealExportView(ExportCSVView):
    model = Deal
    filename = "deals.csv"
