import requests
import time

def percent_differnce(buy, sell):
    difference = round((1 - (sell - buy) / buy), 4)
    print(difference, "%")

def Values(currency):
    r = requests.get("https://bitbay.net/API/Public/"+currency+"/orderbook.json")
    if r.status_code == 200:
        values = r.json()
        buy = values["bids"][0][0]
        sell = values["asks"][0][0]
        percent_differnce(buy,sell)
    else:
        print("Something went wrong")

list_of_currency = ["BTC","LTC","DASH"]

while(True):
    for i in list_of_currency:
        Values(i)
    print()
    time.sleep(5)
