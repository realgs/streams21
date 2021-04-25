import requests
import time
import matplotlib.pyplot as plt

interval = 5
cryptos = ["BTC"]
currency = "PLN"
t = []

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


def cryptostream_to_plot(crypto_set, currency, interval):
    all_data = []
    while True:
        c_list = []
        for crypto in crypto_set:
            response = requests.get("https://bitbay.net/API/Public/" + crypto + currency + "/orderbook.json", timeout=5)
            handle_exceptions(response)
            c_list.append([crypto,sellbuy(response.json()['asks'], response.json()['bids'])])
        all_data.append(c_list)
        graph_gen(all_data,interval)

def graph_gen(all_data,interval):
    t.append(time.strftime("%H:%M:%S", time.localtime()))
    plt.ion()
    nr = len(all_data[0])
    for c in range(nr):
        ys = []
        yb =[]
        for set in all_data:
            ys.append(set[c][1][0])
            yb.append(set[c][1][1])
        plt.plot(t,ys,"--o",label = all_data[0][c][0] + ": sprzedaż")
        plt.plot(t, yb, "--o", label=all_data[0][c][0] + ": kupno")
    plt.legend()
    plt.title("Wykres wartości cryptowalut w czasie")
    plt.xlabel("time")
    plt.ylabel("value")
    plt.xticks(rotation=80)
    plt.draw()
    plt.pause(interval-2)
    plt.clf()

cryptostream_to_plot(cryptos, currency, interval)
