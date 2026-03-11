from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class InventoryIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'inventory/index.html'
