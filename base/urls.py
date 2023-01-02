from django.urls import path
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
    path('login/', views.loginUser, name="login" ),
    path('logout/', views.logoutUser, name="logout" ),
    path('register/', views.addUser, name="register" ),
    path('users/', views.users, name="users" ),
    path('profile/', views.userProfile, name="profile" )





]