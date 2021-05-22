import requests
import time
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.animation import FuncAnimation



def responseerr(crypto):
    response = requests.get(f'https://bitbay.net/API/Public/{crypto}/ticker.json',timeout=5)
    try:
        response
    except requests.exceptions.Timeout as to:
        print(f'Request times out {to}')
    except requests.exceptions.TooManyRedirects as tmr:
        print(f'Request exceeds the configured number of maximum redirections {tmr}')
    except requests.exceptions.HTTPError as http:
        print(f'Request returned an unsuccessful status code {http}')
    except requests.exceptions.RequestException as e:
        print(f'In fact, something went wrong but nobody knows what ¯\_(ツ)_/¯ {e}')
    return response

def get_transactions(crypto, currency):
    response = requests.get(f"https://api.bitbay.net/rest/trading/transactions/{crypto}-{currency}?limit=10")
    transactions = json.loads(response.text)
    if transactions["status"] == "Ok":
        return transactions
    else:
        print("Failed to connect, try again")

def volume(crypto, currency):
    transactions = get_transactions(crypto, currency)
    volume = []
    for key in transactions["items"]:
        key["r"] = float(key["r"])
        volume.append(key["r"])
    volume_ = sum(volume)
    return volume_


def datas(crypto):
    response = responseerr(crypto)
    r1 = response.json()

    bid = r1['bid']
    ask = r1['ask']

    return bid,ask

def averange(data,parameter):
    mean = np.mean(data[-(parameter):])
    return mean

def calc_RSI(data, start, end):
    data = data[-20:]
    rsi_data = data[start:end]
    ups = 0
    up_count = 0
    downs = 0
    down_count = 0
    for i in range(1, len(rsi_data)):
        if rsi_data[i-1] < rsi_data[i]:
            up = rsi_data[i] - rsi_data[i-1]
            ups += up
            up_count += 1
        elif rsi_data[i-1] > rsi_data[i]:
            down = rsi_data[i-1] - rsi_data[i]
            downs += down
            down_count += 1

    if up_count == 0:
        a = 1
    else:
        a = ups/up_count
    if down_count == 0:
        b = 1
    else:
        b = downs/down_count
    rsi = 100 - (100/(1+(a/b)))
    return rsi

def trend(rsi_list):
    rsi = rsi_list[-1]
    if rsi >= 70:
        return 'upward trend'
    elif rsi <= 30:
        return 'downward trend'
    else:
        return 'sideways trend'

def dataslist(currency):
    bid, ask = datas(f"{CRYPTOS[0]}{currency}")
    BTCbid.append(bid)
    BTCask.append(ask)
    BTCvol.append(volume(CRYPTOS[0],CURRENCY))
    BTCaskavg.append(averange(BTCask,5))
    rsi_askBTC.append(calc_RSI(BTCask, 4, 7))
    rsi_bidBTC.append(calc_RSI(BTCbid, 4, 7))   

    bid, ask= datas(f"{CRYPTOS[1]}{currency}")
    ETHbid.append(bid)
    ETHask.append(ask)
    ETHvol.append(volume(CRYPTOS[1],CURRENCY))
    ETHaskavg.append(averange(ETHask,5))
    rsi_askETH.append(calc_RSI(ETHask, 4, 7))
    rsi_bidETH.append(calc_RSI(ETHbid, 4, 7))

    bid, ask= datas(f"{CRYPTOS[2]}{currency}")
    OMGbid.append(bid)
    OMGask.append(ask)
    OMGvol.append(volume(CRYPTOS[2],CURRENCY))  
    OMGaskavg.append(averange(OMGask,5))
    rsi_askOMG.append(calc_RSI(OMGask, 4, 7))
    rsi_bidOMG.append(calc_RSI(OMGbid, 4, 7))


def plot(i):
    time = dt.datetime.now()
    x.append(time.strftime('%H:%M:%S'))

    dataslist("PLN")

    ax[0][0].cla()
    ax[0][0].plot(x,BTCbid,'b', label = "BTCbid")
    ax[0][0].plot(x,BTCask,'r',label = "BTCask")
    ax[0][0].set_xlim(auto = 1)
    ax[0][0].set_title(f"{CRYPTOS[0]} values")
    ax[0][0].set_ylabel('Value [PLN]')
    ax[0][0].set_xlabel('Time')
    ax[0][0].text(0.3, 0.2, f"Volume: {round(BTCvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[0][0].transAxes)
    

    ax[0][1].cla()
    ax[0][1].plot(x,rsi_askBTC,'c', label = "BTCrsi")
    ax[0][1].set_xlim(auto = 1)
    ax[0][1].set_title(f"RSI for {CRYPTOS[0]} ")
    ax[0][1].set_ylabel('Points')
    ax[0][1].set_xlabel('Time')
    ax[0][1].text(0.3, 0.2, f"{trend(rsi_askBTC)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[0][1].transAxes)

    ax[0][2].cla()
    ax[0][2].plot(x,BTCaskavg,'k--',label = "BTCavgask")
    ax[0][2].set_title(f"Mean for {CRYPTOS[0]} ask")
    ax[0][2].set_ylabel('Value [PLN]')
    ax[0][2].set_xlabel('Time')
   
    ax[1][0].cla()
    ax[1][0].plot(x,ETHbid,'b', label = "ETHbid")
    ax[1][0].plot(x,ETHask,'r',label = "ETHask")
    ax[1][0].set_xlim(auto = 1)
    ax[1][0].set_title(f"{CRYPTOS[1]} values")
    ax[1][0].set_ylabel('Value [PLN]')
    ax[1][0].set_xlabel('Time')
    ax[1][0].text(0.3, 0.2, f"Volume: {round(ETHvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[1][0].transAxes)


    ax[1][1].cla()
    ax[1][1].plot(x,rsi_askETH,'c', label = "ETHrsi")
    ax[1][1].set_xlim(auto = 1)
    ax[1][1].set_title(f"RSI for {CRYPTOS[1]} ")
    ax[1][1].set_ylabel('Points')
    ax[1][1].set_xlabel('Time')
    ax[1][1].text(0.3, 0.2, f"{trend(rsi_askETH)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[1][1].transAxes)

    ax[1][2].cla()
    ax[1][2].plot(x,ETHaskavg,'k--',label = "ETHavgask")
    ax[1][2].set_title(f"Mean for {CRYPTOS[1]} ask")
    ax[1][2].set_ylabel('Value [PLN]')
    ax[1][2].set_xlabel('Time')

    ax[2][0].cla()
    ax[2][0].plot(x,OMGbid,'b', label = "OMGbid")
    ax[2][0].plot(x,OMGask,'r',label = "OMGask")
    ax[2][0].set_xlim(auto = 1)
    ax[2][0].set_title(f"{CRYPTOS[2]} values")
    ax[2][0].set_ylabel('Value [PLN]')
    ax[2][0].set_xlabel('Time')
    ax[2][0].text(0.3, 0.2, f"Volume: {round(OMGvol[-1],3)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[2][0].transAxes)

    ax[2][1].cla()
    ax[2][1].plot(x,rsi_askOMG,'c', label = "OMGrsi")
    ax[2][1].set_xlim(auto = 1)
    ax[2][1].set_title(f"RSI for {CRYPTOS[2]} ")
    ax[2][1].set_ylabel('Points')
    ax[2][1].set_xlabel('Time')
    ax[2][1].text(0.3, 0.2, f"{trend(rsi_askOMG)}", horizontalalignment='center',
                  verticalalignment='center', transform=ax[2][1].transAxes)
    


    ax[2][2].cla()
    ax[2][2].plot(x,OMGaskavg,'k--',label = "OMGavgask")
    ax[2][2].set_title(f"Mean for {CRYPTOS[2]} ask")
    ax[2][2].set_ylabel('Value [PLN]')
    ax[2][2].set_xlabel('Time')


    fig.legend(["bid","ask","rsi","avg"],loc = 'upper left', prop = {'size':10}, title =  "Legenda")



CRYPTOS = ["BTC","ETH","OMG"]
CURRENCY = "PLN"


if __name__ == '__main__':

    x = []
    

    BTCbid = []
    BTCask = []
    BTCvol = []
    BTCaskavg = []
    rsi_bidBTC = []
    rsi_askBTC = []


    ETHbid = []
    ETHask = []
    ETHvol = []
    ETHaskavg = []
    rsi_bidETH = []
    rsi_askETH = []

    OMGbid = []
    OMGask = []
    OMGvol = []
    OMGaskavg = []
    rsi_bidOMG = []
    rsi_askOMG = []

    fig, ax = plt.subplots(3,3,tight_layout=True)
    ani = FuncAnimation(fig, plot, interval=5000)

    plt.show()