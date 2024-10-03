from django.shortcuts import render,get_object_or_404,redirect
from .models import Category, Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required

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

#search view
def search(request):
    query = request.GET.get('q', '') # Get the search term from the query parameters
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.none() # No search results if no query
        
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'product_search.html', context)


#cart views
def cart(request):
    return render(request, 'cart.html')


# Product List View
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'product_list.html', {'category': category, 'categories': categories, 'products': products})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'product_detail.html', {'product': product})

# Cart View
@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})

# Add to Cart View
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

# Remove from Cart View
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')

# Checkout View
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user, total_price=calculate_cart_total(cart))
    cart.delete()  # Empty the cart after checkout
    return render(request, 'checkout.html', {'order': order})

def calculate_cart_total(cart):
    return sum(item.product.price * item.quantity for item in cart.items.all())