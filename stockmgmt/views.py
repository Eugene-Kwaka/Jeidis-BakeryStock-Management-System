from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import csv
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *
from .filters import StockFilter

# Create your views here.


def registerPage(request):
    title = "Sign Up"
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + username)
            return redirect('loginPage')

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username OR Password is incorrect!")

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginPage')


def home(request):
    title = 'JEIDIS STOCK MANAGEMENT SYSTEM'
    context = {
        'title': title,
    }
    return render(request, 'home.html', context)


@login_required
def list_items(request):
    title = 'List Items'
    items = Stock.objects.all()

    # SEARCH FUNCTIONALITY USING FILTERS.PY
    #my_filter = StockFilter()
    #my_filter = StockFilter(request.GET, queryset=items)
    #items = my_filter.qs

    # SEARCH FUNCTIONALITY
    form = StockSearchForm(request.POST or None)
    if request.method == 'POST':
        category = form['category'].value()
        items = Stock.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        # If category is not empty
        if (category != ''):
            items = items.filter(category_id=category)

    # EXPORT TO CSV
    if form['export_to_CSV'].value() == True:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="List of stock items.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
        # for each item in the stock list in the CSV this loop will run and write the item details
        for stock in items:
            writer.writerow([stock.category, stock.item_name, stock.quantity])
        return response

    context = {
        'items': items,
        'title': title,
        'form': form,
    }

    return render(request, 'list_items.html', context)


@login_required
def list_history(request):
    title = 'ITEMS HISTORY'
    items = StockHistory.objects.all()

    # ITEM HISTORY SEARCH FORM
    form = StockSearchForm(request.POST or None)
    if request.method == 'POST':
        category = form['category'].value()
        items = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        # If category is not empty and one of the categories has been selected
        if (category != ''):
            items = items.filter(category_id=category)

        # EXPORT TO CSV
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY',
                 'ITEM NAME',
                 'QUANTITY',
                 'ISSUE QUANTITY',
                 'RECEIVE QUANTITY',
                 'RECEIVE BY',
                 'ISSUE BY',
                 'LAST UPDATED'])
            for stock in items:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
                     stock.quantity,
                     stock.issue_quantity,
                     stock.receive_quantity,
                     stock.receive_by,
                     stock.issue_by,
                     stock.last_updated])
            return response

    context = {
        'title': title,
        'items': items,
        'form': form
    }
    return render(request, 'list_history.html', context)


@login_required
def add_items(request):
    title = 'Add Items'
    form = StockCreationForm(request.POST or None)
    if request.method == 'POST':
        form = StockCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully')
            return redirect('list_items')
    context = {
        'form': form,
        'title': title
    }
    return render(request, 'add_items.html', context)


@login_required
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


@login_required
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


@login_required
def issue_item(request, pk):
    title = 'Issue'
    item = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=item)
    if form.is_valid():
        item.quantity -= item.issue_quantity
        form.save()
        issue_history = StockHistory(
            id=item.id,
            last_updated=item.last_updated,
            category_id=item.category_id,
            item_name=item.item_name,
            quantity=item.quantity,
            issue_to=item.issue_to,
            issue_by=item.issue_by,
            issue_quantity=item.issue_quantity,
        )
        issue_history.save()
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


@login_required
def receive_item(request, pk):
    title = 'Receive'
    item = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=item)
    if form.is_valid():
        #instance = form.save(commit=False)
        item.quantity += item.receive_quantity
        form.save()
        receive_history = StockHistory(
            id=item.id,
            last_updated=item.last_updated,
            category_id=item.category_id,
            item_name=item.item_name,
            quantity=item.quantity,
            receive_quantity=item.receive_quantity,
            receive_by=item.receive_by
        )
        receive_history.save()
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


@login_required
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
