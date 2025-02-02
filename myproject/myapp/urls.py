from django.urls import path
from .views import home, medicines

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('medicines/', medicines, name='medicines'),  # Medicines page
]