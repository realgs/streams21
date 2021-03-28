import requests
import time

#2.1
def PobieranieDanych():

    x = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json").json()
    y = requests.get("https://bitbay.net/API/Public/EURPLN/orderbook.json").json()
    z = requests.get("https://bitbay.net/API/Public/USDPLN/orderbook.json").json()

    print(x)
    print(y)
    print(z)

PobieranieDanych()

#2.2
def Różnica5sek():

    while 1:
        a = requests.get("https://bitbay.net/API/Public/EURPLN/orderbook.json").json()
        bid1 = a['bids'][0]
        ask1 = a['asks'][0]
        roznica = 1 - (ask1 - bid1) / ask1
        print("Procentowa różnica między kupnem a sprzedażą to:", roznica)

        print("Pętla rozpoczęta")
        t = 5
        time.sleep(t)
        print("Mineło %d sek"%(t))

Różnica5sek()