import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View

class ExportCSVView(View):
    model = None
    filename = "export.csv"

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}"'
        
        writer = csv.writer(response)
        fields = [field.name for field in self.model._meta.fields]
        writer.writerow(fields)
        
        for obj in self.model.objects.all():
            writer.writerow([getattr(obj, field) for field in fields])
            
        return response

@login_required
def profile_view(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'core/settings.html')
