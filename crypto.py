import requests
import json
import time


def getPath(currency, category):
  # return 'https://bitbay.net/API/Public/THISISWRONG'
  return f'https://bitbay.net/API/Public/{currency}/{category}.json'


def printOffers(offers, title='Offers'):
  print(f'{title}:')
  if len(offers) > 6:  # shorten the list
    offers = offers[:3]+['...']+offers[-3:]
  for offer in offers:
    print(offer)

def fetchOffers(currency):
  API = getPath(currency, 'orderbook')
  req = requests.get(API)
  if req.status_code == 200:
    json = req.json()
    return (json['bids'], json['asks'])
  else:
    print('Error: Connection failed')
    return ()


def fetchAndPrintOffers(currency):
  print('\nFetching data from an external API... ')
  offers = fetchOffers(currency)
  if len(offers):
    bids, asks = offers
    printOffers(bids, f'{currency} Bids')
    printOffers(asks, f'{currency} Asks')
  else:
    print('No data')

def startStream(currency, frequency):
  while 1:
    print('\nFetching data from an external API... ')
    offers = fetchOffers(currency)
    if len(offers):
      bids, asks = offers
      last_bid_rate = bids[0][0]
      last_ask_rate = asks[0][0]
      stat = 1 - (last_ask_rate - last_bid_rate) / last_bid_rate
      print(f'Percentage: {stat}')
      stream.append(stat)
      print(f'Stream: {stream}')
      print(f'Sleeping for {frequency}s...')
    else:
      print('No data. Trying again...')
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
