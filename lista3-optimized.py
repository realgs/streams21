import matplotlib.pyplot as plt
import requests
import time
from requests.exceptions import HTTPError


url_1 = 'https://bitbay.net/API/Public/'
url_2 = '/ticker.json'
base = 'USD'
currencies = ['BTC', 'LTC', 'DASH']
frequency = 5


def data(currency):
    try:
        response = requests.get(url_1 + currency + base + url_2)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
    except Exception:
        print('Other error:', Exception)


def graph():
    asks = {}
    bids = {}
    for currency in currencies:
        asks[currency] = []
        bids[currency] = []

    times = []
    t = 0

    plt.ion()
    figure, ax = plt.subplots(len(currencies), 1, figsize=(9, 8))

    sections = []
    for i in range(len(currencies)):
        sections.append(ax[i].plot(times, asks[currencies[i]], label="asks")[0])
        sections.append(ax[i].plot(times, bids[currencies[i]], label="bids")[0])
        ax[i].set_title(currencies[i])
        ax[i].set_xlim(0, 50)
        ax[i].legend()

    while True:
        for currency in currencies:
            response = data(currency)
            asks[currency].append(response['ask'])
            bids[currency].append(response['bid'])

        t += 1
        times.append(t)

        c = 0
        for i in range(len(sections)):
            if i % 2 == 0:
                sections[i].set_data(times, asks[currencies[c]])
            else:
                sections[i].set_data(times, bids[currencies[c]])
                c += 1

        for i in range(len(currencies)):
            ax[i].set_ylim(max(bids[currencies[i]]) * 0.8, max(asks[currencies[i]])*1.2)

        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(frequency)


graph()
