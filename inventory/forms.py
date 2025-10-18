from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'unit', 'reorder_level']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and InventoryItem.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An inventory item with this name already exists.")
        return name

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if reorder_level and reorder_level < 0:
            raise forms.ValidationError("Reorder level cannot be negative.")
        return reorder_level

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        reorder_level = cleaned_data.get('reorder_level')

        if quantity is not None and reorder_level is not None:
            if quantity < reorder_level:
                raise forms.ValidationError("Quantity cannot be less than the reorder level.")
        return cleaned_data
