import requests
import time

def calculate(BuyPrice, sellPrice):
    output = round((1 - (sellPrice - BuyPrice) / BuyPrice), 3)
    print(str(output) + " %")

def getCurrencyData(currency, category):
    print(f"-----------{currency}-------------")
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url).json()
    sellPrice = response['ask']
    buyPrice = response['bid']
    calculate(buyPrice, sellPrice)

if __name__ == "__main__":
    while(True):
        print("=======DATA========")
        getCurrencyData("BTC", "ticker")
        getCurrencyData("ETH", "ticker")
        getCurrencyData("ZEC", "ticker")
        time.sleep(5)