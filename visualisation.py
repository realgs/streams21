import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt


def diff(purchase, sale):
    return round(((1 - (sale[0][0] - purchase[0][0])/purchase[0][0])*100), 2)


def get_data(currency, p_currency):
    try:
        response = requests.get(f"https://bitbay.net/API/Public/{currency}{p_currency}/orderbook.json")
        response_json = response.json()
        bids = response_json['bids']
        asks = response_json['asks']

        # print(f"{currency}:\n "
        #       f"Purchase price: {bids[0][0]},\n"
        #       f"Selling price: {asks[0][0]},\n "
        #       f"Difference between purchase and selling price: {diff(bids, asks)} %")
        return bids, asks

    except requests.exceptions.HTTPError:
        print("No connection to the server.")
        sys.exit()