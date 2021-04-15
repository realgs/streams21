import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


URL_START='http://bitbay.net/API/Public/'
URL_END='USD/ticker.json'
INTERVAL=5

def crypto_get(data):
    try:
        response = requests.get( URL_START + data + URL_END)
        response.raise_for_status()

    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')

    else:
        originalData = response.json()
        return originalData["bid"], originalData["ask"]

def animate(i):
    bid_LSK, ask_LSK = crypto_get(f'LSK', 'USD', 'ticker.json')
    bid_BAT, ask_BAT = crypto_get(f'BAT', 'USD', 'ticker.json')
    bid_ZRX, ask_ZRX = crypto_get(f'ZRX', 'USD', 'ticker.json')

    x_axis.append(datetime.now().strftime("%H:%M:%S"))

    crypto_bid_LSK.append(ask_LSK)
    crypto_ask_LSK.append(bid_LSK)
    crypto_bid_BAT.append(ask_BAT)
    crypto_ask_BAT.append(bid_BAT)
    crypto_bid_ZRX.append(ask_ZRX)
    crypto_ask_ZRX.append(bid_ZRX)

    x_axis_labels=x_axis.copy()

    # while True:
    #     i=5
    #     step=2
    #     if len(x_axis_labels) > i:
    #         x_axis_labels = x_axis_labels[::step]
    #         i+=5
    #         step+=1


    plt.cla()
    # plt.yscale('log')
    plt.plot(x_axis, crypto_bid_LSK, linewidth=1, label='Bids_LSK', color='#002e4d')
    plt.plot(x_axis, crypto_ask_LSK, linewidth=1, label='Asks_LSK', color='#ff99ff')
    plt.plot(x_axis, crypto_bid_BAT, linewidth=1, label='Bids_BAT', color='#e60000')
    plt.plot(x_axis, crypto_ask_BAT, linewidth=1, label='Asks_BAT', color='#ff8533')
    plt.plot(x_axis, crypto_bid_ZRX, linewidth=1, label='Bids_ZRX', color='#00e600')
    plt.plot(x_axis, crypto_ask_ZRX, linewidth=1, label='Asks_ZRX', color='#bfff00')
    plt.subplots_adjust(bottom=0.2, left=0.2, right=0.9)
    plt.xticks(x_axis_labels, rotation=25)

    plt.xlabel('Czas pobrania danych')
    plt.ylabel('Wartość w USD')
    plt.legend()
if __name__ == '__main__':
    x_axis = []
    crypto_bid_LSK = []
    crypto_ask_LSK = []
    crypto_bid_BAT = []
    crypto_ask_BAT = []
    crypto_bid_ZRX = []
    crypto_ask_ZRX = []
    ani = FuncAnimation(plt.gcf(),animate , interval=5000)
    plt.show()

