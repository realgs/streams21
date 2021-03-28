import requests
import sys
import time

def Price_diff(buy_price,sell_price):
    return round(100*(1-(sell_price/buy_price)),2)

def Print_data(currency,c_buy_price,c_sell_price):
    print(f' BUY  SELL    Currency: {currency}')
    print(c_buy_price, c_sell_price)
    print(f'Difference in prices {Price_diff(c_buy_price, c_sell_price)}%' + '\n')

def Download_data(c_currencies,category): #c_currencies is a list
    for currency in c_currencies:
        url=f"https://bitbay.net/API/Public/{currency}/{category}.json"
        status=requests.get(url).status_code
        if status==200:
            data = requests.get(url).json()
            c_buy_price = data['ask']
            c_sell_price = data['bid']
            Print_data(currency,c_buy_price,c_sell_price)
        else:
            print("Could not download data. Try again later!")
            sys.exit()


if __name__=="__main__":
    while True:
        Download_data(['BTCUSD','LTCUSD' ,'DASHUSD'],'ticker')
        time.sleep(5)

