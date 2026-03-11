from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from olivecrm.sales.models import Deal, Task
from olivecrm.contacts.models import Contact

@login_required
def dashboard(request):
    # Live metrics for the dashboard
    context = {
        'deals_this_month': Deal.objects.count(),
        'revenue_this_month': sum(d.amount for d in Deal.objects.all() if d.amount) or 0,
        'new_contacts': Contact.objects.count(),
        'active_tasks': Task.objects.filter(status='pending').count(),
        'recent_deals': Deal.objects.all().order_by('-id')[:5],
        'recent_tasks': Task.objects.all().order_by('due_date')[:5]
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'core/settings.html')

class SettingsOrganizationView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/organization.html'
