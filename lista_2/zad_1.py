import requests
from requests.exceptions import HTTPError

ADRESS = {
    'BTC-PLN' : 'https://bitbay.net/API/Public/BTCPLN/market.json',
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/market.json',
    'ZRX-PLN' : 'https://bitbay.net/API/Public/ZRXPLN/market.json'
}
CODES = [200,201,202,203,204,205,206]

def my_requests():
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code in CODES:
                print(key, request.json()['transactions'][15])
            else:
                print('Error in ', key, ' request')
        except HTTPError:
            print('Error: ', HTTPError)

my_requests()
