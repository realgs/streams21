import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from matplotlib.font_manager import FontProperties
import numpy as np


fig, axs = plt.subplots(3)

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

def prepare_data(ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean):
    data1 = get_data(currency[0])
    data2 = get_data(currency[1])
    data3 = get_data(currency[2])
    append_not_none(ask1_values,data1.get('ask'))
    append_not_none(bid1_values,data1.get('bid'))
    append_not_none(ask2_values, data2.get('ask'))
    append_not_none(bid2_values, data2.get('bid'))
    append_not_none(ask3_values, data3.get('ask'))
    append_not_none(bid3_values, data3.get('bid'))
    append_mean(ask1_mean,ask1_values,mean_elements)
    append_mean(bid1_mean, bid1_values,mean_elements)
    append_mean(ask2_mean,ask2_values,mean_elements)
    append_mean(bid2_mean,bid2_values,mean_elements)
    append_mean(ask3_mean,ask3_values,mean_elements)
    append_mean(bid3_mean,bid3_values,mean_elements)
    return ask1_values, bid1_values,ask2_values,bid2_values,ask3_values,bid3_values, ask1_mean,bid1_mean,ask2_mean,bid2_mean,ask3_mean,bid3_mean

def make_plot(i):
    now.append(datetime.now().strftime("%H:%M:%S"))
    plt1_ask, plt1_bid,plt2_ask, plt2_bid, plt3_ask, plt3_bid, plt1_ask_mean,plt1_bid_mean,plt2_ask_mean,plt2_bid_mean,plt3_ask_mean,plt3_bid_mean = prepare_data(ask1_values, bid1_values, ask2_values, bid2_values, ask3_values, bid3_values,ask1_mean,bid1_mean, ask2_mean,bid2_mean,ask3_mean,bid3_mean)
    #plt.cla()

    axs[0].cla()
    axs[0].plot(now,plt1_ask, label = f'{currency[0]}:Ask')
    axs[0].plot(now,plt1_bid, label = f'{currency[0]}:Bid')
    axs[0].plot(now,plt1_ask_mean,label = f'{currency[0]}:Ask Mean')
    axs[0].plot(now, plt1_bid_mean, label=f'{currency[0]}:Bid Mean')
    axs[0].text(now[-1], plt1_ask[-1], s=f"{get_data(currency[0]).get('volume')}")
    axs[0].set_xlim(auto = 1)
    axs[0].set_title(f"{currency[0]} values")
    axs[0].set_ylabel('Value [PLN]')
    axs[0].set_xlabel('Time')

    axs[1].cla()
    axs[1].plot(now,plt2_ask, label=f'{currency[1]}:Ask')
    axs[1].plot(now,plt2_bid, label=f'{currency[1]}:Bid')
    axs[1].plot(now, plt2_ask_mean, label=f'{currency[1]}:Ask Mean')
    axs[1].plot(now, plt2_bid_mean, label=f'{currency[1]}:Bid Mean')
    axs[1].text(now[-1], plt2_ask[-1], s=f"{get_data(currency[1]).get('volume')}")
    axs[1].set_title(f"{currency[1]} values")
    axs[1].set_ylabel('Value [PLN]')
    axs[1].set_xlabel('Time')


    axs[2].cla()
    axs[2].plot(now,plt3_ask, label=f'{currency[2]}:Ask')
    axs[2].plot(now,plt3_bid, label=f'{currency[2]}:Bid')
    axs[2].plot(now, plt3_ask_mean, label=f'{currency[2]}:Ask Mean')
    axs[2].plot(now, plt3_bid_mean, label=f'{currency[2]}:Bid Mean')
    axs[2].text(now[-1], plt3_ask[-1],s=f"{get_data(currency[2]).get('volume')}")
    axs[2].set_title(f"{currency[2]} values")
    axs[2].set_ylabel('Value [PLN]')
    axs[2].set_xlabel('Time')
    FontP = FontProperties()
    FontP.set_size('xx-small')
    fig.legend(loc = 'upper left', prop = {'size':6})




if __name__ == "__main__":
    mean_elements = int(input("How many last elements do we use to calculate mean: "))
    currency = ['DASHPLN', 'BTCPLN', 'LTCPLN']
    time_int = 5
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
    animations = FuncAnimation(fig, make_plot, interval=5000)
    plt.show()






