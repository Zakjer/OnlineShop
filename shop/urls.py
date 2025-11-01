from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update-cart/', views.update_cart, name='update_cart'),
]
