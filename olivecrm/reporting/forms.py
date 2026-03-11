from django import forms
from django.utils import timezone
import datetime

class DateRangeForm(forms.Form):
    PERIOD_CHOICES = [
        ('week',    'This Week'),
        ('month',   'This Month'),
        ('quarter', 'This Quarter'),
        ('year',    'This Year'),
        ('custom',  'Custom'),
    ]
    period    = forms.ChoiceField(choices=PERIOD_CHOICES, required=False)
    date_from = forms.DateField(required=False,
                    widget=forms.DateInput(attrs={
                        'type': 'date', 'class': 'form-control form-control-sm'
                    }))
    date_to   = forms.DateField(required=False,
                    widget=forms.DateInput(attrs={
                        'type': 'date', 'class': 'form-control form-control-sm'
                    }))

    def get_date_range(self):
        today   = timezone.now().date()
        period  = self.cleaned_data.get('period') or 'month'
        if period == 'week':
            return today - datetime.timedelta(days=7), today
        elif period == 'month':
            return today.replace(day=1), today
        elif period == 'quarter':
            m = ((today.month - 1) // 3) * 3 + 1
            return today.replace(month=m, day=1), today
        elif period == 'year':
            return today.replace(month=1, day=1), today
        elif period == 'custom':
            df = self.cleaned_data.get('date_from') or today.replace(day=1)
            dt = self.cleaned_data.get('date_to')   or today
            return (dt, df) if df > dt else (df, dt)
        return today.replace(day=1), today
