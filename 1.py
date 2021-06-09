import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from matplotlib.font_manager import FontProperties
import numpy as np
from matplotlib.ticker import MaxNLocator
import json

currency = ['LTCBTC', 'ETHBTC', 'DASHBTC']
fig, axs = plt.subplots(3)
ax02 = axs[0].twinx()
ax12 = axs[1].twinx()
ax22 = axs[2].twinx()
axs[0].locator_params(nbins = 3)
fig.tight_layout(pad = 3)

def get_data(currency):
    try:
        response = requests.get(f'https://bitbay.net/API/Public/{currency}/ticker.json')
        data = response.json()
        return data
    except requests.exceptions.MissingSchema:
        print("Missing URL schema (e.g. http or https)")
    except requests.exceptions.ConnectionError:
        print("Connection Error occured")

def append_not_none(values, a):
    if a != None:
        values.append(a)
    else:
        if len(values)>1:
            values.append(values[-1])

def append_mean(mean_values, values,mean_elements):
    if len(values)>mean_elements:
        mean_values.append(np.mean(values[-(mean_elements):]))
    else:
        mean_values.append(np.mean(values))

def append_rsi(rsi_values, values, mean_elements):
    if len(values)>mean_elements:
        rsi_values.append(100 - (100/(1+max(values[-(mean_elements):])/min(values[-(mean_elements):]))))
    else:
        rsi_values.append(100 - (100/(1+max(values)/min(values))))
def prepare_data(ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean,rsi1_values, rsi2_values, rsi3_values, volume1, large_volumes1,volume2,large_volumes2,volume3,large_volumes3):
    data1 = get_data(currency[0])
    data2 = get_data(currency[1])
    data3 = get_data(currency[2])
    large_volumes1.append(data1.get('volume'))
    volume1.append(abs(large_volumes1[-1]-large_volumes1[-2]))
    large_volumes2.append(data2.get('volume'))
    volume2.append(abs(large_volumes2[-1] - large_volumes2[-2]))
    large_volumes3.append(data3.get('volume'))
    volume3.append(abs(large_volumes3[-1] - large_volumes3[-2]))
    # print(volume1)
    # print(volume2)
    # print(volume3)
    append_not_none(ask1_values,data1.get('ask'))
    append_not_none(bid1_values,data1.get('bid'))
    append_not_none(ask2_values, data2.get('ask'))
    append_not_none(bid2_values, data2.get('bid'))
    append_not_none(ask3_values, data3.get('ask'))
    append_not_none(bid3_values, data3.get('bid'))
    append_rsi(rsi1_values,ask1_values,mean_elements)
    append_rsi(rsi2_values,ask2_values,mean_elements)
    append_rsi(rsi3_values,ask3_values,mean_elements)
    append_mean(ask1_mean,ask1_values,mean_elements)
    append_mean(bid1_mean, bid1_values,mean_elements)
    append_mean(ask2_mean,ask2_values,mean_elements)
    append_mean(bid2_mean,bid2_values,mean_elements)
    append_mean(ask3_mean,ask3_values,mean_elements)
    append_mean(bid3_mean,bid3_values,mean_elements)
    return ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean,rsi1_values, rsi2_values, rsi3_values, volume1, volume2, volume3



def make_plot(i):
    now.append(datetime.now().strftime("%H:%M:%S"))
    plt1_ask, plt1_bid,plt2_ask, plt2_bid, plt3_ask, plt3_bid, plt1_ask_mean,plt1_bid_mean,plt2_ask_mean,plt2_bid_mean,plt3_ask_mean,plt3_bid_mean, plt_rsi1, plt_rsi2, plt_rsi3, plt_volume1, plt_volume2, plt_volume3 = prepare_data(ask1_values, bid1_values, ask2_values, bid2_values, ask3_values, bid3_values,ask1_mean,bid1_mean, ask2_mean,bid2_mean,ask3_mean,bid3_mean,rsi1_values, rsi2_values, rsi3_values, volume1, large_volumes1,volume2,large_volumes2,volume3,large_volumes3)

    axs[0].cla()
    ax02.cla()
    axs[0].locator_params( nbins=3)
    axs[0].plot(now,plt1_ask, label = f'{currency[0]}:Ask')
    axs[0].plot(now,plt1_bid, label = f'{currency[0]}:Bid')
    ax02.bar(now,plt_volume1, label = f"{currency[0]}:Volume", width = 0.2, color = 'g')
    ax02.set_ylabel('Volume', loc = 'bottom')
    ax02.tick_params('both', length=30, which='major')
    if mean_or_rsi == 1:
        axs[0].plot(now,plt1_ask_mean,label = f'{currency[0]}:Ask Mean')
        axs[0].plot(now, plt1_bid_mean, label=f'{currency[0]}:Bid Mean')
    elif mean_or_rsi == 2:
        ax01.cla()
        ax01.plot(now,plt_rsi1,'r',label = f'{currency[0]}:RSI')
        ax01.set_yticks((0, 30, 50, 70, 100))
        ax01.set_ylabel('RSI Value',color = 'r', loc = 'top')
        ax01.tick_params('both',length = 10, color = 'r', labelcolor = 'r')
        if rsi1_values[-1] > 70:
            plt.gcf().text(0.02, 0.8, 'Sygnal \nsprzedazy',c = 'g', fontsize=10)
        elif rsi1_values[-1]< 30:
            plt.gcf().text(0.02, 0.8, 'Sygnal \nkupna',c = 'r', fontsize=10)
        else:
            plt.gcf().text(0.02, 0.8, 'Neutralny', fontsize=10)
    axs[0].set_xlim(auto = 1)
    axs[0].set_title(f"{currency[0]} values")
    axs[0].set_ylabel('Value ')
    axs[0].set_xlabel('Time')


    axs[1].cla()
    ax12.cla()
    axs[1].plot(now, plt2_ask, label=f'{currency[1]}:Ask')
    axs[1].plot(now, plt2_bid, label=f'{currency[1]}:Bid')
    ax12.bar(now,plt_volume2,label = f"{currency[1]}:Volume", width = 0.2, color = 'g')
    ax12.set_ylabel('Volume', loc = 'bottom')
    ax12.tick_params('both', length = 30, which = 'major')
    if mean_or_rsi == 1:
        axs[1].plot(now, plt2_ask_mean, label=f'{currency[1]}:Ask Mean')
        axs[1].plot(now, plt2_bid_mean, label=f'{currency[1]}:Bid Mean')
    elif mean_or_rsi == 2:
        ax11.cla()
        ax11.plot(now, plt_rsi2,'r', label=f'{currency[1]}:RSI')
        ax11.set_ylabel('RSI Value',color = 'r', loc = 'top')
        ax11.set_yticks((0,30,50,70,100))
        ax11.tick_params('both', length = 10, color = 'r', labelcolor = 'r')
        if rsi1_values[-1] > 70:
            plt.gcf().text(0.02, 0.5, 'Sygnal \nsprzedazy',c = 'g', fontsize=10)
        elif rsi1_values[-1]< 30:
            plt.gcf().text(0.02, 0.5, 'Sygnal \nkupna',c = 'r', fontsize=10)
        else:
            plt.gcf().text(0.02, 0.5, 'Neutralny', fontsize=10)
    axs[1].set_title(f"{currency[1]} values")
    axs[1].set_ylabel('Value ')
    axs[1].set_xlabel('Time')

    axs[2].cla()
    ax22.cla()
    axs[2].plot(now, plt3_ask, label=f'{currency[2]}:Ask')
    axs[2].plot(now, plt3_bid, label=f'{currency[2]}:Bid')
    ax22.bar(now, plt_volume3,label = f'{currency[2]}:Volume', width = 0.2, color = 'g')
    ax22.set_ylabel("Volume", loc = 'bottom')
    ax22.tick_params('both', length = 30, which = 'major')
    if mean_or_rsi == 1:
        axs[2].plot(now, plt3_ask_mean, label=f'{currency[2]}:Ask Mean')
        axs[2].plot(now, plt3_bid_mean, label=f'{currency[2]}:Bid Mean')
    elif mean_or_rsi == 2:
        ax21.cla()
        ax21.plot(now, plt_rsi3,'r', label=f'{currency[2]}:RSI')
        ax21.set_ylabel('RSI Value',color = 'r', loc = 'top')
        ax21.set_yticks((0,30,50,70,100))
        ax21.tick_params('both', length = 10, color = 'r', labelcolor = 'r')
        if rsi1_values[-1] > 70:
            plt.gcf().text(0.02, 0.2, 'Sygnal \nsprzedazy',c = 'g', fontsize=10)
        elif rsi1_values[-1]< 30:
            plt.gcf().text(0.02, 0.2, 'Sygnal \nkupna',c = 'r', fontsize=10)
        else:
            plt.gcf().text(0.02, 0.2, 'Neutralny', fontsize=10)
    axs[2].set_title(f"{currency[2]} values")
    axs[2].set_ylabel('Value ')
    axs[2].set_xlabel('Time')
    list_of_rsi = [rsi1_values,rsi2_values,rsi3_values]
    list_of_volumes = [volume1,volume2,volume3]
    trend_checking = [0,0,0]
    if mean_or_rsi == 2:
        for i in range(0,3):
            if list_of_rsi[i][-1]>30:
                trend_checking[i]= list_of_volumes[i][-1]
        #print(f'trend to {trend_checking}')
        array = np.asarray(trend_checking)
        #print(f'array to {array}')
        maxarg = np.argmax(array)
        #print(f'maxarg {maxarg}')
    FontP = FontProperties()
    FontP.set_size('xx-small')
    fig.legend(loc='upper left', prop={'size': 5})




if __name__ == "__main__":
    mean_elements = int(input("How many last elements do we use to calculate mean or RSI: "))
    mean_or_rsi = int(input("1.Mean or 2.RSI "))
    save = int(input("Do you want to save values when closing program?\n1.Yes\n0.No\n"))
    from_saved = int(input("Do you want to use saved data?\n1.Yes\n0.No\n"))
    if mean_or_rsi == 2:
        ax01 = axs[0].twinx()
        ax11 = axs[1].twinx()
        ax21 = axs[2].twinx()
    time_int = 5
    now = []
    large_volumes1 = []
    large_volumes2 = []
    large_volumes3 = []
    large_volumes1.append(get_data(currency[0]).get('volume'))
    large_volumes2.append(get_data(currency[1]).get('volume'))
    large_volumes3.append(get_data(currency[2]).get('volume'))
    if from_saved == 0:
        ask1_values = []
        ask1_mean = []
        bid1_mean = []
        bid1_values = []
        ask2_values = []
        ask2_mean = []
        bid2_mean = []
        bid2_values = []
        ask3_values = []
        ask3_mean = []
        bid3_mean = []
        bid3_values = []
        rsi1_values = []
        rsi2_values = []
        rsi3_values = []
        volume1 = []
        volume2 = []
        volume3 = []

    elif from_saved == 1:
        with open('data.json') as json_file:
            data = json.load(json_file)
        ask1_values = data['ask1_values']
        ask1_mean = data['ask1_mean']
        bid1_mean = data['bid1_mean']
        bid1_values = data['bid1_values']
        ask2_values = data['ask2_values']
        ask2_mean = data['ask2_mean']
        bid2_mean = data['bid2_mean']
        bid2_values = data['bid2_values']
        ask3_values = data['ask3_values']
        ask3_mean = data['ask3_mean']
        bid3_mean = data['bid3_mean']
        bid3_values = data['bid3_values']
        rsi1_values = data['rsi1_values']
        rsi2_values = data['rsi2_values']
        rsi3_values = data['rsi3_values']
        now = data['now']
        volume1 = data['volume1']
        volume2 = data['volume2']
        volume3 = data['volume3']

    animations = FuncAnimation(fig, make_plot, interval=5000)
    axs[0].xaxis.set_major_locator(MaxNLocator(5))
    plt.autoscale()
    plt.show()

    if save == 1:
        data = {}
        data['ask1_values'] = ask1_values
        data['bid1_values'] = bid1_values
        data['ask1_mean'] = ask1_mean
        data['bid1_mean'] = bid1_mean
        data['ask2_values'] = ask2_values
        data['bid2_values'] = bid2_values
        data['ask2_mean'] = ask2_mean
        data['bid2_mean'] = bid2_mean
        data['ask3_values'] = ask3_values
        data['bid3_values'] = bid3_values
        data['ask3_mean'] = ask3_mean
        data['bid3_mean'] = bid3_mean
        data['now'] = now
        data['rsi1_values'] = rsi1_values
        data['rsi2_values'] = rsi2_values
        data['rsi3_values'] = rsi3_values
        data['volume1'] = volume1
        data['volume2'] = volume2
        data['volume3'] = volume3

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)






