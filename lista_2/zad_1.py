import requests
from requests.exceptions import HTTPError

ADRESS = {
    'BTC-PLN' : 'https://bitbay.net/API/Public/BTCPLN/ticker.json',
    'LTC-PLN' : 'https://bitbay.net/API/Public/LTCPLN/ticker.json',
    'ZRX-PLN' : 'https://bitbay.net/API/Public/DASHPLN/ticker.json'
}

def my_requests():
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code == 200:
                print(key, request.json(),'\nLast:',request.json()['last'],'\nAsk:',request.json()['ask'],'\n')
            else:
                print('Error in ', key, ' request')
        except HTTPError:
            print('Error: ', HTTPError)

my_requests()