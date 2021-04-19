from requests.exceptions import HTTPError
import requests
import time
import matplotlib.pyplot as plt


url_1 = 'https://bitbay.net/API/Public/'
currency = 'LTC'
base = 'USD'
url_2 = '/ticker.json'
frequency = 1


def data():
    try:
        response = requests.get(url_1 + currency + base + url_2)
        response.raise_for_status()
        return response.json()
    except HTTPError:
        print('HTTP error:', HTTPError)
    except Exception:
        print('Other error:', Exception)


def graph():

    asks = []
    bids = []
    times = []
    t = 0

    while True:
        response = data()
        asks.append(response['ask'])
        bids.append(response['bid'])
        t += 1
        times.append(t)
        plt.plot(times, asks)
        plt.plot(times, bids)
        plt.xlim(0, 100)
        plt.ylim(max(bids) * 0.9, max(asks) * 1.1)
        plt.show()
        time.sleep(frequency)


graph()
