import requests
import time
import sys

def calculate(BuyPrice, sellPrice):
    output = round((1 - (sellPrice - BuyPrice) / BuyPrice), 3)
    print(str(output) + " %")

def getCurrencyData(currency, category):
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"-----------{currency}-------------")
        json = response.json()
        response = json
        sellPrice = response['ask']
        buyPrice = response['bid']
        calculate(buyPrice, sellPrice)
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

