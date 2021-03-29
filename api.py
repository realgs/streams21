import requests
import sys
import time


def path(currency):
    url = f"https://bitbay.net/API/Public/{currency}/orderbook.json"
    return url


def count(bid, ask):
    diff = round((1 - (ask - bid)) / bid, 4)
    return diff


def connect(currency):
    req = requests.get(path(currency))
    if req.status_code == 200:
        json = req.json()
        print("Bids:", json['bids'])
        print("Asks:", json['asks'])

    else:
        print("Failed to connect, try again")
        sys.exit()


def refresh_connect(currency):
    req = requests.get(path(currency))
    connect(currency)
    json = req.json()
    bid = json['bids'][0][0]
    ask = json['asks'][0][0]
    sol = count(bid, ask)
    print(f"Difference between bid and ask: {sol}%")
    time.sleep(5)
    refresh_connect(currency)

