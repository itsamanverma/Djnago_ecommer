
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


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
    except Cart.DoesNotExist: # if the cart does not exist then create a new cart
        cart = Cart.objects.create(cart_id=_cart_id(request)) # create a new cart if it does not exist
        cart.save()
        
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # get the cart item by product and cart
        if cart_item.quantity < cart_item.product.stock: # if the quantity is less than the stock then add one to the quantity  
            cart_item.quantity += 1 # add one to the quantity if the product is in the cart
            cart_item.save() # save the cart item
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save() 
    return redirect('cart') # return the cart.html template

def remove_cart(request, product_id): # remove the product from the cart by id
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) # get the product by id from the database if it exists otherwise return a 404 error
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1: # if the quantity is greater than one then subtract one from the quantity
        cart_item.quantity -= 1 # subtract one from the quantity
        cart_item.save()
    else:
        cart_item.delete()  # delete the cart item if the quantity is 1
    return redirect('cart') # return the cart.html template

def remove_item_cart(request, product_id): # remove the product from the cart by id
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) # get the product by id from the database if it exists otherwise return a 404 error
    cart_item = CartItem.objects.get(product=product, cart=cart) # get the cart item by product and cart if it exists otherwise return a 404 error
    cart_item.delete() # delete the cart item
    return redirect('cart') # return the cart.html template

def cart(request,total=0,quantity=0,cart_items=None): # render the cart.html template
    try:
        tax = 0
        grand_total = 0 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get all the cart items by cart id and is_active is true
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # add the price of the product to the total
            quantity += cart_item.quantity # add the quantity of the product to the quantity
        tax = round(total * 0.10) # add 10% tax to the total
        grand_total = total + tax # add the tax to the total
    except ObjectDoesNotExist:
        pass # if the cart does not exist then pass

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)
