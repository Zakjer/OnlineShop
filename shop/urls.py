from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('product/<int:pk>/', views.homepage, name='product_detail'),
]