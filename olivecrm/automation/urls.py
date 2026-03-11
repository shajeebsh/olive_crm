from django.urls import path
from . import views

app_name = 'automation'

urlpatterns = [
    path('', views.AutomationIndexView.as_view(), name='index'),
]
