from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('products/<int:category_id>/', views.products_by_category, name='products_by_category'),
]
