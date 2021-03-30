import requests
import time

def sell_offer (currency, N):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{currency}"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()

    i = 0
    result = []
    while i < N:
        result.append(response['sell'][i]['ra'])
        i += 1
    return result

def buy_offer (currency, N):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{currency}"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()

    i = 0
    result = []
    while i < N:
        result.append(response['buy'][i]['ra'])
        i += 1
    return result

def diff (currency):
    while True:
        sell = float(sell_offer(currency, 1)[0])
        buy = float(buy_offer(currency, 1)[0])
        print(1 - (sell - buy) / sell)
        time.sleep(5)

def main():
    # print("BTC-USD")
    # print("Sell prices:", sell_offer("BTC-USD", 3))
    # print("Buy prieces:", buy_offer("BTC-USD", 3))
    # print("LTC-USD")
    # print("Sell prieces:", sell_offer("LTC-USD", 10))
    # print("Buy prieces:", buy_offer("LTC-USD", 10))
    # print("DASH-USD")
    # print("Sell prieces:", sell_offer("DASH-USD", 5))
    # print("Buy prieces:", buy_offer("DASH-USD", 5))
    print("------------")
    # diff("BTC-USD")
    # diff("LTC-USD")
    diff("DASH-USD")

if __name__ == '__main__':
    main()
