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
    except requests.exceptions.HTTPError as erh:
        print("Http Error:", erh)
    except requests.exceptions.ConnectionError as erc:
        print("Error Connecting:", erc)
    except requests.exceptions.Timeout as ert:
        print("Timeout Error:", ert)
    except requests.exceptions.RequestException as er:
        print("OOps: Something Else", er)


def c3cryptos(c1, c2, c3, currency):
    r1 = requests.get("https://bitbay.net/API/Public/"+c1+currency +"/orderbook.json",timeout=5)
    r2 = requests.get("https://bitbay.net/API/Public/"+c2+currency +"/orderbook.json",timeout=5)
    r3 = requests.get("https://bitbay.net/API/Public/"+c3+currency +"/orderbook.json",timeout=5)

    handle_exceptions(r1)
    handle_exceptions(r2)
    handle_exceptions(r3)

    print(r1.json(), "\n",r2.json(),"\n", r3.json())

def cryptostream(c1, c2, c3, currency, f):
    while True:
        r1 = requests.get("https://bitbay.net/API/Public/" + c1 + currency + "/orderbook.json",timeout=5)
        r2 = requests.get("https://bitbay.net/API/Public/" + c2 + currency + "/orderbook.json",timeout=5)
        r3 = requests.get("https://bitbay.net/API/Public/" + c3 + currency + "/orderbook.json",timeout=5)

        handle_exceptions(r1)
        handle_exceptions(r2)
        handle_exceptions(r3)

        print(c1+"/"+currency+" : ", sellbuy_difference(r1.json()['asks'], r1.json()['bids']))
        print(c2 +"/"+currency+" :", sellbuy_difference(r2.json()['asks'], r2.json()['bids']))
        print(c3 +"/"+currency+" :", sellbuy_difference(r3.json()['asks'], r3.json()['bids']))
        time.sleep(f)



c3cryptos("BTC","ZEC","GNT", "USD")

cryptostream("BTC","ZEC","GNT", "USD",5)
