import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import requests
from requests.exceptions import HTTPError


def asknbid(w):
    url = f'https://bitbay.net/API/Public/{w}/ticker.json'
    if not test_con(url):
        return test_con(url)
    response = requests.get(url)
    a = response.json()['ask']
    b = response.json()['bid']
    return a, b


def test_con(url):
    return requests.get(url).ok
