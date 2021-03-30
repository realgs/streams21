import requests


waluty = ['BTCPLN', 'ETHPLN', 'LSKPLN']
adres = [f'https://bitbay.net/API/Public/{waluty[0]}/ticker.json',f'https://bitbay.net/API/Public/{waluty[1]}/ticker.json',f'https://bitbay.net/API/Public/{waluty[2]}/ticker.json']
odpowiedz = requests.get(adres[0])
dane = odpowiedz.json()
for i in range(0,len(adres)):
    odpowiedz = requests.get(adres[i])
    dane = odpowiedz.json()
    print(f'Waluta: {waluty[i]} \n Oferta kupna: {dane["bid"]}, oferta sprzedaży: {dane["ask"]}')



