from django.urls import path
from .views import index, home, update_prices, get_prices, get_currency_pairs

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('update_prices/', update_prices, name='update_prices'),
    path('prices/', get_prices, name='get_prices'),
    path('api/currency_pairs/', get_currency_pairs, name='get_currency_pairs'),
    # Define other URL patterns as needed
]
