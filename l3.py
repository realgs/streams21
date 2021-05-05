import matplotlib.pyplot as plt
import requests
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

def Dates():
    time_list_BTC.append(datetime.datetime.now())
    buy, sell = Values("BTC")
    BTCBuy.append(buy)
    BTCSell.append(sell)

    time_list_LTC.append(datetime.datetime.now())
    buy, sell = Values("LTC")
    LTCBuy.append(buy)
    LTCSell.append(sell)

    time_list_DASH.append(datetime.datetime.now())
    buy, selL = Values("DASH")
    DASHBuy.append(buy)
    DASHSell.append(selL)

def Values(currency):
    r = requests.get(f"https://bitbay.net/API/Public/{currency}/ticker.json")
    try:
        values = r.json()
        buy = values["bid"]
        sell = values["ask"]
        return buy, sell
    except requests.exceptions.HTTPError:
        print("Something went wrong")

def plot():
    global ax
    fig, ax = plt.subplots(3)
    fig.tight_layout(pad=2)

    lines.append(ax[0].plot(BTCBuy, color='purple', label='Buy BTC'))
    lines.append(ax[0].plot(BTCSell, color='blue', label='Sell BTC'))
    ax[0].set_title("Quotation Chart BTC USD")
    ax[0].legend(loc=1)
    ax[0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1].plot(LTCBuy, color='silver', label='Buy LTC'))
    lines.append(ax[1].plot(LTCSell, color='red', label='Sell LTC'))
    ax[1].set_title("Quotation Chart LTC USD")
    ax[1].legend(loc=1)
    ax[1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[2].plot(DASHBuy, color='pink', label='Buy DASH'))
    lines.append(ax[2].plot(DASHSell, color='gold', label='Sell DASH'))
    ax[2].set_title("Quotation Chart DASH USD")
    ax[2].legend(loc=1)
    ax[2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    a = FuncAnimation(fig, func=update_plot, interval=5000)
    plt.autoscale()
    plt.show()

def update_plot(i):
    Dates()
    lines[0][0].set_data(time_list_BTC, BTCBuy)
    lines[1][0].set_data(time_list_BTC, BTCSell)
    lines[2][0].set_data(time_list_LTC, LTCBuy)
    lines[3][0].set_data(time_list_LTC, LTCSell)
    lines[4][0].set_data(time_list_DASH, DASHBuy)
    lines[5][0].set_data(time_list_DASH, DASHSell)

    ax[0].relim()
    ax[1].relim()
    ax[2].relim()
    ax[0].autoscale_view()
    ax[1].autoscale_view()
    ax[2].autoscale_view()

time_list_BTC = list()
time_list_LTC = list()
time_list_DASH = list()
BTCBuy = list()
BTCSell = list()
LTCBuy = list()
LTCSell = list()
DASHBuy = list()
DASHSell = list()
lines = list()
plot()
