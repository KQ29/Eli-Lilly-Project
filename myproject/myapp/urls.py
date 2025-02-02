from django.urls import path
from .views import home, medicines, add_to_cart, cart

urlpatterns = [
    path('', home, name='home'),
    path('medicines/', medicines, name='medicines'),
    path('add_to_cart/<int:med_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
]
