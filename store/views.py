from builtins import Exception
from ast import Or, Try, keyword
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from carts.models import CartItem
from .models import Product
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6) # Show 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-id')
        paginator = Paginator(products, 6) # Show 6 products per page
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
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

def search(request):        # search the product by the name or the description
    if 'keyword' in request.GET:
        keyword = request.GET['keyword'] 
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            # paginator = Paginator(products, 6) # Show 6 products per page
            # page = request.GET.get('page') # get the page number from the url
            # paged_products = paginator.get_page(page) # get the products by the page number
            product_count = products.count()
        
            context = {
                'products': products,
                'keyword': keyword,
                'product_count': product_count
            }
    return render(request, 'store/store.html',context) # render the store.html page
