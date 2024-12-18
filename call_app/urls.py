from django.contrib import admin
from django.urls import path
from .views import ProductDetailView

urlpatterns = [
    path('productdetails/',ProductDetailView.as_view(),name='product_details'),
    path('productupdate/<int:pk>/',ProductDetailView.as_view(),name='product_update'),
    path('productdelete/<int:id>/',ProductDetailView.as_view(),name="product_delete"),
    
]
