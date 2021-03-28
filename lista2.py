import requests
import time
from requests.exceptions import HTTPError

url={'BTCUSD':'https://bitbay.net/API/Public/BTCUSD/orderbook.json',
     'LTCUSD':'https://bitbay.net/API/Public/LTCUSD/orderbook.json',
     'DASHUSD':'https://bitbay.net/API/Public/DASHUSD/orderbook.json'}

def offers():
     for u in url.keys():
          try:
               response=requests.get(url[u])
               print(u,response.json())
               response.raise_for_status()
          except HTTPError:
               print('HTTP error:', HTTPError)
          except Exception:
               print('Other error:',Exception)


def bids_asks_diff():
     while True:
          for u in url.keys():
               try:
                    response=requests.get(url[u])
                    buy = response.json()['bids'][0][0]
                    sell = response.json()['asks'][0][0]
                    difference = 1-(sell-buy)/sell
                    print(u, difference)
               except HTTPError:
                    print('HTTP error:', HTTPError)
               except Exception:
                    print('Other error:', Exception)
          time.sleep(5)


offers()
bids_asks_diff()
