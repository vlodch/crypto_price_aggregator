import requests

def get_crypto_prices():
    bitcoin_price = get_bitcoin_price()
    ethereum_price = get_ethereum_price()
    return {"bitcoin": bitcoin_price, "ethereum": ethereum_price}

def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["bpi"]["USD"]["rate_float"]
    else:
        return None

def get_ethereum_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["ethereum"]["usd"]
    else:
        return None
