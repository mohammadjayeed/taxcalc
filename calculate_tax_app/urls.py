from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('tax/', views.calculate_tax, name='calculate_tax'),
    path('product/', views.ProductViewSet.as_view({'get': 'list','post': 'create'}), name='product-crud')
]
