from . import views
from django.urls import path

urlpatterns = [
    path('',views.cart, name='cart'),
]