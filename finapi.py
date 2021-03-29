import requests
import json
import time


PAIRS = [('BTC','USD'),('ETH','USD'),('BCC','USD')]


def print_orders(first_currency, second_currency):

  try:
    request = requests.get(
      f"https://bitbay.net/API/Public/{first_currency}{second_currency}/orderbook.json"
    )
    orders = request.json()
    print("Bid orders\n", offers['bids'])
    print("Ask orders\n", offers['asks'])

  except requests.exceptions.RequestException as ex:
    orders = None

  return orders

print_offers(PAIRS[0][0],PAIRS[0][1])

