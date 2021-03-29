import requests
import json
import time


PAIRS = [('BTC','USD'),('ETH','USD'),('BCC','USD')]


def get_orders(first_currency, second_currency):
  try:
    request = requests.get(
      f"https://bitbay.net/API/Public/{first_currency}{second_currency}/orderbook.json"
    )
    orders = request.json()

  except requests.exceptions.RequestException:
    print("Connection problem.")
    return None

  return orders


def print_orders(orders):
  print("Bid orders\n", orders['bids'])
  print("Ask orders\n", orders['asks'])


def calculate_difference(ask_price, bid_price):
  return (1 - (ask_price - bid_price) / bid_price) * 100


for pair in PAIRS:
  print_orders(get_orders(pair[0],pair[1]))
  time.sleep(5)
