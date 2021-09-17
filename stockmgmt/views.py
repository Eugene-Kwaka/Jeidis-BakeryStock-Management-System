from django.shortcuts import render, redirect
from django.urls import reverse
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
        form = StockCreationForm(request.POST or None)
        if form.is_valid():
            #item_name = form.cleaned_data.get('item_name')
            #item_name = Stock.objects.filter(item_name__iexact='item_name')
            # if form['item_name'].value() == item_name:
            #     messages.warning(request, 'Item already exists')
            #     return redirect('add_items')
            # else:
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


def item_details(request, pk):
    item = Stock.objects.get(id=pk)
    context = {
        'item': item,
    }

    return render(request, 'item_details.html', context)


def issue_item(request, pk):
    title = 'Issue'
    item = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=item)
    if form.is_valid():
        #instance = form.save(commit=False)
        item.quantity -= item.issue_quantity
        form.save()
        messages.success(request, 'Issued successfully: ' + " " + str(item.quantity) +
                         " " + str(item.item_name) + " " + 'now left in store')
        return redirect(reverse('item_details', kwargs={
            'pk': item.pk,
        }))

    context = {
        'title': title,
        'item': item,
        'form': form,
    }
    return render(request, 'issue_item.html', context)


def receive_item(request, pk):
    title = 'Receive'
    item = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=item)
    if form.is_valid():
        #instance = form.save(commit=False)
        item.quantity += item.receive_quantity
        form.save()
        messages.success(request, 'Received successfully: ' + " " + str(item.quantity) +
                         " " + str(item.item_name) + " " + 'now left in store')
        return redirect(reverse('item_details', kwargs={
            'pk': item.pk,
        }))

    context = {
        'title': title,
        'item': item,
        'form': form,
    }
    return render(request, 'receive_item.html', context)


def reorder_level(request, pk):
    title = 'Reorder levels for'
    item = Stock.objects.get(id=pk)
    form = ReorderLevelForm()
    if request.method == 'POST':
        form = ReorderLevelForm(request.POST or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reorder level for' + " " + str(item.item_name) +
                             " " + " has been updated to" + " " + str(item.reorder_level))
            return redirect('list_items')
    context = {
        'title': title,
        'item': item,
        'form': form,
    }
    return render(request, 'reorder_level.html', context)
