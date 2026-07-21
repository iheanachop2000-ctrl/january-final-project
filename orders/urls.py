from django.urls import path
from .views import manage_cart, add_to_cart, get_cart_items, create_order, get_orders


urlpatterns =[
    path ('cart/', manage_cart),
    path ('cart/add/', add_to_cart),
    path ('cart/items/', get_cart_items),
    path ('checkout/', create_order),
    path ('history/', get_orders),
]