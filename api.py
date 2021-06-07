import requests
from utils import *


def get_data(crypto_pairs, data_storage, askbid_storage):

    curr_temp, askbid_temp = ([] for _ in range(2))

    for pair in crypto_pairs:
        try:
            request_orders = requests.get(
                f"https://bitbay.net/API/Public/{pair[0]}{pair[1]}/ticker.json"
            )
            orders = request_orders.json()
            curr_temp.append([f'{pair[0]}-{pair[1]}', (orders['ask'], orders['bid'])])
            askbid_temp.append((orders['ask'], orders['bid']))

        except requests.exceptions.RequestException:
            print("Connection problem with the ticker API.")
            return None

    askbid_storage.append(askbid_temp)
    data_storage.append(curr_temp)


def get_transactions(crypto_pairs, transaction_storage, limit, timeframe):

    trans_temp = []

    for pair in crypto_pairs:

        unix_epoch_time = get_unix_time(timeframe)

        try:
            request_volume = requests.get(
                f"https://api.bitbay.net/rest/trading/transactions/{pair[0]}-{pair[1]}",
                params={'limit': limit, 'fromTime': unix_epoch_time}
            )
            transactions = request_volume.json()
            trans_temp.append(transactions)

        except requests.exceptions.RequestException:
            print("Connection problem with the transactions API.")
            trans_temp.append(None)

    transaction_storage.append(trans_temp)


def get_volume(transaction_storage, volume_storage):

    vol_temp = []

    for curr_pair in range(3):
        latest_trans = transaction_storage[-1][curr_pair]
        trans_amount = len(latest_trans['items'])
        volume = sum([float(latest_trans['items'][tran]['a']) for tran in range(trans_amount)])
        vol_temp.append(volume)

    volume_storage.append(vol_temp)
