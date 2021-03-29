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
    print("Bid orders\n", orders['bids'])
    print("Ask orders\n", orders['asks'])

  except requests.exceptions.RequestException:
    print("Connection problem.")
    return None

  return orders


for i in PAIRS:
  print_orders(PAIRS[i][0],PAIRS[i][1])
