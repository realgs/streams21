import matplotlib.pyplot as plt
import requests
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

def Dates():
    time_list_BTC.append(datetime.datetime.now())
    buy, sell,volume = Values("BTCPLN")
    BTCBuy.append(buy)
    BTCSell.append(sell)
    BTCVolume.append(volume)

    time_list_LTC.append(datetime.datetime.now())
    buy, sell,volume = Values("LTCPLN")
    LTCBuy.append(buy)
    LTCSell.append(sell)
    LTCVolume.append(volume)

    time_list_DASH.append(datetime.datetime.now())
    buy, sell,volume = Values("DASHPLN")
    DASHBuy.append(buy)
    DASHSell.append(sell)
    DASHVolume.append(volume)
    print(volume)

def Values(currency):
    r = requests.get(f"https://bitbay.net/API/Public/{currency}/ticker.json")
    try:
        values = r.json()
        buy = values["bid"]
        sell = values["ask"]
        volume = values["volume"]
        return buy, sell,volume
    except requests.exceptions.HTTPError:
        print("Something went wrong")

def Avarage(list_buy,list_sell,user_parameter):
    buy = []
    sell = []
    if len(list_sell) <= user_parameter:
        for i in list_buy:
            buy.append(i)
        for i in list_sell:
            sell.append(i)
        buy = sum(buy) / len(list_sell)
        sell = sum(sell) / len(list_buy)
        return buy, sell
    else:
        for i in range(-1,-(user_parameter+1),-1):
            buy.append(list_buy[i])
            sell.append(list_sell[i])
        buy = sum(buy) / user_parameter
        sell = sum(sell) / user_parameter
        return buy, sell


def RSI(sell_list, user_parameter):
    if len(sell_list) > user_parameter:
        value = sell_list[len(sell_list) - 1] - sell_list[len(sell_list) - user_parameter]
        if value > 0:
            Increase_list.append(value)
        elif value < 0:
            Decrease_list.append(value)
        print(Increase_list,Decrease_list)
        a = (sum(Increase_list) + 1) / (len(Increase_list) + 1)
        b = (sum(Decrease_list) + 1) / (len(Decrease_list) + 1)
    else:
        a = 1
        b = 1
    print(a,b)
    RSI = 100 - (100 / (1 + (a / b)))
    return RSI

def plot():
    global ax
    fig, ax = plt.subplots(2,3, figsize=(14,6))
    fig.tight_layout(pad=2)

    lines.append(ax[0][0].plot(time_list_BTC, BTCBuy, color='red', label='Buy BTC',linewidth = 5))
    lines.append(ax[0][0].plot(time_list_BTC, BTCSell, color='royalblue', label='Sell BTC', linewidth = 5))
    lines.append(ax[0][0].plot(time_list_BTC, BTCAVG_buy, color='gold', label='Avg buy BTC'))
    lines.append(ax[0][0].plot(time_list_BTC, BTCAVG_sell, color='lime', label='Avg sell BTC'))
    ax[0][0].set_title("Quotation Chart BTC PLN")
    ax[0][0].legend(loc=1)
    ax[0][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][0].plot(time_list_BTC, BTCVolume, color='green', label='Volume BTC'))
    ax[1][0].set_title("Volume BTC PLN")
    ax[1][0].legend(loc=1)
    ax[1][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[0][1].plot(time_list_LTC, LTCBuy, color='red', label='Buy LTC', linewidth = 5))
    lines.append(ax[0][1].plot(time_list_LTC, LTCSell, color='royalblue', label='Sell LTC', linewidth = 5))
    lines.append(ax[0][1].plot(time_list_LTC, LTCAVG_buy, color='gold', label='Avg buy LTC'))
    lines.append(ax[0][1].plot(time_list_LTC, LTCAVG_sell, color='lime', label='Avg sell LTC'))
    lines.append(ax[0][1].plot(time_list_LTC, RSI_list, color='purple', label='RSI LTC'))

    ax[0][1].set_title("Quotation Chart LTC PLN")
    ax[0][1].legend(loc=1)
    ax[0][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][1].plot(time_list_LTC, LTCVolume, color='green', label='Volume LTC'))
    ax[1][1].set_title("Volume LTC PLN")
    ax[1][1].legend(loc=1)
    ax[1][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[0][2].plot(time_list_DASH, DASHBuy, color='red', label='Buy DASH', linewidth = 5))
    lines.append(ax[0][2].plot(time_list_DASH, DASHSell, color='royalblue', label='Sell DASH', linewidth = 5))
    lines.append(ax[0][2].plot(time_list_DASH, DASHAVG_buy, color='gold', label='Avg buy DASH'))
    lines.append(ax[0][2].plot(time_list_DASH, DASHAVG_sell, color='lime', label='Avg sell DASH'))
    ax[0][2].set_title("Quotation Chart DASH PLN")
    ax[0][2].legend(loc=1)
    ax[0][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][2].plot(time_list_LTC, LTCVolume, color='green', label='Volume DASH'))

    ax[1][2].set_title("Volume DASH PLN")
    ax[1][2].legend(loc=1)
    ax[1][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    fig.autofmt_xdate()

    a = FuncAnimation(fig, func=update_plot, interval=5000)
    plt.autoscale()
    plt.show()

def update_plot(i):
    Dates()
    buy, sell = Avarage(BTCBuy, BTCSell, 3)
    BTCAVG_buy.append(buy)
    BTCAVG_sell.append(sell)
    buy, sell = Avarage(LTCBuy, LTCSell, 3)
    LTCAVG_buy.append(buy)
    LTCAVG_sell.append(sell)
    buy, sell = Avarage(DASHBuy, DASHSell, 3)
    DASHAVG_buy.append(buy)
    DASHAVG_sell.append(sell)

    rsi = RSI(LTCSell, 2)
    print(rsi)
    RSI_list.append(rsi)

    lines[0][0].set_data(time_list_BTC, BTCBuy)
    lines[1][0].set_data(time_list_BTC, BTCSell)
    lines[2][0].set_data(time_list_BTC, BTCAVG_buy)
    lines[3][0].set_data(time_list_BTC, BTCAVG_sell)
    lines[4][0].set_data(time_list_BTC, BTCVolume)
    lines[5][0].set_data(time_list_LTC, LTCBuy)
    lines[6][0].set_data(time_list_LTC, LTCSell)
    lines[7][0].set_data(time_list_LTC, LTCAVG_buy)
    lines[8][0].set_data(time_list_LTC, LTCAVG_sell)
    lines[9][0].set_data(time_list_LTC, RSI_list)
    lines[10][0].set_data(time_list_LTC, LTCVolume)
    lines[11][0].set_data(time_list_DASH, DASHBuy)
    lines[12][0].set_data(time_list_DASH, DASHSell)
    lines[13][0].set_data(time_list_DASH, DASHAVG_sell)
    lines[14][0].set_data(time_list_DASH, DASHAVG_buy)
    lines[15][0].set_data(time_list_DASH, DASHVolume)

    ax[1][0].fill_between(time_list_BTC, BTCVolume, color='green')
    ax[1][1].fill_between(time_list_LTC,LTCVolume, color='green')
    ax[1][2].fill_between(time_list_DASH, DASHVolume, color='green')

    ax[0][0].relim()
    ax[0][1].relim()
    ax[0][2].relim()
    ax[1][0].relim()
    ax[1][1].relim()
    ax[1][2].relim()
    ax[0][0].autoscale_view()
    ax[0][1].autoscale_view()
    ax[0][2].autoscale_view()
    ax[1][0].autoscale_view()
    ax[1][1].autoscale_view()
    ax[1][2].autoscale_view()


time_list_BTC = []
time_list_LTC = []
time_list_DASH = []
BTCBuy = []
BTCSell = []
LTCBuy = []
LTCSell = []
DASHBuy = []
DASHSell = []
lines = []
BTCVolume = []
LTCVolume = []
DASHVolume = []
BTCAVG_buy = []
BTCAVG_sell = []
LTCAVG_buy = []
LTCAVG_sell = []
DASHAVG_buy = []
DASHAVG_sell = []
RSI_list = []
Decrease_list = []
Increase_list = []
plot()