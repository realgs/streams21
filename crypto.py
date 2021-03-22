import requests
import json
import time


def getPath(currency, category):
  return f'https://bitbay.net/API/Public/{currency}/{category}.json'


def printOffers(offers, title='Offers'):
  print(f'\n{title}:')
  if len(offers) > 6:  # shorten the list
    offers = offers[:3]+['...']+offers[-3:]
  for offer in offers:
    print(offer)

def fetchOffers(currency):
  API = getPath(currency, 'orderbook')
  req = requests.get(API)
  json = req.json()
  return (json['bids'], json['asks'])

def fetchAndPrintOffers(currency):
  bids, asks = fetchOffers(currency)
  printOffers(bids, f'{currency} Bids')
  printOffers(asks, f'{currency} Asks')


def startStream(currency, frequency):
  while 1:
    bids, asks = fetchOffers(currency)
    last_bid_rate = bids[0][0]
    last_ask_rate = asks[0][0]
    stat = 1 - (last_ask_rate - last_bid_rate) / last_bid_rate
    print(f'Percentage: {stat}')
    stream.append(stat)
    print(f'Stream: {stream}')
    print(f'Sleeping for {frequency}s...')
    time.sleep(frequency)


RESOURCES = ['BTCUSD','LTCUSD','ETHUSD']
FREQUENCY = 5  # seconds

if __name__ == '__main__':
  # 1
  for currency in RESOURCES:
    fetchAndPrintOffers(currency)
  # 2
  stream = []
  startStream(RESOURCES[0], FREQUENCY)
