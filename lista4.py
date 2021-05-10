import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import numpy as np

fig, axs = plt.subplots(3)


def downloadData(waluty):
    response = requests.get(f'https://bitbay.net/API/Public/{waluty}/ticker.json')
    data = response.json()
    return data

def append_not_none(values, a):
    if a != None:
        values.append(a)
    else:
        if len(values)>1:
            values.append(values[-1])

def append_mean(mean_values, values,liczba_elementow):
    if len(values)>liczba_elementow:
        mean_values.append(np.mean(values[-(liczba_elementow):]))
    else:
        mean_values.append(np.mean(values))

def prepare_data(ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean):
    data1 = downloadData(waluty[0])
    data2 = downloadData(waluty[1])
    data3 = downloadData(waluty[2])
    append_not_none(ask1_values, data1.get('ask'))
    append_not_none(bid1_values, data1.get('bid'))
    append_not_none(ask2_values, data2.get('ask'))
    append_not_none(bid2_values, data2.get('bid'))
    append_not_none(ask3_values, data3.get('ask'))
    append_not_none(bid3_values, data3.get('bid'))
    append_mean(ask1_mean,ask1_values,liczba_elementow)
    append_mean(bid1_mean, bid1_values,liczba_elementow)
    append_mean(ask2_mean,ask2_values,liczba_elementow)
    append_mean(bid2_mean,bid2_values,liczba_elementow)
    append_mean(ask3_mean,ask3_values,liczba_elementow)
    append_mean(bid3_mean,bid3_values,liczba_elementow)
    return ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean

def make_plot(i):
    now.append(datetime.now().strftime("%H:%M:%S"))
    plt1_ask, plt1_bid,plt2_ask, plt2_bid, plt3_ask, plt3_bid, plt1_ask_mean,plt1_bid_mean,plt2_ask_mean,plt2_bid_mean,plt3_ask_mean,plt3_bid_mean = prepare_data(ask1_values, bid1_values, ask2_values, bid2_values, ask3_values, bid3_values,ask1_mean,bid1_mean, ask2_mean,bid2_mean,ask3_mean,bid3_mean)
    #plt.cla()

    axs[0].cla()
    axs[0].plot(now,plt1_ask, label = f'{waluty[0]}:Ask')
    axs[0].plot(now,plt1_bid, label = f'{waluty[0]}:Bid')
    axs[0].plot(now,plt1_ask_mean,label = f'{waluty[0]}:Ask Mean')
    axs[0].plot(now, plt1_bid_mean, label=f'{waluty[0]}:Bid Mean')
    axs[0].text(now[-1], plt1_ask[-1], s=f"{downloadData(waluty[0]).get('volume')}")
    axs[0].set_xlim(auto = 1)
    axs[0].set_title(f"{waluty[0]} values")
    axs[0].set_ylabel('Value [PLN]')
    axs[0].set_xlabel('Time')

    axs[1].cla()
    axs[1].plot(now,plt2_ask, label=f'{waluty[1]}:Ask')
    axs[1].plot(now,plt2_bid, label=f'{waluty[1]}:Bid')
    axs[1].plot(now, plt2_ask_mean, label=f'{waluty[1]}:Ask Mean')
    axs[1].plot(now, plt2_bid_mean, label=f'{waluty[1]}:Bid Mean')
    axs[1].text(now[-1], plt2_ask[-1], s=f"{downloadData(waluty[1]).get('volume')}")
    axs[1].set_title(f"{waluty[1]} values")
    axs[1].set_ylabel('Value [PLN]')
    axs[1].set_xlabel('Time')

    axs[2].cla()
    axs[2].plot(now,plt3_ask, label=f'{waluty[2]}:Ask')
    axs[2].plot(now,plt3_bid, label=f'{waluty[2]}:Bid')
    axs[2].plot(now, plt3_ask_mean, label=f'{waluty[2]}:Ask Mean')
    axs[2].plot(now, plt3_bid_mean, label=f'{waluty[2]}:Bid Mean')
    axs[2].text(now[-1], plt3_ask[-1],s=f"{downloadData(waluty[2]).get('volume')}")
    axs[2].set_title(f"{waluty[2]} values")
    axs[2].set_ylabel('Value [PLN]')
    axs[2].set_xlabel('Time')

    fig.legend(loc='lower right')



if __name__ == "__main__":
    liczba_elementow = 15
    waluty = ['ZECPLN', 'LTCPLN', 'DASHPLN']
    now = []
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
    animations = FuncAnimation(fig, make_plot, interval=3000)
    plt.show()
