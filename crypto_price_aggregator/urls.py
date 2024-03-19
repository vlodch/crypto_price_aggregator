from django.contrib import admin
from django.urls import path, include
from backend.views import index, home, update_prices, get_prices, get_currency_pairs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),  # Include frontend app URLs
    path('api/', include('backend.urls')),  # Include backend app APIs
    path('api/sample/', include('backend.urls')),  # Assuming the sample endpoint is defined in backend.urls
    path('api/home/', include('backend.urls')),  # Assuming the sample endpoint is defined in backend.urls
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('update_prices/', update_prices, name='update_prices'),
    path('prices/', get_prices, name='get_prices'),
    path('api/currency_pairs/', get_currency_pairs, name='get_currency_pairs'),  

]
