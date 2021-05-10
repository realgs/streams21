import requests
import time
from sys import exit
import matplotlib.pyplot as plt
import numpy as np


def link(currency_type):
    return f'https://bitbay.net/API/Public/{currency_type}/orderbook.json'#rozdzielic na pol do stalych co sie da obiekt (moe byc krotka)

def get_data(currency_type): # jeżeli printować wszystkie to tu
    try:
        req = requests.get(link(currency_type)).json()
        bid = req['bids']
        ask = req['asks']
    except Exception as e: # obsługa błęów
        print(e)
        return {}

    return bid, ask

def print_offers(offers):
    if len(offers) > 6:
        short_offers = offers[:3] + ['...'] + offers[-3:]
    for offer in short_offers:
        print(offer)


if __name__ == '__main__':
    SLEEPING_TIME = 5

    currency1 = ['BTC', 'LTC', 'ETH']
    currency2 = 'PLN'
    currency = [c + currency2 for c in currency1]

    bids = []
    asks = []

    plt.ion()
    fig, ax = plt.subplots()
    x, ys, lines = [],[],[]
    line_bids, = ax.plot([],[], label='ETH_bids', marker='o')
    line_asks, = ax.plot([],[], label='ETH_asks', marker='o', linestyle='--')
    lines.append([line_bids,line_asks])

    ax.set_title('Crypto')
    ax.set_xlabel('time [s]')
    ax.set_ylabel('value')
    ax.legend()

    i = 0
    while True:
        x.append(i * SLEEPING_TIME)

        j = 0
        for a, c in enumerate(currency):
            dataset = get_data(c)
            if len(dataset):
                all_bid, all_ask = dataset
                bids.append(all_bid [0] [0])
                asks.append(all_ask [0] [0])
            else:
                print("nie")
                bids.append(None)
                asks.append(None)

 
            ax.set_xlim(min(x) * 1.1  , max(x) * 1.1 )
            ax.set_ylim(min(min(asks), min(bids)) * 1.1 , max(max(asks), max(bids)) * 1.1 )

            lines[0][0].set_xdata(x)
            lines[0][0].set_ydata(asks)
            lines[0][1].set_xdata(x)
            lines[0][1].set_ydata(bids)

            plt.pause(0.1)  # so that I don't get blocked on the API
            j += 1
        time.sleep(SLEEPING_TIME)

        i += 1
        plt.pause(SLEEPING_TIME)