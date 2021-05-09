import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

URL_START='http://bitbay.net/API/Public/'
URL_END='USD/ticker.json'
INTERVAL=5
Volume_bitbay = 'https://api.bitbay.net/rest/trading'

stepback = int(input('How many elements back you want to calculate in RSI :'))
step = int(input('Give a amount of elements for moving average ( 2 - 5 ): '))
while step>5 or step<2:
    print('Give a number from 2 to 5:')
    step = int(input('Give a step for moving average ( 2 - 5 ): '))
wone = str(input('What do you want to see: Volume (V) or RSI (R)'))

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
        return originalData["bid"], originalData["ask"], originalData["volume"]

def animate(i):
    bid_BTC, ask_BTC, volume_BTC = crypto_get(f'BTC', 'PLN', 'ticker.json')
    bid_BAT, ask_BAT, volume_BAT = crypto_get(f'BAT', 'PLN', 'ticker.json')
    bid_ZRX, ask_ZRX, volume_ZRX = crypto_get(f'ZRX', 'PLN', 'ticker.json')

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

        #plots section
        plot1.plot(x_axis, crypto_ask_BTC, linewidth=1, label='Asks_BTC'if i == 0 else "", color='#ff8533')
        plot1.plot(x_axis, crypto_bid_BTC, linewidth=1, label='Bids_BTC'if i == 0 else "", color='#e60000')
        plot1.plot(x_axis, avg_BTC_bid_window , linewidth=1.5,label='BTC bids AVR' if i == 0 else "", color='#003300', linestyle='dotted')
        plot1.set_xlim(left=left, right=right)
        plot1.set_ylabel('PLN', fontsize=15)
        plot1.set_yscale('log')
        plot1.legend()

        plot2.plot(x_axis, crypto_ask_BAT, linewidth=1, label='Asks_BAT'if i == 0 else "", color='#ff99ff')
        plot2.plot(x_axis, crypto_bid_BAT, linewidth=1, label='Bids_BAT'if i == 0 else "", color='#002e4d')
        plot2.plot(x_axis, avg_BAT_ask_window , linewidth=1.5,label='BAT asks AVR' if i == 0 else "", color='#003300', linestyle='dotted')
        plot2.set_xlim(left=left, right=right)
        plot2.set_yscale('log')
        plot2.legend()

        plot3.plot(x_axis, crypto_ask_ZRX, linewidth=1, label='Asks_ZRX'if i == 0 else "", color='#bfff00')
        plot3.plot(x_axis, crypto_bid_ZRX, linewidth=1, label='Bids_ZRX'if i == 0 else "", color='#00e600')
        plot3.set_xlim(left=left, right=right)
        plot3.set_yscale('log')
        plot3.legend()

        if wone == 'V':
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

        plt.suptitle("Best bids and asks offers / Volumen / RSI")


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


# def Avarage(a, b, c):
#     avg = 0
#     for i in range(len(a) - step, len(a)):
#         if i >= 0:
#             avg += a[i]
#     if len(a) > 3:
#         avg /= 3
#         c.append(avg)
#     else:
#         c.append(b)

# Avarage(crypto_bid_BTC, bid_BTC, avg_BTC_bid_window)
# Avarage(crypto_ask_BAT, ask_BAT, avg_BAT_ask_window)

