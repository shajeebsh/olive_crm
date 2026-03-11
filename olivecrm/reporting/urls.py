from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('',              views.ReportsIndexView.as_view(),      name='index'),
    path('sales/',        views.SalesReportView.as_view(),       name='sales'),
    path('revenue/',      views.RevenueReportView.as_view(),     name='revenue'),
    path('contacts/',     views.ContactsReportView.as_view(),    name='contacts'),
    path('performance/',  views.PerformanceReportView.as_view(), name='performance'),
    path('export/sales/',     views.ExportSalesCSVView.as_view(),    name='export_sales'),
    path('export/revenue/',   views.ExportRevenueCSVView.as_view(),  name='export_revenue'),
    path('export/contacts/',  views.ExportContactsCSVView.as_view(), name='export_contacts'),
]
