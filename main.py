import requests
from time import sleep
from math import inf

# 1
def print_trades(crypt): # podział na drobniejsze funkcje (nazwa odpowiadająca działaniu, które wykonuje funkcja) i odwoływane się ni nich
    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json".format(Currency=[crypt, 'USD'],
                                                                                            Category='trades')
    response = requests.get(url)
    if response.status_code != 200:
        print("Status_code : ", response.status_code)
    else:
        print(response.json())

for crypt in ['BTC', 'LTC', 'DASH']: # funkcja zawieszona w powietrzu
    print_trades(crypt)

    
# 2
def data_stream(crypt, period):
    url = "https://bitbay.net/API/Public/{Currency[0]}{Currency[1]}/{Category}.json".format(Currency=[crypt, 'USD'],
                                                                                            Category='trades')
    while 1: #lepiej nie używać nieskończonych pętli
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            max_sell = -inf
            min_buy = inf
            for trade in data:
                if trade['type'] == 'sell':
                    if max_sell < trade['price']:
                        max_sell = trade['price']
                elif trade['type'] == 'buy':
                    if min_buy > trade['price']:
                        min_buy = trade['price']
            sell_buy_diff = 1 - (max_sell - min_buy) / min_buy
            print("Difference between sell and buy prices = ", sell_buy_diff * 100, "%")
            sleep(period)
        else:
            print("Can't get data from API \n status code: ", response.status_code)

data_stream('DASH', 5)