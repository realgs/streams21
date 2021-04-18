import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import requests
from requests.exceptions import HTTPError


def asknbid(w):
    url = f'https://bitbay.net/API/Public/{w}/ticker.json'
    if not test_con(url):
        return test_con(url)
    response = requests.get(url)
    a = response.json()['ask']
    b = response.json()['bid']
    return a, b


def test_con(url):
    return requests.get(url).ok

xv = []
w = ('XRP', 'MANA', 'BAT')
oferty = {}
index = count()


def animate(i):
    xv.append(next(index))
    for i in w:
        if i + 'asks' not in oferty.keys():
            oferty[i + 'asks'] = []
            oferty[i + 'bids'] = []
        oferty[i + 'asks'].append(asknbid(i + 'PLN')[0])
        oferty[i + 'bids'].append(asknbid(i + 'PLN')[1])
        oferty[i + 'asks'] = oferty[i + 'asks'][-5:]
        oferty[i + 'bids'] = oferty[i + 'bids'][-5:]
    plt.cla()
    for k, v in oferty.items():
        plt.plot(xv[-5:], v, '.-', label=k)
    plt.legend(loc='upper left')
    plt.title(f'Currency rate graph of: {w}')


ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()