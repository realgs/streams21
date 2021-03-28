import requests
import sys
import time

def diff(purchase, sale):
    return round(((1 - (sale[0][0] - purchase[0][0])/purchase[0][0])*100), 2)

def get_data(currency):
    try:
        response = requests.get(f"https://bitbay.net/API/Public/{currency}/orderbook.json")
        response_json = response.json()
        bids = response_json['bids']
        asks = response_json['asks']

        print(f"{currency}:\n "
              f"Purchase price: {bids[0][0]},\n"
              f"Selling price: {asks[0][0]},\n "
              f"Difference between purchase and selling price: {diff(bids, asks)} %")
    except requests.exceptions.HTTPError:
        print("No connection to the server.")
        sys.exit()



currency = ['BTC', 'BCC', 'DASH']
while True:
    print(get_data(currency[0]))
    print(get_data(currency[1]))
    print(get_data(currency[2]))
    time.sleep(5)







