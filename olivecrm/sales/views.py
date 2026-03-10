from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Deal, Task

@login_required
def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'sales/deal_list.html', {'deals': deals})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'sales/task_list.html', {'tasks': tasks})
