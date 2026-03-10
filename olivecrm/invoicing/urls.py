from django.urls import path
from . import views

app_name = 'invoicing'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('create/', views.InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('export/', views.InvoiceExportView.as_view(), name='invoice_export'),
]
