import requests
import time
import sys
import urllib.request

def calculate(buy_price, sell_price):
    output = round((1 - (sell_price - buy_price) / buy_price), 3)
    print(str(output) + " %")

def connect():
    try:
        urllib.request.urlopen('http://google.com')
    except:
        print("No internet connection")
        sys.exit()

def getCurrencyData(currency, category):
    connect()
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"-----------{currency}-------------")
        json = response.json()
        response = json
        sell_price = response['ask']
        buy_price = response['bid']
        calculate(buy_price, sell_price)
    else:
        print("Error when trying to fetch")
        sys.exit()

if __name__ == "__main__":
    while(True):
        print("=======DATA========")
        getCurrencyData("BTC", "ticker")
        getCurrencyData("ETH", "ticker")
        getCurrencyData("ZEC", "ticker")
        time.sleep(5)
        