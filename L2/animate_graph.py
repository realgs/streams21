import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv


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


def open_user_input_data():
    with open('user_input.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    data.append([-1, -1, -1])

    cur1 = []
    cur2 = []
    cur3 = []
    for info in data:
        if info[0] == '1':
            cur1.append(info[1:])
        elif info[0] == '2':
            cur2.append(info[1:])
        elif info[0] == '3':
            cur3.append(info[1:])
    return cur1, cur2, cur3


def animate(i):
    show_average = False
    # read data
    data = pd.read_csv('data.csv')
    x = data['time']
    len_data = len(data)
    bid_cur1 = data['bid_cur1']
    ask_cur1 = data['ask_cur1']
    bid_cur2 = data['bid_cur2']
    ask_cur2 = data['ask_cur2']
    bid_cur3 = data['bid_cur3']
    ask_cur3 = data['ask_cur3']

    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax5.cla()
    ax6.cla()
    ax1v.cla()
    ax3v.cla()
    ax5v.cla()

    plt.style.use('seaborn')
    currencies = ['ETH-PLN', 'BTC-PLN', 'DASH-PLN']
    # plot bid and ask
    ax1.plot(x, bid_cur1, label=f'Bid')
    ax1.plot(x, ask_cur1, label=f'Ask')
    ax3.plot(x, bid_cur2, label=f'Bid')
    ax3.plot(x, ask_cur2, label=f'Ask')
    ax5.plot(x, bid_cur3, label=f'Bid')
    ax5.plot(x, ask_cur3, label=f'Ask')

    if show_average:
        # prepare data for average, plot averaeg
        sliced_data = data[int(len_data/3):]
        sliced_x = sliced_data['time']
        sliced_bid_cur1 = sliced_data['bid_cur1']
        sliced_ask_cur1 = sliced_data['ask_cur1']
        average_bid_cur1 = average(sliced_bid_cur1)
        average_ask_cur1 = average(sliced_ask_cur1)
        ax1.plot(sliced_x, average_bid_cur1, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur1))}')
        ax1.plot(sliced_x, average_ask_cur1, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur1))}')
        sliced_bid_cur2 = sliced_data['bid_cur2']
        sliced_ask_cur2 = sliced_data['ask_cur2']
        average_bid_cur2 = average(sliced_bid_cur2)
        average_ask_cur2 = average(sliced_ask_cur2)
        ax3.plot(sliced_x, average_bid_cur2, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur2))}')
        ax3.plot(sliced_x, average_ask_cur2, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur2))}')
        sliced_bid_cur3 = sliced_data['bid_cur3']
        sliced_ask_cur3 = sliced_data['ask_cur3']
        average_bid_cur3 = average(sliced_bid_cur3)
        average_ask_cur3 = average(sliced_ask_cur3)
        ax5.plot(sliced_x, average_bid_cur3, label=f'AVG bid, TOTAL: {round(total_avg(sliced_bid_cur3))}')
        ax5.plot(sliced_x, average_ask_cur3, label=f'AVG ask, TOTAL: {round(total_avg(sliced_ask_cur3))}')

    # volumen24
    vol24 = pd.read_csv('volumen24.csv')
    vol1 = vol24['vol1']
    vol2 = vol24['vol2']
    vol3 = vol24['vol3']

    ax1v.set_ylim([min(vol1)-1/10*(max(vol1)-min(vol1)), (max(vol1)-min(vol1))*3 + min(vol1)])
    ax1v.yaxis.tick_right()
    ax1v.fill_between(x, vol1, alpha=0.4)

    ax3v.set_ylim([min(vol2)-1/10*(max(vol2)-min(vol2)), (max(vol2)-min(vol2))*3 + min(vol2)])
    ax3v.yaxis.tick_right()
    ax3v.fill_between(x, vol2, alpha=0.4)

    ax5v.set_ylim([min(vol3)-1/10*(max(vol3)-min(vol3)), (max(vol3)-min(vol3))*3 + min(vol3)])
    ax5v.yaxis.tick_right()
    ax5v.fill_between(x, vol3, alpha=0.4)

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

    # prepare volunen and RSI, plot them
    volume = count_volumen()
    rsi = pd.read_csv('rsi.csv')
    rs1 = rsi['rsi1'][0]
    rs2 = rsi['rsi2'][0]
    rs3 = rsi['rsi3'][0]
    ax2.barh('-', volume[0], align='edge')
    ax4.barh('-', volume[1], align='edge')
    ax6.barh('-', volume[2], align='edge')

    if rs1 > 70:
        trend1 = 'overbought'
    elif 30 < rs1 < 70:
        trend1 = 'neutral'
    else:
        trend1 = 'oversold'

    if rs2 > 70:
        trend2 = 'overbought'
    elif 30 < rs2 < 70:
        trend2 = 'neutral'
    else:
        trend2 = 'oversold'

    if rs3 > 70:
        trend3 = 'overbought'
    elif rs3 < 70 and rs1 > 30:
        trend3 = 'neutral'
    else:
        trend3 = 'oversold'

    candidate = []
    for trend in (trend1, trend2, trend3):
        if trend != 'overbought':
            candidate.append(1)
        else:
            candidate.append(-1)

    lastv1 = round(vol1[len(vol1)-1], 2)
    lastv2 = round(vol2[len(vol2)-1], 2)
    lastv3 = round(vol3[len(vol3)-1], 2)

    lastvall = [lastv1, lastv2, lastv3]

    for i in range(3):
        if candidate[i] == 1:
            candidate[i] = lastvall[i]

    maxv_candidate = max(candidate)
    candtext = ['-']*3
    index = 0
    if maxv_candidate != -1:
        index = lastvall.index(maxv_candidate)

    Y_samples = 5
    X_percentage = 0.3
    volatile = data[-Y_samples:]
    volatilebid = list(volatile[f'bid_cur{index + 1}'])
    volatileask = list(volatile[f'ask_cur{index + 1}'])

    if 1 - (volatileask[0] + abs(volatileask[-1]-volatileask[0]))/volatileask[0] > X_percentage \
            or 1 - (volatilebid[0] + abs(volatilebid[-1]-volatilebid[0]))/volatilebid[0] > X_percentage:
        volatiletext = "yes"
    else:
        volatiletext = 'no'

    Spread = 0.5
    spreadask = data[f'ask_cur{index + 1}'][len(data)-1]
    spreadabid = data[f'bid_cur{index + 1}'][len(data) - 1]
    if (spreadask/spreadabid - 1) * 100 < Spread:
        spreadtext = 'yes'
    else:
        spreadtext = 'no'

    candtext[index] = '\n**Best candidate**' \
                      f'\nVolatile asset: {volatiletext}' \
                      f'\nLiquid asset: {spreadtext}'

    profit = list()
    with open('profit.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            profit.append(row)
    profit.pop(0)
    print(profit)

    ax2.set_title(f'VOLUMEN {currencies[0]} {candtext[0]}')
    ax4.set_title(f'VOLUMEN {currencies[1]} {candtext[1]}')
    ax6.set_title(f'VOLUMEN {currencies[2]} {candtext[2]}')
    ax2.set_xlabel(f'Volume: {lastv1} \n RSI: {round(rs1, 2)} \n TREND: {trend1} \n PROFIT: {round(float(profit[0][0]), 2)}')
    ax4.set_xlabel(f'Volume {lastv2} \n RSI: {round(rs2, 2)} \n TREND: {trend2} \n PROFIT: {round(float(profit[0][1]), 2)}')
    ax6.set_xlabel(f'Volume {lastv3} \n RSI: {round(rs3, 2)} \n TREND: {trend3} \n PROFIT: {round(float(profit[0][2]), 2)}')

    for ax in (ax2, ax4, ax6):
        plt.sca(ax)
        plt.xticks(rotation=45)
        plt.xticks(visible=False, rotation="horizontal")

    ax1.set_title(f'{currencies[0]}')
    ax3.set_title(f'{currencies[1]}')
    ax5.set_title(f'{currencies[2]}')
    if index == 0:
        ax1.set_title(f'***{currencies[0]}***', color='red')
    if index == 1:
        ax3.set_title(f'{currencies[0]}', color='red')
    if index == 2:
        ax5.set_title(f'{currencies[0]}', color='red')

    # grid disable
    for ax in (ax1, ax2, ax3, ax4, ax5, ax6, ax1v, ax3v, ax5v):
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)

    # ask user input
    cur1, cur2, cur3 = open_user_input_data()
    suma = 0
    wages = 0
    if cur1:
        for data in cur1:
            suma += float(data[0])*float(data[1])
            wages += float(data[0])
        avg1 = [suma/wages]*2
        x_val1 = [list(x)[0], list(x)[int(cur1[-1][2])]]
        ax1.plot(x_val1, avg1, color='red', linestyle='dashed', linewidth=0.5, label='User Ask Average')
        ax1.legend(loc="upper left")
    suma = 0
    wages = 0
    if cur2:
        for data in cur2:
            suma += float(data[0])*float(data[1])
            wages += float(data[0])
        avg1 = [suma/wages]*2
        x_val1 = [list(x)[0], list(x)[int(cur2[-1][2])]]
        ax3.plot(x_val1, avg1, color='red', linestyle='dashed', linewidth=0.5, label='User Ask Average')
        ax3.legend(loc="upper left")
    suma = 0
    wages = 0
    if cur3:
        for data in cur3:
            suma += float(data[0])*float(data[1])
            wages += float(data[0])
        avg1 = [suma/wages]*2
        x_val1 = [list(x)[0], list(x)[int(cur3[-1][2])]]
        ax5.plot(x_val1, avg1, color='red', linestyle='dashed', linewidth=0.5, label='User Ask Average')
        ax5.legend(loc="upper left")

    plt.tight_layout()


if __name__ == '__main__':
    fig = plt.figure()
    ax1 = plt.subplot2grid((3, 6), (0, 0), rowspan=1, colspan=5)
    ax2 = plt.subplot2grid((3, 6), (0, 5), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((3, 6), (1, 0), rowspan=1, colspan=5)
    ax4 = plt.subplot2grid((3, 6), (1, 5), rowspan=1, colspan=1)
    ax5 = plt.subplot2grid((3, 6), (2, 0), rowspan=1, colspan=5)
    ax6 = plt.subplot2grid((3, 6), (2, 5), rowspan=1, colspan=1)

    ax1v = ax1.twinx()
    ax3v = ax3.twinx()
    ax5v = ax5.twinx()

    fig.set_size_inches(12, 8, forward=True)
    plt.locator_params(axis='x', nbins=10)
    anim = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.show()
