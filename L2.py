import requests
import time

#2.1
def PobieranieDanych():

    x = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json").json()
    print(x)
    y = requests.get("https://bitbay.net/API/Public/EURPLN/orderbook.json").json()
    print(y)
    z = requests.get("https://bitbay.net/API/Public/USDPLN/orderbook.json").json()
    print(z)


PobieranieDanych()

#2.2
def Różnica5sek():

    while 1:
        dict = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json").json()
        bid1 = float(dict["bids"][0][0]) #Kupno
        ask1 = float(dict["asks"][0][0]) #Sprzedaż
        roznica = float(((1 - (ask1 - bid1)) / ask1) * 100)
        print("Procentowa różnica między kupnem a sprzedażą to:", roznica, "%")
        print("Pętla rozpoczęta")
        t = 5
        time.sleep(t)
        print("Mineło %d sek" % (t))

    #dict = requests.get("https://bitbay.net/API/Public/EURPLN/orderbook.json").json()
    #for Wartosc in dict:
            #print(Wartosc)
            #print("Pętla rozpoczęta")
            #t = 5
            #time.sleep(t)
            #print("Mineło %d sek" % (t))








Różnica5sek()