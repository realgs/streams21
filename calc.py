from utils import *


def calculate_mov_avg(askbid_storage, avg_storage, window_size):

    storage_slice = askbid_storage[-window_size:]
    temp = []

    for curr_pair in range(3):
        inner_temp = []

        for ask_or_bid in range(2):
            summation = 0

            for sample in range(0, len(storage_slice)):
                summation += storage_slice[sample][curr_pair][ask_or_bid]
            summation /= len(storage_slice)
            inner_temp.append(summation)

        temp.append(inner_temp)

    avg_storage.append(temp)


def calculate_rsi(askbid_storage, rsi_storage, window_size):

    storage_slice = askbid_storage[-window_size:]
    temp = []

    for curr_pair in range(3):
        inner_temp = []

        for ask_or_bid in range(2):
            upward, upward_counter = 0, 0
            downward, downward_counter = 0, 0

            for sample in range(1, len(storage_slice)):
                if storage_slice[sample-1][curr_pair][ask_or_bid] \
                        < storage_slice[sample][curr_pair][ask_or_bid]:

                    up = storage_slice[sample][curr_pair][ask_or_bid] \
                           - storage_slice[sample-1][curr_pair][ask_or_bid]
                    upward += up
                    upward_counter += 1

                elif storage_slice[sample-1][curr_pair][ask_or_bid] \
                        > storage_slice[sample][curr_pair][ask_or_bid]:

                    down = storage_slice[sample-1][curr_pair][ask_or_bid] \
                           - storage_slice[sample][curr_pair][ask_or_bid]
                    downward += down
                    downward_counter += 1

            if upward_counter == 0:
                a = 1
            else:
                a = upward / upward_counter

            if downward_counter == 0:
                b = 1
            else:
                b = downward / downward_counter

            try:
                rsi = 100 - (100 / (1 + (a / b)))
            except ZeroDivisionError:
                a, b = 1, 1
                rsi = 100 - (100 / (1 + (a / b)))
            inner_temp.append(rsi)

        temp.append(inner_temp)

    rsi_storage.append(temp)


def classify_trend(rsi_storage, trend_list):

    for curr_pair in range(3):

        latest_ask_rsi = rsi_storage[-1][curr_pair][0]
        if latest_ask_rsi >= 65:
            trend_list[curr_pair] = 'upward'
        elif latest_ask_rsi <= 35:
            trend_list[curr_pair] = 'downward'
        else:
            trend_list[curr_pair] = 'horizontal'


def select_candidate(trends_list, volume_slice):

    temp = []
    for curr_pair in range(3):

        if trends_list[curr_pair] != 'downward':
            temp.append(volume_slice[curr_pair])

    if temp:
        highest_volume = max(temp)
        return volume_slice.index(highest_volume)
    else:
        return None


def check_volatility(transaction_storage, pair, threshold, samples):

    trans_slice = transaction_storage[-samples:]
    temp = []
    for sample in range(len(trans_slice)):
        curr_trans = trans_slice[sample][pair]
        trans_amount = len(curr_trans['items'])
        inner_temp = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)]
        temp.extend(inner_temp)

    try:
        percentage = calculate_percent_diff(max(temp), min(temp))
    except ValueError:
        percentage = 0

    return (lambda perc: True if perc > threshold else False)(percentage)


def check_liquidity(transaction_storage, pair, threshold):

    trans_slice = transaction_storage[-1:]
    curr_trans = trans_slice[0][pair]
    trans_amount = len(curr_trans['items'])

    temp_asks = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)
                 if curr_trans['items'][tran]['ty'] == "Buy"]
    temp_bids = [float(curr_trans['items'][tran]['r']) for tran in range(trans_amount)
                 if curr_trans['items'][tran]['ty'] == "Sell"]

    try:
        ask = sum(temp_asks) / len(temp_asks)
    except ZeroDivisionError:
        return 0

    try:
        bid = sum(temp_bids) / len(temp_bids)
    except ZeroDivisionError:
        return 0

    try:
        percentage = calculate_percent_diff(ask, bid)
    except ValueError:
        percentage = 0

    return (lambda spread: True if spread < threshold else False)(percentage)
