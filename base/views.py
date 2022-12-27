from django.shortcuts import render, redirect
from .forms import FuelForm, StockForm, SaleForm
from .models import Fuel, Sale, Stock
from django.db.models import Sum
from django.contrib import messages

# Create your views here.


def home(request):
    form = SaleForm()
    total_fuels = Fuel.objects.count()
    fuels = Fuel.objects.all()

    total_amount = Sale.objects.filter(fuel__id__in = fuels).aggregate(Sum('amount'))['amount__sum']
    print(total_amount)
    print(total_fuels)
    context = {
        "total_fuel":total_fuels,
        "total_sales": total_amount,
        "fuels": fuels,
        "form":form
        
    }
    return render(request, 'base/home.html', context)

def fuelView(request):
    fuels = Fuel.objects.all()
    context = {
        "fuels":fuels
    }
    return render(request, 'base/fuel_list.html', context)

def saveFuel(request):
    form = FuelForm()
    context = {
        "form":form
    }
    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'fuel added successfully')
            return redirect('fuels')
    
    return render(request, 'base/fuelform.html', context)
        
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

def saveSale(request):
    form = SaleForm()
    context = {
        "form":form
    }
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            price = sale.fuel.price
            sale_volume = sale.volume
            
            fuel = sale.fuel
            sales_volume = 0
            fuel_sales_volume = Sale.objects.filter(fuel__id = fuel.id).aggregate(Sum('volume'))['volume__sum']
            if fuel_sales_volume is None:
                sales_volume = 0
            else:
                sales_volume = fuel_sales_volume
            stock_volume = 0
            fuel_stock_volume = Stock.objects.filter(fuel__id = fuel.id).aggregate(Sum('volume'))['volume__sum']
            if fuel_stock_volume is None:
                stock_volume = 0
            else:
                stock_volume = fuel_stock_volume
            fuel_volume = stock_volume - sales_volume 
            if sale_volume > fuel_volume:
                # print("you cant do it man.")
                messages.error(request, 'Your volume exceeds available Volume')
                return redirect('new_sale')
            elif sale_volume <= 0:
                messages.error(request, 'Volume should be greator than 0')
                return redirect('new_sale')
            else:
                sale.amount = sale.volume*price
                sale.save()
                messages.success(request, 'Sale added successfully')
                return redirect('sales')
    
    return render(request, 'base/saleform.html', context)
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

def stockView(request):
    fuels = Fuel.objects.all().values_list('id')
    stocks = Stock.objects.filter(fuel__id__in = fuels).all()
    context = {
        "stocks":stocks,
        "fuels":fuels
    }

    return render(request, 'base/stock_list.html', context)

#sale view
def saleView(request):
    fuels = Fuel.objects.all().values_list('id')
    sales = Sale.objects.filter(fuel__id__in=fuels).all()

    context = {
        "sales":sales
    }
    return render(request, 'base/sale_list.html', context)

def inventoryView(request):
    fuels = Fuel.objects.all()

    context = {
        "fuels":fuels
    }
    return render(request, 'base/inventory.html', context)
