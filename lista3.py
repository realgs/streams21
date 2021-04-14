import numpy as np
import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

FREQUENCY = 5
BITBAY_ADRES = 'https://bitbay.net/API/Public'

def dataPicker(resource, currency, format):
    try:
        _ADRES = f'{BITBAY_ADRES}/{resource}/{currency}/{format}'
        response = requests.get(_ADRES)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        _DATA = response.json()
        print(_DATA)
        return _DATA["bid"], _DATA["ask"]

def animate(i):
    bidLSK, askLSK = dataPicker('LSK', 'USD', 'ticker.json')
    bidOMG, askOMG = dataPicker('OMG', 'USD', 'ticker.json')
    bidXRP, askXRP = dataPicker('XRP', 'USD', 'ticker.json')
    points_LSK_bid.append(bidLSK)
    points_LSK_ask.append(askLSK)
    points_OMG_bid.append(bidOMG)
    points_OMG_ask.append(askOMG)
    points_XRP_bid.append(bidXRP)
    points_XRP_ask.append(askXRP)
    points_x.append(datetime.now().strftime("%H:%M:%S"))

    # fig, ax = plt.subplots()  PSUJE SIE PROGRAM

    points_x_labels = points_x.copy()
    if len(points_x_labels) > 10:
        points_x_labels = points_x_labels[::2]
    elif len(points_x_labels) > 20:
        points_x_labels = points_x_labels[::5]

    plt.cla()
    plt.plot(points_x, points_LSK_bid, color='#ff4d4d', linewidth=1.5, label='LSK Bids')
    plt.plot(points_x, points_LSK_ask, color='#cc0000', linewidth=1.5, label='LSK Asks')
    plt.plot(points_x, points_OMG_bid, color='#944dff', linewidth=1.5, label='OMG Bids')
    plt.plot(points_x, points_OMG_ask, color='#5200cc', linewidth=1.5, label='OMG Asks')
    plt.plot(points_x, points_XRP_bid, color='#4dff88', linewidth=1.5, label='XRP Bids')
    plt.plot(points_x, points_XRP_ask, color='#00cc44', linewidth=1.5, label='XRP Asks')
    plt.xticks(points_x_labels, rotation=20)
    plt.xlabel("Czas")
    plt.ylabel("Wartość w dolarach")
    plt.title("Najlepsze kursy kupna oraz sprzedaży")
    # plt.yscale('log', base=2)
    plt.yscale('log')
    plt.subplots_adjust(bottom=0.15)
    plt.legend()


if __name__ == '__main__':
    points_x = []
    points_LSK_bid = []
    points_LSK_ask = []
    points_OMG_bid = []
    points_OMG_ask = []
    points_XRP_bid = []
    points_XRP_ask = []

    ani = FuncAnimation(plt.gcf(), animate, interval=3000)
    plt.show()
