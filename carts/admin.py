from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class cardAdmin(admin.ModelAdmin):
    list_display = ['cart_id','date_added']
    list_filter = ['date_added',]
    search_fields = ['cart_id',]
    ordering = ['date_added',]
    # readonly_fields = ['date_added']
    # fieldsets = [
    #     ('Cart ID', {'fields': ['cart_id']}),
    #     ('Date', {'fields': ['date_added']}),
    # ]
    # class Meta:
    #     model = Cart
    #     verbose_name = 'Cart'
    #     verbose_name_plural = 'Carts'
    #     ordering = ['-date_added']
    #     readonly_fields = ['date_added']
    #     fieldsets = [
    #         ('Cart ID', {'fields': ['cart_id']}),
    #         ('Date', {'fields': ['date_added']}),
    #     ]

class cartItemAdmin(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']
    list_filter = ['product','is_active']
    search_fields = ['product',]
    ordering = ['product',]
    # readonly_fields = ['date_added']
    # fieldsets = [
    #     ('Product', {'fields': ['product']}),
    #     ('Quantity', {'fields': ['quantity']}),
    #     ('Is Active', {'fields': ['is_active']}),
    # ]
    # class Meta:
    #     model = CartItem
    #     verbose_name = 'Cart Item'
    #     verbose_name_plural = 'Cart Items'
    #     ordering = ['-date_added']
    #     readonly_fields = ['date_added']
    #     fieldsets = [
    #         ('Product', {'fields': ['product']}),
    #         ('Quantity', {'fields': ['quantity']}),
    #         ('Is Active', {'fields': ['is_active']}),
    #     ]


admin.site.register(Cart, cardAdmin)
admin.site.register(CartItem, cartItemAdmin)    
