from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from olivecrm.sales.models import Deal
from olivecrm.contacts.models import Contact

@login_required
def dashboard(request):
    # Mock some data for the dashboard
    context = {
        'deals_this_month': 12,
        'revenue_this_month': 45000,
        'new_contacts': 8,
        'active_tasks': 5,
    }
    return render(request, 'core/dashboard.html', context)
