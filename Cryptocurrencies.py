import requests
import sys

def Price_diff(buy_price,sell_price):
    return round(100*(1-sell_price/buy_price),2)

def Download_data(c_currencies,Category): #c_currencies is a list
    for Currency in c_currencies:
        url=f"https://bitbay.net/API/Public/{Currency}/{Category}.json"
        status=requests.get(url).status_code
        if status==200:
            data = requests.get(url).json()
            c_buy_price = data['ask']
            c_sell_price = data['bid']
            Price_diff(c_buy_price,c_sell_price)
        else:
            print("Could not download data. Try again later!")
            sys.exit()

Download_data(['BTCUSD','LTCUSD' ,'DASHUSD'],'ticker')

