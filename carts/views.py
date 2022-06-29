
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from store.models import Product
from carts.models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    """
    Private method to get the cart id from the request
    """
    cart = request.session.session_key  # get the session key
    if not cart:
        cart = request.session.create()
    return cart # return the session key

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product by id from the database and add it to the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart by cart_id from the seesion
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # get the cart item by product and cart
        if cart_item.quantity < cart_item.product.stock: # if the quantity is less than the stock then add one to the quantity  
            cart_item.quantity += 1 # add one to the quantity if the product is in the cart
            cart_item.save() # save the cart item
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
    return HttpResponse(cart_item.product) # return the product
    exit() 
    return render(request, 'cart') # return the cart.html template

def cart(request):
    return render(request, 'store/cart.html')
