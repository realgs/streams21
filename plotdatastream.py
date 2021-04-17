import requests
import time
import matplotlib.pyplot as plt
import numpy as np
interval = 5
cryptos = ["BTC","ETH","TRX"]
currency = "USD"


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


def cryptostream_to_plot(crypto_set, currency, interval):
    all_data = []
    while True:
        c_list = []
        for crypto in crypto_set:
            response = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/orderbook.json", timeout=5)
            handle_exceptions(response)
            c_list.append([crypto+"/"+currency,sellbuy_difference(response.json()['asks'], response.json()['bids'])])
        all_data.append(c_list)
        graph_gen(all_data,interval)

def graph_gen(all_data,interval):
    t = np.arange(0,5*(len(all_data)),5)
    plt.ion()
    nr = len(all_data[0])
    for c in range(nr):
        y = []
        for set in all_data:
            y.append(set[c][1])
        plt.plot(t,y,"--o",label = all_data[0][c][0])
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("value")
    plt.xlim([-0.25,t[-1]+1])
    plt.draw()
    plt.pause(interval)
    plt.clf()


cryptostream_to_plot(cryptos,currency, interval)


