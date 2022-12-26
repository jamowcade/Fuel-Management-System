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