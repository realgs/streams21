import requests
from time import sleep
from numpy import round


currency = ['BTCPLN', 'ETHPLN', 'LSKPLN']


def get_data(currency):
    try:
        response = requests.get(f'https://bitbay.net/API/Public/{currency}/ticker.json')
        data = response.json()
        return data
    except requests.exceptions.MissingSchema:
        print("Missing URL schema (e.g. http or https)")
    except requests.exceptions.ConnectionError:
        print("Connection Error occured")


def calculate_spread(currency):
    data = get_data(currency)
    return ((data['ask'] - data['bid']) / data['bid']) * 100

def show_result(time_interval):
    while True:
        for i in range (0,len(currency)):
            print(f'For {currency[i]} difference between selling and buying is {round(calculate_spread(currency[i]),5)}% ')
        print("------------------------")
        sleep(time_interval)

try:
    show_result(5)
except KeyboardInterrupt:
    print("End of work")
