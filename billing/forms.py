from django import forms
from .models import Invoice
from django.utils import timezone

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['patient', 'issue_date', 'due_date', 'total_amount', 'paid', 'insurance_claimed', 'details']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make dates not required since they have defaults
        self.fields['issue_date'].required = False
        self.fields['due_date'].required = False
