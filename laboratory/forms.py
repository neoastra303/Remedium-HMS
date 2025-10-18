from django import forms
from .models import LabTest

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        requested_date = cleaned_data.get('requested_date')
        result_date = cleaned_data.get('result_date')
        result = cleaned_data.get('result')
        status = cleaned_data.get('status')

        if requested_date and result_date and result_date < requested_date:
            self.add_error('result_date', "Result date cannot be earlier than the requested date.")

        if status == "Completed":
            if not result:
                self.add_error('result', "Result is required when status is 'Completed'.")
            if not result_date:
                self.add_error('result_date', "Result date is required when status is 'Completed'.")
        
        return cleaned_data
