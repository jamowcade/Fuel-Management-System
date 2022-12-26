from django.urls import path
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path('fuels/', views.fuelView, name="fuels"),
    path('stocks/', views.stockView, name="stocks"),
    path('sales/', views.saleView, name="sales"),


]