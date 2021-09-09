import django_filters
from django import forms

from .models import Stock


class StockFilter(django_filters.FilterSet):
    export_to_CSV = django_filters.BooleanFilter(
        widget=forms.CheckboxInput, required=False)

    class Meta:
        model = Stock
        fields = [
            'category',
            'item_name',
            'export_to_CSV'
        ]
