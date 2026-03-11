import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.utils import timezone


# ── Helper ────────────────────────────────────────────────────────────────────

def _get_range(request):
    from .forms import DateRangeForm
    today = timezone.now().date()
    form  = DateRangeForm(request.GET or None)
    if form.is_valid():
        return form, *form.get_date_range()
    return form, today.replace(day=1), today


# ── Index View ────────────────────────────────────────────────────────────────

class ReportsIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reporting/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import DateRangeForm
        
        context['active_tab'] = self.request.GET.get('tab', 'sales')
        context['tab'] = context['active_tab']
        context['period'] = self.request.GET.get('period', 'month')
        context['tabs'] = [
            ('sales', 'Sales'),
            ('revenue', 'Revenue'),
            ('contacts', 'Contacts'),
            ('performance', 'Performance'),
        ]
        context['periods'] = DateRangeForm.PERIOD_CHOICES[:4]  # don't show custom here directly
        return context


# ── Sales Report ──────────────────────────────────────────────────────────────

class SalesReportView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.sales.models import Deal

        form, date_from, date_to = _get_range(request)

        deals = Deal.objects.filter(
            created_at__date__range=(date_from, date_to)
        )

        total_value = deals.aggregate(total=Sum('amount'))['total'] or 0
        total_count = deals.count()
        won = deals.filter(stage='Closed Won').count()
        lost = deals.filter(stage='Closed Lost').count()
        win_rate = round((won / (won + lost) * 100), 1) if (won + lost) > 0 else 0
        avg_deal = deals.aggregate(avg=Avg('amount'))['avg'] or 0

        by_stage = list(
            deals.values('stage')
                 .annotate(count=Count('id'), value=Sum('amount'))
                 .order_by('stage')
        )
        
        # Monthly trend still shows last 12 months from the end date
        from datetime import timedelta
        year_ago = date_to - timedelta(days=365)
        monthly = list(
            Deal.objects.filter(created_at__date__gte=year_ago)
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('id'), value=Sum('amount'))
                .order_by('month')
        )

        context = {
            'form': form,
            'tab': 'sales',
            'active_period': request.GET.get('period', 'month'),
            'date_from': date_from,
            'date_to': date_to,
            'total_value': total_value,
            'total_count': total_count,
            'win_rate': win_rate,
            'avg_deal': avg_deal,
            'by_stage': by_stage,
            'monthly': monthly,
            'deals': deals.select_related('contact', 'deal_owner')[:20],
            'period': request.GET.get('period', 'month'),
        }
        return render(request, 'reporting/partials/sales_tab.html', context)


# ── Revenue Report ────────────────────────────────────────────────────────────

class RevenueReportView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.invoicing.models import Invoice

        form, date_from, date_to = _get_range(request)

        invoices = Invoice.objects.filter(issue_date__range=(date_from, date_to))

        total_invoiced = invoices.aggregate(t=Sum('total_amount'))['t'] or 0
        total_paid = invoices.filter(status='paid').aggregate(t=Sum('total_amount'))['t'] or 0
        outstanding = total_invoiced - total_paid
        overdue = invoices.filter(status='overdue').aggregate(t=Sum('total_amount'))['t'] or 0

        by_status = list(
            invoices.values('status')
                    .annotate(count=Count('id'), value=Sum('total_amount'))
        )

        from datetime import timedelta
        year_ago = date_to - timedelta(days=365)
        monthly_revenue = list(
            Invoice.objects.filter(
                status='paid',
                issue_date__gte=year_ago
            ).annotate(month=TruncMonth('issue_date'))
             .values('month')
             .annotate(value=Sum('total_amount'))
             .order_by('month')
        )

        context = {
            'form': form,
            'tab': 'revenue',
            'active_period': request.GET.get('period', 'month'),
            'date_from': date_from,
            'date_to': date_to,
            'total_invoiced': total_invoiced,
            'total_paid': total_paid,
            'outstanding': outstanding,
            'overdue': overdue,
            'by_status': by_status,
            'monthly_revenue': monthly_revenue,
            'invoices': invoices.select_related('contact')[:20],
            'period': request.GET.get('period', 'month'),
            'total_count': invoices.count(),
        }
        return render(request, 'reporting/partials/revenue_tab.html', context)


# ── Contacts Report ───────────────────────────────────────────────────────────

class ContactsReportView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.contacts.models import Contact

        form, date_from, date_to = _get_range(request)

        contacts = Contact.objects.filter(created_at__date__range=(date_from, date_to))

        by_status = list(
            contacts.values('lead_status').annotate(count=Count('id'))
        )

        from datetime import timedelta
        year_ago = date_to - timedelta(days=365)
        monthly_new = list(
            Contact.objects.filter(created_at__date__gte=year_ago)
                .annotate(month=TruncMonth('created_at'))
                .values('month')
                .annotate(count=Count('id'))
                .order_by('month')
        )

        context = {
            'form': form,
            'tab': 'contacts',
            'active_period': request.GET.get('period', 'month'),
            'date_from': date_from,
            'date_to': date_to,
            'total_count': contacts.count(),
            'total': contacts.count(),
            'hot': contacts.filter(lead_status='hot').count(),
            'warm': contacts.filter(lead_status='warm').count(),
            'cold': contacts.filter(lead_status='cold').count(),
            'by_status': by_status,
            'monthly_new': monthly_new,
            'contacts': contacts.select_related('company')[:20],
            'period': request.GET.get('period', 'month'),
        }
        return render(request, 'reporting/partials/contacts_tab.html', context)


# ── Performance Report ────────────────────────────────────────────────────────

class PerformanceReportView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.sales.models import Deal, Task

        form, date_from, date_to = _get_range(request)

        leaderboard = list(
            Deal.objects.filter(
                created_at__date__range=(date_from, date_to),
                stage='Closed Won'
            ).values(
                'deal_owner__first_name',
                'deal_owner__last_name',
                'deal_owner__username'
            ).annotate(
                deals_won=Count('id'),
                revenue=Sum('amount')
            ).order_by('-revenue')
        )

        deals = Deal.objects.filter(created_at__date__range=(date_from, date_to))
        stage_counts = list(
            deals.values('stage')
                 .annotate(count=Count('id'))
                 .order_by('stage')
        )

        now = timezone.now()
        tasks = Task.objects.filter(due_date__date__range=(date_from, date_to))
        
        tasks_total = tasks.count()
        tasks_done = tasks.filter(status='completed').count()
        tasks_overdue = Task.objects.filter(due_date__lt=now, status__in=['pending', 'in_progress']).count()
        task_completion_rate = round((tasks_done / tasks_total * 100), 1) if tasks_total > 0 else 0

        context = {
            'form': form,
            'tab': 'performance',
            'active_period': request.GET.get('period', 'month'),
            'date_from': date_from,
            'date_to': date_to,
            'total_count': deals.count(),
            'leaderboard': leaderboard,
            'stage_counts': stage_counts,
            'tasks_total': tasks_total,
            'tasks_done': tasks_done,
            'tasks_overdue': tasks_overdue,
            'task_completion_rate': task_completion_rate,
            'period': request.GET.get('period', 'month'),
        }
        return render(request, 'reporting/partials/performance_tab.html', context)


# ── CSV Exports ───────────────────────────────────────────────────────────────

class ExportSalesCSVView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.sales.models import Deal

        form, date_from, date_to = _get_range(request)
        deals = Deal.objects.filter(
            created_at__date__range=(date_from, date_to)
        ).select_related('contact', 'deal_owner')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Deal Name', 'Contact', 'Amount', 'Stage', 'Expected Close', 'Owner'])
        for deal in deals:
            writer.writerow([
                deal.name,
                str(deal.contact) if deal.contact else '',
                deal.amount,
                deal.stage,
                deal.expected_close_date,
                str(deal.deal_owner) if deal.deal_owner else '',
            ])
        return response


class ExportRevenueCSVView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.invoicing.models import Invoice

        form, date_from, date_to = _get_range(request)
        invoices = Invoice.objects.filter(
            issue_date__range=(date_from, date_to)
        ).select_related('contact')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="revenue_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Invoice Number', 'Contact', 'Total Amount', 'Status', 'Issue Date'])
        for inv in invoices:
            writer.writerow([
                inv.number,
                str(inv.contact) if inv.contact else '',
                inv.total_amount,
                inv.status,
                inv.issue_date,
            ])
        return response


class ExportContactsCSVView(LoginRequiredMixin, View):
    def get(self, request):
        from olivecrm.contacts.models import Contact

        form, date_from, date_to = _get_range(request)
        contacts = Contact.objects.filter(
            created_at__date__range=(date_from, date_to)
        ).select_related('company')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contacts_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Company', 'Lead Status', 'Lead Score', 'Created At'])
        for contact in contacts:
            writer.writerow([
                str(contact),
                str(contact.company) if contact.company else '',
                contact.lead_status,
                contact.lead_score,
                contact.created_at.date(),
            ])
        return response
