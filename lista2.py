import requests
import sys
import time


def currency_data(currency, category):
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url)
    if response.status_code == 200:

        if category == "orderbook":
            json = response.json()
            response = json
            sell_price = response['asks']
            buy_price = response['bids']
            print(f'Ceny sprzedazy {currency} to: {sell_price}')
            print(f'Ceny kupna {currency} to: {buy_price}')

        if category == "ticker":
            json = response.json()
            response = json
            sell_price = response['ask']
            buy_price = response['bid']
            percent_calculation(sell_price, buy_price, currency)

    else:
        print("connection error")
        sys.exit()


def percent_calculation(buy_price, sell_price, currency):
    score = round((1 - (sell_price - buy_price) / buy_price), 5)
    print(f' Procentowa roznica kupna i sprzedazy {currency} wyniosla: {score} %')


if __name__ == "__main__":
    currency_data("BTCUSD", "orderbook")
    currency_data("ETHUSD", "orderbook")
    currency_data("ZECUSD", "orderbook")
    print("--------------------------------------------------------------------")
    while True:
        currency_data("BTCUSD", "ticker")
        currency_data("ETHUSD", "ticker")
        currency_data("ZECUSD", "ticker")
        print("--------------------------------------------------------------------")
        time.sleep(10)
