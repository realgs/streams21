import requests
import time

def percent_differnce(buy, sell):
    difference = round((1 - (sell - buy) / buy), 4)
    print(difference, "%")

def connection(currency):
    r = requests.get("https://bitbay.net/API/Public/" + currency + "/orderbook.json")
    if r.status_code == 200:
        values = r.json()
        print(currency+" purchase list",values["bids"])
        print(currency + " sales list", values["asks"])

def values(currency):
    r = requests.get("https://bitbay.net/API/Public/"+currency+"/ticker.json")
    if r.status_code == 200:
        values = r.json()
        buy = values["bid"]
        sell = values["ask"]
        percent_differnce(buy,sell)
    else:
        print("Something went wrong")

list_of_currency = ["BTC","LTC","DASH"]

for i in list_of_currency:
    connection(i)

while(True):
    for i in list_of_currency:
        values(i)
    print()
    time.sleep(5)
