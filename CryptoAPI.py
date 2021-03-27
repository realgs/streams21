import requests
import time

def sellbuy_difference(sells, buys):
    sa,sp,ba,bp = 0,0,0,0
    for s in sells:
        sa, sp = sa+s[0],sp+s[1]
    for b in buys:
        ba, bp = ba+b[0],bp+b[1]
    sellprice = sp/sa
    buyprice= bp/ba
    return (1 - (sellprice - buyprice) / buyprice)


def cryptomarket_3cryptos(crypto1, crypto2, crypto3, currency):
        response1 = requests.get("https://bitbay.net/API/Public/"+crypto1+currency +"/orderbook.json")
        response2 = requests.get("https://bitbay.net/API/Public/"+crypto2+currency +"/orderbook.json")
        response3 = requests.get("https://bitbay.net/API/Public/"+crypto3+currency +"/orderbook.json")

        print(response1.json(), "\n",response2.json(),"\n", response3.json())

def cryptostream(crypto1, crypto2, crypto3, currency, frequency):
    while True:
        response1 = requests.get("https://bitbay.net/API/Public/" + crypto1 + currency + "/orderbook.json")
        response2 = requests.get("https://bitbay.net/API/Public/" + crypto2 + currency + "/orderbook.json")
        response3 = requests.get("https://bitbay.net/API/Public/" + crypto3 + currency + "/orderbook.json")

        print(crypto1+"/"+currency+" : ", sellbuy_difference(response1.json()['asks'], response1.json()['bids']))
        print(crypto2 +"/"+currency+" :", sellbuy_difference(response2.json()['asks'], response2.json()['bids']))
        print(crypto3 +"/"+currency+" :", sellbuy_difference(response3.json()['asks'], response3.json()['bids']))
        time.sleep(frequency)


freq = 5 # frequency of sending requests to the API

#cryptomarket_3cryptos("BTC","ETH","TRX", "USD")
cryptostream("BTC","ETH","TRX", "USD",freq)
