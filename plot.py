import requests
import sys
import matplotlib.pyplot as plt
import datetime


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


def animated_plot(i):
    time = datetime.datetime.now()
    x_val.append(time.strftime('%H:%M:%S'))

    bid_and_ask_BTC = connect_and_check(f'{crypto[0]}{curr}')
    bid_y_val_BTC.append(bid_and_ask_BTC[0])
    ask_y_val_BTC.append(bid_and_ask_BTC[1])

    bid_and_ask_LTC = connect_and_check(f'{crypto[1]}{curr}')
    bid_y_val_LTC.append(bid_and_ask_LTC[0])
    ask_y_val_LTC.append(bid_and_ask_LTC[1])

    bid_and_ask_DASH = connect_and_check(f'{crypto[2]}{curr}')
    bid_y_val_DASH.append(bid_and_ask_DASH[0])
    ask_y_val_DASH.append(bid_and_ask_DASH[1])

    plt.cla()
    plt.plot(x_val, bid_y_val_BTC)
    plt.plot(x_val, ask_y_val_BTC)
    plt.plot(x_val, bid_y_val_LTC)
    plt.plot(x_val, ask_y_val_LTC)
    plt.plot(x_val, bid_y_val_DASH)
    plt.plot(x_val, ask_y_val_DASH)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(["Bid BTC", "Ask BTC", "Bid LTC", "Ask LTC", "Bid DASH", "Ask DASH"])
