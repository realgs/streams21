import requests
import time


base_currency = 'USD'
currencies = ['BTC', 'LTC', 'DASH']
url = 'https://bitbay.net/API/Public/'
post = '/orderbook.json'
time_interval = 5


def get_data(currency):
    try:
        r = requests.get(url+currency+base_currency+post)
        r.raise_for_status()
        return r.json()

    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


if __name__ == '__main__':
    #1
    for currency in currencies:
        r = get_data(currency)
        print(f'{currency+base_currency} -----------------------------------')
        print(r)

    #2
    print('\nThe difference between bids and asks:')
    while True:
        for currency in currencies:
            r = get_data(currency)
            result = 1 - (r['asks'][0][0] - r['bids'][0][0]) / r['bids'][0][0]
            print(f'{currency+base_currency}: ', round(result, 4))

        print('\n')
        time.sleep(time_interval)
