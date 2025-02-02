from django.urls import path
from .views import (
    home,
    medicines,
    add_to_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
)

urlpatterns = [
    path('', home, name='home'),
    path('medicines/', medicines, name='medicines'),
    path('add_to_cart/<int:med_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('cart/increase/<int:med_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:med_id>/', decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:med_id>/', remove_from_cart, name='remove_from_cart'),
]
