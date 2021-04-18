import requests
from requests.exceptions import HTTPError
from itertools import count
import time
import random
import openpyxl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ADRESS = {
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/orderbook.json',
    'ZRX-PLN' : 'https://bitbay.net/API/Public/ZRXPLN/orderbook.json',
    'BCC-PLN' : 'https://bitbay.net/API/Public/BCCPLN/orderbook.json',
    'OMG-PLN' : 'https://bitbay.net/API/Public/OMGPLN/orderbook.json'
}

CODES = [200,201,202,203,204,205,206]


def market():
    counter = 1
    global df_b
    global df_a
    bids_table = []
    asks_table = []
    FILE_PATH = 'market.csv'
    while True:
        print(counter, "survey of buy - sell difference:")
        for key in ADRESS.keys():
            try:
                request = requests.get(ADRESS[key])
                if request.status_code in CODES:
                    bids = request.json()['bids'][0][0]
                    asks = request.json()['asks'][0][0]
                    print(key,'->',calc(bids,asks),"%")
                    bids_table.append(bids)
                    asks_table.append(asks)
                    df_b = pd.DataFrame(bids_table)
                    df_a = pd.DataFrame(asks_table)
                    df_b = df_b.T
                    df_a = df_a.T
                else:
                    print('ERROR')
            except HTTPError:
                print('ERROR: ',HTTPError)
        counter += 1
        print('------------------')
        time.sleep(1)


def calc(bids, asks):
    return round(((1 - (asks - bids)/bids)*100),2)
    

ani = FuncAnimation(plt.gcf(), market, interval=250)

print(market())
