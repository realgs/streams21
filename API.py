import requests
import time

def calculate(buyPrice, sellPrice):
    difference = round((1 - (sellPrice - buyPrice) / buyPrice), 3)
    print(str(difference) + "%")

def getCurrencyData(currency, category):
    print(f"Różnica kupna a sprzedaży waluty: {currency}")
    url = f"https://bitbay.net/API/Public/{currency}/{category}.json"
    response = requests.get(url).json()
    sellPrice = response['ask']
    buyPrice = response['bid']
    calculate(buyPrice, sellPrice)

if __name__ == "__main__":
    while(True):
        print("===================================================")
        print("POBIERAMY DANE")
        getCurrencyData("BTC", "ticker") #bitcoin
        getCurrencyData("LTC", "ticker") #litecoin
        getCurrencyData("ETH", "ticker") #ethereum
        time.sleep(5)
