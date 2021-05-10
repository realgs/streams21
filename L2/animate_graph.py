import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def every_nth_func(x_val):
    x_val = list(x_val)
    if x_val:
        if len(x_val)//10 == 0:
            return 1
        else:
            return len(x_val)//10
    else:
        return 1


def count_volumen():
    data = pd.read_csv('volumen.csv')

    transactions1 = zip(data['last_1_id'], data['last_1_val'])
    transactions1 = list(transactions1)
    set_1 = set(transactions1)
    sum_1 = 0
    for elem in set_1:
        sum_1 += elem[1]

    transactions2 = zip(data['last_2_id'], data['last_2_val'])
    transactions2 = list(transactions2)
    set_2 = set(transactions2)
    sum_2 = 0
    for elem in set_2:
        sum_2 += elem[1]

    transactions3 = zip(data['last_3_id'], data['last_3_val'])
    transactions3 = list(transactions3)
    set_3 = set(transactions3)
    sum_3 = 0
    for elem in set_3:
        sum_3 += elem[1]
    return [sum_1, sum_2, sum_3]

def average(mylist):
    mylist = list(mylist)
    N = 3
    cumsum, moving_aves = [0], []
    moving_aves.append(mylist[0])
    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i - N]) / N
            moving_aves.append(moving_ave)
    moving_aves.append(mylist[-1])
    return moving_aves

def total_avg(mylist):
    mylist = list(mylist)
    return sum(mylist)/len(mylist)


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['time']
    len_data = len(data)
    bid_cur1 = data['bid_cur1']
    ask_cur1 = data['ask_cur1']
    bid_cur2 = data['bid_cur2']
    ask_cur2 = data['ask_cur2']
    bid_cur3 = data['bid_cur3']
    ask_cur3 = data['ask_cur3']

    volume = count_volumen()

    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    ax6.cla()

    plt.style.use('seaborn')
    currencies = ['ETH-PLN', 'BTC-PLN', 'DASH-PLN']
    ax1.plot(x, bid_cur1, label=f'Bid')
    ax1.plot(x, ask_cur1, label=f'Ask')
    ax3.plot(x, bid_cur2, label=f'Bid')
    ax3.plot(x, ask_cur2, label=f'Ask')
    ax5.plot(x, bid_cur3, label=f'Bid')
    ax5.plot(x, ask_cur3, label=f'Ask')

    sliced_data = data[int(len_data/3):]
    sliced_x = sliced_data['time']
    sliced_bid_cur1 = sliced_data['bid_cur1']
    sliced_ask_cur1 = sliced_data['ask_cur1']
    average_bid_cur1 = average(sliced_bid_cur1)
    average_ask_cur1 = average(sliced_ask_cur1)

    ax1.plot(sliced_x, average_bid_cur1, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur1))}')
    ax1.plot(sliced_x, average_ask_cur1, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur1))}')

    sliced_bid_cur2= sliced_data['bid_cur2']
    sliced_ask_cur2 = sliced_data['ask_cur2']
    average_bid_cur2 = average(sliced_bid_cur2)
    average_ask_cur2 = average(sliced_ask_cur2)

    ax3.plot(sliced_x, average_bid_cur2, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur2))}')
    ax3.plot(sliced_x, average_ask_cur2, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur2))}')
    
    sliced_bid_cur3= sliced_data['bid_cur3']
    sliced_ask_cur3 = sliced_data['ask_cur3']
    average_bid_cur3 = average(sliced_bid_cur3)
    average_ask_cur3 = average(sliced_ask_cur3)

    ax5.plot(sliced_x, average_bid_cur3, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur3))}')
    ax5.plot(sliced_x, average_ask_cur3, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur3))}')


    ax2.barh('-', volume[0], align='edge')
    ax2.set_title(f'VOLUMEN {currencies[0]}')
    ax2.set_xlabel(f'Amount of crypto tranferred {round(volume[0], 4)}')

    ax4.barh('-', volume[1], align='edge')
    ax4.set_title(f'VOLUMEN {currencies[1]}')
    ax4.set_xlabel(f'Amount of crypto tranferred {round(volume[1], 4)}')

    ax6.barh('-', volume[2], align='edge')
    ax6.set_title(f'VOLUMEN {currencies[2]}')
    ax6.set_xlabel(f'Amount of crypto tranferred {round(volume[2], 4)}')

    for ax in (ax2, ax4, ax6):
        plt.sca(ax)
        plt.xticks(rotation=45)
        plt.xticks(visible=False, rotation="horizontal")

    ax1.set_title(f'{currencies[0]}')
    ax3.set_title(f'{currencies[1]}')
    ax5.set_title(f'{currencies[2]}')

    for ax in (ax1, ax3, ax5):
        ax.legend(loc="upper left")
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        plt.sca(ax)
        plt.xticks(rotation=45)

        every_nth = every_nth_func(x)
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
    plt.tight_layout()


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2, gridspec_kw={'width_ratios': [5, 1]})
fig.set_size_inches(12, 8, forward=True)
plt.locator_params(axis='x', nbins=10)
anim = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()
