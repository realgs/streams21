import requests
import sys
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as animation


CURRIENCES = ['ZEC','ETH']
SLEEP_TIME = 5
URL_BEG = 'https://bitbay.net/API/Public/'
URL_END = '/ticker.json'

def dataFrame(CURRIENCES=CURRIENCES, prices = {}):
    for cur in CURRIENCES:
        buy, sell = getData(cur)
        prices[cur] = {'buy': [], 'sell': []}
    return prices    

def getPath(currency, category):
    return f'{URL_BEG}{currency}/{category}{URL_END}'

def getOffers(currency, category):
    try:
        response = requests.get(getPath(currency,category))
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exception:
        print(exception)
        sys.exit()

def getData(currency):
    data = getOffers(currency, 'ticker')
    buy = data["bid"]
    sell = data["ask"]
    return buy, sell