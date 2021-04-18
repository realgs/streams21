import requests
import time
URL = "https://api.bitbay.net/rest/trading/orderbook/"
FIRST_POSITION = 0
FIFE = 5
CURRENCY = ["BTC-USD", "LTC-USD", "DASH-USD"]


def get_data(currency):
    temp_url = URL + currency
    print(temp_url)
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", temp_url, headers=headers).json()

    try:
        buy = float(response['buy'][FIRST_POSITION]['ra'])
        sell = float(response['sell'][FIRST_POSITION]['ra'])
    except ValueError:
        print(">>> ValueError: could not convert string to float ")

    return (buy, sell)



def diff (currency):
    while True:
        buy, sell = get_data(currency)
        print((1 - (sell - buy) / sell) * 100)
        time.sleep(FIFE)

def main():
    diff("DASH-USD")

if __name__ == '__main__':
    main()
