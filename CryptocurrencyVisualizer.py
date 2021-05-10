import requests
import argparse 
from sys import exit

from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

BIDS = "bid"
ASKS = "ask"
VOLUME = "volume"
TIMELINE_SHIFT = 20
LOWER_RSI = 0
UPPER_RSI = 20
BASE_URL = "https://bitbay.net/API/Public/"
REGUESTED_JSON= "ticker.json"
STYLE_NAME = 'dark_background'

def get_url(cryptocurrency, currency):

    return f"{BASE_URL}{cryptocurrency}{currency}/{REGUESTED_JSON}"

def get_trades(cryptocurrency, currency):
    trades = None

    try:
        request = requests.get(get_url(cryptocurrency, currency))
        trades = request.json()
    except requests.exceptions.RequestException as ex:
        trades = None
        print(ex)
    
    return trades

def extract_best_trade(trades):
    
    return trades[BIDS], trades[ASKS], trades[VOLUME]

def calculate_avg(data):
    
    return  sum(data)/len(data)

def calculate_RSI(data, lower, upper):
    sub_data = data[-20:]
    sub_data = sub_data[lower:upper]
    rises = 0
    rises_count = 0
    losses = 0
    losses_count = 0

    for i in range (1,len(sub_data)):
        
        if sub_data[i - 1] < sub_data[i]:
            rise = sub_data[i] - sub_data[i - 1]
            rises += rise
            rises_count += 1
        elif sub_data[i - 1] > sub_data[i]:
            loss = sub_data[i - 1] - sub_data[i]
            losses += loss
            losses_count += 1
    
    if rises_count == 0:
        a = 1
    else:
        a = rises / rises_count
    
    if losses_count == 0:
        b = 1
    else:
        b = losses / losses_count

    return 100 - (100 / (1 + (a / b)))


def add_data(cryptocurrency, currency, best_bids, best_asks, volumes, bids_avg, asks_avg, bids_rsis, asks_rsis, intervals):
        
        intervals.append(datetime.now().strftime("%H:%M:%S"))
        best_bid, best_ask, volume = extract_best_trade((get_trades(cryptocurrency, currency)))
        best_bids.append(best_bid)
        best_asks.append(best_ask)
        volumes.append(volume)
        bids_avg.append(calculate_avg(best_bids))
        asks_avg.append(calculate_avg(best_asks))
        bids_rsis.append(calculate_RSI(best_bids, LOWER_RSI, UPPER_RSI))
        asks_rsis.append(calculate_RSI(best_asks, LOWER_RSI, UPPER_RSI))

def visualize(i, cryptocurrency, currency, best_bids, best_asks, volumes, bids_avg, asks_avg, bids_rsis, asks_rsis, intervals):

        TITLE = f'Wykres notowań {cryptocurrency} - {currency}'
        add_data(cryptocurrency, currency, best_bids, best_asks, volumes, bids_avg, asks_avg, bids_rsis, asks_rsis, intervals)
        
        plt.gcf().canvas.set_window_title(TITLE)

        gs  =  gridspec.GridSpec ( 3 ,  1, height_ratios=[1,5,1])

        plt.subplot(gs[0])
        plt.cla()
        plt.title(TITLE)
        plt.ylabel('RSI')
        
        plt.plot(intervals[-TIMELINE_SHIFT:], asks_rsis[-TIMELINE_SHIFT:], label="RSI asks")
        plt.plot(intervals[-TIMELINE_SHIFT:], bids_rsis[-TIMELINE_SHIFT:], label="RSI bids")

        plt.xticks([])
        plt.legend(loc='center left')

        plt.subplot(gs[1])
        plt.cla()
        plt.ylabel('kurs wymiany')

        plt.plot(intervals[-TIMELINE_SHIFT:], best_asks[-TIMELINE_SHIFT:], label=ASKS)
        plt.plot(intervals[-TIMELINE_SHIFT:], best_bids[-TIMELINE_SHIFT:], label=BIDS)
        plt.plot(intervals[-TIMELINE_SHIFT:], asks_avg[-TIMELINE_SHIFT:], label=ASKS+" avg")
        plt.plot(intervals[-TIMELINE_SHIFT:], bids_avg[-TIMELINE_SHIFT:], label=BIDS+" avg")

        plt.xticks([])
        
        plt.legend(loc='center left')

        plt.subplot(gs[2])
        plt.cla()
        plt.bar(intervals[-TIMELINE_SHIFT:], volumes[-TIMELINE_SHIFT:], alpha=0.5)
        plt.ylabel("wolumen")
        plt.xlabel('czas')

        plt.gcf().autofmt_xdate()

def prepare_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("cryptocurrency")
    parser.add_argument("currency")
    parser.add_argument("-r", "--refresh_time", type=int, choices=range(1, 31))

    return parser

def get_animation_function(cryptocurrency, currency, refresh_time):

    return FuncAnimation(plt.figure(), 
                        visualize, 
                        fargs=(cryptocurrency, currency, [], [], [], [], [], [], [], []), 
                        interval = refresh_time*1000)

def build_windows(cryptocurrency, currency, animations, refresh_time):
    animations.append(get_animation_function(cryptocurrency, currency, refresh_time))

def main():
    args = prepare_parser().parse_args()
    args.refresh_time = 10 if args.refresh_time is None else args.refresh_time
    animations = []

    plt.style.use(STYLE_NAME)

    if args.cryptocurrency is not None and args.currency is not None:
         build_windows(args.cryptocurrency, args.currency, animations, args.refresh_time)
        
    try:         
        plt.show()

    except Exception:
        exit(0)

main()
