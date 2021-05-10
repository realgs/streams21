import requests
import time
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def responseerr(crypto):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}/ticker.json',timeout=5)
    try:
        response
    except requests.exceptions.Timeout as to:
        print(f'Request times out {to}')
    except requests.exceptions.TooManyRedirects as tmr:
        print(f'Request exceeds the configured number of maximum redirections {tmr}')
    except requests.exceptions.HTTPError as http:
        print(f'Request returned an unsuccessful status code {http}')
    except requests.exceptions.RequestException as e:
        print(f'In fact, something went wrong but nobody knows what ¯\_(ツ)_/¯ {e}')
    return response

def bidsandasks(crypto):
    response = responseerr(crypto)
    r1 = response.json()

    bid = r1['bid']
    ask = r1['ask']

    return bid,ask

def bidaskstimelist(currency):
    bid , ask = bidsandasks(f"{CRYPTOS[0]}{currency}")
    BTCbid.append(bid)
    BTCask.append(ask)

    bid , ask = bidsandasks(f"{CRYPTOS[1]}{currency}")
    ETHbid.append(bid)
    ETHask.append(ask)

    bid , ask = bidsandasks(f"{CRYPTOS[2]}{currency}")
    OMGbid.append(bid)
    OMGask.append(ask)

def plot(i):
    time = dt.datetime.now()
    x.append(time.strftime('%H:%M:%S'))

    bidaskstimelist("PLN")

    plt.plot(x,BTCbid)
    plt.plot(x,BTCask)

    plt.plot(x,ETHbid)
    plt.plot(x,ETHask)

    plt.plot(x,OMGbid)
    plt.plot(x,OMGask)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(["Bid BTC", "Ask BTC", "Bid ETH", "Ask ETH", "Bid OMG", "Ask OMG"])

CRYPTOS = ["BTC","ETH","OMG"]
CURRENCY = "PLN"


if __name__ == '__main__':
    x = []
    BTCbid = []
    BTCask = []

    ETHbid = []
    ETHask = []

    OMGbid = []
    OMGask = []

    fig = plt.figure(figsize=(23, 10))
    ani = FuncAnimation(fig, plot, interval=5000)

    plt.show()
