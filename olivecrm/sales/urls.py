from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.deal_list, name='deal_list'),
    path('tasks/', views.task_list, name='task_list'),
]
