from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('export/', views.ContactExportView.as_view(), name='contact_export'),
]
