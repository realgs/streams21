import requests
import sys


def path(currency):
    url = f"https://bitbay.net/API/Public/{currency}/ticker.json"
    return url


def connect_and_check(currency):
    req = requests.get(path(currency))
    if req.status_code == 200:
        json = req.json()
        bid_and_ask = [json["bid"], json["ask"]]
        return bid_and_ask
    else:
        print("Failed to connect, try again")
        sys.exit()

