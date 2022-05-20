from django.urls import path
from . import views
from .views import StockDetailView

urlpatterns = [
    path('', views.stock_home, name='stock-home'),
    path('detail/<int:pk>', StockDetailView.as_view(), name='stock-detail'),
    path('register/', views.stock_register, name='stock-register'),
    path('search/', views.stock_search, name='stock-search'),
]