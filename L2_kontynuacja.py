import requests
from requests.exceptions import HTTPError
import time
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
        # print(_DATA["bids"])
        # print()
        # print(_DATA["asks"])
        return _DATA["bid"], _DATA["ask"]
def animate(i):
    bid, ask = dataPicker('BTC', 'USD', 'ticker.json')
    points_BTC_x.append(datetime.now().strftime("%H:%M:%S"))
    points_BTC_bid.append(bid)
    points_BTC_ask.append(ask)
    plt.cla()
    plt.plot(points_BTC_x, points_BTC_bid, linewidth=1.5, label='Bids')
    plt.plot(points_BTC_x, points_BTC_ask, linewidth=1.5, label='Asks')
    plt.subplots_adjust(bottom=0.15)
    plt.xticks(points_BTC_x, rotation=20)
    plt.legend()
if __name__ == '__main__':
    points_BTC_x = []
    points_BTC_bid = []
    points_BTC_ask = []
    ani = FuncAnimation(plt.gcf(), animate, interval=15000)
    plt.show()