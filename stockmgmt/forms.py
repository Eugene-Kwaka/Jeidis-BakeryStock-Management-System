from django import forms
from .models import Stock

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StockCreationForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']
    # This code ensures that the user cannot add an item that already exists

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        for item in Stock.objects.all():
            if item.item_name == item_name:
                raise forms.ValidationError(
                    str(item_name) + '  already exists')
        return item_name


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if not category:
    #         raise forms.ValidationError('A category is required')
    #     return category


class StockSearchForm(forms.ModelForm):
    # This helps us choose which search field to fill without necessarily filling all required fields
    #category = forms.CharField(required=False)
    item_name = forms.CharField(required=False)
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']
