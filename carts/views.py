
from statistics import quantiles
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Variation
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

def add_cart(request, product_id): # add the product to the cart by id

    product = Product.objects.get(id=product_id) # get the product by id from the database and add it to the cart
    product_variation = []
    if request.method == 'POST': # if the request is a post then get the product variation by id
        for item in request.POST:
           key = item
           value = request.POST[key]
           
           try: # try to get the product variation by id
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value) # get the product variation by product and variation category and variation value if it exists otherwise return a 404 error
                product_variation.append(variation) # add the product variation to the product variation list
           except:
                pass # if the product variation does not exist then pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart by cart_id from the seesion
    except Cart.DoesNotExist: # if the cart does not exist then create a new cart
        cart = Cart.objects.create(cart_id=_cart_id(request)) # create a new cart if it does not exist
        cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart, is_active=True).exists() # get the cart item by product and cart if it exists otherwise return a 404 error
        
    if is_cart_item_exists: # if the cart item exists then add one to the quantity
        cart_item = CartItem.objects.filter(product=product, cart=cart) # get the cart item by product and cart if it exists otherwise return a 404 error
        # existing_variation = cart_item.variation.all() # get the existing variation by cart item
        # current_variation  = product_variation # get the current variation by product variation
        # item_id = cart_item.id # get the cart item 

        ex_var_list = [] # create a list to store the existing variation
        id = [] # create a list to store the cart item id
        for item in cart_item: 
            existing_variation = item.variations.all() # get the existing variation by cart item
            ex_var_list.append(list(existing_variation)) # add the existing variation to the list to compare with the current variation
            id.append(item.id) # add the cart item id to the list

        print(ex_var_list) # print the existing variation list

        if product_variation in ex_var_list: # if the product variation is in the existing variation list then add one to the quantity
            # increase the cart item quantity
            index = ex_var_list.index(product_variation) # get the index of the product variation in the existing variation list
            item_id= id[index] # get the cart item id by index
            item = CartItem.objects.get(product=product, id=item_id) # get the cart item by id 
            item.quantity += 1 # add one to the quantity
            item.save() # save the cart item

        else:
            # create a new cart item
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart) # create a new cart item by product and cart if it does not exist otherwise return a 404 error

            if cart_item.quantity < cart_item.product.stock: # if the quantity is less than the stock then add one to the quantity  
                if len(product_variation) > 0: # if the product variation is greater than 0 then add the product variation to the cart item
                    cart_item.variations.clear() # clear the cart item variations
                    # for item in product_variation: # for each product variation in the product_variation
                    cart_item.variations.add(*product_variation) # add the product variation to the cart item variations 
                    # cart_item.quantity += 1 # add one to the quantity if the product is in the cart
                    cart_item.save() # save the cart item
    else:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation) > 0: # if the product variation is greater than 0 then add the product variation to the cart item
                cart_item.variations.clear() # clear the cart item variations
                for item in product_variation: # for each product variation in the product_variation add the product variation to the cart item
                    cart_item.variations.add(item) # add the product variation to the cart item 
        cart_item.save() 
    return redirect('cart') # return the cart.html template

def remove_cart(request, product_id, cart_item_id): # remove the product from the cart by id
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart by cart_id from the seesion
    product = get_object_or_404(Product, id=product_id) # get the product by id from the database if it exists otherwise return a 404 error
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cart item by product and cart if it exists otherwise return a 404 error
        if cart_item.quantity > 1: # if the quantity is greater than one then subtract one from the quantity
            cart_item.quantity -= 1 # subtract one from the quantity
            cart_item.save() # save the cart item
        else:
            cart_item.delete()  # delete the cart item if the quantity is 1
    except:
        pass
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
