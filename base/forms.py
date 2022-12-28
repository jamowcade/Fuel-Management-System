from django.forms import ModelForm
from .models import Fuel, Stock, Sale



class FuelForm(ModelForm):
    class Meta:
        model = Fuel
        fields = ['name','price','status']
    


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['fuel','volume']
    

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name','fuel','volume']