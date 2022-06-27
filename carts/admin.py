from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     readonly_fields = ('cart',)
#     fields = ('product', 'quantity', 'is_active')
#     ordering = ('-is_active',)
#     can_delete = False
#     verbose_name_plural = 'Cart Items'
#     verbose_name = 'Cart Item'

admin.site.register(Cart)
admin.site.register(CartItem)
