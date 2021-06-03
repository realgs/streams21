import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

Interval = 5
Cryptos = ["ETH","LTC","BTC"]
Currency = "PLN"
T = []
All_data = []
Mlwinwsize = 3
Meanlist = []
Volstor = []
Rsisize = 3
Rsistore = []
Y = 6
X = 0.1
S = 50
Tranurl = "https://api.bitbay.net/rest/trading/transactions/"
Apiurl = "https://bitbay.net/API/Public/"

def spread(Y,S,All_data,C):
    if Y > len(All_data):
        y = len(All_data)
    else:
        y = Y
    sbuy = float(0)
    ssell = float(0)
    for i in range(-y,-1):
        ssell = ssell + float(All_data[i][C][1][0])
        sbuy = sbuy +float(All_data[i][C][1][1])
    spr = ((sbuy - ssell) / sbuy )* 100
    if spr < S:
        return True
    else:
        return False

def transactions(Y,X,Crypto,Currency):
    y = Y
    queryparams = {'limit': y}
    tran = requests.get(Tranurl + Crypto + '-' + Currency, params = queryparams)
    handle_exceptions(tran)
    tran = tran.json()
    vlist = []
    for i in tran['items']:
        vlist.append(i['r'])
    maxl = float(max(vlist))
    minl = float(min(vlist))
    value = ((maxl - minl) / maxl) * 100
    if value > X:
        return True
    else:
        return False



def candidate():
    vl = []
    for c in range(len(Cryptos)):
        if Rsistore[-1][c][0] != None:
            if Rsistore[-1][c][0] < 50:
                vl.append(None)
            else:
                vl.append(Volstor[-1][c])
        else:
            vl.append(None)
    v = -1
    vv = 0
    for i in range(len(vl)):
        if vl[i] != None:
            if vl[i] > vv:
                vv = vl[i]
                v = i
    return v

def get_volumen(Crypto,Currency):
    fromtime = datetime.now() - timedelta(minutes=0.5)
    fromtime = int(fromtime.timestamp()) * 100
    queryparams = {'fromTime': fromtime}
    response = requests.get(Tranurl + Crypto + "-" + Currency, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))]) * 10

def rsicount(All_data, store,size):
    nr = len(All_data[0])
    if len(All_data) >= size:
        shift = len(All_data) - size
        reg = []
        for c in range(nr):
            cry = []
            for n in range(2):
                p = 0
                m = 0
                pc = 0
                mc = 0
                for i in range(0 + shift, size + shift - 1):
                    change = float(All_data[i + 1][c][1][n]) - float(All_data[i][c][1][n])
                    if change > 0:
                        p += change
                        pc += 1
                    elif change < 0:
                        m -= change
                        mc += 1
                if pc == 0:
                    pc = 1
                if mc == 0:
                    mc = 1
                a = p / pc
                b = m / mc
                if b == 0:
                    b = 1
                rsi = 100 - 100/(1 + a / b)
                cry.append(rsi)
            reg.append(cry)
        store.append(reg)

    else:
        r = []
        for c in range(nr):
            r.append([None,None])
        store.append(r)


def handlemean(All_data, winsize, Meanlist):
    nr = len(All_data[0])
    if len(All_data) >= winsize:
        shift = len(All_data) - winsize
        reg = []
        for c in range(nr):
            cry = []
            for n in range(2):
                sum = 0
                for i in range(0 + shift,winsize + shift):
                    sum = sum + All_data[i][c][1][n]
                mean = sum/winsize
                cry.append(mean)
            reg.append(cry)
        Meanlist.append(reg)

    else:
        v = []
        for c in range(nr):
            v.append([None,None])
        Meanlist.append(v)


def sellbuy(sells, buys):
    sa,sp,ba,bp = 0,0,0,0
    for s in sells:
        sa, sp = sa + s[0],sp + s[1]
    for b in buys:
        ba, bp = ba + b[0],bp + b[1]
    sellprice = sp
    buyprice= bp
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
        response = requests.get(Apiurl + crypto + currency + "/orderbook.json", timeout=15)
        handle_exceptions(response)
        v_list.append(get_volumen(crypto,currency) * 10)
        c_list.append([crypto,sellbuy(response.json()['asks'], response.json()['bids'])])
    Volstor.append(v_list)
    all_data.append(c_list)

def graph_gen(a):
    global T
    T.append(time.strftime("%H:%M:%S", time.localtime()))
    if len(T) > 8:
        T= T[-8:]
    cryptostream_to_plot(Cryptos,Currency,All_data)
    handlemean(All_data, Mlwinwsize, Meanlist)
    rsicount(All_data, Rsistore, Rsisize)
    hv = candidate()
    plt.ion()
    plt.clf()
    plt.suptitle("Wykresy notowań kryptowalut")
    nr = len(All_data[0])
    for c in range(nr):
        ax = plt.subplot(3,nr, c+1)
        plt.title("Purchase / sale price",size = 6,loc = 'right')
        ys = []
        yb =[]
        yas = []
        yab = []
        for set in All_data:
            ys.append(set[c][1][0])
            yb.append(set[c][1][1])
        for aveset in Meanlist:
            yas.append(aveset[c][0])
            yab.append(aveset[c][1])
        if len(ys) > 8:
            ys = ys[-8:]
            yb = yb[-8:]

        if len(yab) > 8:
            yab = yab[-8:]
            yas = yas[-8:]
        plt.plot(T,ys,"-o",label = All_data[0][c][0] + ": sell")
        plt.plot(T, yb, "-o", label=All_data[0][c][0] + ": buy")
        plt.plot(T, yas, "o--", label=All_data[0][c][0] + ": sell avarage")
        plt.plot(T, yab, "o--", label=All_data[0][c][0] + ": buy avarage")
        if Rsistore[-1][c][0] != None:
            if Rsistore[-1][c][0] >= 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('green')
                    ax.spines[side].set_linewidth(3)
            elif Rsistore[-1][c][0] < 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('red')
                    ax.spines[side].set_linewidth(3)
        if hv ==c:
            if spread(Y,S,All_data,c):
            #if True:
                ax.text(0.3, 1.1, 'liquid asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size = 12)
            else:
                ax.text(0.4, 1.1, 'not liquid asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size=12)
            if transactions(Y,X,Cryptos[c],Currency):
            #if True:
                ax.text(0.8, 1.1, 'volatile asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size = 12)
            else:
                ax.text(0.9, 1.1, 'not volatile asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size=12)
        plt.xticks(rotation = 10, fontsize = 5 )
        plt.legend()
    for c in range(nr):
        ax = plt.subplot(3,nr, c + 1 + nr)
        plt.title("Volume",size = 6,loc = 'right')
        yv = []
        for vset in Volstor:
            yv.append(vset[c])
        if len(yv) > 8:
            yv = yv[-8:]
        plt.bar(T, yv, align = "center")
        plt.ylabel("Volume")
        plt.xticks(rotation = 10, fontsize = 5 )
        if hv == c:
            for side in ['bottom', 'top', 'left', 'right']:
                ax.spines[side].set_color('orange')
                ax.spines[side].set_linewidth(3)
    for c in range(nr):
        ax = plt.subplot(3,nr, c + 1 + 2 * nr)
        plt.title("Rsi value",size = 6,loc = 'right')
        yrsis = []
        #yrsib = []
        for rsiset in Rsistore:
            yrsis.append(rsiset[c][0])
            #yrsib.append(rsiset[c][1])
        if len(yrsis) > 8:
            yrsis = yrsis[-8:]
        plt.plot(T, yrsis,"o--",label = All_data[0][c][0] + ": sell RSI")
        #plt.plot(t, yrsib, "o--",label = all_data[0][c][0] + ": buy RSI")
        plt.ylabel("RSI")
        if Rsistore[-1][c][0] != None:
            if Rsistore[-1][c][0] >= 50:
                for side in ['bottom','top','left','right']:
                    ax.spines[side].set_color('green')
                    ax.spines[side].set_linewidth(3)
            elif Rsistore[-1][c][0] < 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('red')
                    ax.spines[side].set_linewidth(3)
        plt.legend()
        plt.xticks(rotation = 10, fontsize = 5 )


def main():
    animation = FuncAnimation(plt.figure(), graph_gen, interval = 5000)
    plt.show()

if __name__ == '__main__':
    main()