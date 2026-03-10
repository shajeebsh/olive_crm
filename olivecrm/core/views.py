from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from olivecrm.sales.models import Deal
from olivecrm.contacts.models import Contact

@login_required
def dashboard(request):
    from olivecrm.sales.models import Deal
    # Mock some data for the dashboard
    context = {
        'deals_this_month': 12,
        'revenue_this_month': 45000,
        'new_contacts': 8,
        'active_tasks': 5,
        'recent_deals': Deal.objects.all().order_by('-id')[:5]
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'core/settings.html')
