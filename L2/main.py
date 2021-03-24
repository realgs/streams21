import requests
import time
from requests.exceptions import HTTPError
import json

def down_n_print(url1,url2):

    for url in [url1, url2]:
        try:
            response = requests.get(url)
            print(response.json())
            print(type(response.json()))

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')



url1 = "https://bitbay.net/API/Public/BTC/trades.json"
url2 = "https://btbay.net/API/Public/BTC/trades.json"

down_n_print(url1,url2)

