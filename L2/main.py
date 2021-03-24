import requests
import time
from requests.exceptions import HTTPError
import json

def down_n_print(url1,url2,url3):

    for url in [url1, url2,url3]:
        try:
            response = requests.get(url)
            print(response.json())

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')


cur1,cur2,cur3 = "BTC","GNT","GNT"
url1 = f"https://bitbay.net/API/Public/{cur1}/trades.json"
url2 = f"https://bitbay.net/API/Public/{cur2}/trades.json"
url3 = f"https://bitbay.net/API/Public/{cur3}/trades.json"

down_n_print(url1,url2,url3)

