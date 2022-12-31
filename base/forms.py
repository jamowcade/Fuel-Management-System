from django.forms import ModelForm
from .models import Fuel, Stock, Sale
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm




class UserForm(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="The Username field is required.")
    email = forms.EmailField(max_length=250,help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250,help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250,help_text="The Last Name field is required.")
    password1 = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username','first_name', 'last_name','password1', 'password2',)

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