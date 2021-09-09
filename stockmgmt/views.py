from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages


from .models import Stock
from .forms import *
from .filters import StockFilter

# Create your views here.


def home(request):
    title = 'JEIDIS STOCK MANAGEMENT SYSTEM'
    context = {
        'title': title,
    }
    return render(request, 'home.html', context)


def list_items(request):
    title = 'List Items'
    items = Stock.objects.all()
    my_filter = StockFilter()

    # SEARCH FUNCTIONALITY
    my_filter = StockFilter(request.GET, queryset=items)
    items = my_filter.qs

    # EXPORT TO CSV
    if my_filter.form['export_to_CSV'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="List of stock items.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
        instance = items
        # for each item in the stock list in the CSV this loop will run and write the item details
        for stock in instance:
            writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

    context = {
        'items': items,
        'title': title,
        'my_filter': my_filter,
    }

    return render(request, 'list_items.html', context)


def add_items(request):
    title = 'Add Items'
    form = StockCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            item_name = form.cleaned_data.get('item_name')
            if form['item_name'].value() == item_name:
                messages.warning(request, 'Item already exists')
                return redirect('add_items')
            else:
                form.save()
                messages.success(request, 'Item added successfully')
                return redirect('list_items')
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'add_items.html', context)


def update_items(request, pk):
    title = 'Update item details'
    item = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=item)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            return redirect('list_items')

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'update_item.html', context)


def delete_items(request, pk):
    title = 'Delete item'
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully')
        return redirect('list_items')
    context = {
        'title': title,
        'item': item,
    }

    return render(request, 'delete_items.html', context)
