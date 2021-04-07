import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_val']
    bid_cur1 = data['bid_cur1']
    ask_cur1 = data['ask_cur1']
    bid_cur2 = data['bid_cur2']
    ask_cur2 = data['ask_cur2']
    bid_cur3 = data['bid_cur3']
    ask_cur3 = data['ask_cur3']

    plt.cla()
    currencies = ['BTC', 'GNT', 'DASH']
    plt.plot(x, bid_cur1, label=f'Bid {currencies[0]}')
    plt.plot(x, ask_cur1, label=f'Ask {currencies[0]}')
    plt.plot(x, bid_cur2, label=f'Bid {currencies[1]}')
    plt.plot(x, ask_cur2, label=f'Ask {currencies[1]}')
    plt.plot(x, bid_cur3, label=f'Bid {currencies[2]}')
    plt.plot(x, ask_cur3, label=f'Ask {currencies[2]}')


    plt.legend(loc='upper left')
    plt.tight_layout()

plt.style.use('fivethirtyeight')
anim = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()