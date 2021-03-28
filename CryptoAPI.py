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

def handle_exceptions(req):
    try:
        r = req
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def cryptomarket_3cryptos(crypto1, crypto2, crypto3, currency):
        response1 = requests.get("https://bitbay.net/API/Public/"+crypto1+currency +"/orderbook.json",timeout=5)
        response2 = requests.get("https://bitbay.net/API/Public/"+crypto2+currency +"/orderbook.json",timeout=5)
        response3 = requests.get("https://bitbay.net/API/Public/"+crypto3+currency +"/orderbook.json",timeout=5)

        handle_exceptions(response1)
        handle_exceptions(response2)
        handle_exceptions(response3)

        print(response1.json(), "\n",response2.json(),"\n", response3.json())

def cryptostream(crypto1, crypto2, crypto3, currency, frequency):
    while True:
        response1 = requests.get("https://bitbay.net/API/Public/" + crypto1 + currency + "/orderbook.json",timeout=5)
        response2 = requests.get("https://bitbay.net/API/Public/" + crypto2 + currency + "/orderbook.json",timeout=5)
        response3 = requests.get("https://bitbay.net/API/Public/" + crypto3 + currency + "/orderbook.json",timeout=5)

        handle_exceptions(response1)
        handle_exceptions(response2)
        handle_exceptions(response3)

        print(crypto1+"/"+currency+" : ", sellbuy_difference(response1.json()['asks'], response1.json()['bids']))
        print(crypto2 +"/"+currency+" :", sellbuy_difference(response2.json()['asks'], response2.json()['bids']))
        print(crypto3 +"/"+currency+" :", sellbuy_difference(response3.json()['asks'], response3.json()['bids']))
        time.sleep(frequency)



cryptomarket_3cryptos("BTC","ETH","TRX", "USD")

cryptostream("BTC","ETH","TRX", "USD",5)
