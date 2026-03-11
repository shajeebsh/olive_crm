from django.urls import path
from . import views

app_name = 'invoicing'

urlpatterns = [
    path('', views.invoice_list, name='list'),
    path('create/', views.InvoiceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='delete'),
    path('<int:pk>/mark-sent/', views.mark_invoice_sent, name='mark_sent'),
    path('<int:pk>/mark-paid/', views.mark_invoice_paid, name='mark_paid'),
    path('export/', views.InvoiceExportView.as_view(), name='export'),
]
