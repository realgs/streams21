import requests
from time import sleep
from numpy import round


waluty = ['BTCPLN', 'ETHPLN', 'LSKPLN']
adres = [f'https://bitbay.net/API/Public/{waluty[0]}/ticker.json',f'https://bitbay.net/API/Public/{waluty[1]}/ticker.json',f'https://bitbay.net/API/Public/{waluty[2]}/ticker.json']

def stosunek(url):
    odpowiedz = requests.get(url)
    dane = odpowiedz.json()
    return ((dane['ask'] - dane['bid']) / dane['bid']) * 100

def wypisz():
    while True:
        print(f'Dla {waluty[0]} różnica między sprzedażą, a kupnem to {round(stosunek(adres[0]),5)}% ')
        print(f'Dla {waluty[1]} różnica między sprzedażą, a kupnem to {round(stosunek(adres[1]),5)}% ')
        print(f'Dla {waluty[2]} różnica między sprzedażą, a kupnem to {round(stosunek(adres[2]),5)}% \n')
        sleep(5)

wypisz()
