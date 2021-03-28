import requests
import time

def curr_data(currency,category):
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url)
    if response.status_code ==200:
        if category == "orderbook":
            json = response.json()
            response = json
            sell = response['asks']
            buy = response['bids']
            print(f"sprzedaż {currency} wynosi {sell} ")
            print(f"kupno {currency} będzie wynosić {buy} ")
        if category == "ticker":
            json = response.json()
            response = json
            sell = response['ask']
            buy = response['bid']
            percentage(buy, sell, currency)




def percentage(buy,sell,currency):
    result = round((1-(sell-buy)/buy),6)
    print(f"różnica kupna i sprzedaży {currency} wynosi {result} %")


if __name__ == "__main__":
    curr_data("BTCUSD", "orderbook")
    curr_data("LTCUSD", "orderbook")
    curr_data("DASHUSD", "orderbook")
    while True:
        curr_data("BTCUSD", "ticker")
        curr_data("LTCUSD", "ticker")
        curr_data("DASHUSD", "ticker")
        print("................................")
        time.sleep(5)
