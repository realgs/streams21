import requests
from requests.exceptions import HTTPError
from time import sleep


def data_bit_bay1(currency1, n):
    try:
        response1 = requests.get(f'https://bitbay.net/API/Public/{currency1}/USD/orderbook.json')
        response1.raise_for_status()
    except HTTPError as http_error:
        print(f'Error! Operation failed:{http_error}')
    except Exception as error:
        print(f'Error! Operation failed:{error}')
    else:
        response2 = response1.json()
        bids = response2['bids']
        for i in range(n):
            print(f'{currency1} USD', bids[i])


def data_bit_bay2(currency2):
    try:
        response3 = requests.get(f'http://bitbay.net/API/Public/{currency2}/USD/orderbook.json')
        response3.raise_for_status()
    except HTTPError as http_error:
        print(f'Error! Operation failed:{http_error}')
    except Exception as error:
        print(f'Error! Operation failed:{error}')
    else:
        response4 = response3.json()
        bids_price = response4['bids'][0][1]
        asks_price = response4['asks'][0][1]
        result = round((1 - (asks_price - bids_price) / bids_price), 2)
        print(f'{currency2} : {result} % ')


def show_data():
    print('Purchase price')
    data_bit_bay1('BTC', 3)
    data_bit_bay1('LTC', 3)
    data_bit_bay1('DASH', 3)


def discreate_data_stream():
    print('The difference between buying and selling:')
    while True:
        data_bit_bay2('BTC')
        data_bit_bay2('LTC')
        data_bit_bay2('DASH')
        sleep(5)


#show_data()
discreate_data_stream()
