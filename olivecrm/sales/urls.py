from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.deal_list, name='deal_list'),
    path('create/', views.DealCreateView.as_view(), name='deal_create'),
    path('<int:pk>/', views.DealDetailView.as_view(), name='deal_detail'),
    path('<int:pk>/edit/', views.DealUpdateView.as_view(), name='deal_edit'),
    path('<int:pk>/delete/', views.DealDeleteView.as_view(), name='deal_delete'),
    
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    
    path('export/', views.DealExportView.as_view(), name='deal_export'),
    path('pipeline/', views.PipelineKanbanView.as_view(), name='pipeline_kanban'),
]
