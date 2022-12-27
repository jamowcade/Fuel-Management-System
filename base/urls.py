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





]