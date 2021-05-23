import requests
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
interval = 5
cryptos = ["ETH","LTC","BTC"]
currency = "PLN"
t = []
all_data = []
mlwinwsize = 3
meanlist = []
volstor = []
rsisize = 3
rsistore = []
Y = 6
X = 20
S = 40


def spread(Y,S,all_data,c):
    if Y > len(all_data):
        y = len(all_data)
    else:
        y = Y
    sbuy = float(0)
    ssell = float(0)
    for i in range(-y,-1):
        ssell = ssell + float(all_data[i][c][1][0])
        sbuy = sbuy +float(all_data[i][c][1][1])
    spr = ((sbuy - ssell) / sbuy )* 100
    if spr < S:
        return True
    else:
        return False

def transactions(Y,X,crypto,currency):
    y = Y
    queryparams = {'limit': y}
    tran = requests.get("https://api.bitbay.net/rest/trading/transactions/"+crypto+'-'+currency, params = queryparams)
    handle_exceptions(tran)
    tran = tran.json()
    vlist = []
    for i in tran['items']:
        vlist.append(i['r'])
    maxl = float(max(vlist))
    minl = float(min(vlist))
    value = (abs(maxl - minl) / maxl) * 100
    if value > X:
        return True
    else:
        return False



def candidate():
    vl = []
    for c in range(len(cryptos)):
        if rsistore[-1][c][0] != None:
            if rsistore[-1][c][0] < 50:
                vl.append(None)
            else:
                vl.append(volstor[-1][c])
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

def get_volumen(crypto,currency):
    fromtime = datetime.now() - timedelta(minutes=0.5)
    fromtime = int(fromtime.timestamp()) * 100
    queryparams = {'fromTime': fromtime}
    response = requests.get("https://api.bitbay.net/rest/trading/transactions/"+crypto+"-"+currency, params=queryparams)
    response = eval(response.text)
    return sum([float(response['items'][i]['a']) for i in range(len(response['items']))]) * 10

def rsicount(all_data, store,size):
    nr = len(all_data[0])
    if len(all_data) >= size:
        shift = len(all_data) - size
        reg = []
        for c in range(nr):
            cry = []
            for n in range(2):
                p = 0
                m = 0
                pc = 0
                mc = 0
                for i in range(0 + shift, size + shift - 1):
                    change = float(all_data[i + 1][c][1][n]) - float(all_data[i][c][1][n])
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


def handlemean(all_data,winsize,meanlist):
    nr = len(all_data[0])
    if len(all_data) >= winsize:
        shift = len(all_data) - winsize
        reg = []
        for c in range(nr):
            cry = []
            for n in range(2):
                sum = 0
                for i in range(0 + shift,winsize + shift):
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
        sa, sp = sa + s[0],sp + s[1]
    for b in buys:
        ba, bp = ba + b[0],bp + b[1]
    sellprice = sp / sa
    buyprice= bp / ba
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
        response = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/orderbook.json", timeout=15)
        handle_exceptions(response)
        v_list.append(get_volumen(crypto,currency))
        c_list.append([crypto,sellbuy(response.json()['asks'], response.json()['bids'])])
    volstor.append(v_list)
    all_data.append(c_list)


def graph_gen(a):
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    cryptostream_to_plot(cryptos,currency,all_data)
    handlemean(all_data, mlwinwsize, meanlist)
    rsicount(all_data, rsistore, rsisize)
    hv = candidate()
    plt.ion()
    plt.clf()
    plt.suptitle("Wykresy notowań kryptowalut")
    nr = len(all_data[0])
    for c in range(nr):
        ax = plt.subplot(3,nr, c+1)
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
        if rsistore[-1][c][0] != None:
            if rsistore[-1][c][0] >= 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('green')
                    ax.spines[side].set_linewidth(3)
            elif rsistore[-1][c][0] < 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('red')
                    ax.spines[side].set_linewidth(3)
        if hv ==c:
            if spread(Y,S,all_data,c):
                ax.text(0.3, 1.1, 'liquid asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size = 12)
            if transactions(Y,X,cryptos[c],currency):
                ax.text(0.8, 1.1, 'volatile asset',
                        verticalalignment='bottom', horizontalalignment='right',
                        transform=ax.transAxes,
                        color='orange', size = 12)
        plt.xticks(rotation = 30, fontsize = 6 )
        plt.legend()
    for c in range(nr):
        ax = plt.subplot(3,nr, c + 1 + nr)
        yv = []
        for vset in volstor:
            yv.append(vset[c])
        plt.bar(t, yv, align = "center")
        plt.ylabel("Volume")
        plt.xticks(rotation = 30, fontsize = 6)
        if hv == c:
            for side in ['bottom', 'top', 'left', 'right']:
                ax.spines[side].set_color('orange')
                ax.spines[side].set_linewidth(3)
    for c in range(nr):
        ax = plt.subplot(3,nr, c + 1 + 2 * nr)
        yrsis = []
        #yrsib = []
        for rsiset in rsistore:
            yrsis.append(rsiset[c][0])
            #yrsib.append(rsiset[c][1])
        plt.plot(t, yrsis,"o--",label = all_data[0][c][0] + ": sell RSI")
        #plt.plot(t, yrsib, "o--",label = all_data[0][c][0] + ": buy RSI")
        plt.ylabel("RSI")
        if rsistore[-1][c][0] != None:
            if rsistore[-1][c][0] >= 50:
                for side in ['bottom','top','left','right']:
                    ax.spines[side].set_color('green')
                    ax.spines[side].set_linewidth(3)
            elif rsistore[-1][c][0] < 50:
                for side in ['bottom', 'top', 'left', 'right']:
                    ax.spines[side].set_color('red')
                    ax.spines[side].set_linewidth(3)
        plt.legend()
        plt.xticks(rotation=30, fontsize=6)


def main():
    animation = FuncAnimation(plt.figure(), graph_gen, interval = 5000)
    plt.show()

if __name__ == '__main__':
    main()