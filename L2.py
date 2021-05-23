import requests
import time


def responseerr(currency,crypto,category):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}{currency}/{category}.json',timeout=5)
    try:
        response
    except requests.exceptions.Timeout as to:
        print(f'Request times out {to}')
    except requests.exceptions.TooManyRedirects as tmr:
        print(f'Request exceeds the configured number of maximum redirections {tmr}')
    except requests.exceptions.HTTPError as http:
        print(f'Request returned an unsuccessful status code {http}')
    except requests.exceptions.RequestException as e:
        print(f'In fact, something went wrong but nobody knows what ¯\_(ツ)_/¯ {e}')
    return response

def calculations(bid,ask):
    score = round((1 - (ask-bid)/bid),3)
    return score 

def percent_difference(currency,crypto):
    CATEGORY = "ticker"
    response = responseerr(currency,crypto,CATEGORY)
    r1 = response.json()

    bid = r1['bid']
    ask = r1['ask']

    score = calculations(bid,ask)

    return score

def bidsandasks(currency,crypto):
    CATEGORY = "orderbook"
    response = responseerr(currency,crypto,CATEGORY)
    r1 = response.json()

    newline = "\n"
    
    bid = r1['bids']
    ask = r1['asks']

    print(f'Ceny sprzedazy {crypto}{currency}: {bid}{newline}')
    
    print(f'Ceny kupna {crypto}{currency}: {ask}{newline}')

    return True


CRYPTO1 = "BTC"
CRYPTO2 = "ETH"
CRYPTO3 = "OMG"
CURRENCY = "PLN"

CRYPTOS = [CRYPTO1, CRYPTO2, CRYPTO3]

def bidsandasksloop(currency,cryptos):
    for crypto in CRYPTOS: 
        bidsandasks(currency,crypto)

# bidsandasksloop(CURRENCY,CRYPTOS)


while True:
    for crypto in CRYPTOS:
        score = percent_difference(CURRENCY,crypto)
        print(f'Percent difference beetwen bid and ask {crypto}{CURRENCY}: {score}%')
    time.sleep(5)
