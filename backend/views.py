from django.http import JsonResponse, HttpResponse
from .models import Currency
import requests
from django.shortcuts import render
from .utils import get_crypto_prices
from django.db.models import ObjectDoesNotExist
from datetime import datetime, timedelta

last_request_times = {}


def index(request):
    return HttpResponse("Hello, world. You're at the index page.")

def update_prices(request):
    # Fetch prices from an external API (replace 'URL_OF_EXTERNAL_API' with actual API URL)
    response = requests.get(' https://api.coingecko.com/api/v3/coins/markets')
    data = response.json()

    # Update Currency model with fetched prices
    for currency_data in data:
        currency_name = currency_data['name']
        currency_symbol = currency_data['symbol']
        currency_price = currency_data['price']

        # Update or create currency entry
        currency, created = Currency.objects.update_or_create(
            name=currency_name,
            defaults={'symbol': currency_symbol, 'price': currency_price}
        )

    return JsonResponse({'message': 'Prices updated successfully'})

def home(request):
    # Get all currencies from the database
    currencies = Currency.objects.all()

    # Create a dictionary to store currency prices
    currency_prices = {}
    for currency in currencies:
        currency_prices[currency.name] = currency.price

    # Pass the currency prices to the template
    return render(request, 'home.html', {'currency_prices': currency_prices})

import requests

# Define a dictionary to store the last request time for each IP address
last_request_times = {}

# Define the rate limit: maximum number of requests allowed per minute from the same IP address
RATE_LIMIT = 60  # Adjust as needed

def get_prices(request):
    try:
        ip = request.META.get('REMOTE_ADDR')
        now = datetime.now()

        # Check if the IP address has made more than the allowed number of requests within the last minute
        if ip in last_request_times:
            num_requests = sum(1 for t in last_request_times[ip] if now - t < timedelta(minutes=1))
            if num_requests >= RATE_LIMIT:
                # Return a rate limit exceeded response
                return JsonResponse({'error': 'Rate limit exceeded. Please try again later.'}, status=429)

        # Update the last request time for this IP address
        if ip not in last_request_times:
            last_request_times[ip] = []
        last_request_times[ip].append(now)

        # Fetch updated exchange rates from the Coinbase API
        response = requests.get('https://api.coinbase.com/v2/exchange-rates', params={'currency': 'USD'})

        # Check if the response indicates a rate limit error
        if response.status_code == 429:
            return JsonResponse({'error': 'Rate limit exceeded. Please try again later.'}, status=429)

        data = response.json()
        
        # Process the response data to extract exchange rates for different currencies relative to USD
        exchange_rates = data['data']['rates']

        # Prepare the response with pairs of currencies to USD
        currencies_to_usd = {}
        for currency_code, exchange_rate in exchange_rates.items():
            currencies_to_usd[currency_code] = exchange_rate

        # Return the exchange rates of currencies to USD
        return JsonResponse({'currencies_to_usd': currencies_to_usd}, status=200)

    except Exception as e:
        # Handle any exceptions and return an error response
        return JsonResponse({'error': str(e)}, status=500)
    
# Add or modify the existing view to fetch and return currency pairs data from the Coinbase API
# def get_currency_pairs(request):
#     try:
#         # Fetch currency pairs data from the Coinbase API
#         response = requests.get('https://api.coinbase.com/v2/exchange-rates')
        
#         # Check if the request was successful
#         if response.status_code == 200:
#             data = response.json()['data']['rates']
            
#             # Extract relevant data for currency pairs
#             currency_pairs = {}
#             for currency, rate in data.items():
#                 currency_pairs[currency] = rate
            
#             # Return currency pairs data as JSON response
#             return JsonResponse(currency_pairs)
#         else:
#             # Return an error response if the request failed
#             return JsonResponse({'error': 'Failed to fetch currency pairs.'}, status=500)

            
#     except Exception as e:
#         # Return an error response for any exceptions
#         return JsonResponse({'error': str(e)}, status=500)
def get_currency_pairs(request):
    try:
        # Fetch currency pairs data from the Coinbase API
        response = requests.get('https://api.coinbase.com/v2/exchange-rates')
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()['data']['rates']
            
            # Extract relevant data for currency pairs with titles
            currency_pairs = [{'currency': currency, 'rate': rate} for currency, rate in data.items()]
            
            # Return currency pairs data as JSON response
            return JsonResponse({'currency_pairs': currency_pairs})
        else:
            # Return an error response if the request failed
            return JsonResponse({'error': 'Failed to fetch currency pairs.'}, status=500)
            
    except Exception as e:
        # Return an error response for any exceptions
        return JsonResponse({'error': str(e)}, status=500)