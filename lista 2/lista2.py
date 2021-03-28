import requests

def sell_offer (fromTo, N):
    url = f"https://api.bitbay.net/rest/trading/orderbook/{fromTo}"
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()

    i = 0
    while i < N:
        print(response['sell'][i]['ra'])
        i += 1

def main():
    sell_offer("BTC-USD", 3)
    print("=========")
    sell_offer("LTC-USD", 10)
    print("=========")
    sell_offer("DASH-USD", 5)
    print("=========")


if __name__ == '__main__':
    main()