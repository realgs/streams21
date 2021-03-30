import requests
from requests.exceptions import HTTPError

ADRESS = {
    'btcpln' : 'https://bitbay.net/API/Public/BTCPLN/orderbook.json',
    'ltcusd' : 'https://bitbay.net/API/Public/LTCPLN/orderbook.json',
    'dashusd': 'https://bitbay.net/API/Public/DASHPLN/orderbook.json'
}

def my_requests():
    for key in ADRESS.keys():
        try:
            request = requests.get(ADRESS[key])
            if request.status_code == 200:
                print(key,request.json(),'\n')
            else:
                print('Error in ', key, ' request')
        except HTTPError:
            print('Error: ', HTTPError)

my_requests()