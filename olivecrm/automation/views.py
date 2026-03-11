from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class AutomationIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'automation/index.html'
