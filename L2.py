import requests
import time
from sys import exit


def connect(currency):
    return f'https://bitbay.net/API/Public/{currency}/orderbook.json'


def calculate_diff(buy, sell):
    return round((1 - (sell - buy) / buy), 3)


def get_values(currency):
    try:
        req = requests.get(connect(currency)).json()
        bid = req['bids']
        ask = req['asks']

    except Exception as e:

        print ('ERROR:', e)

    return bid, ask


def print_data(currency):
    bids, asks = get_values(currency)
    print ("Bid for", currency, "equals", bids, "and asks for", currency, "equals", asks)


def calc_data(currency):
    bids, asks = get_values(currency)

    if len(bids) == 0:
        print ("There is no value to show")

    elif len(asks) == 0:
        print ("There is no value to show")

    else:

        bid = bids[0][0]
        ask = asks[0][0]
        diff = calculate_diff(bid, ask)
        print ("The difference between bids and asks for", currency, "equals", diff)


if __name__ == '__main__':

    currencies = ['BTCUSD', 'LTCUSD', 'ETHUSD']

    while True:

        try:
            for i in currencies:
                calc_data(i)
                time.sleep(5)

        except KeyboardInterrupt:

            print ("Error due to user interuption")
            exit()
