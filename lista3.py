import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

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
    bidBTC, askBTC = dataPicker('BTC', 'USD', 'ticker.json')
    bidLTC, askLTC = dataPicker('LTC', 'USD', 'ticker.json')
    bidDASH, askDASH = dataPicker('DASH', 'USD', 'ticker.json')
    points_x.append(datetime.now().strftime("%H:%M:%S"))
    points_BTC_bid.append(bidBTC)
    points_BTC_ask.append(askBTC)
    points_LTC_bid.append(bidLTC)
    points_LTC_ask.append(askLTC)
    points_DASH_bid.append(bidDASH)
    points_DASH_ask.append(askDASH)

    plt.cla()
    plt.plot(points_x, points_BTC_bid, color='#ff4d4d', linewidth=1.5, label='Bids')
    plt.plot(points_x, points_BTC_ask, color='#cc0000', linewidth=1.5, label='Asks')
    plt.plot(points_x, points_LTC_bid, color='#944dff', linewidth=1.5, label='Bids')
    plt.plot(points_x, points_LTC_ask, color='#5200cc', linewidth=1.5, label='Asks')
    plt.plot(points_x, points_DASH_bid, color='#4dff88', linewidth=1.5, label='Bids')
    plt.plot(points_x, points_DASH_ask, color='#00cc44', linewidth=1.5, label='Asks')
    plt.subplots_adjust(bottom=0.15)
    plt.xticks(points_x, rotation=20)
    plt.legend()

if __name__ == '__main__':
    points_x = []
    points_BTC_bid = []
    points_BTC_ask = []
    points_LTC_bid = []
    points_LTC_ask = []
    points_DASH_bid = []
    points_DASH_ask = []

    ani = FuncAnimation(plt.gcf(), animate, interval=3000)
    plt.show()
