from django.shortcuts import render
from datetime import datetime
from .models import Product

def homepage(request):
    products = Product.objects.all()[:8]
    return render(request, "homepage.html", {
        "products": products,
        "year": datetime.now().year
    })
