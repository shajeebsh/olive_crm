from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryIndexView.as_view(), name='index'),
]
