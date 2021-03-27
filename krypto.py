import requests


def fetchBitbayAPI(category, resource):
    URL = f'https://bitbay.net/API/Public/{resource}/{category}.json'
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()


def printOffers(trades, resource):
    try:
        buy = []
        sell = []
        for record in trades:
            if record['type'] == 'buy':
                buy.append(record)
            elif record['type'] == 'sell':
                sell.append(record)

        print(f'{resource}:')
        print('    buy:')
        for b in buy:
            print(f'\t{b}')
        print('    sell:')
        for s in sell:
            print(f'\t{s}')
    except Exception as e:
        print(e)


if __name__ == '__main__':

    RESOURCES = ['BTCUSD', 'LTCUSD', 'DASHUSD']

    for R in RESOURCES:
        trades = fetchBitbayAPI(category='trades', resource=R)
        printOffers(trades, R)
