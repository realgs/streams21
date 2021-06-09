import datetime
import requests
from datetime import datetime, timedelta

def getVolumeNewAPI(fromCurrancy, toCurrancy, time):
    url = f'https://api.bitbay.net/rest/trading/transactions/{fromCurrancy}-{toCurrancy}'

    now = datetime.now()
    before = int((now - timedelta(0, time)).timestamp()) * 1000
    querystring = {"from": before}

    try:
        response = requests.request("GET", url, params=querystring)
        a = float(response.json()['items'][0]['a'])
    except:
        a = 0
    return a