import requests
import time
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
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


def datas(crypto):
    response = responseerr(crypto)
    r1 = response.json()

    bid = r1['bid']
    ask = r1['ask']
    volume = r1['volume']

    return bid,ask,volume

def averange(data,parameter):
    mean = np.mean(data[-(parameter):])
    return mean


def dataslist(currency):
    bid , ask, vol = datas(f"{CRYPTOS[0]}{currency}")
    BTCbid.append(bid)
    BTCask.append(ask)
    BTCvol.append(vol)
    BTCaskavg.append(averange(BTCask,5))


    bid , ask, vol = datas(f"{CRYPTOS[1]}{currency}")
    ETHbid.append(bid)
    ETHask.append(ask)
    ETHvol.append(vol)
    ETHaskavg.append(averange(ETHask,5))


    bid , ask, vol = datas(f"{CRYPTOS[2]}{currency}")
    OMGbid.append(bid)
    OMGask.append(ask)
    OMGvol.append(vol)    
    OMGaskavg.append(averange(OMGask,5))



def plot(i):
    time = dt.datetime.now()
    x.append(time.strftime('%H:%M:%S'))

    dataslist("PLN")

    ax[0].cla()
    ax[0].plot(x,BTCbid,'b', label = "BTCbid")
    ax[0].plot(x,BTCask,'r',label = "BTCask")
    ax[0].plot(x,BTCaskavg,'salmon',label = "BTCavgask")
    ax[0].set_xlim(auto = 1)
    ax[0].text(x[-1], BTCask[-1],s=round(BTCvol[-1],3))
    ax[0].text(x[-1], BTCaskavg[-1],s=round(BTCaskavg[-1],2),color='darkgreen')
    ax[0].set_title(f"{CRYPTOS[0]} values")
    ax[0].set_ylabel('Value [PLN]')
    ax[0].set_xlabel('Time')


    ax[1].cla()
    ax[1].plot(x,ETHbid, 'g', label = "ETHbid")
    ax[1].plot(x,ETHask, 'y',label = "ETHask")
    ax[1].plot(x,ETHaskavg,'salmon',label = "ETHavgask")
    ax[1].set_xlim(auto = 1)
    ax[1].text(x[-1], ETHask[-1],s=round(ETHvol[-1],3),color='indigo')
    ax[1].text(x[-1], ETHaskavg[-1],s=round(ETHaskavg[-1],2),color='darkgreen')
    ax[1].set_title(f"{CRYPTOS[1]} values")
    ax[1].set_ylabel('Value [PLN]')
    ax[1].set_xlabel('Time')

    ax[2].cla()
    ax[2].plot(x,OMGbid, 'm',label = "OMGbid")
    ax[2].plot(x,OMGask, 'c',label = "OMGask")
    ax[2].plot(x,OMGaskavg,'salmon',label = "OMGavgask")
    ax[2].set_xlim(auto = 1)
    ax[2].text(x[-1], OMGask[-1],s=round(OMGvol[-1],3),color='indigo')
    ax[2].text(x[-1], OMGaskavg[-1],s=round(OMGaskavg[-1],2),color='darkgreen')
    ax[2].set_title(f"{CRYPTOS[2]} values")
    ax[2].set_ylabel('Value [PLN]')
    ax[2].set_xlabel('Time')


    fig.legend(loc = 'upper left', prop = {'size':10}, title =  "Legenda")
    fig.tight_layout()


CRYPTOS = ["BTC","ETH","OMG"]
CURRENCY = "PLN"


if __name__ == '__main__':
    x = []

    BTCbid = []
    BTCask = []
    BTCvol = []
    BTCaskavg = []


    ETHbid = []
    ETHask = []
    ETHvol = []
    ETHaskavg = []

    OMGbid = []
    OMGask = []
    OMGvol = []
    OMGaskavg = []

    fig, ax = plt.subplots(3)
    ani = FuncAnimation(fig, plot, interval=5000)

    plt.show()
