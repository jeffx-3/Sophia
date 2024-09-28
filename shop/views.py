from django.shortcuts import render
from .models import Product

#home view
def home(request):
    return render(request, 'home.html')

#discover view
def discover(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'discover.html',context)