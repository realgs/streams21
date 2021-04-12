import requests


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

def show_rates():
    for i in range(0,len(currency)):
        data = get_data(currency[i])
        print(f'Currency: {currency[i]} \n Bid: {data["bid"]} Ask: {data["ask"]}')


show_rates()
