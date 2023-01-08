from django.shortcuts import render, redirect
from .forms import FuelForm, StockForm, UserProfile, SaleForm, UpdateProfile, UpdatePasswords, userUpdate, GroupForm
from .models import Fuel, Sale, Stock
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# Create your views here.


#get all users.
"""
METHOD: GET
   get all the users in the system. login is required with @login_required decorator.
   if user is not logged in redirects to login page. 
    :param users: iterable of users
    :param page_name: page name a string used  to display in the template. "users List

"""
@login_required(login_url='login')
@permission_required('auth.view_user', raise_exception=True)
def users(request):
    users = User.objects.all()
    context = {
        "users":users,
        "page_name": "Users List"
    }

    return render(request, 'base/users.html', context)


#create new user.
"""
    METHOD: POST.
    adds new user to the system. login is required with @login_required decorator.
    if user is not aunthenticated it redirects to login page. permission 'auth.add_user' is required.
    required fields: (username, password1, password2).
    if form data is valid it is saved and  success message is displayed else error is raised.
    :param form: instance of userCreationForm used to display a form in template.
    :param page_name: page name a string used  to display in the page name in template.

"""
@login_required(login_url='login')
@permission_required('auth.add_user', raise_exception=True)
def addUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'user  added successfully')
            return redirect('users')
        else:
            messages.error(request, f'user cannot be saved', extra_tags='danger')

    context = {
        "form":form,
        "page_name":"Add New User"
    }
    return render(request, 'base/register.html', context)

#login user.
"""
    METHOD: POST
    login user to the system.
    username and password is checked,
    if user exists and not none, user is logged in, else
    error is raised.
    :param username: user name 
    : Password: user password
    :param page_name: page name a string used  to display in the page name in template.

"""

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


#logout user
"""
    logout user from the system.
    logout method from django.contrib.auth is used.
    user session is destroyed. 
    and then redirects the user to login page.
"""

def logoutUser(request):
    logout(request)
    # messages.success(request, 'you are looged out')
    return redirect('login')


#edit user profile.
"""
    METHOD: POST
    edit user profile.
    a user can edit his/her information such as (first_name, last_name, email, picture)
    only logged in users can edit their profile. 
    UpdateProfile form from forms.py is used, if form data is valid it is saved and success message
    is displayed else error message is displayed.
    :param user: user object retrieved from the current session. (request.user) 
    :parem user_form: instance of UserchangeForm, here UpdateProfile form imported from the forms.py.

"""
@login_required(login_url='login')
def userProfile(request):
    user = User.objects.get(id = request.user.id)
    user_form = UpdateProfile()
    profile_form = UserProfile()
    if request.method == 'POST':
        user_form = UpdateProfile(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'user updated')
            return redirect('profile')
        else:
            messages.error(request, 'user is not updated', extra_tags='danger')
    else:
        user_form = UpdateProfile(instance=user)
    context = {
        "user_form":user_form,
        "profile_form":profile_form
    }
    return render(request, 'base/profile.html', context)

#Update User Password.
"""
    METHOD: POST
    chanage user Password.
    a user can change his/her password. fields required (old_password, new_password1, new_password2)
    only logged in users can change their password. 
    PasswordChangeForm from forms.py is used, if form data is valid it is saved and success message
    is displayed else error message is displayed.
    instance of PasswordChangeForm is returned to the template. to render the form html.
"""

@login_required(login_url='login')
def updatePassword(request):
    form = UpdatePasswords(request.user) # initiates form with the current user.
    context = {
        "form":form
    }
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form

    return render(request, 'base/update_password.html', context)

#Edit User informatioin.
"""
    METHOD: POST
    change user information.
    a user with change_user permission can edit user information. user can be assigned 
    or reasigned groups and permissions. 
    :param pk: the primary key of the user.
    :param user: instance of User object to be edited.
    :param form: instance of userUpdate form.
    form is initiated  with request.POST data nad user instance.
    if form data is valid it is saved and success message is displayed, else error raised. 
    template expects context of form with user data.
"""
@login_required(login_url='login')
@permission_required('auth.change_user', raise_exception=True)
def editUser(request, pk):
    user = User.objects.get(id=pk)
    form = userUpdate(instance = user)
    if request.method == 'POST':
        form = userUpdate(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    
    context = {
        "form":form
    }

    return render(request, 'base/edit_user.html', context)

#delete user..
"""
    METHOD: DELETE
    delete a user
    a user with delete_user permission can delete a user. 
    the primary key of the user to be deleted is required. ance the user is captured
    from the User model it is deleted.
    :param pk: the primary key of the user to be deleted
    once user is deleted success message is displated and returns to user page.
"""
@permission_required('auth.delete_user', raise_exception=True)
def deleteUser(request, pk):
    user = User.objects.get(id=pk).delete()
    return redirect(users)

#Home page..
"""
    only logged in user can access this page.
    Renders the home page template.
    the template expects the following.
    :total_fuels: the total of all active fuels/petrols.
    :total_sales: the total of all sales in the system.
    :fuels: a list of of all available fuels/petrols.
    :page_name: the name of the current page.
"""

@login_required(login_url='login')
# @permission_required('base.view_fuel', raise_exception=True)
def home(request):
    form = SaleForm()
    total_fuels = Fuel.objects.filter(delete_flag=0, status=1).count()
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()

    total_amount = Sale.objects.filter(fuel__id__in = fuels).aggregate(Sum('amount'))['amount__sum']
    
    print(total_amount)
    # print(total_fuels)
    context = {
        "total_fuel":total_fuels,
        "total_sales": total_amount,
        "fuels": fuels,
        "form":form,
        "page_name":"Main Dashboard"
        
    }
    return render(request, 'base/index.html', context)

#Fuel list Page
"""
    MEHTOD: POST.
    only logged in users with view_fuel permission can access this page.
    Renders the fuel_list template.
    the template expects the following.
    :fuels: a list of of all available fuels/petrols.
    :page_name: the name of the current page.
    if there is a post from this page it saves data to Fuel Model using FuelForm.
"""

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

#create new fuel type.
"""
    MEHTOD: POST.
    only logged in users with add_fuel permission can access this view.
    Renders the fuelform.html template.
    url: new_fuel
    the template expects:
    :form: instance of FuelForm.
    :page_name: the name of the current page.
    if there is a post from this page new record is added to Fuel Model using FuelForm.
"""

@login_required(login_url='login')
@permission_required('base.add_fuel', raise_exception=True)
def saveFuel(request):
    form = FuelForm()
    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'fuel added successfully')
            return redirect('fuels')
        else:
            messages.warning(request, 'fuel cannot be saved')
            return redirect('new_fuel')
    context = {
        "page_name":"Add New Petrol",
        "form":form
    }
    return render(request, 'base/fuelform.html', context)  

#Update fuel type.
"""
    MEHTOD: PATCH.
    only logged in users with change_fuel permission can access this view.
    Renders the fuelform.html template with fuel instance.
    url: update_fuel/pk where pk is the primary key of the fuel, for example; update_fuel/2
    fuel instance is captured using pk returned from the template.
    pk: primary key of the selected fuel type. for example. 
    the template expects the following.
    :form: instance of FuelForm.
    :fuel: instance of Fuel Model.
    :page_name: the name of the current page.
    if there is a post from this page it saves data to Fuel Model using FuelForm.
"""

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

# delte fuel
"""
    METHOD: DELETE.
    deletes fuel type. 
    url: delete_fuel/pk where pk is the primary key of the fuel, for example, delete_fuel/3
    once fuel is deleted return to fuels url with success message.

"""

@login_required(login_url='login')
@permission_required('base.delete_fuel', raise_exception=True)
def deleteFuel(request, pk = None):
    fuel = Fuel.objects.filter(id=pk).delete()
    messages.success(request, f"Fuel {fuel} has been deleted successfully")
    return redirect('fuels')


#Stock list Page
"""
    only logged in users with view_stock permission can access this view.
    Renders the stock_list template.
    url: stocks
    the template expects the following.
    :stocks: a list of of all available stocks.
    :fuels: a list of of all available fuels/petrols.
    :page_name: the name of the current page.
"""

@login_required(login_url='login')
@permission_required('base.view_stock', raise_exception=True)
def stockView(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()
    stocks = Stock.objects.filter(fuel__id__in = fuels).all()
    context = {
        "stocks":stocks,
        "fuels":fuels,
        "page_name":"Stock List"
    }

    return render(request, 'base/stock_list.html', context)

#create new stock.
"""
    MEHTOD: POST.
    only logged in users with add_stock permission can access this view.
    Renders the stockform.html template.
    url: new_stock
    the template expects:
    :form: instance of StockForm.
    :fuels: the list of all available fuels.
    :page_name: the name of the current page.
    if there is a post from this page new record is added to Stock Model using StockForm.
"""

@login_required(login_url='login')
@permission_required('base.add_fuel', raise_exception=True)
def saveStock(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()
    form = StockForm()
    context = {
        "form":form,
        "fuels":fuels,
        "page_name": "Add new Stock"
    }
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock added successfully')
            return redirect('stocks')
        else:
            messages.warning(request, 'Stock didnot saved')
            return redirect('stocks')

    
    return render(request, 'base/stockform.html', context)


#Update stock.
"""
    MEHTOD: UPDATE.
    only logged in users with change_stock permission can access this view.
    Renders the fuelform.html template with stock instance.
    url: update_stock/pk where pk is the primary key of the stock, for example; update_stock/2
    stock instance is captured using pk returned from the template.
    pk: primary key of the selected stock.
    the template expects the following.
    :form: instance of StockForm.
    :stock: instance of Stock Model.
    :fuels: the list of all available fuels
    :page_name: the name of the current page.
    if there is a post from this page it saves data to Fuel Model using FuelForm.
"""

@login_required(login_url='login')
@permission_required('base.change_stock', raise_exception=True)
def updateStock(request, pk):
    # if not request.user.has_perm('base.change_stock'):
    #     messages.error(request, 'You don\'t have permission to change stock', extra_tags='danger')
    #     return redirect('stocks')
    form = StockForm()
    stock = Stock.objects.get(id=pk)
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()
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
        "page_name":"Update Stock",
        "stock":stock,
        "fuels":fuels

    }
    return render(request, 'base/stockform.html', context)

# delete Stock
"""
    METHOD: DELETE.
    deletes stock. 
    only logged in user with permsiion of delete_stock can access thie view.
    url: delete_stock/pk where pk is the primary key of the stock, for example, delete_stock/3
    if stock is deleted returns to stocks url with success message  else error is raised..

"""

@login_required(login_url='login')
@permission_required('base.delete_stock', raise_exception=True)
def deleteStock(request, pk):
    try:
        stock = Stock.objects.filter(id=pk).delete()
        messages.success(request, f'stock {stock} has been deleted')
        return redirect('stocks')
    except:
        messages.error(request, 'invalid stock id')

#sales list view
"""
    lists all sales.
    only logged in user with permission fo view sales can access this view.
    renders sales_list.html template.
    url: sales
    the template expecst the following.
    :sales: a list of all sales in the system.
    :page_name: the name of the page.

"""

@login_required(login_url='login')
@permission_required('base.view_sale', raise_exception=True)
def saleView(request):
    context = {
        "page_name":"Sales list"
    }
    fuels = Fuel.objects.filter(delete_flag=0, status = 1).all()
    if request.method=='POST':
        search_term = request.POST.get('search_term')
        if search_term != 'all':
            sales = Sale.objects.filter(fuel__id = search_term).all()
            context['sales'] = sales
            context['fuels'] = fuels
            context['page_name'] = 'Sales List'
        else:
            fuels = Fuel.objects.filter(delete_flag=0, status = 1).all()
            sales = Sale.objects.filter(fuel__id__in=fuels).all()
            context['sales'] = sales
            context['fuels'] = fuels
    else:
        fuels = Fuel.objects.filter(delete_flag=0, status = 1).all()
        sales = Sale.objects.filter(fuel__id__in=fuels).all()
        context['sales'] = sales
        context['fuels'] = fuels
    return render(request, 'base/sale_list.html', context)

#create new sale.
"""
    MEHTOD: POST.
    only logged in users with add_sale permission can access this view.
    Renders the saleform.html template.
    url: new_sale
    the template expects:
    :form: instance of SaleForm.
    :fuels: the list of all available fuels.
    :page_name: the name of the current page.
    if there is a post from this page new record is added to Sale Model using SaleForm.
"""


@login_required(login_url='login')
@permission_required('base.add_sale', raise_exception=True)
def saveSale(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()
    form = SaleForm()
    if request.method == 'POST':
        print(request.POST)
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
                messages.error(request, 'Your volume exceeds available Volume', extra_tags='danger')
                return redirect('new_sale')
            elif sale_volume <= 0: # if user entered zero or negative number
                messages.error(request, 'Volume should be greator than 0')
                return redirect('new_sale')
            else:
                sale.amount = sale.volume*price # calculate the total amount
                sale.save()
                messages.success(request, 'Sale added successfully')
                return redirect('sales')
    context = {
        "form":form,
        "page_name":"Add New Sale",
        "fuels":fuels
    }
    return render(request, 'base/saleform.html', context)

#Update sale.
"""
    MEHTOD: UPDATE.
    only logged in users with change_sale permission can access this view.
    Renders the fuelform.html template with sale instance.
    url: update_sale/pk where pk is the primary key of the sale, for example; update_sale/10
    sale instance is captured using pk returned from the template.
    pk: primary key of the selected sale.
    the template expects the following.
    :form: instance of SaleForm.
    :sale: instance of stock Object.
    :fuels: the list of all available fuels
    :page_name: the name of the current page.
    if there is a post from this page it saves data to Sale Model using SaleForm.
"""


@login_required(login_url='login')
@permission_required('base.change_sale', raise_exception=True)
def updateSale(request, pk):
    sale = Sale.objects.get(id=pk)
    fuels = Fuel.objects.filter(delete_flag=0, status = 1).all()
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
            return redirect('home')
            messages.success(request, 'sale cannot be updated')
    context = {
        "form":form,
        "page_name":"Update Sale",
        "sale":sale,
        "fuels":fuels
    }
    
    return render(request, 'base/saleform.html', context)


# delete Stock
"""
    METHOD: DELETE.
    deletes sale. 
    only logged in user with permsiion of delete_sale can access thie view.
    url: delete_sale/pk where pk is the primary key of the sale, for example, delete_sale/10
    if sale is deleted returns to sales url with success message  else error is raised..

"""
@login_required(login_url='login')
@permission_required('base.delete_sale', raise_exception=True)
def deleteSale(request, pk):
    try:
        sale = Sale.objects.filter(id=pk).delete() 
        messages.success(request, f'stock {sale} has been deleted')
        return redirect('sales')
    except:
        messages.error(request, 'invalid stock id')

      
#fuel details.
"""
    display full information of the selected fuel.
    only logged in users with view_fuel can access this view.
    url: fuel_detail/pk where pk is the primary key of the selected fuel.
    renders fuel_detail.html template.
    the template expects the following.
    :fuel: instance of the Fuel Object.
    :stocks: list of related stocks of the current fuel.
    :sales: list of related stocks of the current fuel.
    :total_sale: total sales of the current fuel.

"""


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


#inventory
"""
    list of inventory.
    only logged in user with view permission can see this view.
    renders inventory.html template. 
    url: inventory.
    template expects:
    :fuels: a list of all a vailable fuels.
    :page_name: the name of the page.
"""

@login_required(login_url='login')
@permission_required('base.view_stock', raise_exception=True)
def inventoryView(request):
    fuels = Fuel.objects.filter(delete_flag=0, status=1).all()

    context = {
        "fuels":fuels,
        "page_name": "Inventory"
    }
    return render(request, 'base/inventory.html', context)


#================================================================================
#GROUPS
#add new group.

"""
    METHOD: POST
    list available groups and ads new group to the system.
    url: groups.
    renders template groups.html.
    the template expects:
    :groups: list of all available groups.
    :page_name: the name of the page.
    if there is a post method data is saved to Group model and success message is displayed
    selse error is raised.

"""
def addGroup(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        if name != "":
            if len(Group.objects.filter(name=name)) == 0:
                group = Group(name=name)
                group.save()
                messages.success(request, 'group added successfully')
            else:
                messages.error(request, 'group couln\'t be added', extra_tags='danger')
    groups = Group.objects.all()
    context = {
        "groups":groups,
        "page_name":"Group List"
    }
    return render(request, 'base/groups.html', context)


# delete group
"""
    METHOD: DELETE.
    deletes group. 
    url: delete_group/pk where pk is the primary key of the group, for example, delete_group/5
    once group is deleted return to groups url with success message.

"""
def deleteGroup(request, pk):
    group = Group(id=pk)
    group.delete()
    messages.success(request, 'group deleted')
    return redirect('groups')

#assign user to group.
"""
    METHOD: POST
   display user's groups and assign new group
    url: user_group/pk where pk primary key of the the selected user.
    renders template user_groups.html.
    user is retrieved from the User model using pk.
    the template expects:
    :groups: list of all available groups.
    :user_groups: list of user's groups.
    :page_name: the name of the page.
    if there is a post method user.groups is updated and success message is displayed
    selse error is raised.

"""
def userGroup(request, pk):
    groups = Group.objects.all()
   
    if request.method == 'POST':
        gname = request.POST.get('gname')
        group = Group.objects.get(id=gname)
        user = User.objects.get(id=pk)
        user.groups.add(group)

    user = User.objects.get(id=pk)
    user_group = [i for i in user.groups.all()]
    context = {
        "groups": groups,
        "user_group": user_group
    }

    return render(request, 'base/user_groups.html', context)

# remove group from user
"""
    METHOD: DELETE.
    remove groups from the user. 
    url: del_user_group/pk/name where pk is the primary key of the user, and name is the group name
    to be removed for example, del_user_group/5/group1.

"""

def del_user_group(request, pk, name):
    group = Group.objects.get(name=name)
    user = User.objects.get(id=pk)
    print(user)
    print(group)
    user.groups.remove(group)
    # return redirect('user_group')


#permissions.
"""
    list all permissions.
    url: permissions.
    renders permissions.html template.
    template expects.
    :permissions: list of all available permissions.

"""
def permissions(request):
    permissions = Permission.objects.all()

    context = {
        "permissions":permissions,
        "page_name":"All Pernissions"
    }

    return render(request, 'base/permissions.html', context)


#Group Permissions.
"""
    METHOD: POST.
    lists group permissions.
    url: group_perms/pk where pk is the primay key of the group.
    renders template group_permissions.html.
    the template expects.
    :permissions: list of all permissions.
    :group_permission: list of all group permissions.
    If ther is a post method group.permissions is updated.

"""

def group_perms(request, pk):
    permissions = Permission.objects.all()
    group = Group.objects.get(id=pk)
    group_perms = [i for i in group.permissions.all()]
    
    if request.method == 'POST':
        pnane = request.POST.get('pname')
        perm = Permission.objects.get(id=pnane)
        # user = User.objects.get(id=pk)
        group.permissions.add(perm)
    context = {
        "permissions": permissions,
        "group_permission": group_perms
    }

    return render(request, 'base/group_permissions.html', context)


# edit groups.
"""
    Edit group informations. assign groups to permissions.


"""
def edit_group(request, pk):
    group = Group.objects.get(id=pk)
    group_form = GroupForm(instance=group)
    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, 'Group data is updated')
            return redirect('groups')
    context = {
        "group_form":group_form
    }

    return render(request, 'base/edit_group.html', context)

@login_required(login_url='login')
@permission_required('base.view_sale', raise_exception=True)
def sales_report(request, rep_date=None):
    
    context = {
        
    }
    if request.method == 'POST':
        rep_date = request.POST.get('rep_date')
        print(rep_date)
        if rep_date is not None:
            rep_date = datetime.strptime(rep_date, "%Y-%m-%d")
        else:
            rep_date = datetime.now()
        year = rep_date.strftime("%Y")
        month = rep_date.strftime("%m")
        day = rep_date.strftime("%d")
        fuels = Fuel.objects.filter(delete_flag = 0, status = 1).all().values_list('id')
        sales = Sale.objects.filter(fuel__id__in = fuels, 
                                                    created__month = month,
                                                    created__day = day,
                                                    created__year = year,
                                                    )

        context = {
            "page_name":"Sale report",
            "rep_date": rep_date,
            "sales": sales.all(),
            "total_amount": sales.aggregate(Sum('amount'))['amount__sum']

        }                                    
    
        if context['total_amount'] is None:
            context['total_amount']= 0

    return render(request, "base/sales_report.html", context)
    