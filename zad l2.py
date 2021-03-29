from requests import get
from time import sleep

req_temp = ('https://bitbay.net/API/Public/', '/ticker.json')
cryptos = ['BTC', 'LTC', 'ETH']
status = '200'


def request_crypto(crypt):
    try:
        request = req_temp[0] + crypt + req_temp[1]
        resp = get(request)
        status = str(resp.status_code)
        assert status[0] == '2', "wrong status: " + status
        resp_dict = eval(resp.text)
        sell = resp_dict['ask']
        buy = resp_dict['bid']
        value = (1 - (sell - buy) / buy) * 100
        return sell, buy, value
    except KeyError:
        print(resp_dict['message'])


while status[0] == '2':
    for crypto in cryptos:
        sell_val, buy_val, ratio_val = req_temp(crypto)
        print(f'{crypto}: sell - {sell_val} buy - {buy_val} buy/sell ratio - {ratio_val}')
    sleep(5)
