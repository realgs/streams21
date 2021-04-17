import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt

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

def plot_data(x_data_BTC,x_data_LTC,x_data_DASH,plt_BTC,plt_LTC,plt_DASH):
    x_data_BTC.append(datetime.now().strftime("%H:%M:%S"))
    ask_BTC, bid_BTC = download_data(Currencies[0], Currency_category, url_beg, url_end)
    x_data_LTC.append(datetime.now().strftime("%H:%M:%S"))
    ask_LTC, bid_LTC = download_data(Currencies[1], Currency_category, url_beg, url_end)
    x_data_DASH.append(datetime.now().strftime("%H:%M:%S"))
    ask_DASH, bid_DASH = download_data(Currencies[2], Currency_category, url_beg, url_end)

    plt_BTC.append(ask_BTC)
    plt_BTC.append(bid_BTC)
    plt_LTC.append(ask_LTC)
    plt_LTC.append(bid_LTC)
    plt_DASH.append(ask_DASH)
    plt_DASH.append(bid_DASH)

    return x_data_BTC,x_data_LTC,x_data_DASH,plt_BTC,plt_LTC,plt_DASH