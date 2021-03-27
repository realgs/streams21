import requests


def getPath(currency, category):
    return f'https://bitbay.net/API/Public/{currency}/{category}.json'

def getOffers(currency, category='trades'):
    req = requests.get(getPath(currency,category))
    if req.status_code == 200:
        return (req.json())
    else:
        print (f'Connection error - {currency}')


def printOffers(cur):
    for currency in cur:
            data = getOffers(currency)
            print(f'--- {currency} ---')
            for x in data:
                print(f"Date: {x['date']} | Type: {x['type']} | Price: {x['price']} | Amount: {x['amount']}")


printOffers(['BTC', 'LTCUSD', 'DASHUSD'])