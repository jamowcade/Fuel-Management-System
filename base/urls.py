from django.urls import path
# from django.conf.urls import url
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('fuels/', views.fuelView, name="fuels"),
    path('stocks/', views.stockView, name="stocks"),
    path('sales/', views.saleView, name="sales"),
    path('inventory/', views.inventoryView, name="inventory"),
    path('new_fuel/', views.saveFuel, name="new_fuel"),
    path('fuel_details/<str:pk>/', views.fuelDetail, name="fuel_detail"),
    path('new_stock/', views.saveStock, name="new_stock"),
    path('new_sale/', views.saveSale, name="new_sale"),
    path('update_fuel/<str:pk>/', views.updateFuel, name="update_fuel"),
    path('delete_fuel/<str:pk>/', views.deleteFuel, name="delete_fuel"),
    path('update_stock/<str:pk>/', views.updateStock, name="update_stock"),
    path('delete_stock/<str:pk>/', views.deleteStock, name="delete_stock"),
    path('update_sale/<str:pk>/', views.updateSale, name="update_sale"),
    path('delete_sale/<str:pk>/', views.deleteSale, name="delete_sale"),
    path('sale_report/', views.sales_report, name="sale_report"),
    path('login/', views.loginUser, name="login" ),
    path('logout/', views.logoutUser, name="logout" ),
    path('register/', views.addUser, name="register" ),
    path('users/', views.users, name="users" ),
    path('profile/', views.userProfile, name="profile" ),
    path('update_password/', views.updatePassword, name="update_password" ),
    path('edit_user/<str:pk>/', views.editUser, name="edit_user" ),
    path('delete_user/<str:pk>/', views.deleteUser, name="delete_user"),
    path('delete_user_group/<str:pk>/', views.del_user_group, name="delete_user_group"),
    path('groups/', views.addGroup, name="groups" ),
    path('delete_group/<str:pk>/', views.deleteGroup, name="delete_group" ),
    path('user_group/<int:pk>/', views.userGroup, name="user_group" ),
    path('permissions/', views.permissions, name="permissions" ),
    path('group_perms/<str:pk>/', views.group_perms, name="group_perms" ),
    path('edit_group/<str:pk>/', views.edit_group, name="edit_group" ),


]