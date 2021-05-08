import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
interval = 5
cryptos = ["ETH","LTC","BTC"]
currency = "PLN"
t = []
all_data = []
mlwinwsize = 4
meanlist = []
volstor = []


def maxwinsize(size):
    assert type(size) == int
    assert size >= 2
    if size > 8:
        size = 8

def handlemean(all_data,winsize,meanlist):
    nr = len(all_data[0])
    if len(all_data) >= winsize:
        shift = len(all_data) - winsize
        reg = []
        for c in range(nr):
            cry = []
            for n in range(2):
                sum = 0
                for i in range(0+shift,winsize+shift):
                    sum = sum + all_data[i][c][1][n]
                mean = sum/winsize
                cry.append(mean)
            reg.append(cry)
        meanlist.append(reg)

    else:
        v = []
        for c in range(nr):
            v.append([None,None])
        meanlist.append(v)


def sellbuy(sells, buys):
    sa,sp,ba,bp = 0,0,0,0
    for s in sells:
        sa, sp = sa+s[0],sp+s[1]
    for b in buys:
        ba, bp = ba+b[0],bp+b[1]
    sellprice = sp/sa
    buyprice= bp/ba
    return (sellprice , buyprice)


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


def cryptostream_to_plot(crypto_set, currency, all_data):
    v_list = []
    c_list = []
    for crypto in crypto_set:
        response = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/orderbook.json", timeout=5)
        handle_exceptions(response)
        vol = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/ticker.json", timeout=5)
        handle_exceptions(vol)
        v_list.append(vol.json()['volume'])
        c_list.append([crypto,sellbuy(response.json()['asks'], response.json()['bids'])])
    volstor.append(v_list)
    all_data.append(c_list)


def graph_gen(a):
    cryptostream_to_plot(cryptos,currency,all_data)
    handlemean(all_data, mlwinwsize, meanlist)
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    plt.ion()
    plt.clf()
    plt.suptitle("Wykresy notowań kryptowalut")
    nr = len(all_data[0])
    for c in range(nr):
        plt.subplot(2,nr, c+1)
        ys = []
        yb =[]
        yas = []
        yab = []
        for set in all_data:
            ys.append(set[c][1][0])
            yb.append(set[c][1][1])
        for aveset in meanlist:
            yas.append(aveset[c][0])
            yab.append(aveset[c][1])
        plt.plot(t,ys,"-o",label = all_data[0][c][0] + ": sell")
        plt.plot(t, yb, "-o", label=all_data[0][c][0] + ": buy")
        plt.plot(t, yas, "o--", label=all_data[0][c][0] + ": sell avarage")
        plt.plot(t, yab, "o--", label=all_data[0][c][0] + ": buy avarage")
        plt.ylabel("Value")
        plt.xticks(rotation = 40, fontsize= 7 )
        plt.legend()
    for c in range(nr):
        plt.subplot(2,nr, c+1+nr)
        yv = []
        for vset in volstor:
            yv.append(vset[c])
        plt.bar(t, yv, align="center")
        plt.ylabel("volume")
        plt.xticks(rotation=40, fontsize=7)
#na wykresie lub pod wykresem dodać wolumen transakcji



#dodać oscylator RSI. Przedział y do ustalenia przez użytkownika


def main():
    maxwinsize(mlwinwsize)
    animation = FuncAnimation(plt.figure(), graph_gen, interval= 5000)
    plt.show()

if __name__ == '__main__':
    main()