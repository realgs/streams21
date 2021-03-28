import time
import requests
from requests.exceptions import HTTPError


def calculator():
    currency_base = ['BTC', 'LTC', 'DASH']
    while True:
        for currency in currency_base:
            print(currency)
            new_data = []
            try:
                response = requests.get(url=f'https://bitbay.net/API/Public/{currency}{"USD"}/{"trades"}.json')
                new_data += response.json()

                buy_prices = []
                sell_prices = []

                for data_row in new_data:
                    if data_row["type"] == "buy":
                        buy_prices.append([data_row["date"], data_row["price"]])
                    elif data_row["type"] == "sell":
                        sell_prices.append([data_row["date"], data_row["price"]])

                for i in range(min(len(buy_prices), len(sell_prices))):
                    tmp = (1 - (sell_prices[i][1] - buy_prices[i][1]) / sell_prices[i][1]) * 100
                    print(str(float("{:.2f}".format(tmp))) + "%")

            except HTTPError:
                print('HTTP error:', HTTPError)

            print("\n")
        time.sleep(5)


if __name__ == "__main__":
    calculator()
