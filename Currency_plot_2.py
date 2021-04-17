import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation

Currencies=['BTC' , 'LTC' , 'DASH']
Currency_category='USD'
url_beg="https://bitbay.net/API/Public/"
url_end="/ticker.json"
time_sleep=5

def download_data(currency,curr_category,url_beg,url_end): #c_currencies is a list
    url=url_beg+currency+curr_category+url_end
    status=requests.get(url).status_code
    if status==200:
        data = requests.get(url).json()
        return data['ask'],data['bid']
    else:
        print("Could not download data. Try again later!")
        sys.exit()

def plot_data(x_data,plt_BTC,plt_LTC,plt_DASH):
    ask_BTC, bid_BTC = download_data(Currencies[0], Currency_category, url_beg, url_end)
    ask_LTC, bid_LTC = download_data(Currencies[1], Currency_category, url_beg, url_end)
    ask_DASH, bid_DASH = download_data(Currencies[2], Currency_category, url_beg, url_end)

    x_data.append(datetime.now().strftime("%H:%M:%S"))
    plt_BTC.append(ask_BTC)
    plt_BTC.append(bid_BTC)
    plt_LTC.append(ask_LTC)
    plt_LTC.append(bid_LTC)
    plt_DASH.append(ask_DASH)
    plt_DASH.append(bid_DASH)

    return x_data,plt_BTC,plt_LTC,plt_DASH

def draw_plot(i):
    x_data_a, plt_BTC_a, plt_LTC_a, plt_DASH_a = plot_data(x_data, plt_BTC, plt_LTC, plt_DASH)
    plt.cla()

    plt.plot(x_data_a, plt_BTC_a[::2], label='BTC_ask')
    plt.plot(x_data_a, plt_BTC_a[1::2], label='BTC_bid')

    plt.plot(x_data_a, plt_LTC_a[::2], label='LTC_ask')
    plt.plot(x_data_a, plt_LTC_a[1::2], label='LTC_bid')

    plt.plot(x_data_a, plt_DASH_a[::2], label='DASH_ask')
    plt.plot(x_data_a, plt_DASH_a[1::2], label='DASH_bid')

    plt.xticks(x_data_a, rotation=35)

    plt.xlabel('Godzina')
    plt.ylabel('Wartość')
    plt.legend()


if __name__=="__main__":
    x_data = []
    plt_BTC= []
    plt_LTC = []
    plt_DASH = []
    T_animation=animation(plt.figure(),draw_plot,interval=1000*time_sleep)
    plt.show()
