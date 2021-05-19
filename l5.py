import matplotlib.pyplot as plt
import requests
import datetime
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import numpy as np

def Values(currency):
    r = requests.get(f"https://bitbay.net/API/Public/{currency}PLN/ticker.json")
    try:
        values = r.json()
        buy = values["bid"]
        sell = values["ask"]
        return buy, sell
    except requests.exceptions.HTTPError:
        print("An error has occured")


def getVolumeNewAPI(currency, time):
    url = f'https://api.bitbay.net/rest/trading/transactions/{currency}-PLN'

    now = datetime.datetime.now()
    before = int((now - datetime.timedelta(0, time)).timestamp()) * 1000
    querystring = {"from": before}
    try:
        response = requests.request("GET", url, params=querystring)
        volume = float(response.json()['items'][0]['a'])
    except:
        volume = 0
    return volume

def Average(list_buy, list_sell, user_parameter):
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
        for i in range(-1, -(user_parameter + 1), -1):
            buy.append(list_buy[i])
            sell.append(list_sell[i])
        buy = sum(buy) / user_parameter
        sell = sum(sell) / user_parameter
        return buy, sell

def RSI(sell_list, user_parameter, Increase_list, Decrease_list):
    if len(sell_list) > user_parameter:
        value = sell_list[len(sell_list) - 1] - sell_list[len(sell_list) - user_parameter]  
        if value > 0:
            Increase_list.append(value)
        elif value < 0:
            Decrease_list.append(value*(-1))
        a = (sum(Increase_list) + 1) / (len(Increase_list) + 1)
        b = (sum(Decrease_list) + 1) / (len(Decrease_list) + 1)
    else:
        a = 1
        b = 1
    RSI = 100 - (100 / (1 +((a + 1) / (b + 1))))
    return RSI

def checkWhatTrend(RSIArray):
    if (RSIArray[-1] < RSIArray[-2]) and (RSIArray[-2] < RSIArray[-3]):
        return "Downward trend"
    elif (RSIArray[-1] > RSIArray[-2]) and (RSIArray[-2] > RSIArray[-3]):
        return "Rising trend"
    elif ((RSIArray[-1] > RSIArray[-2]) and (RSIArray[-2] < RSIArray[-3])) or ((RSIArray[-1] < RSIArray[-2]) and (RSIArray[-2] > RSIArray[-3])):
        return "Sideways trend"
    else:
        return "Too few data"

def defineCandidate(ETHTrend, LTCTrend, DASHTrend, ETHVolume, LTCVolume, DASHVolume):

    ETHLastVolume = float(ETHVolume[-1])
    LTCLastVolume = float(LTCVolume[-1])
    DASHLastVolume = float(DASHVolume[-1])

    LastVolumeArray = [ETHLastVolume, LTCLastVolume, DASHLastVolume]
    maxArray = list()

    if ETHTrend != "Downward trend":
        maxArray.append(LastVolumeArray[0])
    else:
        maxArray.append(0)
    if LTCTrend != "Downward trend":
        maxArray.append(LastVolumeArray[0])
    else:
        maxArray.append(0)
    if DASHTrend != "Downward trend":
        maxArray.append(LastVolumeArray[2])
    else:
        maxArray.append(0)

    out = maxArray.index(np.max(maxArray))
    if out == 0:
        max = "ETH"
    elif out == 1:
        max = "LTC"
    elif out == 2:
        max = "DASH"
    else:
        max = None
    return max

def defineAsLiquid(buy, sell, S):
    if buy > sell:
        max = buy
        min = sell
    else:
        max = sell
        min = buy

    out = min * 100/max
    percent = 100 - out

    if percent < S:
        return True
    else:
        return False

def defineAsVolatile(samplesArray, Y, X):
    if Y < len(samplesArray):
        Ysample = list()
        for i in range(Y):
            Ysample.append(samplesArray[-i])
    else:
        Ysample = samplesArray
        Ysample.pop(0)

    currentSample = samplesArray[0]
    for i in range(len(Ysample)):
        if Ysample[i] > currentSample:
            max = Ysample[i]
            min = currentSample
        else:
            max = currentSample
            min = Ysample[i]

        out = min * 100/max
        percent = 100 - out

        if percent > X:
            return True

    return False

def plot():
    global ax
    fig, ax = plt.subplots(2, 3, figsize=(10, 5))
    fig.tight_layout(pad=3)

    lines.append(ax[0][0].plot(time_list_ETH, ETHBuy, color='red', label='Buy ETH', linewidth=5))
    lines.append(ax[0][0].plot(time_list_ETH, ETHSell, color='black', label='Sell ETH', linewidth=5))
    lines.append(ax[0][0].plot(time_list_ETH, ETHAVG_buy, color='blue', label='Avg buy ETH'))
    lines.append(ax[0][0].plot(time_list_ETH, ETHAVG_sell, color='purple', label='Avg sell ETH'))
    lines.append(ax[0][0].plot(time_list_ETH, RSI_list_ETH, color='brown', label='RSI ETH'))
    ax[0][0].set_title("Quotation Chart ETH PLN")
    ax[0][0].legend(loc=1)
    ax[0][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][0].plot(time_list_ETH, ETHVolume, color='royalblue', label='Volume ETH'))
    ax[1][0].set_title("Volume ETH PLN")
    ax[1][0].legend(loc=1)
    ax[1][0].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[0][1].plot(time_list_LTC, LTCBuy, color='red', label='Buy LTC', linewidth=5))
    lines.append(ax[0][1].plot(time_list_LTC, LTCSell, color='black', label='Sell LTC', linewidth=5))
    lines.append(ax[0][1].plot(time_list_LTC, LTCAVG_buy, color='blue', label='Avg buy LTC'))
    lines.append(ax[0][1].plot(time_list_LTC, LTCAVG_sell, color='purple', label='Avg sell LTC'))
    lines.append(ax[0][1].plot(time_list_LTC, RSI_list_LTC, color='brown', label='RSI LTC'))

    ax[0][1].set_title("Quotation Chart LTC PLN")
    ax[0][1].legend(loc=1)
    ax[0][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][1].plot(time_list_LTC, LTCVolume, color='royalblue', label='Volume LTC'))
    ax[1][1].set_title("Volume LTC PLN")
    ax[1][1].legend(loc=1)
    ax[1][1].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[0][2].plot(time_list_DASH, DASHBuy, color='red', label='Buy DASH', linewidth=5))
    lines.append(ax[0][2].plot(time_list_DASH, DASHSell, color='black', label='Sell DASH', linewidth=5))
    lines.append(ax[0][2].plot(time_list_DASH, DASHAVG_buy, color='blue', label='Avg buy DASH'))
    lines.append(ax[0][2].plot(time_list_DASH, DASHAVG_sell, color='purple', label='Avg sell DASH'))
    lines.append(ax[0][2].plot(time_list_DASH, RSI_list_DASH, color='brown', label='RSI LTC'))
    ax[0][2].set_title("Quotation Chart DASH PLN")
    ax[0][2].legend(loc=1)
    ax[0][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    lines.append(ax[1][2].plot(time_list_LTC, LTCVolume, color='royalblue', label='Volume DASH'))

    ax[1][2].set_title("Volume DASH PLN")
    ax[1][2].legend(loc=1)
    ax[1][2].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

    ax[0][0].set_yscale('log')
    ax[0][1].set_yscale('log')
    ax[0][2].set_yscale('log')

    fig.autofmt_xdate()

    a = FuncAnimation(fig, func=update_plot, interval=3000)
    plt.autoscale()
    plt.show()


def update_plot(i):
    time_list_ETH.append(datetime.datetime.now())
    buyETH, sellETH = Values("ETH")
    ETHBuy.append(buyETH)
    ETHSell.append(sellETH)
    volume = getVolumeNewAPI("ETH", 5)
    ETHVolume.append(volume)

    time_list_LTC.append(datetime.datetime.now())
    buyLTC, sellLTC = Values("LTC")
    LTCBuy.append(buyLTC)
    LTCSell.append(sellLTC)
    volume = getVolumeNewAPI("LTC", 5)
    LTCVolume.append(volume)

    time_list_DASH.append(datetime.datetime.now())
    buyDASH, sellDASH = Values("DASH")
    DASHBuy.append(buyDASH)
    DASHSell.append(sellDASH)
    volume = getVolumeNewAPI("DASH", 5)
    DASHVolume.append(volume)

    buy, sell = Average(ETHBuy, ETHSell, 3)
    ETHAVG_buy.append(buy)
    ETHAVG_sell.append(sell)

    buy, sell = Average(LTCBuy, LTCSell, 3)
    LTCAVG_buy.append(buy)
    LTCAVG_sell.append(sell)

    buy, sell = Average(DASHBuy, DASHSell, 3)
    DASHAVG_buy.append(buy)
    DASHAVG_sell.append(sell)

    rsi = RSI(ETHSell, 2, Increase_list_ETH, Decrease_list_ETH)
    RSI_list_ETH.append(rsi)

    rsi = RSI(LTCSell, 2, Increase_list_LTC, Decrease_list_LTC)
    RSI_list_LTC.append(rsi)

    rsi = RSI(DASHSell, 2, Increase_list_DASH, Decrease_list_DASH)
    RSI_list_DASH.append(rsi)

    if len(RSI_list_ETH) > 3:
        trendETH = checkWhatTrend(RSI_list_ETH)
        ax[0][0].set_xlabel(f'ETH Trend: {trendETH}')
    if len(RSI_list_LTC) > 3:
        trendLTC = checkWhatTrend(RSI_list_LTC)
        ax[0][1].set_xlabel(f'LTC Trend: {trendLTC}')
    if len(RSI_list_DASH) > 3:
        trendDASH = checkWhatTrend(RSI_list_DASH)
        ax[0][2].set_xlabel(f'DASH Trend: {trendDASH}')

    if len(RSI_list_LTC) > 3 and len(RSI_list_ETH) > 3 and len(RSI_list_DASH) > 3:
        out = defineCandidate(trendETH, trendLTC, trendDASH, ETHVolume, LTCVolume, DASHVolume)
        if out == "ETH":
            ax[0][0].set_xlabel(f'ETH Trend: {trendETH}|candidate')
            if (defineAsLiquid(buyETH, sellETH, S)) and (defineAsVolatile(ETHBuy, Y, X)):
                ax[0][0].set_xlabel(f'ETH Trend: {trendETH}|candidate, volatile and liquid asset')
            elif defineAsLiquid(buyETH, sellETH, S):
                ax[0][0].set_xlabel(f'ETH Trend: {trendETH}|candidate, liquid asset')
            elif defineAsVolatile(ETHBuy, Y, X):
                ax[0][0].set_xlabel(f'ETH Trend: {trendETH}|candidate, volatile asset')
        elif out == "LTC":
            ax[0][1].set_xlabel(f'LTC Trend: {trendLTC}|candidate')
            if (defineAsLiquid(buyLTC, sellLTC, S)) and (defineAsVolatile(LTCBuy, Y, X)):
                ax[0][1].set_xlabel(f'LTC Trend: {trendLTC}|candidate, volatile and liquid asset')
            elif defineAsLiquid(buyLTC, sellLTC, S):
                ax[0][1].set_xlabel(f'LTC Trend: {trendLTC}|candidate, liquid asset')
            elif defineAsVolatile(LTCBuy, Y, X):
                ax[0][1].set_xlabel(f'LTC Trend: {trendLTC}|candidate, volatile asset')
        elif out == "DASH":
            ax[0][2].set_xlabel(f'DASH Trend: {trendDASH}|candidate')
            if (defineAsLiquid(buyDASH, sellDASH, S)) and (defineAsVolatile(DASHBuy, Y, X)):
                ax[0][1].set_xlabel(f'DASH Trend: {trendDASH}|candidate, volatile and liquid asset')
            elif defineAsLiquid(buyDASH, sellDASH, S):
                ax[0][2].set_xlabel(f'DASH Trend: {trendDASH}|candidate ,liquid asset')
            elif defineAsVolatile(DASHBuy, Y, X):
                ax[0][1].set_xlabel(f'DASH Trend: {trendDASH}|candidate, volatile asset')


    lines[0][0].set_data(time_list_ETH, ETHBuy)
    lines[1][0].set_data(time_list_ETH, ETHSell)
    lines[2][0].set_data(time_list_ETH, ETHAVG_buy)
    lines[3][0].set_data(time_list_ETH, ETHAVG_sell)
    lines[4][0].set_data(time_list_ETH, RSI_list_ETH)
    lines[5][0].set_data(time_list_ETH, ETHVolume)
    lines[6][0].set_data(time_list_LTC, LTCBuy)
    lines[7][0].set_data(time_list_LTC, LTCSell)
    lines[8][0].set_data(time_list_LTC, LTCAVG_buy)
    lines[9][0].set_data(time_list_LTC, LTCAVG_sell)
    lines[10][0].set_data(time_list_LTC, RSI_list_LTC)
    lines[11][0].set_data(time_list_LTC, LTCVolume)
    lines[12][0].set_data(time_list_DASH, DASHBuy)
    lines[13][0].set_data(time_list_DASH, DASHSell)
    lines[14][0].set_data(time_list_DASH, DASHAVG_sell)
    lines[15][0].set_data(time_list_DASH, DASHAVG_buy)
    lines[16][0].set_data(time_list_DASH, RSI_list_DASH)
    lines[17][0].set_data(time_list_DASH, DASHVolume)

    ax[1][0].fill_between(time_list_ETH, ETHVolume, color='royalblue')
    ax[1][1].fill_between(time_list_LTC, LTCVolume, color='royalblue')
    ax[1][2].fill_between(time_list_DASH, DASHVolume, color='royalblue')

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


time_list_ETH = list()
time_list_LTC = list()
time_list_DASH = list()
ETHBuy = list()
ETHSell = list()
LTCBuy = list()
LTCSell = list()
DASHBuy = list()
DASHSell = list()
lines = list()
ETHVolume = list()
LTCVolume = list()
DASHVolume = list()
ETHAVG_buy = list()
ETHAVG_sell = list()
LTCAVG_buy = list()
LTCAVG_sell = list()
DASHAVG_buy = list()
DASHAVG_sell = list()
RSI_list_ETH = list()
RSI_list_DASH = list()
RSI_list_LTC = list()
Decrease_list_DASH = list()
Increase_list_DASH = list()
Decrease_list_ETH = list()
Increase_list_ETH = list()
Decrease_list_LTC = list()
Increase_list_LTC = list()
S = 5
X = 5
Y = 3
plot()
