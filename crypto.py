import requests


def getPath(currency, category):
    return f'https://bitbay.net/API/Public/{currency}/{category}.json'

def getOffers(currency, category='trades'):
    req = requests.get(getPath(currency,category))
    if req.status_code == 200:
        return (req.json())
    else:
        print (f'Connection error - {currency}')


print(getOffers('BTC'))