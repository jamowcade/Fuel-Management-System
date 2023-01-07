from django.forms import ModelForm
from .models import Fuel, Stock, Sale
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm




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


class UpdateProfile(UserChangeForm):
    # first_name = forms.CharField(max_length=100, )
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'username')

class userUpdate(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="First name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Last name")
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="User name")
    # groups = forms.MultipleChoiceField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Groups")
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Email")
    # groups = forms.MultipleChoiceFieldwidget=forms.TextInput(attrs={'class':'form-control' }),label="groups")
    # new_Password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")

    class Meta:
        model = User
        fields =  ['username','first_name','last_name','email','is_active','is_staff','is_superuser','groups','last_login','date_joined']   
        

class UpdatePasswords(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Old Password")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="New Password")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm rounded-0'}), label="Confirm New Password")
    class Meta:
        model = User
        fields = ['old_password','new_password1', 'new_password2']

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


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