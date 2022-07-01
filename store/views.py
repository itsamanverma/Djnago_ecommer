from builtins import Exception
from ast import Try
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from carts.models import CartItem
from .models import Product
from category.models import Category
from carts.views import _cart_id


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug=None, product_slug=None):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(product=single_product, cart__cart_id=_cart_id(request)).exists() # check if the product is in the cart or not if it is then return true otherwise return false
        # return HttpResponse(in_cart) # return the in_cart variable as a json object 
        # exit()
    except Exception as e:
        raise e # raise the exception
        
    context = {
        'single_product': single_product, # get the product by slug from the database
        'in_cart': in_cart  # return the in_cart variable as a json object 
    }
    return render(request, 'store/product_detail.html', context)