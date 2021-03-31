import requests
from time import sleep
from numpy import round


currency = ['BTCPLN', 'ETHPLN', 'LSKPLN']
urls = [f'https://bitbay.net/API/Public/{currency[0]}/ticker.json',f'https://bitbay.net/API/Public/{currency[1]}/ticker.json',f'https://bitbay.net/API/Public/{currency[2]}/ticker.json']


def get_data(url):
    response = requests.get(url)
    data = response.json()
    return data

def calculate(url):
    data = get_data(url)
    return ((data['ask'] - data['bid']) / data['bid']) * 100

def show_result():
    while True:
        for i in range (0,len(urls)):
            print(f'For {currency[i]} difference between selling and buying is {round(calculate(urls[i]),5)}% ')
        print("------------------------")
        sleep(5)

show_result()
