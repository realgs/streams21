import requests
import sys
from time import sleep

def getPath(currency, category):
    return f'https://bitbay.net/API/Public/{currency}/{category}.json'

def getOffers(currency, category):
    req = requests.get(getPath(currency,category))
    if req.status_code == 200:
        return (req.json())
    else:
        print (f'Connection error - {currency}')
        sys.exit()


def printOffers(cur, category):
    for currency in cur:
            data = getOffers(currency, category)
            print(f'--- {currency} ---')
            for x in data:
                print(f"Date: {x['date']} | Type: {x['type']} | Price: {x['price']} | Amount: {x['amount']}")

printOffers(['BTC', 'LTCUSD', 'DASHUSD'],'trades')

def priceDiff(buy,sell):
    return round(100*(1-sell/buy),2)

def ticker(currency):
    data = getOffers(currency, 'ticker')
    buy = data["bid"]
    sell = data["ask"]
    print(f'Currency: {currency} | Bid: {buy} | Ask: {sell} | Diffrence: {priceDiff(buy,sell)} ')

def dataLoop(cur):
    for c in cur:
        ticker(c)
    sleep(5)
    dataLoop(cur)

dataLoop(['BTC', 'LTCUSD', 'DASHUSD'])