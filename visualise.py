import requests as r
from time import sleep

SLEEP_VALUE = 5


def add_currency_to_currencies(currencies, currency):
    result = []
    for c in currencies:
        result.append(c+currency)
    return result


def download_data(currency, caregory):
    URL = f'https://bitbay.net/API/Public/{currency}/{category}.json'
    try:
        response = r.get(URL)
        response.raise_for_status()

    except HTTPError:
        print(f'Error: : {HTTPError}')

    else:
        return response.json()
    return r.get(URL).json()


def print_data(currency, buy_price, sell_price):
    print(
        f'Currency: {currency} Buy price: {buy_price} Sell price: {sell_price}')


def fetchFromAPI(currencies, category):  # 1
    result = []
    for currency in currencies:
        data = download_data(currency, category)
        sleep(1)  # Cooldown between download data in loop
        buy_price = data['ask']
        sell_price = data['bid']
        print_data(currency, buy_price, sell_price)
        result.append([currency, buy_price, sell_price])
    # example [['BTCUSD', 59899.79, 58567.03], ['LTCUSD', 199.99, 185.1], ['DASHUSD', 224.9, 201.74]]
    return result


def calculate_percentage_diffrence_of_buy_and_sell_price(buy_price, sell_price):
    return round(100*(1-sell_price/buy_price), 3)


def refreshing_results(currencies, category):  # 2
    while(True):
        data = fetchFromAPI(currencies, category)
        i = 0
        for currency in currencies:
            print(
                f'{currency} % diffrence between sell and buy price: {calculate_percentage_diffrence_of_buy_and_sell_price(data[i][1],data[i][2])}%')
            i += 1
        print('======================')
        sleep(SLEEP_VALUE)


if __name__ == "__main__":
    currencies = ['BTC', 'LTC', 'DASH']
    currency = 'USD'
    currencies = add_currency_to_currencies(currencies, currency)
    category = 'ticker'
    refreshing_results(currencies, category)