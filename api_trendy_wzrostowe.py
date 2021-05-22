import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import requests
from statistics import mean
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from datetime import datetime
import random

inc = [[], [], []]
dec = [[], [], []]


def czy_liquid_asset(asks, bids, x):
    x = x * 0.01
    if asks[-1] / bids[-1] < x:
        return 1
    return 0


def m(a):
    return (sum(a) + 1) / (len(a) + 1)


def con_t(url):
    return requests.get(url).ok


def calc_rsi(t, da, ia, bhist):
    x = y = 1
    if len(bhist) > t:
        l = bhist[-1] - bhist[-t]
        if l > 0:
            ia.append(l)
        else:
            da.append(l)
        x = m(ia)
        y = m(da)
    return 100 - (100 / (1 + (x + 1 / y + 1)))


def vol_calc(cur, t):
    url = f'https://api.bitbay.net/rest/trading/transactions/{cur}'
    if not con_t(url):
        return con_t(url)
    time = int((datetime.now() - timedelta(0, t)).timestamp()) * 1000  # zmienia format na sekundowy
    par = {"fromTime": time}
    response = requests.request("GET", url, params=par)
    response.raise_for_status()
    _DATA = response.json()
    try:
        volume = _DATA['items'][0]['a']
    except IndexError:
        volume = 0.0
    return float(volume)


def asknbid(w):
    url = f'https://api.bitbay.net/rest/trading/ticker/{w}'
    if not con_t(url):
        return con_t(url)
    response = requests.get(url)
    a = response.json()['ticker']['lowestAsk']
    b = response.json()['ticker']['highestBid']
    return (float(a), float(b))


def czy_liquid_asset(ask, bid, x):
    spread = round(100 - (1 - (ask - bid) / bid) * 100, 4)
    # print(spread)
    if spread < x:
        return 1
    return 0


def czy_volatile(x, p):
    for i in range(2):
        # print('TTT', x[i] / x[i + 1], 'qqqq', x[i + 1] / x[i])
        if x[i] / x[i + 1] > 1 + p or x[i + 1] / x[i] < 1 - p:
            return 1
    return 0


oferts = {}
fig, axs = plt.subplots(3, sharex=True)
pointers = [axs[0].twinx(), axs[1].twinx(), axs[2].twinx()]
for i in range(3):
    axs[i].set_zorder(1)
    axs[i].set_frame_on(False)

w = ('BTC', 'LTC', 'ETH')
choice = input("rsi czy vol ?").lower()
assert choice in ('rsi', 'vol'), 'Wybierz między RSI/VOL'
avg_section = int(input("Wskaż przedział dla średniej"))
rsi_section = int(input("Wskaż przedział dla RSI"))
s = 3  # float(input("podaj spread"))
czas = []
avg = [[], [], []]
vol = [[], [], []]
rsi = [[], [], []]
czy_spadkowy = [0, 0, 0]
czy_kandydat = [0, 0, 0]
X = 0.01
Y = 3


def animate(i):
    app = False

    for i in w:
        if i + 'asks' not in oferts.keys():
            oferts[i + 'asks'] = []
            oferts[i + 'bids'] = []
        oferts[i + 'asks'].append(asknbid(i + '-PLN')[0])
        oferts[i + 'bids'].append(asknbid(i + '-PLN')[1])
        oferts[i + 'asks'] = oferts[i + 'asks'][-5:]
        oferts[i + 'bids'] = oferts[i + 'bids'][-5:]
    oferts_list = list(oferts.values())
    now = datetime.now()
    czas.append(now.strftime("%H:%M:%S"))
    for i, ax in enumerate(axs):

        axs[i].cla()
        pointers[i].cla()

        vol[i].append(vol_calc(f'{w[i]}-PLN', 100))
        avg[i].append(mean(oferts_list[2 * i][-avg_section:] + oferts_list[2 * i + 1][-avg_section:]))
        rsi[i].append(calc_rsi(rsi_section, dec[i], inc[i], oferts_list[2 * i + 1]))
        if rsi[i][-1] < 70:
            czy_spadkowy[i] = vol[i][-1]
        volmaks = czy_spadkowy.index(max(czy_spadkowy))
        axs[i].plot(czas[-5:], oferts_list[2 * i], label=w[i] + ' asks')
        axs[i].plot(czas[-5:], oferts_list[2 * i + 1], label=w[i] + ' bids')
        axs[i].plot(czas[-5:], avg[i][-5:], label='avg')
        axs[i].legend(loc='upper left')
        axs[i].set_title(w[i])
        if rsi[i][-1] > 80:
            czy_kandydat[i] = 1
        else:
            czy_kandydat[i] = 0

        if czy_kandydat[i] and len(oferts_list[2 * i][-4:]) > 3 and app == 0:
            app = True
            if czy_liquid_asset(oferts_list[2 * i][-1], oferts_list[2 * i + 1][-1], s):
                pointers[i].text(0.8, 0.05, "Liquid asset",
                                 verticalalignment='bottom', horizontalalignment='right',
                                 transform=ax.transAxes,
                                 color="orange", fontsize=12)
            if czy_volatile(oferts_list[2 * i][-4:], 0.00000001):
                pointers[i].text(0.5, 0.05, "Volatile asset",
                                 verticalalignment='bottom', horizontalalignment='right',
                                 transform=ax.transAxes,
                                 color="hotpink", fontsize=12)
        if choice == 'vol':
            cv = 'silver'
            if volmaks == i:
                cv = 'green'
            pointers[i].bar(czas[-5:], vol[i][-5:], width=0.2, label="vol", color=cv)
            pointers[i].legend(loc='lower left')
        else:
            pointers[i].plot(czas[-5:], rsi[i][-5:], color='red', label=f'{w[i]} RSI')
            if len(rsi[i]) > 2:
                if rsi[i][-1] >= 95:
                    info = 'will go down'
                    c = 'black'
                elif rsi[i][-1] >= 70:
                    info = 'sell'
                    c = 'red'
                elif rsi[i][-1] <= 60 and rsi[i][-1] >= 30:
                    info = ''
                    c = 'red'
                elif rsi[i][-1] <= 30 and rsi[i][-1] >= 10:
                    info = 'buy'
                    c = 'green'
                elif rsi[i][-1] < 10:
                    info = 'will go up'
                    c = 'black'
                pointers[i].text(0.95, 0.05, info,
                                 verticalalignment='bottom', horizontalalignment='right',
                                 transform=ax.transAxes,
                                 color=c, fontsize=12)
            pointers[i].legend(loc='lower left')


ani = FuncAnimation(fig, animate, interval=1000)
plt.show()
