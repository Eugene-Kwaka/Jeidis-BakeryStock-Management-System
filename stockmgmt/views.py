from django.shortcuts import render, redirect
from .models import Stock
from .forms import *

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
    # SEARCH FUNCTIONALITY
    form = StockSearchForm()
    if request.method == 'POST':
        form = StockSearchForm(request.POST or None)
        items = Stock.objects.filter(category__icontains=form['category'].value(),
                                     item_name__icontains=form['item_name'].value())

    context = {
        'items': items,
        'title': title,
        'form': form,
    }

    return render(request, 'list_items.html', context)


def add_items(request):
    title = 'Add Items'
    form = StockCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
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
        return redirect('list_items')
    context = {
        'title': title,
        'item': item,
    }

    return render(request, 'delete_items.html', context)
