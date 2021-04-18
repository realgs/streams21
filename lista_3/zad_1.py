import requests
from requests.exceptions import HTTPError
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

ADRESS = {
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/orderbook.json',
    'ZRX-PLN' : 'https://bitbay.net/API/Public/ZRXPLN/orderbook.json',
    'BCC-PLN' : 'https://bitbay.net/API/Public/BCCPLN/orderbook.json',
    'OMG-PLN' : 'https://bitbay.net/API/Public/OMGPLN/orderbook.json'
}

CODES = [200,201,202,203,204,205,206]


def market():
    bids_table = []
    asks_table = []
    req_times = []
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code in CODES:
                bids = request.json()['bids'][0][0]
                asks = request.json()['asks'][0][0]
                req_time = datetime.now()
                bids_table.append(bids)
                asks_table.append(asks)
                req_times.append(req_time)
            else:
                print('ERROR')
        except HTTPError:
            print('ERROR: ',HTTPError)
    return bids_table, asks_table, req_times


def calc(bids, asks):
    return round(((1 - (asks - bids)/bids)*100),2)
    

ani = FuncAnimation(plt.gcf(), market, interval=250)
