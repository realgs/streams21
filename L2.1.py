import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

URL_START = 'http://bitbay.net/API/Public/'
URL_END = 'USD/ticker.json'
INTERVAL = 5
Volume_bitbay = 'https://api.bitbay.net/rest/trading'

stepback = int(input('How many elements back you want to calculate in RSI :'))
step = int(input('Give a amount of elements for moving average ( 2 - 5 ): '))
while step > 5 or step < 2:
    print('Give a number from 2 to 5:')
    step = int(input('Give a step for moving average ( 2 - 5 ): '))
wone = str(input('What do you want to see: Volume (V) or RSI (R)'))

S = 0.1
X = 0.1
Y = 3

def volatile_asset():
    V_assert = ''
    print("==== VOLATILE ASSERCION ====")
    if len(crypto_bid_BTC) > 3:
        for i in range(Y):
            tablica =[]
            tablica.append(crypto_bid_BTC[-i])
        if max(tablica) - min(tablica) > crypto_bid_BTC[-1] * X:
            print('BTC jest volatile_asset')
            V_assert = 'BTC jest volatile_asset'
        # else:
        #     print('BTC NIEE jest volatile_asset')

        if len(crypto_bid_BAT) > 3:
            for i in range(Y):
                tablica1 = []
                tablica1.append(crypto_bid_BAT[-i])
            if max(tablica1) - min(tablica1) > crypto_bid_BAT[-1] * X:
                print('BAT jest volatile_asset')
                V_assert = 'BAT jest volatile_asset'
            # else:
            #     print('BAT NIEE jest volatile_asset')

        if len(crypto_bid_ZRX) > 3:
            for i in range(Y):
                tablica2 = []
                tablica2.append(crypto_bid_ZRX[-i])
            if max(tablica2) - min(tablica2) > crypto_bid_ZRX[-1] * X:
                print('ZRX jest volatile_asset')
                V_assert = 'ZRX jest volatile_asset'
            # else:
            #     print('ZRX NIEE jest volatile_asset')
    return V_assert
    print('___________________________')

def liquid_asset():
    L_assert = ''
    print('==== LIQUID ASSERCION ====')
    if abs( crypto_bid_BTC[-1] - crypto_ask_BTC[-1] ) < ((crypto_bid_BTC[-1] + crypto_ask_BTC[-1])*S)/2:
        print('BTC jest liquid asset ')
        L_assert = 'BTC jest liquid asset '
    if abs( crypto_bid_BAT[-1] - crypto_ask_BAT[-1] ) < ((crypto_bid_BAT[-1] + crypto_ask_BAT[-1])*S)/2:
        print('BAT jest liquid asset ')
        L_assert = 'BAT jest liquid asset '
    if abs( crypto_bid_ZRX[-1] - crypto_ask_ZRX[-1] ) < ((crypto_bid_ZRX[-1] + crypto_ask_ZRX[-1])*S)/2:
        print('ZRX jest liquid asset ')
        L_assert = 'ZRX jest liquid asset '
    return L_assert
    print('==========================')


def choose_candidate():
    candidate_Volume = ''
    btc_variable = 0
    bat_variable = 0
    zrx_variable = 0
    if len(crypto_ask_BTC) > 1:
        if crypto_ask_BTC[-1] >= crypto_ask_BTC[-2]:
            btc_variable += 1
        if crypto_ask_BAT[-1] >= crypto_ask_BAT[-2]:
            bat_variable += 1
        if crypto_ask_ZRX[-1] >= crypto_ask_ZRX[-2]:
            zrx_variable += 1
    if max(crypto_BTC_volume, crypto_BAT_volume, crypto_ZRX_volume) == crypto_BTC_volume:
        btc_variable += 1
    if max(crypto_BTC_volume, crypto_BAT_volume, crypto_ZRX_volume) == crypto_BAT_volume:
        bat_variable += 1
    if max(crypto_BTC_volume, crypto_BAT_volume, crypto_ZRX_volume) == crypto_ZRX_volume:
        zrx_variable += 1
    if btc_variable == 2:
        print("BTC - tendencja niespadkowa, największy wolumen")
        candidate_Volume = "BTC - tendencja niespadkowa, największy wolumen"
    if bat_variable == 2:
        print("BAT - tendencja niespadkowa, największy wolumen")
        candidate_Volume = "BAT - tendencja niespadkowa, największy wolumen"
    if zrx_variable == 2:
        print("ZRX - tendencja niespadkowa, największy wolumen")
        candidate_Volume = "ZRX - tendencja niespadkowa, największy wolumen"
    return candidate_Volume
    print('============================')

def RSI_clasificator():
    if RSI_BTC == 0:
        print("Nastapi odwrócenie trendu na zwyżkowy dla BTC")
    if 0 < RSI_BTC[-1] <= 30:
        print("Kupuj BTC")
    if 30 < RSI_BTC[-1] < 70:
        print("Nie z rób nic ze swoim BTC")
    if 70 <= RSI_BTC[-1] < 100:
        print("Sprzedawaj BTC")
    if RSI_BTC[-1] == 100:
        print("Nastapi odwrócenie trendu na zniżkowy dla BTC")

    if RSI_BAT == 0:
        print("Nastapi odwrócenie trendu na zwyżkowy dla BAT")
    if 0 < RSI_BAT[-1] <= 30:
        print("Kupuj BTC")
    if 30 < RSI_BAT[-1] < 70:
        print("Nie z rób nic ze swoim BAT")
    if 70 <= RSI_BAT[-1] < 100:
        print("Sprzedawaj BAT")
    if RSI_BAT[-1] == 100:
        print("Nastapi odwrócenie trendu na zniżkowy dla BAT")

    if RSI_ZRX == 0:
        print("Nastapi odwrócenie trendu na zwyżkowy dla ZRX")
    if 0 < RSI_ZRX[-1] <= 30:
        print("Kupuj ZRX")
    if 30 < RSI_ZRX[-1] < 70:
        print("Nie z rób nic ze swoim ZRX")
    if 70 <= RSI_ZRX[-1] < 100:
        print("Sprzedawaj ZRX")
    if RSI_ZRX[-1] == 100:
        print("Nastapi odwrócenie trendu na zniżkowy dla ZRX")


    print('============================')

rsi_state = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

def Value_RSI(bessa, hossa, buyArray, stepback):
    if len(buyArray) > stepback:
        value = buyArray[len(buyArray) - 1] - buyArray[len(buyArray) - stepback]
        if value > 0:
            hossa.append(value)
        else:
            bessa.append(value)
        x = (sum(hossa) + 1) / (len(hossa) + 1)
        y = (sum(bessa) + 1) / (len(bessa) + 1)
    else:
        x = 1
        y = 1
    RSI = 100 - (100 / (1 + (x/y)))
    return RSI

def Volume_get(resource, currency, fromTime):
    try:
        _ADRES = f'{Volume_bitbay}/{resource}/{currency}'

        now = datetime.now()
        before = int((now - timedelta(0, fromTime)).timestamp()) * 1000
        headers = {'content-type': 'application/json'}
        querystring = {"fromTime": before, "limit": 1}

        response = requests.request("GET", _ADRES, headers=headers, params=querystring)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    else:
        _DATA = response.json()
        try:
            volume = _DATA['items'][0]['a']
        except IndexError:
            volume = str(0.0)
        return volume

def crypto_get(data, cryptovault, json):
    try:
        response = requests.get( URL_START + data + URL_END)
        response.raise_for_status()

    except HTTPError as error_with_http:
        print(f'Błąd z adresem HTTP : {error_with_http}')

    else:
        originalData = response.json()
        return originalData["bid"], originalData["ask"]

def animate(i):
    bid_BTC, ask_BTC = crypto_get(f'BTC', 'PLN', 'ticker.json')
    bid_BAT, ask_BAT = crypto_get(f'BAT', 'PLN', 'ticker.json')
    bid_ZRX, ask_ZRX = crypto_get(f'ZRX', 'PLN', 'ticker.json')

    volume_BTC = Volume_get(f'transactions', 'BTC-PLN', 60)
    volume_BAT = Volume_get(f'transactions', 'BAT-PLN', 60)
    volume_ZRX = Volume_get(f'transactions', 'ZRX-PLN', 60)

    x_axis.append(datetime.now().strftime("%H:%M:%S"))

    crypto_bid_BTC.append(bid_BTC)
    crypto_ask_BTC.append(ask_BTC)
    crypto_BTC_volume.append(volume_BTC)

    crypto_bid_BAT.append(bid_BAT)
    crypto_ask_BAT.append(ask_BAT)
    crypto_BAT_volume.append(volume_BAT)

    crypto_bid_ZRX.append(bid_ZRX)
    crypto_ask_ZRX.append(ask_ZRX)
    crypto_ZRX_volume.append(volume_ZRX)

    left = max(0, len(x_axis) - 5)
    right = (len(x_axis))

    with plt.style.context('seaborn'):
        plt.cla()

        #Rsi section
        RSI_BTC.append(Value_RSI(bessa_BTC, hossa_BTC, crypto_bid_BTC, stepback))
        RSI_BAT.append(Value_RSI(bessa_BAT, hossa_BAT, crypto_bid_BAT, stepback))
        RSI_ZRX.append(Value_RSI(bessa_ZRX, hossa_ZRX, crypto_bid_ZRX, stepback))

        avg = 0
        for i in range(len(crypto_bid_BTC) - step, len(crypto_bid_BTC)):
            if i >= 0:
                avg += crypto_bid_BTC[i]
        if len(crypto_bid_BTC) > 3:
            avg /= 3
            avg_BTC_bid_window.append(avg)
        else:
            avg_BTC_bid_window.append(bid_BTC)

        avg2 = 0
        for i in range(len(crypto_ask_BAT) - step, len(crypto_ask_BAT)):
            if i >= 0:
                avg2 += crypto_ask_BAT[i]
        if len(crypto_ask_BAT) > 3:
            avg2 /= 3
            avg_BAT_ask_window.append(avg2)
        else:
            avg_BAT_ask_window.append(ask_BAT)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("-------Obecny czas =", dt_string)

        if wone == 'V':

            if choose_candidate() == "BTC - tendencja niespadkowa, największy wolumen":
                label1 = "Kandydat"
            else:
                label1 = ' '
            if choose_candidate() == "BAT - tendencja niespadkowa, największy wolumen":
                label2 = "Kandydat"
            else:
                label2 = ' '
            if choose_candidate() == "ZRX - tendencja niespadkowa, największy wolumen":
                label3 = "Kandydat"
            else:
                label3 = ' '

            plot1.plot(x_axis, crypto_ask_BTC, linewidth=1, label='Asks_BTC' if i == 0 else "", color='#ff8533')
            plot1.plot(x_axis, crypto_bid_BTC, linewidth=1, label='Bids_BTC' if i == 0 else "", color='#e60000')
            plot1.plot(x_axis, avg_BTC_bid_window, linewidth=1.5, label='BTC bids AVR' if i == 0 else "",
                       color='#003300', linestyle='dotted')
            plot1.set_xlim(left=left, right=right)
            plot1.set_xlabel(f'{label1}', fontsize=15)
            plot1.set_ylabel('PLN', fontsize=15)
            plot1.set_yscale('log')
            plot1.legend()

            plot2.plot(x_axis, crypto_ask_BAT, linewidth=1, label='Asks_BAT' if i == 0 else "", color='#ff99ff')
            plot2.plot(x_axis, crypto_bid_BAT, linewidth=1, label='Bids_BAT' if i == 0 else "", color='#002e4d')
            plot2.plot(x_axis, avg_BAT_ask_window, linewidth=1.5, label='BAT asks AVR' if i == 0 else "",
                       color='#003300', linestyle='dotted')
            plot2.set_xlim(left=left, right=right)
            plot2.set_xlabel(f'{label2}', fontsize=15)
            plot2.set_yscale('log')
            plot2.legend()

            plot3.plot(x_axis, crypto_ask_ZRX, linewidth=1, label='Asks_ZRX' if i == 0 else "", color='#bfff00')
            plot3.plot(x_axis, crypto_bid_ZRX, linewidth=1, label='Bids_ZRX' if i == 0 else "", color='#00e600')
            plot3.set_xlim(left=left, right=right)
            plot3.set_xlabel(f'{label3}', fontsize=15)
            plot3.set_yscale('log')
            plot3.legend()

            plot4.bar(x_axis, crypto_BTC_volume, color='#969696')
            plot4.set_xlim(left=left, right=right)
            plot4.set_ylabel('Volume of volumen', fontsize=15)
            plot4.set_xlabel('Time', fontsize=15)

            plot5.bar(x_axis, crypto_BAT_volume, color='#969696')
            plot5.set_xlim(left=left, right=right)
            plot5.set_xlabel('Time', fontsize=15)

            plot6.bar(x_axis, crypto_ZRX_volume, color='#969696')
            plot6.set_xlim(left=left, right=right)
            plot6.set_xlabel('Time', fontsize=15)

        if wone == 'R':
            if volatile_asset() == 'BTCjest volatile_asset':
                label11 = "Volatile"
            else:
                label11 = ' '
            if volatile_asset() == 'BAT jest volatile_asset':
                label21 = "Volatile"
            else:
                label21 = ' '
            if volatile_asset() == 'ZRX jest volatile_asset':
                label31 = "Volatile"
            else:
                label31 = ' '

            if liquid_asset() == 'BTC jest liquid asset ':
                label12 = "Liquid"
            else:
                label12 = ' '
            if liquid_asset() == 'BAT jest liquid asset ':
                label22 = "Liquid"
            else:
                label22 = ' '
            if liquid_asset() == 'ZRX jest liquid asset ':
                label32 = "Liquid"
            else:
                label32 = ' '

            plot1.plot(x_axis, crypto_ask_BTC, linewidth=1, label='Asks_BTC' if i == 0 else "", color='#ff8533')
            plot1.plot(x_axis, crypto_bid_BTC, linewidth=1, label='Bids_BTC' if i == 0 else "", color='#e60000')
            plot1.plot(x_axis, avg_BTC_bid_window, linewidth=1.5, label='BTC bids AVR' if i == 0 else "",
                       color='#003300', linestyle='dotted')
            plot1.set_xlim(left=left, right=right)
            plot1.set_xlabel(f'{label11}/ {label12}', fontsize=15)
            plot1.set_ylabel('PLN', fontsize=15)
            plot1.set_yscale('log')
            plot1.legend()

            plot2.plot(x_axis, crypto_ask_BAT, linewidth=1, label='Asks_BAT' if i == 0 else "", color='#ff99ff')
            plot2.plot(x_axis, crypto_bid_BAT, linewidth=1, label='Bids_BAT' if i == 0 else "", color='#002e4d')
            plot2.plot(x_axis, avg_BAT_ask_window, linewidth=1.5, label='BAT asks AVR' if i == 0 else "",
                       color='#003300', linestyle='dotted')
            plot2.set_xlim(left=left, right=right)
            plot2.set_xlabel(f'{label21}/ {label22}', fontsize=15)
            plot2.set_yscale('log')
            plot2.legend()

            plot3.plot(x_axis, crypto_ask_ZRX, linewidth=1, label='Asks_ZRX' if i == 0 else "", color='#bfff00')
            plot3.plot(x_axis, crypto_bid_ZRX, linewidth=1, label='Bids_ZRX' if i == 0 else "", color='#00e600')
            plot3.set_xlim(left=left, right=right)
            plot3.set_xlabel(f'{label31}/ {label32}', fontsize=15)
            plot3.set_yscale('log')
            plot3.legend()

            plot4.plot(x_axis, RSI_BTC, color='#969696')
            plot4.set_xlim(left=left, right=right)
            plot4.set_ylabel('RSI value', fontsize=15)
            plot4.set_xlabel('Time', fontsize=15)

            plot5.plot(x_axis, RSI_BAT, color='#969696')
            plot5.set_xlim(left=left, right=right)
            plot5.set_xlabel('Time', fontsize=15)

            plot6.plot(x_axis, RSI_ZRX, color='#969696')
            plot6.set_xlim(left=left, right=right)
            plot6.set_xlabel('Time', fontsize=15)

            RSI_clasificator()

        plt.suptitle("Best bids and asks offers / Volumen / RSI")
        liquid_asset()
        volatile_asset()

if __name__ == '__main__':
    x_axis = []
    crypto_bid_BTC = []
    crypto_ask_BTC = []
    crypto_BTC_volume = []
    avg_BTC_bid_window = []
    bessa_BTC = []
    hossa_BTC = []
    RSI_BTC = []

    crypto_bid_BAT = []
    crypto_ask_BAT = []
    crypto_BAT_volume = []
    avg_BAT_ask_window = []
    bessa_BAT = []
    hossa_BAT = []
    RSI_BAT = []

    crypto_bid_ZRX = []
    crypto_ask_ZRX = []
    crypto_ZRX_volume = []
    bessa_ZRX = []
    hossa_ZRX = []
    RSI_ZRX = []

    fig, ((plot1, plot2, plot3), (plot4, plot5, plot6)) = plt.subplots(2, 3)

    ani = FuncAnimation(plt.gcf(),animate , interval=5000)
    plt.show()
