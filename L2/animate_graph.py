import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def every_nth_func(x_val):
    x_val = list(x_val)
    if x_val:
        if len(x_val)//10 == 0:
            return 1
        else:
            return len(x_val)//10
    else:
        return 1

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['time']
    bid_cur1 = data['bid_cur1']
    ask_cur1 = data['ask_cur1']
    bid_cur2 = data['bid_cur2']
    ask_cur2 = data['ask_cur2']
    bid_cur3 = data['bid_cur3']
    ask_cur3 = data['ask_cur3']

    ax1.cla()
    ax2.cla()
    ax3.cla()

    plt.style.use('seaborn')
    currencies = ['BTC', 'GNT', 'DASH']
    ax1.plot(x, bid_cur1, label=f'Bid')
    ax1.plot(x, ask_cur1, label=f'Ask')
    ax2.plot(x, bid_cur2, label=f'Bid')
    ax2.plot(x, ask_cur2, label=f'Ask')
    ax3.plot(x, bid_cur3, label=f'Bid')
    ax3.plot(x, ask_cur3, label=f'Ask')

    ax1.set_title(f'{currencies[0]} and USD')
    ax2.set_title(f'{currencies[1]} and USD')
    ax3.set_title(f'{currencies[2]} and USD')

    for ax in (ax1, ax2, ax3):
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


fig, (ax1, ax2, ax3) = plt.subplots(nrows=3,ncols=1)
fig.set_size_inches(12, 8, forward=True)
plt.locator_params(axis='x', nbins=10)
anim = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()

