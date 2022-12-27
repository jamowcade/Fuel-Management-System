from django.shortcuts import render
from .forms import FuelForm, StockForm, SaleForm
from .models import Fuel, Sale, Stock
from django.db.models import Sum

# Create your views here.


def home(request):
   
    total_fuels = Fuel.objects.count()
    fuels = Fuel.objects.all()

    total_amount = Sale.objects.filter(fuel__id__in = fuels).aggregate(Sum('amount'))['amount__sum']
    print(total_amount)
    print(total_fuels)
    context = {
        "total_fuel":total_fuels,
        "total_sales": total_amount,
        "fuels": fuels
        
    }
    return render(request, 'base/home.html', context)

def fuelView(request):
    fuels = Fuel.objects.all()
    context = {
        "fuels":fuels
    }
    return render(request, 'base/fuel_list.html', context)

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
