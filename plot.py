import requests

PAIRS = [('BTC','PLN'), ('ETH','PLN'), ('BCC','PLN')]


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