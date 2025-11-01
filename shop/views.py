from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from requests import request
from .models import Product, Cart, CartItem
import json

def homepage(request):
    products = Product.objects.all()[:8]
    return render(request, "homepage.html", {
        "products": products,
        "year": datetime.now().year
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]

    return render(request, "product_detail.html", {
        "product": product,
        "related_products": related_products,
        "year": datetime.now().year
    })

def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
        cart_items = cart.items.select_related('product')
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0

    return render(request, "cart.html", {"cart_items": cart_items, "total": total})

def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    cart, _ = Cart.objects.get_or_create(customer=customer)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if action == 'add':
        cart_item.quantity += 1
    elif action == 'delete':
        cart_item.quantity -= 1
    elif action == 'remove':
        cart_item.quantity = 0

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    return JsonResponse({'message': 'Cart updated'})