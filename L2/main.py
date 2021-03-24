import requests
import time

def down_n_print(url):
    status_code = 200
    while status_code == 200:
        a = requests.get(url)
        print(a.content)
        time.sleep(10)


url = "https://bitbay.net/API/Public/BTC/trades.json"


down_n_print(url)
