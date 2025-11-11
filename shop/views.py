from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from requests import request
from decimal import Decimal
from .models import *
from .forms import *
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

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {
        'category': category,
        'products': products
    })

@csrf_exempt
def update_cart(request):
    data = json.loads(request.body)
    product_id = str(data['productId'])
    action = data['action']
    quantity = int(data.get('quantity', 1))

    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if action == 'add':
            cart_item.quantity += quantity
        elif action == 'delete':
            cart_item.quantity -= 1
        elif action == 'remove':
            cart_item.quantity = 0

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

        return JsonResponse({'message': 'Cart updated successfully (auth user)'})

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = {}

        if product_id not in cart:
            cart[product_id] = {'quantity': 0}

        if action == 'add':
            cart[product_id]['quantity'] += quantity
        elif action == 'delete':
            cart[product_id]['quantity'] -= 1
        elif action == 'remove':
            cart[product_id]['quantity'] = 0

        if cart[product_id]['quantity'] <= 0:
            del cart[product_id]

        response = JsonResponse({'message': 'Cart updated successfully (guest)'})
        response.set_cookie('cart', json.dumps(cart))
        return response

def cart_view(request):
    items, cart = get_cart_and_items(request)
    total = 0
    normalized_items = []

    for item in items:
        if isinstance(item, dict):
                total += float(item.get('total_price', 0))
                normalized_items.append(item)

        else:
            total += float(item.total_price)
            normalized_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'total_price': item.total_price,
            })

    context = {
        'cart_items': items,
        'cart': cart,
        'total': total,
    }
    return render(request, 'cart.html', context)

def get_cart_and_items(request):
    if request.user.is_authenticated:
        customer, _ = Customer.objects.get_or_create(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=customer)
        items = cart.items.all()
        cart_items = sum([item.quantity for item in items])

        return items, cart

    else:
        try:
            order = json.loads(request.COOKIES['cart'])
        except KeyError:
            order = {}

        items = []
        cart = {'total_without_tax': 0, 'tax': 0, 'total_with_tax': 0, 'total_quantity': 0}

        for i in order:
            product = Product.objects.get(id=i)
            quantity = order[i]['quantity']
            total = product.price * quantity
            tax = round(total * Decimal(0.2), 2)
            total_with_tax = total + tax

            cart['total_without_tax'] += total
            cart['total_with_tax'] += total_with_tax
            cart['tax'] += tax
            cart['total_quantity'] += quantity

            item = {
                'product': product,
                'quantity': quantity,
                'total_price': total,
            }
            items.append(item)

        return items, cart

@csrf_exempt
def login_page(request):

    items, cart = get_cart_and_items(request)

    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method == 'POST':
            username = request.POST.get('username') 
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {'cart': cart}
    return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('login')

@csrf_exempt
def signup(request):
    form = CreateUserForm()
    items, cart = get_cart_and_items(request)

    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                Customer.objects.create(user=user)
                current_user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + current_user)
                return redirect('login')
    
    context = {'form': form, 'cart': cart}
    return render(request, 'signup.html', context)

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

