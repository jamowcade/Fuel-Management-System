from django.urls import path
from .import views

urlpatterns = [
    path('', views.getRoutes ),
    path('fuels/', views.getFuels),
    path('fuels/<int:pk>/', views.getFuel),
]