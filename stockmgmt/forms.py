from django import forms
from .models import Stock


class StockCreationForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if not category:
    #         raise forms.ValidationError('A category is required')
    #     return category

    # def clean_item_name(self):
    #     item_name = self.cleaned_data.get('item_name')
    #     if not item_name:
    #         raise forms.ValidationError('An item is required')
    #     return item_name


class StockSearchForm(forms.ModelForm):
    # This helps us choose which search field to fill without necessarily filling all required fields
    category = forms.CharField(required=False)
    item_name = forms.CharField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']
