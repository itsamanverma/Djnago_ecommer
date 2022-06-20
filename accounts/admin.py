import imp
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','username','first_name','last_name','last_login','date_joined','is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

admin.site.register(Account,AccountAdmin)