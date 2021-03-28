import requests
import time



def errors(request):
    try:
        request.raise_for_status()
    except requests.exceptions.Timeout as to:
        print(f'Request times out {to}')
    except requests.exceptions.TooManyRedirects as tmr:
        print(f'Request exceeds the configured number of maximum redirections {tmr}')
    except requests.exceptions.HTTPError as http:
        print(f'Request returned an unsuccessful status code {http}')
    except requests.exceptions.RequestException as e:
        print(f'In fact, something went wrong but nobody knows what ¯\_(ツ)_/¯ {e}')


def calculations(bid,ask):
    score = round((1 - (ask-bid)/bid),3)
    return score 

def percent_difference(currency,crypto):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}{currency}/ticker.json',timeout=5)
    errors(response)
    r1 = response.json()

    bid = r1['bid']
    ask = r1['ask']

    score = calculations(bid,ask)

    return score

def bidsandasks(currency,crypto):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}{currency}/orderbook.json',timeout=5)
    errors(response)
    r = response.json()

    newline = "\n"

    bid = r['bids']
    ask = r['asks']

    print(f'Ceny sprzedazy {crypto}{currency}: {bid}{newline}')
    
    print(f'Ceny kupna {crypto}{currency}: {ask}{newline}')

    return True


crypto1 = "BTC"
crypto2 = "ETH"
crypto3 = "OMG"
currency = "PLN"


 
bidsandasks(currency,crypto1)
bidsandasks(currency,crypto2)
bidsandasks(currency,crypto3)

while True:
    score = percent_difference(currency,crypto1)
    print(f'Percent difference beetwen bid and ask {crypto1}{currency}: {score}%')
    score = percent_difference(currency,crypto2)
    print(f'Percent difference beetwen bid and ask {crypto2}{currency}: {score}%')
    score = percent_difference(currency,crypto3)
    print(f'Percent difference beetwen bid and ask {crypto3}{currency}: {score}%')
    print(f'--------------------------------------------------------------------')
    time.sleep(5)
