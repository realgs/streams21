import requests
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt

Currencies=['BTC' , 'LTC' , 'DASH']
Currency_category='USD'
url_beg="https://bitbay.net/API/Public/"
url_end="/ticker.json"
time_sleep=5

def download_data(currency,curr_category,url_beg,url_end): #c_currencies is a list
    url=url_beg+currency+curr_category+url_end
    status=requests.get(url).status_code
    if status==200:
        data = requests.get(url).json()
        return data['ask'],data['bid']
    else:
        print("Could not download data. Try again later!")
        sys.exit()

