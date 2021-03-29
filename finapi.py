import requests
import json
import time


PAIRS = [('BTC','USD'), ('ETH','USD'), ('BCC','USD')]


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


def calculate_difference(asks, bids):
  ask_amount, ask_price = 0, 0
  for a in asks:
    ask_amount += a[0]
    ask_price += a[1]

  bid_amount, bid_price = 0, 0
  for b in bids:
    bid_amount += b[0]
    bid_price += b[1]

  final_ask_price = ask_price / ask_amount
  final_bid_price = bid_price / bid_amount

  return round((1 - (final_ask_price - final_bid_price) / final_bid_price), 4)

def discrete_stream(first_currency, second_currency):
  while True:
    try:
      orders = get_orders(first_currency, second_currency)
      asks, bids = orders['asks'], orders['bids']
      diff = calculate_difference(asks, bids)
      print(f'Difference between ask and bid for {first_currency}{second_currency}: {diff}%')
      time.sleep(5)

    except requests.exceptions.RequestException:
      print("Connection problem. Terminating...")
      break


for pair in PAIRS:
  print_orders(get_orders(pair[0],pair[1]))
  time.sleep(5)

discrete_stream(PAIRS[1][0],PAIRS[1][1])