import requests


currency = ['BTCPLN', 'ETHPLN', 'LSKPLN']
urls = [f'https://bitbay.net/API/Public/{currency[0]}/ticker.json',f'https://bitbay.net/API/Public/{currency[1]}/ticker.json',f'https://bitbay.net/API/Public/{currency[2]}/ticker.json']

for i in range(0,len(urls)):
    odpowiedz = requests.get(urls[i])
    data = odpowiedz.json()
    print(f'Waluta: {currency[i]} \n Oferta kupna: {data["bid"]}, oferta sprzedaży: {data["ask"]}')



