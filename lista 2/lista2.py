import requests

def sell_offer (fromTo, N):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{fromTo}"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()

    i = 0
    while i < N:
        print(response['sell'][i]['ra'])
        i += 1

def buy_offer (fromTo, N):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{fromTo}"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()

    i = 0
    while i < N:
        print(response['buy'][i]['ra'])
        i += 1

def main():
    print("Sprzedaż:")
    sell_offer("BTC-USD", 3)
    print("Kupno:")
    buy_offer("BTC-USD", 3)
    print("Sprzedaż:")
    sell_offer("LTC-USD", 10)
    print("Kupno:")
    buy_offer("LTC-USD", 10)
    print("Sprzedaż:")
    sell_offer("DASH-USD", 5)
    print("Kupno:")
    buy_offer("DASH-USD", 5)


if __name__ == '__main__':
    main()