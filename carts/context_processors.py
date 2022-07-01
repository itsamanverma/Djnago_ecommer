from calendar import c
from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) # get the cart by the cart_id from the database
            cart_items = CartItem.objects.filter(cart=cart[:1]) # get the cart items by cart id
            for  cart_item in cart_items:
                cart_count += cart_item.quantity # add the quantity of the product to the cart_count
        except Cart.DoesNotExist:
            cart_count = 0  # if the cart does not exist then set the cart count to 0    
        
    return dict(cart_count=cart_count)