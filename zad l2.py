from requests import get
from time import sleep
r = 'https://bitbay.net/API/Public/BTC/ticker.json'
crypts = ['BTC','LTC','ETH']
status = '200'
try:
    while status[0] == '2':
        for crypto in crypts:
            resp = get(f'https://bitbay.net/API/Public/{crypto}/ticker.json')
            status = str(resp.status_code)
            assert status[0] == '2', "wrong status: "+status
            resp_dict = eval(resp.text)
            sell =  resp_dict['ask']
            buy = resp_dict['bid']
            value = (1-(sell-buy)/buy)*100
            print(f'{crypto}: sell - {sell} buy - {buy} buy/sell ratio - {value}')
        sleep(5)
except KeyError:
    print(resp_dict['message'])