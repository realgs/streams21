import requests
import time


def link(typ_walut):
    return f'https://bitbay.net/API/Public/{typ_walut}/ook.json'

def get_data(typ_walut):#+ obsługa błęów
    try:
        req = requests.get(link(typ_walut))
    except Exception as e:
        print(e)
        return {}

    return req 

def json(typ_walut):
    return get_data(typ_walut).json()

def main():
    waluty = ['BTCUSD', 'LTCUSD', 'ETHUSD']

    while True:
        for w in waluty:
            json(w) 
            print('im')
        time.sleep(5)

main()