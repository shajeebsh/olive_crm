from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class CommunicationsIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'communication/index.html'
