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


def fetchFromAPI(currencies, category):
    result = []
    for currency in currencies:
        data = download_data(currency, category)
        sleep(SLEEP_VALUE)
        buy_price = data['ask']
        sell_price = data['bid']
        result.append([currency, buy_price, sell_price])
    return result


def calculate_percentage_diffrence_of_buy_and_sell_price(buy_price, sell_price):
    return round(100*(1-sell_price/buy_price), 3)

def split_data_into_packages(data):
    names = []
    result = {}
    for val in data:
        names.append(val[0])
        ask = val[1]
        bid = val[2]
        time = datetime.now().strftime("%H:%M:%S")
        result.setdefault('ask', []).append(ask)
        result.setdefault('bid', []).append(bid)
    return names, result


if __name__ == "__main__":
    currencies = ['BTC', 'LTC', 'DASH']
    currency = 'USD'
    currencies = add_currency_to_currencies(currencies, currency)
    category = 'ticker'
    refreshing_results(currencies, category)