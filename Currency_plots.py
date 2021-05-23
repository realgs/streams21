import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation
from statistics import mean

Currencies=['BCC' , 'LTC' , 'ETH']
Currency_category='PLN'
Url_beg="https://bitbay.net/API/Public/"
Url_end="/ticker.json"

Time_sleep=5

Trans_url = "https://api.bitbay.net/rest/trading/transactions/"
Volume_range=60

Window_RSI=40
Window_mean=20

S=3
X=10
Y=12

def download_data(currency,curr_category,url_beg,url_end): #c_currencies is a list
    url=url_beg+currency+curr_category+url_end
    status=requests.get(url).status_code
    if status==200:
        data = requests.get(url).json()
        return data['ask'],data['bid'],data['volume']
    else:
        print("Could not download data. Try again later!")
        sys.exit()

def download_trans(currency,curr_category,trans_url,Y): #c_currencies is a list
    url=trans_url+currency+'-'+curr_category
    status=requests.get(url).status_code
    trans=[]
    if status==200:
        par={"limit":Y}
        data = requests.get(url,params=par).json()
        for key in data["items"]:
            trans.append(float(key["a"]) * float(key["r"]))
        return trans
    else:
        print("Could not download data. Try again later!")
        sys.exit()


def plot_data(x_data,plt,volumes,i):
    x_data.append(datetime.now().strftime("%H:%M:%S"))
    ask, bid,volume = download_data(Currencies[i], Currency_category, Url_beg, Url_end)

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
    RSI_vol=RSI(Window_RSI,y_data[::2],wzrost,spadek,RSI_value)
    volume = find_volume(volumes,changed_volumes)
    x=x_data(data)
    sell,buy=mean_data(window_mean,y_data[::2], y_data[1::2],sell_mean,buy_mean)


    axs[0][l].plot(data,sell,label=currency+'_ask_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[::2],label=currency+'_ask')

    axs[0][l].plot(data, buy,label=currency+'_bid_mean',alpha=0.5,ls='--')
    axs[0][l].plot(data, y_data[1::2],label=currency+'_bid')


    axs[1][l].bar(data, volume,color='r',alpha=0.7)
    axs[1][l].set_ylim(bottom=0,top=None)
    axs[1][l].set_ylabel('Wolumen',color='r')
    val=f'Wolumen: {round(sum(volume[-int(Volume_range/Time_sleep):]),3)}'
    axs[1][l].text(0.2, 0.05, val, horizontalalignment='center',
                  verticalalignment='center', transform=axs[1][l].transAxes)

    axs2= axs[1][l].twinx()
    axs2.plot(data, RSI_vol)
    axs2.set_ylim(0, 100)
    axs2.set_ylabel('RSI',color='b')
    val=f'RSI: {round((RSI_vol[-1]),2)}'
    axs2.text(0.15, 0.95, val, horizontalalignment='center',
                   verticalalignment='center', transform=axs2.transAxes)


    axs[1][l].set_xlabel('Godzina')
    axs[0][l].set_ylabel('Cena')
    axs[1][l].set_xticks((x))
    axs[1][l].set_xticklabels(x, rotation=45)

    axs[0][l].legend(bbox_to_anchor=(0, 1.3), loc='center')

    fig.tight_layout()

    return RSI_vol,volume,y_data

def volatile_asset(X, Y,i):
    data=download_trans(Currencies[i],Currency_category,Trans_url,Y)

    minimum = min(data)
    maximum = max(data)

    diff = (abs(maximum - minimum) / maximum) * 100
    diff = round(diff, 2)
    if diff > X:
        return 'Volatile asset'
    else:
        return ''

def spread(S,y_data):
    diff = 100*((y_data[-2]- y_data[-1]) / y_data[-2])

    if diff<S:
        return 'Liquid asset'
    else:
        return ''



def increase_decrease_RSI(RSI_list,volume_list,axs,y_data):
    decisions=[]
    volume_max=[]
    for r in range(len(RSI_list)):
        if RSI_list[r][-1] <= 40:
            decisions.append("Trend spadkowy")
        if RSI_list[r][-1] >= 60:
            decisions.append("Trend wzrostowy")
            volume_max.append(round(sum(volume_list[r][-int(Volume_range/Time_sleep):]),3))
        if RSI_list[r][-1] > 40 and RSI_list[r][-1] <60:
            decisions.append('Trend boczny')
    for i in range(len(decisions)):
        if RSI_list[i][-1]!=0:
            axs[1][i].text(0.5, 0.95, decisions[i], horizontalalignment='center',
                       verticalalignment='center', transform=axs[1][i].transAxes)
            if len(volume_max) >= 1:
                if decisions[i]=='Trend wzrostowy' and round(sum(volume_list[i][-int(Volume_range/Time_sleep):]),3)==max(volume_max):
                    s=spread(S,y_data[i])
                    v=volatile_asset(X, Y,i)
                    axs[0][i].set_title("Najlepszy kandydat \n"+s+'\n'+v)


def draw_plot(i):
    x_data_BCC_d,plt_BCC_d,BCC_volumes_d=plot_data(x_data_BCC,plt_BCC, BCC_volumes,0)
    x_data_LTC_d, plt_LTC_d, LTC_volumes_d = plot_data(x_data_LTC, plt_LTC, LTC_volumes,1)
    x_data_ETH_d, plt_ETH_d, ETH_volumes_d = plot_data(x_data_ETH, plt_ETH, ETH_volumes,2)
    plt.clf()
    gs = fig.add_gridspec(2, 3, hspace=0)
    axs = gs.subplots(sharex=True)

    BCC_RSI,BCC_volume,BCC_plt=plot(x_data_BCC_d,plt_BCC_d,BCC_volumes_d, Window_mean, 'BCC',axs,0,sell_mean_BCC,buy_mean_BCC,wzrost_BCC,spadek_BCC,RSI_BCC,choice,changed_volumes_BCC)
    LTC_RSI,LTC_volume,LTC_plt=plot(x_data_LTC_d, plt_LTC_d, LTC_volumes_d, Window_mean, 'LTC',axs, 1,sell_mean_LTC,buy_mean_LTC,wzrost_LTC,spadek_LTC,RSI_LTC,choice,changed_volumes_LTC)
    ETH_RSI,ETH_volume,ETH_plt=plot(x_data_ETH_d, plt_ETH_d, ETH_volumes_d, Window_mean, 'ETH',axs, 2,sell_mean_ETH,buy_mean_ETH,wzrost_ETH,spadek_ETH,RSI_ETH,choice,changed_volumes_ETH)

    increase_decrease_RSI([BCC_RSI,LTC_RSI,ETH_RSI],[BCC_volume,LTC_volume,ETH_volume],axs,[BCC_plt,LTC_plt,ETH_plt])

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
    # choice=input("RSI or volume?")
    choice='RSI and volume'
    T_animation=animation(fig,draw_plot,interval=1000*Time_sleep)
    plt.show()