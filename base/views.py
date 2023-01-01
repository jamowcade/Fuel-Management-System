from django.shortcuts import render, redirect
from .forms import FuelForm, StockForm, SaleForm, UserForm
from .models import Fuel, Sale, Stock
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Create your views here.
@login_required(login_url='login')
@permission_required('auth.view_user', raise_exception=True)
def users(request):
    users = User.objects.all()
    context = {
        "users":users,
        "page_name": "Users List"
    }

    return render(request, 'base/users.html', context)

@login_required(login_url='login')
@permission_required('auth.add_user', raise_exception=True)
def addUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'user  added successfully')
        else:
            messages.error(request, f'user cannot be saved', extra_tags='danger')

    context = {
        "form":form,
        "page_name":"Add New User"
    }
    return render(request, 'base/register.html', context)


#login user.

def loginUser(request):
    context = {
        "page_name":"Login"
    }
    if request.user.is_authenticated:
        return redirect('home')

    username = ""
    password = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid username or password', extra_tags='danger')
    
    return render(request, 'base/login.html')

def logoutUser(request):
    logout(request)
    # messages.success(request, 'you are looged out')
    return redirect('login')

@login_required(login_url='login')
def home(request):
    form = SaleForm()
    total_fuels = Fuel.objects.filter(delete_flag=0, status=1).count()
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()

    total_amount = Sale.objects.filter(fuel__id__in = fuels).aggregate(Sum('amount'))['amount__sum']
    print(total_amount)
    print(total_fuels)
    context = {
        "total_fuel":total_fuels,
        "total_sales": total_amount,
        "fuels": fuels,
        "form":form,
        "page_name":"Main Dashboard"
        
    }
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
@permission_required('base.view_fuel', raise_exception=True)
def fuelView(request):
    if request.method == 'POST':
        form = FuelForm()
        if form.is_valid():
            form.save()
            messages.success(request, 'fuel added successfully')
            return redirect('fuels')
    fuels = Fuel.objects.filter(delete_flag = 0).all()
    context = {
        "fuels":fuels,
        "page_name":"Fuel List"
    }
    return render(request, 'base/fuel_list.html', context)
@login_required(login_url='login')
@permission_required('base.add_fuel', raise_exception=True)
def saveFuel(request):
    # form = FuelForm()
    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'fuel added successfully')
            return redirect('fuels')
        else:
            messages.warning(request, 'fuel cannot be saved')
            return redirect('fuels')
    context = {
        "page_name":"Add New Petrol"
    }
    return render(request, 'base/fuelform.html', context)  

@login_required(login_url='login')
def updateFuel(request, pk):
    fuel = Fuel.objects.get(id=pk)
    form = FuelForm()
    # form = FuelForm(instance=fuel)
    if request.method == 'POST':
        form = FuelForm(request.POST, instance=fuel)
        if form.is_valid():
            form.save()
            messages.success(request, f'fuel {fuel} successfully updated ')
            return redirect('fuels')
    context = {
        "form":form,
        "page_name":"Update Fuel",
        "fuel":fuel

    }
    return render(request, 'base/fuelform.html', context)
@login_required(login_url='login')
def deleteFuel(request, pk = None):
    fuel = Fuel.objects.filter(id=pk).delete()
    messages.success(request, f"Fuel {fuel} has been deleted successfully")
    return redirect('fuels')


@login_required(login_url='login')
@permission_required('base.view_stock', raise_exception=True)
def stockView(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()
    stocks = Stock.objects.filter(fuel__id__in = fuels).all()
    context = {
        "stocks":stocks,
        "fuels":fuels,
        "page_name":"Add New Stock"
    }

    return render(request, 'base/stock_list.html', context)


@login_required(login_url='login')
@permission_required('base.add_fuel', raise_exception=True)
def saveStock(request):
    form = StockForm()
    context = {
        "form":form
    }
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock added successfully')
            return redirect('stocks')
    
    return render(request, 'base/stockform.html', context)

#update stock
@login_required(login_url='login')
@permission_required('base.change_stock', raise_exception=True)
def updateStock(request, pk):
    # if not request.user.has_perm('base.change_stock'):
    #     messages.error(request, 'You don\'t have permission to change stock', extra_tags='danger')
    #     return redirect('stocks')
    form = StockForm()
    stock = Stock.objects.get(id=pk)
    form = StockForm(instance=stock)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, f'Stock {stock} successfully updated ')
            return redirect('stocks')
        else:
            messages.error(request, 'form cannot be updated', extra_tags='danger')
    context = {
        "form":form,
        "page_name":"Update Stock"

    }
    return render(request, 'base/stockform.html', context)

@login_required(login_url='login')
@permission_required('base.delete_stock', raise_exception=True)
def deleteStock(request, pk):
    # if not request.user.has_perm('base.delete_Stock'):
    #     messages.warning(request, 'You don\'t have permission to delete stock', extra_tags="danger")
    #     return redirect('stocks')
    try:
        stock = Stock.objects.filter(id=pk).delete()
        messages.success(request, f'stock {stock} has been deleted')
        return redirect('stocks')
    except:
        messages.error(request, 'invalid stock id')

@login_required(login_url='login')
@permission_required('base.add_sale', raise_exception=True)
def saveSale(request):
    form = SaleForm()
    context = {
        "form":form,
        "page_name":"Add New Sale"
    }
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            price = sale.fuel.price
            sale_volume = sale.volume # get the volume of the current sale instance
            
            # before we go a head we need to compare the volume user entered and the
            fuel = sale.fuel # get the selected fuel from the dropdown
            sales_volume = 0
            # sums the volume of the selected fuel in Sale model. and stores in a variable 'fuel_sales_volume'
            fuel_sales_volume = Sale.objects.filter(fuel__id = fuel.id).aggregate(Sum('volume'))['volume__sum'] 
            if fuel_sales_volume is None:
                sales_volume = 0
            else:
                sales_volume = fuel_sales_volume
            stock_volume = 0
            # sums the volume of the selected fuel in Stock model. and stores in a variable 'fuel_stocks_volume'
            fuel_stock_volume = Stock.objects.filter(fuel__id = fuel.id).aggregate(Sum('volume'))['volume__sum']
            if fuel_stock_volume is None:
                stock_volume = 0
            else:
                stock_volume = fuel_stock_volume
            fuel_volume = stock_volume - sales_volume # subtruct the two volumes to get the available volume for the selected fuel.
            if sale_volume > fuel_volume: # compare the result to the user intered volume. to check if the selected fuel has enough volume.
                messages.error(request, 'Your volume exceeds available Volume')
                return redirect('new_sale')
            elif sale_volume <= 0: # if user entered zero or negative number
                messages.error(request, 'Volume should be greator than 0')
                return redirect('new_sale')
            else:
                sale.amount = sale.volume*price # calculate the amount
                sale.save()
                messages.success(request, 'Sale added successfully')
                return redirect('sales')
    
    return render(request, 'base/saleform.html', context)

@login_required(login_url='login')
@permission_required('base.change_sale', raise_exception=True)
#update sales
def updateSale(request, pk):
    sale = Sale.objects.get(id=pk)
    form  = SaleForm(instance=sale)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            sale = form.save(commit=False)
            price = sale.fuel.price
            sale.amount = sale.volume*price
            sale.save()
            messages.success(request, 'sale updated')
            return redirect('sales')
        else:
            return redirect('sales')
            messages.success(request, 'sale cannot be updated')
    context = {
        "form":form,
        "page_name":"Update Sale"
    }
    
    return render(request, 'base/saleform.html', context)

@login_required(login_url='login')
@permission_required('base.delete_sale', raise_exception=True)
def deleteSale(request, pk):
    try:
        sale = Sale.objects.filter(id=pk).delete() 
        messages.success(request, f'stock {sale} has been deleted')
        return redirect('sales')
    except:
        messages.error(request, 'invalid stock id')
@permission_required('base.view_fuel', login_url='fuels')
@login_required(login_url='login')
def fuelDetail(request, pk):
    fuel = Fuel.objects.get(id=pk)
    stocks = Stock.objects.filter(fuel__id = fuel.id).all()
    sales = Sale.objects.filter(fuel__id = fuel.id ).all()
    total_sale = Sale.objects.filter(fuel__id = fuel.id).aggregate(Sum('amount'))
    print(total_sale)
    context = {
        "fuel":fuel,
        "stocks": stocks,
        "sales":sales,
        "total_sale":total_sale
    }
    
    return render(request, 'base/fuel_details.html', context)




@login_required(login_url='login')
@permission_required('base.view_sale', raise_exception=True)
#sale view
def saleView(request):
    fuels = Fuel.objects.filter(delete_flag=0, status = 1).all()
    sales = Sale.objects.filter(fuel__id__in=fuels).all()

    context = {
        "sales":sales,
        "page_name":"Sales List"
    }
    return render(request, 'base/sale_list.html', context)


@login_required(login_url='login')
@permission_required('base.view_stock', raise_exception=True)
def inventoryView(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()

    context = {
        "fuels":fuels
    }
    return render(request, 'base/inventory.html', context)
