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

    def clean_total_amount(self):
        total_amount = self.cleaned_data.get('total_amount')
        if total_amount and total_amount < 0:
            raise forms.ValidationError("Total amount cannot be negative.")
        return total_amount

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get("issue_date")
        due_date = cleaned_data.get("due_date")

        if issue_date and due_date and due_date < issue_date:
            raise forms.ValidationError(
                "Due date cannot be before the issue date."
            )
