from requests import get
import time
import sys

def connection(currency):
    return f'https://bitbay.net/API/Public/{currency}/orderbook.json'

def get_values(currency):
    try:
        request = get(connection(currency)).json()
        bid = request['bids']
        ask = request['asks']
    except Exception as e:
        print(e)
    return bid, ask

def print_offers(offers):
    offer_parts = offers[:1] + ['...'] + offers[-1:]
    for offer in offer_parts:
        print(offer)
    return offer

def calc_diffrence(currency):
    bids, asks = get_values(currency)
    bid = bids[0][0]
    ask = asks[0][0]
    difference = (1 - (ask - bid) / bid)
    print(currency)
    print('bid: ', bid, '\nask: ', ask, '\ndifference: ', round(difference, 3), '%', '\n')
    return bids, asks

if __name__ == '__main__':
    currencies = ['BTCUSD', 'LTCUSD', 'ETHUSD']
    for currency in currencies:
        bids, asks = get_values(currency)
        print(currency)
        print('bids:'), print_offers(bids)
        print('asks:'), print_offers(asks)
        print('\n')
    while True:
        try:
            for currency in currencies:
                calc_diffrence(currency)
            time.sleep(5)
        except KeyboardInterrupt:
            print('User hit the interrupt key')
            sys.exit()
