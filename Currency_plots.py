import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from statistics import mean

Currencies=['BCC' , 'LTC' , 'ETH']
Currency_category='PLN'
url_beg="https://bitbay.net/API/Public/"
url_end="/ticker.json"
time_sleep=5

window_RSI=40
window_mean=20

def download_data(currency,curr_category,url_beg,url_end): #c_currencies is a list
    url=url_beg+currency+curr_category+url_end
    status=requests.get(url).status_code
    if status==200:
        data = requests.get(url).json()
        return data['ask'],data['bid'],data['volume']
    else:
        print("Could not download data. Try again later!")
        sys.exit()

def plot_data(x_data,plt,volumes,i):
    x_data.append(datetime.now().strftime("%H:%M:%S"))
    ask, bid,volume = download_data(Currencies[i], Currency_category, url_beg, url_end)

    plt.append(ask)
    plt.append(bid)

    volumes.append(volume)
    return x_data,plt,volumes

def RSI(window_RSI,sell,wzrost,spadek,RSI_value):
    if len(sell)==1:
        wzrost.append(0)
        spadek.append(0)
    else:
        if (sell[-1]-sell[-2])>=0:
            wzrost.append(sell[-1]-sell[-2])
            spadek.append(0)
        else:
            wzrost.append(0)
            spadek.append(sell[-1] - sell[-2])

    if len(sell)<=window_RSI:
        if mean(spadek) == 0:
            RSI_value.append(0)
            return RSI_value
        RSI_value.append(100 - (100 / (1 + (mean(wzrost) / abs(mean(spadek))))))
    else:
        if mean(spadek[-window_RSI:]) == 0:
            RSI_value.append(0)
            return RSI_value
        RSI_value.append(100-(100/(1+(mean(wzrost[-window_RSI:])/abs(mean(spadek[-window_RSI:]))))))
    return RSI_value



def mean_data(window_mean,sell_data, buy_data,sell_data_mean,buy_data_mean):
    if len(sell_data)>=window_mean and len(buy_data)>=window_mean:
        sell_data_mean.append(mean(sell_data[-window_mean:]))
        buy_data_mean.append(mean(buy_data[-window_mean:]))
    else:
        sell_data_mean.append(mean(sell_data))
        buy_data_mean.append(mean(buy_data))
    return sell_data_mean,buy_data_mean

def find_volume(volumes,changed_volumes):
    if len(volumes)>=2:
        if volumes[-2]>=volumes[-1]:
            changed_volumes.append(0)
        else:
            changed_volumes.append(volumes[-1]-volumes[-2])
    else:
        changed_volumes.append(0)
    return changed_volumes


def x_range_plot(data):
    if len(data)>=10:
        l=int(len(data)//10)
        data=data[::l+1]
    return data

def x_data(data):
    data=x_range_plot(data)
    return data

def plot(data,y_data,volumes,window_mean,currency,axs,l,sell_mean,buy_mean,wzrost,spadek,RSI_value,choice,changed_volumes):
    RSI_vol=RSI(window_RSI,y_data[::2],wzrost,spadek,RSI_value)
    volume = find_volume(volumes,changed_volumes)
    x=x_data(data)
    sell,buy=mean_data(window_mean,y_data[::2], y_data[1::2],sell_mean,buy_mean)


    axs[0][l].plot(data,sell,label=currency+'_ask_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[::2],label=currency+'_ask')

    axs[0][l].plot(data, buy,label=currency+'_bid_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[1::2],label=currency+'_bid')


    if choice=='RSI':
        axs[1][l].plot(data, RSI_vol)
        axs[1][l].set_ylim(0, 100)
        axs[1][l].set_ylabel('RSI')
    if choice=='volume':
        axs[1][l].bar(data, volume)
        axs[1][l].set_ylim(bottom=0,top=None)
        axs[1][l].set_ylabel('Wolumen')


    axs[1][l].set_xlabel('Godzina')
    axs[0][l].set_ylabel('Cena')
    axs[1][l].set_xticks((x))
    axs[1][l].set_xticklabels(x, rotation=45)

    axs[0][l].legend(bbox_to_anchor=(0, 1.1), loc='center')

    fig.tight_layout()



def draw_plot(i):
    x_data_BCC_d,plt_BCC_d,BCC_volumes_d=plot_data(x_data_BCC,plt_BCC, BCC_volumes,0)
    x_data_LTC_d, plt_LTC_d, LTC_volumes_d = plot_data(x_data_LTC, plt_LTC, LTC_volumes,1)
    x_data_ETH_d, plt_ETH_d, ETH_volumes_d = plot_data(x_data_ETH, plt_ETH, ETH_volumes,2)
    plt.clf()
    gs = fig.add_gridspec(2, 3, hspace=0)
    axs = gs.subplots(sharex=True)

    plot(x_data_BCC_d,plt_BCC_d,BCC_volumes_d, window_mean, 'BCC',axs,0,sell_mean_BCC,buy_mean_BCC,wzrost_BCC,spadek_BCC,RSI_BCC,choice,changed_volumes_BCC)
    plot(x_data_LTC_d, plt_LTC_d, LTC_volumes_d, window_mean, 'LTC',axs, 1,sell_mean_LTC,buy_mean_LTC,wzrost_LTC,spadek_LTC,RSI_LTC,choice,changed_volumes_LTC)
    plot(x_data_ETH_d, plt_ETH_d, ETH_volumes_d, window_mean, 'ETH',axs, 2,sell_mean_ETH,buy_mean_ETH,wzrost_ETH,spadek_ETH,RSI_ETH,choice,changed_volumes_ETH)

if __name__=="__main__":
    x_data_BCC= [];x_data_LTC = [];x_data_ETH = []
    plt_BCC= [];plt_LTC = [];plt_ETH = []
    BCC_volumes=[];LTC_volumes=[];ETH_volumes=[]
    sell_mean_BCC=[];buy_mean_BCC=[]
    sell_mean_LTC=[];buy_mean_LTC=[]
    sell_mean_ETH=[];buy_mean_ETH=[]
    wzrost_BCC = [];spadek_BCC = []
    wzrost_LTC = [];spadek_LTC = []
    wzrost_ETH=[];spadek_ETH=[]
    RSI_BCC=[];RSI_LTC=[];RSI_ETH=[]
    changed_volumes_BCC=[];changed_volumes_LTC=[];changed_volumes_ETH=[]
    fig = plt.figure()
    choice=input("RSI or volume?")
    T_animation=animation(fig,draw_plot,interval=1000*time_sleep)
    plt.show()
