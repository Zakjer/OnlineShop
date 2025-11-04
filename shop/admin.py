from django.contrib import admin
from .models import Category, Product, Customer, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # auto-fills slug from name
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'discount_price', 'stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category__name')
    ordering = ('-created_at',)
    list_editable = ('price', 'discount_price', 'stock')
    date_hierarchy = 'created_at'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email')
    search_fields = ('user__username', 'name', 'email')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    search_fields = ('customer__user__username',)
    ordering = ('-created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart', 'product')
    search_fields = ('product__title',)
