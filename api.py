import requests
import sys

def path(currency):
    url = f"https://bitbay.net/API/Public/{currency}/orderbook.json"
    return url

def connect(currency):
    req = requests.get(path(currency))
    if req.status_code == 200:
        json = req.json()
        print("Bids:", json['bids'])
        print("Asks:", json['asks'])

    else:
        print("Failed to connect, try again")
        sys.exit()

