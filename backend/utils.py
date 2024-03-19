# backend/utils.py
import requests

def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,litecoin',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
